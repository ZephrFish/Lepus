from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["But if you're looking to build your own website"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "s.strikinglydns.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Strikingly", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "54.183.102.22":
			if findSignatures(domain, signatures, 1):
				outcome = ["Strikingly", domain, str(entry)]

	return outcome
