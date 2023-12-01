from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["404 Page Not Found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "clientaccess.tave.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Tave", domain, CNAME]

	return outcome
