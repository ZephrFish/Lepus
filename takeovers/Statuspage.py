from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Build trust with every incident"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "statuspage.io" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Statuspage", domain, CNAME]

	return outcome
