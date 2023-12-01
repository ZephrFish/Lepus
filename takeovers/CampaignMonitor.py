from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Wait, what's this charge on my credit card?"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "createsend.com" in CNAME:
			if findSignatures(CNAME, signatures, 1):
				outcome = ["Campaign Monitor", domain, CNAME]

	return outcome
