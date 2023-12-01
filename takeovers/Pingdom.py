from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Sorry, couldn&rsquo;t find the status page"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "stats.pingdom.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Pingdom", domain, CNAME]

	return outcome
