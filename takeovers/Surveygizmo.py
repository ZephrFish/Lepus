from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["https://www.alchemer.com"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "privatedomain.sgizmo.com" in CNAME or "privatedomain.surveygizmo.eu" in CNAME or "privatedomain.sgizmoca.com" in CNAME:
			if findSignatures(domain, signatures, 2):
				outcome = ["Surveygizmo", domain, CNAME]

	return outcome
