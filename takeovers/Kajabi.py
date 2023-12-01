from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["No such app", "not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "endpoint.mykajabi.com" in CNAME or "ssl.kajabi.com" in CNAME:
			if findSignatures(domain, signatures, 2):
				outcome = ["Kajabi", domain, CNAME]

	return outcome
