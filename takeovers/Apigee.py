from utilities.ScanHelpers import findNX


def init(domain, ARecords, CNAMERecords):
	outcome = []

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "-portal.apigee.net" in CNAME:
			if findNX(CNAME):
				outcome = ["Apigee", domain, CNAME]

	return outcome
