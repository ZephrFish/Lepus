from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Requested system was not found."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "zammad.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Zammad", domain, CNAME]

	return outcome
