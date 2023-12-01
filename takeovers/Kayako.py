from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["That's not an active Kayako account"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "kayako.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Kayako", domain, CNAME]

	return outcome
