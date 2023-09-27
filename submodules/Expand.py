from re import findall
from gc import collect
from termcolor import colored
from utilities.DatabaseHelpers import Resolution, Unresolved
from utilities.ScanHelpers import identifyWildcards, massResolve
import utilities.MiscHelpers


def extract_subdomains(subdomain_parts, level):
	extracted_subdomains = set()
    
	for part in subdomain_parts:
		subdomain_parts_list = part.split('.')

		if len(subdomain_parts_list) >= level:
			if level == 1:
				extracted_subdomain = subdomain_parts_list[-1]
			else:
				extracted_subdomain = ".".join(subdomain_parts_list[-level:])
			extracted_subdomains.add(extracted_subdomain)
    
	return extracted_subdomains


def init(db, domain, level, wordlist, hideWildcards, hideFindings, threads):
	base = set()
	extracted = set()

	for row in db.query(Resolution).filter(Resolution.domain == domain, Resolution.isWildcard == False):
		if row.subdomain:
			base.add(row.subdomain)

	for row in db.query(Unresolved).filter(Unresolved.domain == domain):
		if row.subdomain:
			base.add(row.subdomain)

	words = [line.strip() for line in wordlist.readlines()]
	wordlist.close()

	for i in range(1, level+1):
		extracted.update(extract_subdomains(base, level))
	
	chunkSize = int(len(extracted) / (int((len(words) * len(extracted)) / 500000) + 1))

	if len(extracted) <= chunkSize:
		print("{0} {1} {2}".format(colored("\n[*]-Performing expansions on", "yellow"), colored(len(extracted), "cyan"), colored("subdomains...", "yellow")))
	
	else:
		print("{0} {1} {2}".format(colored("\n[*]-Performing expansions on", "yellow"), colored(len(extracted), "cyan"), colored(f"subdomains in chunks of {str(format (chunkSize, ',d'))}...", "yellow")))

	if len(extracted) % chunkSize > 0:
		numberOfChunks = len(extracted) // chunkSize + 1
	else:
		numberOfChunks = len(extracted) // chunkSize

	baseChunks = utilities.MiscHelpers.chunkify(list(extracted), chunkSize)
	iteration = 1

	for chunk in baseChunks:
		expansions = set()

		for subdomain in chunk:
			for word in words:
				expansions.add(f"{word}.{subdomain}")

		expansions.difference_update(base)
		expansions = [(subdomain, "Expand") for subdomain in expansions]

		print("{0} {1} {2} {3}".format(colored("\n[*]-Generated", "yellow"), colored(len(expansions), "cyan"), colored("expanded subdomains for chunk", "yellow"), colored(str(iteration) + "/" + str(numberOfChunks), "cyan")))
		iteration += 1

		identifyWildcards(db, expansions, domain, hideFindings, threads)
		massResolve(db, expansions, domain, hideWildcards, hideFindings, threads)
