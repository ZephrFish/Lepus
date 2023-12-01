from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Whatever you were looking for doesn't currently exist at this address."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "domains.tumblr.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Tumblr", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "66.6.44.4":
			if findSignatures(domain, signatures, 1):
				outcome = ["Tumblr", domain, str(entry)]

	return outcome
