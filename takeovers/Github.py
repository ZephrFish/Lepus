from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["There isn't a GitHub Pages site here."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "github.io" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Github", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "192.30.252.153" or str(entry) == "192.30.252.154":
			if findSignatures(domain, signatures, 1):
				outcome = ["Github", domain, str(entry)]

	return outcome
