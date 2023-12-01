from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["404 Blog is not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "hatenablog.com" in CNAME or "hatenadiary.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Hatena", domain, CNAME]

	return outcome
