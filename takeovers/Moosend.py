from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["One account fits everything:"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "moosend.com" in CNAME or "m-pages.com" in CNAME:

			if "m-pages.com" in CNAME:
				outcome = ["Moosend Landing Page", domain, CNAME]

			elif not findSignatures(domain, signatures, 1):
				outcome = ["Moosend", domain, CNAME]

	return outcome
