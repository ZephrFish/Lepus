import re
import string
import datrie
import logging
import argparse
import tldextract
import editdistance

from tqdm import tqdm
from gc import collect
from typing import List, Set
from termcolor import colored
from itertools import combinations_with_replacement
from concurrent.futures import ThreadPoolExecutor, as_completed

from dank.DankEncoder import DankEncoder
from dank.DankGenerator import DankGenerator

from utilities.DatabaseHelpers import Resolution, Unresolved
from utilities.ScanHelpers import identifyWildcards, massResolve
import utilities.MiscHelpers

MEMO = {}
DNS_CHARS = string.ascii_lowercase + string.digits + '._-'


def edit_closures(items: List[str], delta: int = 5) -> List[Set[str]]:
	"""computes all subsets of items bounded by fixed edit distance"""
	global MEMO
	ret = []

	for a in items:
		found = False
		r = set([a])

		for b in items:
			dist = MEMO[a + b] if a + b in MEMO else MEMO[b + a]
			if dist < delta:
				r.add(b)

		for s in ret:
			if r == s:
				found = True
				break

		if not found:
			ret.append(r)

	return ret


def tokenize(items: List[str]):
	"""tokenize DNS hostnames into leveled word tokens"""
	ret = []
	hosts = []
	
	for item in items:
		t = tldextract.extract(item)
		hosts.append(t.subdomain)
	
	labels = [host.split(".") for host in hosts]
	
	for label in labels:
		n = []

		for item in label:
			t = []
			tokens = [f"-{e}" if i != 0 else e for i, e in enumerate(item.split("-"))]

			for token in tokens:
				subtokens = [x for x in re.split("([0-9]+)", token) if len(x) > 0]
				for i in range(len(subtokens)):

					# Special case where we have a hyphenated number: foo-12.example.com
					if subtokens[i] == "-" and i + 1 < len(subtokens):
						subtokens[i + 1] = "-" + subtokens[i + 1]
					else:
						t.append(subtokens[i])

			n.append(t)
		ret.append(n)
	return ret


def compress_number_ranges(regex: str) -> str:
	"""given an 'uncompressed' regex, returns a regex with ranges instead"""
	ret = regex[:]
	stack, groups, repl, extra, hyphen = [], [], {}, {}, {}

	for i, e in enumerate(regex):

		if e == "(":
			stack.append(i)

		elif e == ")":
			start = stack.pop()
			group = regex[start + 1 : i]
			tokens = group.split("|")
			numbers = [token for token in tokens if token.isnumeric()]
			nonnumbers = [
				token
				for token in tokens
				if not token.isnumeric() and not re.match("-[0-9]+", token)
			]
			hyphenatednumbers = [
				token[1:] for token in tokens if re.match("-[0-9]+", token)
			]

			# Only primitive groups: a single alteration of tokens
			if "?" in group or ")" in group or "(" in group:
				continue

			# Only allow one or the other for now
			elif len(numbers) != 0 and len(hyphenatednumbers) != 0:
				continue

			# At least 2 numerical tokens
			elif len(numbers) > 1:
				g1 = "|".join(numbers)
				g2 = "|".join(nonnumbers)
				repl[g1] = group
				extra[g1] = g2
				groups.append(g1)

			# At least 2 hyphenated numerical tokens
			elif len(hyphenatednumbers) > 1:
				g1 = "|".join(hyphenatednumbers)
				g2 = "|".join(nonnumbers)
				repl[g1] = group
				extra[g1] = g2
				groups.append(g1)
				hyphen[g1] = True

	for group in groups:
		generalized = "(" if not group in hyphen else "(-"
		positions = {}

		# Reverse because of the way integers are interpreted in hostnames
		tokens = [g[::-1] for g in group.split("|")]
		for token in tokens:
			for position, symbol in enumerate(token):
				if not position in positions:
					positions[position] = set([])
				positions[position].add(int(symbol))

		# A position is optional iff some token doesn't have that position
		s = sorted(tokens, key=lambda x: len(x))
		start, end = len(s[-1]) - 1, len(s[0]) - 1
		for i in range(start, end, -1):
			positions[i].add(None)

		# We go in reverse because of reversing the token order above
		for i, symbols in sorted(positions.items(), key=lambda x: x[0], reverse=True):
			optional = None in symbols

			if optional:
				symbols.remove(None)

			s = sorted(symbols)
			start, end = s[0], s[-1]

			if start != end:
				generalized += f'[{start}-{end}]{"?" if optional else ""}'

			else:
				generalized += f'{start}{"?" if optional else ""}'

		generalized += ")"
		ext = extra[group]
		rep = repl[group]

		if ext != "":
			generalized = f"({generalized}|({ext}))"

		ret = ret.replace(f"({rep})", generalized)

	return ret


def closure_to_regex(domain: str, members: List[str]) -> str:
	"""converts edit closure to a regular language"""
	ret, levels, optional = "", {}, {}
	tokens = tokenize(members)
	
	for member in tokens:
		for i, level in enumerate(member):
			if i not in levels:
				levels[i] = {}
				optional[i] = {}
			
			for j, token in enumerate(level):
				if not j in levels[i]:
					levels[i][j] = set([])
					optional[i][j] = []
				
				levels[i][j].add(token)
				optional[i][j].append(token)

	for i, level in enumerate(levels):
		n = "(." if i != 0 else ""
		
		for j, position in enumerate(levels[level]):
			k = len(levels[level][position])
		
			# Special case: first token in DNS name
			if i == 0 and j == 0:
				n += f"({'|'.join(levels[level][position])})"
		
			# Special case: single element in alternation at start of level
			elif k == 1 and j == 0:
				# TODO: Should we make this optional too?
				n += f"{'|'.join(levels[level][position])}"
		
			# General case
			else:
				# A position is optional if some token doesn't have that position
				isoptional = len(optional[level][position]) != len(members)
				n += f"({'|'.join(levels[level][position])}){'?' if isoptional else ''}"

		# A level is optional if either not every host has the level, or if there
		# are distinct level values
		values = list(map(lambda x: "".join(x), zip(*optional[level].values())))
		isoptional = len(set(values)) != 1 or len(values) != len(members)
		ret += (n + ")?" if isoptional else n + ")") if i != 0 else n

	return compress_number_ranges(f"{ret}.{domain}")


def is_good_rule(regex: str, nkeys: int, threshold: int, max_ratio: float) -> bool:
	"""applies ratio test to determine if a rule is acceptable"""
	e = DankEncoder(regex, 256)
	nwords = e.num_words(1, 256)
	return nwords < threshold or (nwords / nkeys) < max_ratio


def init(db, domain, regThreshold, regMaxRatio, regMaxLength, regDistLow, regDistHigh, hideWildcards, hideFindings, threads):
	global DNS_CHARS, MEMO

	trie = datrie.Trie(DNS_CHARS)
	known_hosts, new_rules = set([]), set([])

	def first_token(item: str):
		tokens = tokenize([item])
		return tokens[0][0][0]

	base = set()

	for row in db.query(Resolution).filter(Resolution.domain == domain, Resolution.isWildcard == False):
		if row.subdomain:
			base.add(row.subdomain)

	for row in db.query(Unresolved).filter(Unresolved.domain == domain):
		if row.subdomain:
			base.add(row.subdomain)

	known_hosts = sorted(list(set([f"{subdomain}.{domain}" for subdomain in base])))

	for host in known_hosts:
		if host != domain:

			tokens = tokenize([host])

			if len(tokens) > 0 and len(tokens[0]) > 0 and len(tokens[0][0]) > 0:
				trie[host] = True

			else:
				known_hosts.remove(host)

	print("{0} {1} {2}".format(colored("\n[*]-Using regular language ranking against", "yellow"), colored(len(known_hosts), "cyan"), colored("known hosts...", "yellow")))

	print(colored("\n[*]-Performing rule generation. This might take a while...", "yellow"))

	for s, t in combinations_with_replacement(known_hosts, 2):
		MEMO[s+t] = editdistance.eval(s,t)

	for k in range(regDistLow, regDistHigh):
		closures = edit_closures(known_hosts, delta=k)

		for closure in closures:
			if len(closure) > 1:
				r = closure_to_regex(domain, closure)

				if len(r) > regMaxLength:
					continue

				if r not in new_rules and is_good_rule(r, len(closure), regThreshold, regMaxRatio):
					new_rules.add(r)

				else:
					pass

	ngrams = sorted(list(set(DNS_CHARS) | set([''.join([i,j]) for i in DNS_CHARS for j in DNS_CHARS])))
	
	for ngram in ngrams:
		keys = trie.keys(ngram)
		
		if len(keys) == 0:
			continue
		
		r = closure_to_regex(domain, keys)
		if r not in new_rules and is_good_rule(r, len(keys), regThreshold, regMaxRatio):
			new_rules.add(r)
		
		last, prefixes = None, sorted(list(set([first_token(k) for k in trie.keys(ngram)])))

		for prefix in prefixes:
			keys = trie.keys(prefix)
			r = closure_to_regex(domain, keys)

			if r not in new_rules and is_good_rule(r, len(keys), regThreshold, regMaxRatio):
				if last is None or not prefix.startswith(last):
					last = prefix
				else:
					continue
			
				new_rules.add(r)

			if len(prefix) > 1:
				
				for k in range(regDistLow, regDistHigh):
					closures = edit_closures(keys, delta=k)
					
					for closure in closures:
						r = closure_to_regex(domain, closure)

						if r not in new_rules and is_good_rule(r, len(closure), regThreshold, regMaxRatio):
							new_rules.add(r)
						elif r not in new_rules:
							pass

	print("  \__ {0} {1}".format(colored("Rules generated:", "yellow"), colored(len(new_rules), "cyan")))

	chunkSize = 1000
	if len(new_rules) <= chunkSize:
		print("{0} {1} {2}".format(colored("\n[*]-Generating candidates for ", "yellow"), colored("{0}".format(len(new_rules)), "cyan"), colored("rules...", "yellow")))

	else:
		print("{0} {1} {2}".format(colored("\n[*]-Generating candidates for", "yellow"), colored("{0}".format(len(new_rules)), "cyan"), colored(f"rules in chunks of {str(format (chunkSize, ',d'))}...", "yellow")))

	leaveFlag = True
	numberOfChunks = len(list(new_rules)) // chunkSize + 1
	baseChunks = utilities.MiscHelpers.chunkify(list(new_rules), chunkSize)
	iteration = 1

	for baseChunk in baseChunks:
		generators = []
		with ThreadPoolExecutor(max_workers=1) as executor:
			tasks = {executor.submit(DankGenerator, rule.strip()): rule for rule in baseChunk}
			print("{0} {1}".format(colored("\n[*]-Generating candidates for chunk", "yellow"), colored(str(iteration) + "/" + str(numberOfChunks), "cyan")))
			
			try:
				completed = as_completed(tasks)

				if iteration == numberOfChunks:
					leaveFlag = True

				if numberOfChunks == 1:
					completed = tqdm(completed, total=len(baseChunk), desc="  \__ {0}".format(colored("Progress", "cyan")), dynamic_ncols=True, leave=leaveFlag)

				else:
					completed = tqdm(completed, total=len(baseChunk), desc="  \__ {0}".format(colored("Progress", "cyan")), dynamic_ncols=True, leave=leaveFlag)

				for task in completed:
					result = task.result()
					generators.append(result)

			except KeyboardInterrupt:
				completed.close()
				print(colored("\n[*]-Received keyboard interrupt! Shutting down...", "red"))
				utilities.MiscHelpers.exportFindings(db, domain, [], True)
				executor.shutdown(wait=False)
				exit(-1)
		
		iteration += 1
		regulated = set()

		for generator in generators:
			for subdomain in generator:
				regulated.add(subdomain.decode('utf-8'))

		regulated = list(regulated)
		for i in range(0, len(regulated)):
			regulated[i] = re.sub(f"\.{domain}$", "", regulated[i])

		regulated = set(regulated)
		regulated.difference_update(base)
		finalRegulated = []

		for item in regulated:
			finalRegulated.append((item, "Regulator"))

		print("{0} {1} {2} {3}".format(colored("\n[*]-Generated", "yellow"), colored(len(finalRegulated), "cyan"), colored("candidates for chunk", "yellow"), colored(str(iteration - 1) + "/" + str(numberOfChunks), "cyan")))

		identifyWildcards(db, finalRegulated, domain, hideFindings, threads)
		massResolve(db, finalRegulated, domain, hideWildcards, hideFindings, threads)
