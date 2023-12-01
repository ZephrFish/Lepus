from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Oops.</h2><p class=\"text-muted text-tight\">The page you're looking for doesn't exist."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "aftership.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Aftership", domain, CNAME]

	return outcome
