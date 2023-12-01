from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Sign Up and Get Started"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "redirect.feedpress.me" in CNAME:
			if findSignatures(domain, signatures, 2):
				outcome = ["Feedpress", domain, CNAME]

	return outcome
