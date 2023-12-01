from utilities.ScanHelpers import findNX


def init(domain, ARecords, CNAMERecords):
	outcome = []

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "netdna-cdn.com" in CNAME:
			if findNX(CNAME):
				outcome = ["MaxCDN", domain, CNAME]

	return outcome