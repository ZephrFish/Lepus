from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["page not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "stats.uptimerobot.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Uptime Robot", domain, CNAME]

	return outcome
