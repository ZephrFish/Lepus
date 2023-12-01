from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["<p class=\"bc-gallery-error-code\">Error Code: 404</p>"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "bcvp0rtal.com" in CNAME or "brightcovegallery.com" in CNAME or "gallery.video" in CNAME or "cloudfront.net" in CNAME:
			if findSignatures(domain, signatures, 1):
				outcome = ["Brightcove", domain, CNAME]

	return outcome
