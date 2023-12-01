from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Sorry, we couldn't find that page."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if ".desk.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Desk", domain, CNAME]

	return outcome