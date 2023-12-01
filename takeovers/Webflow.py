from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["The page you are looking for doesn't exist or has been moved", "Page not found"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "proxy.webflow.com" in CNAME or "proxy-ssl.webflow.com" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Webflow", domain, CNAME]

	for entry in ARecords:

		if str(entry) == "34.193.69.252" or str(entry) == "34.193.204.92" or str(entry) == "23.235.33.229" or str(entry) == "104.156.81.229":
			if findSignatures(domain, signatures, 1):
				outcome = ["Webflow", domain, str(entry)]

	return outcome
