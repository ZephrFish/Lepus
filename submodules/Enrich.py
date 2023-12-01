from re import findall
from gc import collect
from termcolor import colored
from utilities.DatabaseHelpers import Resolution, Unresolved
from utilities.ScanHelpers import identifyWildcards, massResolve
import utilities.MiscHelpers


def permuteDash(subdomain, wordlist):
	for word in wordlist:
		yield "-".join([word, subdomain])
		yield "-".join([subdomain, word])

	if "." in subdomain:
		subParts = subdomain.split(".")

		for part in subParts:
			for word in wordlist:
				yield subdomain.replace(part, "-".join([word, part]))
				yield subdomain.replace(part, "-".join([part, word]))


def permuteDot(subdomain, wordlist):
	for word in wordlist:
		yield ".".join([word, subdomain])
		yield ".".join([subdomain, word])

	if "." in subdomain:
		subParts = subdomain.split(".")

		for part in subParts:
			for word in wordlist:
				yield subdomain.replace(part, ".".join([word, part]))


def permuteWords(subdomain, wordlist):
	for word in wordlist:
		yield "".join([word, subdomain])
		yield "".join([subdomain, word])

	if "." in subdomain:
		subParts = subdomain.split(".")

		for part in subParts:
			for word in wordlist:
				yield subdomain.replace(part, "".join([word, part]))
				yield subdomain.replace(part, "".join([part, word]))


def permuteNumbers(subdomain):
	for number in range(10):
		yield "-".join([subdomain, str(number)])
		yield "".join([subdomain, str(number)])

	if "." in subdomain:
		subParts = subdomain.split(".")

		for part in subParts:
			for number in range(10):
				yield subdomain.replace(part, "-".join([part, str(number)]))
				yield subdomain.replace(part, "".join([part, str(number)]))


def permuteIterations(subdomain):
	instancesOfNumbers = findall("\d+", subdomain)	
	for instance in instancesOfNumbers:
		instancelength = len(instance)
		
		if instancelength == 1:				
			for newinstance in range(0,10):
				yield subdomain.replace(instance, str(newinstance))		
		
		elif instancelength == 2:				
			for newinstance in range(0,100):
				yield subdomain.replace(instance, str(newinstance))
		
		elif instancelength == 3:				
			for newinstance in range(0,1000):
				yield subdomain.replace(instance, str(newinstance))


def createWords(length, subdomains):
	words = set()

	for subdomain in subdomains:
		pattern1 = "[a-z]" * length + "+"
		pattern2 = "[0-9]" * length + "+"
		pattern3 = "\w" * length + "+"

		words.update(set(findall(pattern1, subdomain)))
		words.update(set(findall(pattern2, subdomain)))
		words.update(set(findall(pattern3, subdomain)))

	return words


def init(db, domain, enrichLength, hideWildcards, hideFindings, excludeUnresolved, threads):
	base = set()

	for row in db.query(Resolution).filter(Resolution.domain == domain, Resolution.isWildcard == False):
		if row.subdomain:
			base.add(row.subdomain)

	if not excludeUnresolved:
		for row in db.query(Unresolved).filter(Unresolved.domain == domain):
			if row.subdomain:
				base.add(row.subdomain)

	if len(base) <= 100:
		print("{0} {1} {2}".format(colored("\n[*]-Performing enrichment on", "yellow"), colored(len(base), "cyan"), colored("hostnames...", "yellow")))
	
	else:
		print("{0} {1} {2}".format(colored("\n[*]-Performing enrichment on", "yellow"), colored(len(base), "cyan"), colored("hostnames in chunks of 100...", "yellow")))
	
	numberOfChunks = len(base) // 100 + 1

	baseChunks = utilities.MiscHelpers.chunkify(list(base), 100)
	iteration = 1

	words = list(createWords(enrichLength, base))

	for chunk in baseChunks:
		generators = []
		permutations = set()

		for subdomain in chunk:
			generators.append(permuteDash(subdomain, words))
			generators.append(permuteDot(subdomain, words))
			generators.append(permuteWords(subdomain, words))
			generators.append(permuteNumbers(subdomain))
			generators.append(permuteIterations(subdomain))

		for generator in generators:
			for subdomain in generator:
				permutations.add(subdomain)

		permutations.difference_update(base)
		permutations = [(subdomain, "Enrich") for subdomain in permutations]

		print("{0} {1} {2} {3}".format(colored("\n[*]-Generated", "yellow"), colored(len(permutations), "cyan"), colored("enriched subdomain candidates for chunk", "yellow"), colored(str(iteration) + "/" + str(numberOfChunks), "cyan")))
		iteration += 1

		identifyWildcards(db, permutations, domain, hideFindings, threads)
		massResolve(db, permutations, domain, hideWildcards, hideFindings, threads)
