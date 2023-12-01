import os
import importlib
from time import time
from tqdm import tqdm
from gc import collect
from re import findall
from sys import stderr
from requests import get
from termcolor import colored
from dns.name import EmptyLabel
from warnings import simplefilter
from dns.exception import DNSException
from configparser import RawConfigParser
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError
from concurrent.futures import ThreadPoolExecutor, as_completed
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers, Timeout
from utilities.DatabaseHelpers import Resolution, Unresolved, Takeover
from utilities.MiscHelpers import chunkify, slackNotification


template_functions = {}


def loadTemplates():
	template_files = [file for file in os.listdir("takeovers") if file.endswith(".py") and not file.endswith("__init__.py")]

	for file in template_files:
		module_name = os.path.splitext(file)[0]
		module = importlib.import_module(f"takeovers.{module_name}")

		if hasattr(module, "init") and callable(module.init):
			template_functions[module_name] = module.init

		else:
			print(f"Module '{module_name}' does not have an 'init' function.")


def takeOver(domain):
	A = []
	CNAME = []
	results = []
	resolver = Resolver()
	resolver.timeout = 1
	resolver.lifetime = 1
	types = ["A", "CNAME"]

	for type in types:
		try:
			answers = resolver.query(domain, type)

			for answer in answers:
				if type == "A":
					A.append(answer.address)

				if type == "CNAME":
					CNAME.append(answer.target)

		except (NXDOMAIN, NoAnswer, EmptyLabel, NoNameservers, Timeout, DNSException):
			pass

		except Exception:
			return None

	results = None

	for template_name, template_function in template_functions.items():
		results = template_function(domain, A, CNAME)
		
		if results:
			return results


def massTakeOver(targets, threads):
	takeovers = []
	numberOfChunks = 1
	leaveFlag = False

	if len(targets) <= 100000:
		print("{0} {1} {2}".format(colored("\n[*]-Scanning", "yellow"), colored(len(targets), "cyan"), colored("domains for potential takeover...", "yellow")))

	else:
		print("{0} {1} {2}".format(colored("\n[*]-Scanning", "yellow"), colored(len(targets), "cyan"), colored("domains for potential takeover, in chunks of 100,000...", "yellow")))
		numberOfChunks = len(targets) // 100000 + 1

	targetChunks = chunkify(targets, 100000)
	iteration = 1

	for targetChunk in targetChunks:
		with ThreadPoolExecutor(max_workers=threads) as executor:
			tasks = {executor.submit(takeOver, target) for target in targetChunk}

			try:
				completed = as_completed(tasks)

				if iteration == numberOfChunks:
					leaveFlag = True

				if numberOfChunks == 1:
					completed = tqdm(completed, total=len(targetChunk), desc="  \__ {0}".format(colored("Progress", "cyan")), dynamic_ncols=True, leave=leaveFlag)

				else:
					completed = tqdm(completed, total=len(targetChunk), desc="  \__ {0}".format(colored("Progress {0}/{1}".format(iteration, numberOfChunks), "cyan")), dynamic_ncols=True, leave=leaveFlag)

				for task in completed:
					result = task.result()

					if result is not None:
						takeovers.append(result)

			except KeyboardInterrupt:
				completed.close()
				print(colored("\n[*]-Received keyboard interrupt! Shutting down...\n", "red"))
				executor.shutdown(wait=False)
				exit(-1)

		if iteration < numberOfChunks:
			stderr.write("\033[F")

		iteration += 1

	return takeovers


def init(db, domain, old_takeovers, hideFindings, threads):
	loadTemplates()

	targets = set()
	notify = False
	takeovers = []
	notifications = []
	timestamp = int(time())

	parser = RawConfigParser()
	parser.read("config.ini")
	SLACK_LEGACY_TOKEN = parser.get("Slack", "SLACK_LEGACY_TOKEN")
	SLACK_CHANNEL = parser.get("Slack", "SLACK_CHANNEL")

	if SLACK_LEGACY_TOKEN and SLACK_CHANNEL:
		notify = True

	for row in db.query(Resolution).filter(Resolution.domain == domain):
		if row.subdomain:
			targets.add(".".join([row.subdomain, domain]))

		else:
			targets.add(domain)

	for row in db.query(Unresolved).filter(Unresolved.domain == domain):
		if row.subdomain:
			targets.add(".".join([row.subdomain, domain]))

		else:
			targets.add(domain)

	targets = list(targets)
	results = massTakeOver(targets, threads)

	del targets
	collect()

	for result in results:
		if result:
			db.add(Takeover(subdomain=".".join(result[1].split(".")[:-1 * len(domain.split("."))]), domain=domain, provider=result[0], signature=result[2], timestamp=timestamp))

			try:
				db.commit()

			except (IntegrityError, FlushError):
				db.rollback()

	del results
	collect()

	for row in db.query(Takeover).filter(Takeover.domain == domain, Takeover.timestamp == timestamp).order_by(Takeover.subdomain):
		if row.subdomain:
			takeovers.append((".".join([row.subdomain, domain]), row.provider, row.signature))

		else:
			takeovers.append((domain, row.provider, row.signature))

	print("    \__ {0} {1}".format(colored("New takeover vulnerabilities that were identified:", "yellow"), colored(len(takeovers), "cyan")))

	if not hideFindings:
		for takeover in takeovers:
			print("      \__ {0}: {1}, {2}".format(colored(takeover[0], "cyan"), colored(takeover[1], "yellow"), colored(takeover[2], "yellow")))

	if notify:
		for takeover in takeovers:
			if takeover[0] not in old_takeovers:
				notifications.append([takeover[0], takeover[1], takeover[2]])
	
	if notify:
		text = ""
		counter = 0			
		
		for notification in notifications:
			text += """Subdomain: {0}\nProvider: {1}\nSignature: {2}\n\n""".format(notification[0], notification[1], notification[2])
			counter += 1

			if counter % 20 == 0:
				slackNotification(SLACK_LEGACY_TOKEN, SLACK_CHANNEL, "```\n{0}```".format(text[:-1]))
				text = ""

		if text != "":
			slackNotification(SLACK_LEGACY_TOKEN, SLACK_CHANNEL, "```\n{0}```".format(text[:-1]))
