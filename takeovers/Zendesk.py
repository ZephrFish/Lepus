from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Help Center Closed"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if ".zendesk.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Zendesk", domain, CNAME]

	return outcome
