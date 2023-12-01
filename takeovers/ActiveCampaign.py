from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["LIGHTTPD - fly light."]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "activehosted.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Activecampaign", domain, CNAME]

	return outcome
