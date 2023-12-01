from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Looks Like You're Lost"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "pageserve.co" in CNAME or "secure.pageserve.co" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Instapage", domain, CNAME]

	return outcome
