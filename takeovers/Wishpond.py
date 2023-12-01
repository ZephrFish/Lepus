from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["https://www.wishpond.com/404?campaign=true"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "wishpond.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Wishpond", domain, CNAME]

	return outcome
