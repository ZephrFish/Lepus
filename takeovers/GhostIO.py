from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Failed to resolve DNS path for this host"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "ghost.io" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Ghost.io", domain, CNAME]

	return outcome
