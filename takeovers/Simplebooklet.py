from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["you're looking for isn't here."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "simplebooklet.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Simplebooklet", domain, CNAME]

	return outcome
