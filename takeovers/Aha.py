from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Unable to load ideas portal", "There is no portal here ... sending you back to Aha!"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "ideas.aha.io" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["aha!", domain, CNAME]

	return outcome
