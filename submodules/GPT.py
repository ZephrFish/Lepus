import re
import base64
import openai
import requests
from tqdm import tqdm
from re import findall
from gc import collect
from time import sleep
from termcolor import colored
from configparser import RawConfigParser
from concurrent.futures import ThreadPoolExecutor, as_completed

from utilities.DatabaseHelpers import Resolution, Unresolved
from utilities.ScanHelpers import identifyWildcards, massResolve
import utilities.MiscHelpers


def getKey():
	parser = RawConfigParser()
	parser.read("config.ini")
	CHATGPT_API_KEY = parser.get("ChatGPT", "CHATGPT_API_KEY")

	if CHATGPT_API_KEY == "":
		return None
	else:
		return CHATGPT_API_KEY


def generateWithKey(key, domain, gptGive, gptReceive, gptLoop, chunk):
	sleep(2)
	subdomains = []

	for i in range(0, len(chunk)):
		chunk[i] = "{0}.{1}".format(chunk[i], domain)

	prompt = "Please generate {0} subdomains similar to {1}".format(gptReceive, ", ".join(chunk))
	openai.api_key = key

	errors = 0

	for i in range(0, gptLoop):
		while errors < 10:
			
			try: 
				response = openai.ChatCompletion.create(
					model="gpt-3.5-turbo",
					messages=[
						{"role": "system", "content": "You are a helpful assistant."},
						{"role": "user", "content": prompt},
					],
				)
				findings = re.findall("([\w\d][\w\d\-\.]*\.{0})".format(domain.replace(".", "\.")), str(response))
				subdomains.extend(findings)
				break

			except openai.error.RateLimitError as e:
				time.sleep(30)
				errors += 1

			except Exception as e:
				errors += 1

	return subdomains


def init(db, domain, gptGive, gptReceive, gptConcurrent, gptLoop, hideWildcards, hideFindings, excludeUnresolved, threads):
	base = set()
	key = getKey()

	if not key:
		print("{0}".format(colored("\n[*]-Using ChatGPT requires an API key which has not been provided...", "yellow")))
		return

	for row in db.query(Resolution).filter(Resolution.domain == domain, Resolution.isWildcard == False):
		if row.subdomain:
			base.add(row.subdomain)

	if not excludeUnresolved:
		for row in db.query(Unresolved).filter(Unresolved.domain == domain):
			if row.subdomain:
				base.add(row.subdomain)

	chunkSize = gptGive

	if len(base) % chunkSize > 0:
		numberOfChunks = len(base) // chunkSize + 1
	else:
		numberOfChunks = len(base) // chunkSize

	baseChunks = utilities.MiscHelpers.chunkify(list(base), chunkSize)
	subdomains = []

	with ThreadPoolExecutor(max_workers=gptConcurrent) as executor:
		tasks = {executor.submit(generateWithKey, key, domain, gptGive, gptReceive, gptLoop, chunk): chunk for chunk in baseChunks}

		print("{0} {1} {2}".format(colored("\n[*]-Using ChatGPT to generate candidates based on", "yellow"), colored("{0}".format(len(base)), "cyan"), colored(f"hostnames found...", "yellow")))

		try:
			completed = as_completed(tasks)
			completed = tqdm(completed, total=numberOfChunks, desc="  \__ {0}".format(colored("Progress", "cyan")), dynamic_ncols=True, leave=True)

			for task in completed:
				result = task.result()
				subdomains.extend(result)

		except KeyboardInterrupt:
			completed.close()
			print(colored("\n[*]-Received keyboard interrupt! Shutting down...", "red"))
			utilities.MiscHelpers.exportFindings(db, domain, [], True)
			executor.shutdown(wait=False)
			exit(-1)

	for i in range(0, len(subdomains)):
		subdomains[i] = re.sub(f"\.{domain}$", "", subdomains[i])

	subdomains = set(subdomains)
	subdomains.difference_update(base)
	finalSubdomains = []

	for item in subdomains:
		finalSubdomains.append((item, "GPT"))

	print("{0} {1} {2}".format(colored("\n[*]-Generated", "yellow"), colored(len(finalSubdomains), "cyan"), colored("hostname candidates", "yellow")))

	identifyWildcards(db, finalSubdomains, domain, hideFindings, threads)
	massResolve(db, finalSubdomains, domain, hideWildcards, hideFindings, threads)
