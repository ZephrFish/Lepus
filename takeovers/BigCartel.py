from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["<h1>Oops! We couldn&#8217;t find that page.</h1>"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "bigcartel.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Bigcartel", domain, CNAME]

	return outcome
