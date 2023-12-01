from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["YouTrack Starting Page"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "myjetbrains.com" in CNAME or "youtrack.cloud" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["JetBrains", domain, CNAME]

	return outcome
