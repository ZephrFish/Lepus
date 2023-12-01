from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Perhaps you meant to visit", "This UserVoice subdomain is currently available!"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "uservoice.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["UserVoice", domain, CNAME]

	return outcome
