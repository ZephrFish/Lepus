from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["You may have mistyped the address or the page may have moved."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "thinkific.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Thinkific", domain, CNAME]

	return outcome
