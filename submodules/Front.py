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
from utilities.DatabaseHelpers import Resolution, Unresolved, Front
from utilities.MiscHelpers import chunkify, slackNotification


def identify(domain, ARecords, CNAMERecords):
	outcome = []

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "cloudfront" in CNAME:
			outcome = ["Cloudfront", domain, CNAME]
 
		elif 'appspot.com' in CNAME:
			outcome = ["Google", domain, CNAME]

		elif 'msecnd.net' in CNAME:
			outcome = ["Azure", domain, CNAME]

		elif 'aspnetcdn.com' in CNAME:
			outcome = ["Azure", domain, CNAME]

		elif 'azureedge.net' in CNAME:
			outcome = ["Azure", domain, CNAME]

		elif 'azurefd.net' in CNAME:
			outcome = ["Azure", domain, CNAME]

		elif 'a248.e.akamai.net' in CNAME:
			outcome = ["Akamai", domain, CNAME]

		elif 'secure.footprint.net' in CNAME:
			outcome = ["Level3", domain, CNAME]

		elif 'cloudflare' in CNAME:
			outcome = ["Cloudflare", domain, CNAME]

		elif 'unbouncepages.com' in CNAME:
			outcome = ["Unbounce", domain, CNAME]

		elif 'x.incapdns.net' in CNAME:
			outcome = ["Incapsula", domain, CNAME]

		elif 'fastly' in CNAME:
			outcome = ["Fastly", domain, CNAME]

	return outcome


def checkFront(domain):
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

	results = identify(domain, A, CNAME)
	return results


def massFront(targets, threads):
	fronts = []
	numberOfChunks = 1
	leaveFlag = False

	if len(targets) <= 100000:
		print("{0} {1} {2}".format(colored("\n[*]-Scanning", "yellow"), colored(len(targets), "cyan"), colored("domains for domain fronting...", "yellow")))

	else:
		print("{0} {1} {2}".format(colored("\n[*]-Scanning", "yellow"), colored(len(targets), "cyan"), colored("domains for domain fronting, in chunks of 100,000...", "yellow")))
		numberOfChunks = len(targets) // 100000 + 1

	targetChunks = chunkify(targets, 100000)
	iteration = 1

	for targetChunk in targetChunks:
		with ThreadPoolExecutor(max_workers=threads) as executor:
			tasks = {executor.submit(checkFront, target) for target in targetChunk}

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
						fronts.append(result)

			except KeyboardInterrupt:
				completed.close()
				print(colored("\n[*]-Received keyboard interrupt! Shutting down...\n", "red"))
				executor.shutdown(wait=False)
				exit(-1)

		if iteration < numberOfChunks:
			stderr.write("\033[F")

		iteration += 1

	return fronts


def init(db, domain, old_fronts, threads):
	targets = set()
	notify = False
	fronts = []
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
	results = massFront(targets, threads)

	del targets
	collect()

	for result in results:
		if result:
			db.add(Front(subdomain=".".join(result[1].split(".")[:-1 * len(domain.split("."))]), domain=domain, provider=result[0], signature=result[2], timestamp=timestamp))

			try:
				db.commit()

			except (IntegrityError, FlushError):
				db.rollback()

	del results
	collect()

	for row in db.query(Front).filter(Front.domain == domain, Front.timestamp == timestamp).order_by(Front.subdomain):
		if row.subdomain:
			fronts.append((".".join([row.subdomain, domain]), row.provider, row.signature))

		else:
			fronts.append((domain, row.provider, row.signature))

	print("    \__ {0} {1}".format(colored("New frontable domains that were identified:", "yellow"), colored(len(fronts), "cyan")))

	for front in fronts:
		print("      \__ {0}: {1}, {2}".format(colored(front[0], "cyan"), colored(front[1], "yellow"), colored(front[2], "yellow")))

		if notify:
			if front[0] not in old_fronts:
				notifications.append([front[0], front[1], front[2]])
	
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
