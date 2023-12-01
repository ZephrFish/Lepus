from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["https://www.alchemer.com"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "privatedomain.alchemer.com" in CNAME or "privatedomain.alchemer.eu" in CNAME or "privatedomain.alchemer-ca.com" in CNAME:
			if findSignatures(domain, signatures, 2):
				outcome = ["Alchemer", domain, CNAME]

	return outcome
