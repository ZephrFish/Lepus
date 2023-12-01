from requests import get
from warnings import simplefilter
from dns.resolver import Resolver, NXDOMAIN, NoAnswer, NoNameservers, Timeout


simplefilter("ignore")


def init(domain, ARecords, CNAMERecords):
	outcome = []
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if "domains.smugmug.com" in CNAME:
			try:
				if get("http://" + domain, headers=headers).status_code == 404:
					outcome = ["Smugmug", domain, CNAME]
					return outcome

			except Exception as e:
				pass

			try:
				if get("https://" + domain, headers=headers, verify=False).status_code == 404:
					outcome = ["Smugmug", domain, CNAME]
					return outcome

			except Exception as e:
				pass

			resolver = Resolver()
			resolver.timeout = 1
			resolver.lifetime = 1

			try:
				resolver.query(CNAME)

			except NXDOMAIN:
				outcome = ["Smugmug", domain, CNAME]

			return outcome
