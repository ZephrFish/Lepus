from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "custom.intercom.help" in CNAME or "custom.eu.intercom.help" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Intercom", domain, CNAME]

	return outcome
