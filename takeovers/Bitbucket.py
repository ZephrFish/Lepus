from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Repository not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "bitbucket.io" in CNAME:
			if findSignatures(CNAME, signatures, 1):
				outcome = ["Bitbucket", domain, CNAME]

	return outcome