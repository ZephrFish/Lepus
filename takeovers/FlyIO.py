from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["not found:"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "edgeapp.net" in CNAME:
			if findSignatures(CNAME, signatures, 1):
				outcome = ["Fly.io", domain, CNAME]

	return outcome
