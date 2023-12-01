from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Do you want to register"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "wordpress.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Wordpress", domain, CNAME]

	return outcome
