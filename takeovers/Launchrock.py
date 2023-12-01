from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Oops! Something went wrong."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "launchrock.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Launchrock", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "54.243.190.28" or str(entry) == "54.243.190.39" or str(entry) == "54.243.190.47" or str(entry) == "54.243.190.54":
			if findSignatures(domain, signatures, 1):
				outcome = ["Launchrock", domain, str(entry)]

	return outcome
