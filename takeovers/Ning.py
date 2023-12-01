from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Please double-check the address", "is free to take"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "ning.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Ning", domain, CNAME]

	return outcome
