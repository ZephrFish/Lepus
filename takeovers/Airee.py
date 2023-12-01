from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["https://xn--80aqc2a.xn--p1ai/"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "cdn.airee.ru" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Airee", domain, CNAME]

	return outcome
