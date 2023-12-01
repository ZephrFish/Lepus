from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["The gods are wise"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "pantheonsite.io" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Pantheon", domain, CNAME]

	for entry in ARecords:

		if "23.185.0." in str(entry) or "23.253." in str(entry):
			if findSignatures(domain, signatures, 1):
				outcome = ["Pantheon", domain, str(entry)]

	return outcome
