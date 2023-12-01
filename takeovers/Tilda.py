from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["Domain has been assigned.", "Please renew your subscription"]

	for entry in ARecords:

		if str(entry) == "185.203.72.17":
			if findSignatures(domain, signatures, 1):
				outcome = ["Tilda", domain, str(entry)]

	return outcome
