from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["project not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "surge.sh" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Surge.sh", domain, CNAME]

	return outcome
