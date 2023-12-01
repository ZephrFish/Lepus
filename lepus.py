#!/usr/bin/env python3

from argparse import ArgumentParser, FileType
from warnings import simplefilter
from termcolor import colored
from time import sleep
from gc import collect
from glob import glob
import sys
import importlib.util
import submodules.Permutations
import submodules.Expand
import submodules.Enrich
import submodules.PortScan
import submodules.ReverseLookups
import submodules.TakeOver
import submodules.Front
import submodules.Markov
import submodules.GPT
import submodules.Regulator
import utilities.DatabaseHelpers
import utilities.MiscHelpers
import utilities.ScanHelpers

simplefilter("ignore")
version = "3.5.0"


def printBanner():
	print(colored("         ______  _____           ______", "yellow"))
	print(colored(" |      |______ |_____) |     | (_____ ", "yellow"))
	print(colored(" |_____ |______ |       |_____| ______)", "yellow"))
	print(colored("                                v{0}".format(version), "cyan"))
	sleep(1)


if __name__ == "__main__":
	parser = ArgumentParser(prog="lepus.py", description="Infrastructure OSINT")
	parser.add_argument("domain", help="domain to search")
	parser.add_argument("-w", "--wordlist", action="store", dest="wordlist", help="wordlist with subdomains", type=FileType("r"))
	parser.add_argument("-eu", "--exclude-unresolved", action="store_true", dest="excludeUnresolved", help="exclude unresolved domains from all modules", default=False)
	parser.add_argument("-hw", "--hide-wildcards", action="store_true", dest="hideWildcards", help="hide wildcard resolutions", default=False)
	parser.add_argument("-hf", "--hide-findings", action="store_true", dest="hideFindings", help="hide all findings from all modules (only write to db and files)", default=False)
	parser.add_argument("-t", "--threads", action="store", dest="threads", help="number of threads [default is 100]", type=int, default=100)
	parser.add_argument("-nc", "--no-collectors", action="store_true", dest="noCollectors", help="skip passive subdomain enumeration", default=False)
	parser.add_argument("-zt", "--zone-transfer", action="store_true", dest="zoneTransfer", help="attempt to zone transfer from identified name servers", default=False)
	parser.add_argument("--permutate", action="store_true", dest="permutate", help="perform permutations on resolved domains", default=False)
	parser.add_argument("-pw", "--permutation-wordlist", action="store", dest="permutation_wordlist", help="wordlist to perform permutations with [default is lists/words.txt]", type=FileType("r"), default="lists/words.txt")
	parser.add_argument("--expand", action="store_true", dest="expand", help="expand subdomains from a subdomain level", default=False)
	parser.add_argument("-ed", "--expand-depth", action="store", dest="expand_depth", help="level of subdomains to start from", type=int, default=1)
	parser.add_argument("-ew", "--expand-wordlist", action="store", dest="expand_wordlist", help="wordlist to perform expansions with [default is lists/subdomains-top5000.txt]", type=FileType("r"), default="lists/subdomains-top5000.txt")
	parser.add_argument("--enrich", action="store_true", dest="enrich", help="perform enrichment permutations on resolved domains", default=False)
	parser.add_argument("-el", "--enrich-length", action="store", dest="enrich_length", help="min length of strings used [default is 2]", type=int, default=2)
	parser.add_argument("--gpt", action="store_true", dest="gpt", help="use ChatGPT to generate potential subdomains", default=False)
	parser.add_argument("-gg", "--gpt-give", action="store", dest="gpt_give", help="how many of subdomains to give ChatGPT as an example [default is 10]", type=int, default=10)
	parser.add_argument("-gr", "--gpt-receive", action="store", dest="gpt_receive", help="how many of subdomains to request from ChatGPT [default is 100]", type=int, default=100)
	parser.add_argument("-gc", "--gpt-concurrent", action="store", dest="gpt_concurrent", help="ChatGPT concurrent qury count [default is 4]", type=int, default=4)
	parser.add_argument("-gl", "--gpt-loop", action="store", dest="gpt_loop", help="how many times to run each query [default is 1]", type=int, default=1)
	parser.add_argument("--reverse", action="store_true", dest="reverse", help="perform reverse dns lookups on resolved public IP addresses", default=False)
	parser.add_argument("-ripe", "--ripe", action="store_true", dest="ripe", help="query ripe database with the 2nd level domain for networks to be used for reverse lookups", default=False)
	parser.add_argument("-r", "--ranges", action="store", dest="ranges", help="comma seperated ip ranges to perform reverse dns lookups on", type=str, default=None)
	parser.add_argument("-or", "--only-ranges", action="store_true", dest="only_ranges", help="use only ranges provided with -r or -ripe and not all previously identified IPs", default=False)
	parser.add_argument("--markovify", action="store_true", dest="markovify", help="use markov chains to identify more subdomains", default=False)
	parser.add_argument("-ms", "--markov-state", action="store", dest="markov_state", help="markov state size [default is 3]", type=int, default=3)
	parser.add_argument("-ml", "--markov-length", action="store", dest="markov_length", help="max length of markov substitutions [default is 5]", type=int, default=5)
	parser.add_argument("-mq", "--markov-quantity", action="store", dest="markov_quantity", help="max quantity of markov results per candidate length [default is 5]", type=int, default=5)
	parser.add_argument("--regulate", action="store_true", dest="regulate", help="use regular language ranking to identify more subdomains", default=False)
	parser.add_argument("-rt", "--reg-threshold", action="store", dest="reg_threshold", help="Threshold to start performing ratio test [default is 500]", type=int, default=500)
	parser.add_argument("-rmr", "--reg-max-ratio", action="store", dest="reg_max_ration", help="Ratio test parameter R: len(Synth)/len(Obs) < R [default is 25]", type=int, default=25)
	parser.add_argument("-rml", "--reg-max-length", action="store", dest="reg_max_length", help="Maximum rule length for global search [default is 1000]", type=int, default=1000)
	parser.add_argument("-rdl", "--reg-dist-low", action="store", dest="reg_dist_low", help="Lower bound on string edit distance range [default is 2]", type=int, default=2)
	parser.add_argument("-rdh", "--reg-dist-high", action="store", dest="reg_dist_high", help="Upper bound on string edit distance range [default is 10]", type=int, default=10)
	parser.add_argument("--portscan", action="store_true", dest="portscan", help="scan resolved public IP addresses for open ports", default=False)
	parser.add_argument("-p", "--ports", action="store", dest="ports", help="set of ports to be used by the portscan module [default is medium]", type=str)
	parser.add_argument("--takeover", action="store_true", dest="takeover", help="check identified hosts for potential subdomain take-overs", default=False)
	parser.add_argument("--front", action="store_true", dest="front", help="check identified hosts for potentially frontable domains", default=False)
	parser.add_argument("-f", "--flush", action="store_true", dest="doFlush", help="purge all records of the specified domain from the database", default=False)
	parser.add_argument("-v", "--version", action="version", version="Lepus v{0}".format(version))
	args = parser.parse_args()

	if not utilities.MiscHelpers.checkArgumentValidity(parser, args):
		exit(1)

	printBanner()
	db = utilities.DatabaseHelpers.init()

	if args.doFlush:
		utilities.MiscHelpers.purgeOldFindings(db, args.domain)
		print("{0} {1} {2}".format(colored("\n[*]-Flushed", "yellow"), colored(args.domain, "cyan"), colored("from the database", "yellow")))
		exit(0)

	print("{0} {1}".format(colored("\n[*]-Running against:", "yellow"), colored(args.domain, "cyan")))

	old_resolved, old_unresolved, old_takeovers, old_fronts = utilities.MiscHelpers.loadOldFindings(db, args.domain)
	utilities.MiscHelpers.purgeOldFindings(db, args.domain)

	try:
		utilities.ScanHelpers.retrieveDNSRecords(db, args.domain)

		if args.zoneTransfer:
			zt_subdomains = utilities.ScanHelpers.zoneTransfer(db, args.domain)

		else:
			zt_subdomains = None

		if args.noCollectors:
			collector_subdomains = None

		else:
			print()
			collector_subdomains = []
			modules = glob("collectors/*.py")
			modules.sort()

			for module in modules:
				if not module.endswith("__init__.py") and module[-3:] == ".py":
					spec = importlib.util.spec_from_file_location("module.name", module)
					mod = importlib.util.module_from_spec(spec)
					sys.modules["module.name"] = mod
					spec.loader.exec_module(mod)
					collector_subdomains += mod.init(args.domain)

		if args.wordlist:
			wordlist_subdomains = utilities.MiscHelpers.loadWordlist(args.domain, args.wordlist)

		else:
			wordlist_subdomains = None

		findings = utilities.MiscHelpers.cleanupFindings(args.domain, old_resolved, old_unresolved, zt_subdomains, collector_subdomains, wordlist_subdomains)

		del old_unresolved
		del zt_subdomains
		del collector_subdomains
		del wordlist_subdomains
		collect()

		if findings:
			utilities.ScanHelpers.identifyWildcards(db, findings, args.domain, args.hideFindings, args.threads)
			utilities.ScanHelpers.massResolve(db, findings, args.domain, args.hideWildcards, args.hideFindings, args.threads)

			del findings
			collect()

			if args.permutate:
				submodules.Permutations.init(db, args.domain, args.permutation_wordlist, args.hideWildcards, args.hideFindings, args.excludeUnresolved, args.threads)

			if args.expand:
				submodules.Expand.init(db, args.domain, args.expand_depth, args.expand_wordlist, args.hideWildcards, args.hideFindings, args.excludeUnresolved, args.threads)

			if args.enrich:
				submodules.Enrich.init(db, args.domain, args.enrich_length, args.hideWildcards, args.hideFindings, args.excludeUnresolved, args.threads)

			if args.reverse:
				submodules.ReverseLookups.init(db, args.domain, args.ripe, args.ranges, args.only_ranges, args.hideFindings, args.threads)

			if args.markovify:
				submodules.Markov.init(db, args.domain, args.markov_state, args.markov_length, args.markov_quantity, args.hideWildcards, args.hideFindings, args.excludeUnresolved, args.threads)

			if args.gpt:
				submodules.GPT.init(db, args.domain, args.gpt_give, args.gpt_receive, args.gpt_concurrent, args.gpt_loop, args.hideWildcards, args.hideFindings, args.excludeUnresolved, args.threads)

			if args.regulate:
				try:
					submodules.Regulator.init(db, args.domain, args.reg_threshold, args.reg_max_ration, args.reg_max_length, args.reg_dist_low, args.reg_dist_high, args.hideWildcards, args.excludeUnresolved, args.hideFindings, args.threads)
				except MemoryError:
					collect()
					print("  \__", colored("MemoryError, module execution failed...", "red"))
					
			utilities.ScanHelpers.massRDAP(db, args.domain, args.hideFindings, args.threads)

			if args.portscan:
				submodules.PortScan.init(db, args.domain, args.ports, args.hideFindings, args.threads)

			if args.takeover:
				submodules.TakeOver.init(db, args.domain, old_takeovers, args.hideFindings, args.threads)

			if args.front:
				submodules.Front.init(db, args.domain, old_fronts, args.hideFindings, args.threads)

		utilities.MiscHelpers.exportFindings(db, args.domain, old_resolved, False)

	except KeyboardInterrupt:
		print(colored("\n[*]-Received keyboard interrupt! Shutting down...", "red"))
		utilities.MiscHelpers.exportFindings(db, args.domain, old_resolved, True)
		exit(-1)
