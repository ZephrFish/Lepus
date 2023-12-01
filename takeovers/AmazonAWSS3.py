from re import findall
from utilities.ScanHelpers import findSignatures


def init(domain, ARecords, CNAMERecords):
	outcome = []

	signatures = ["NoSuchBucket"]

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if (findall(".*s3.*.amazonaws\.com", CNAME)):
			if findSignatures(domain, signatures, 2):
				outcome = ["Amazon AWS/S3", domain, CNAME]

	return outcome