from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Want to create landing pages that will bring more people"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if ".gr8.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Getresponse", domain, CNAME]

	return outcome
