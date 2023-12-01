from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Looks like you've traveled too far into cyberspace"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "vendecommerce.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Vend", domain, CNAME]

	return outcome
