from utilities.ScanHelpers import findNX


def init(domain, ARecords, CNAMERecords):
	outcome = []

	for entry in CNAMERecords:
		CNAME = str(entry)[:-1]

		if any(azureSub in CNAME for azureSub in ["azure-api.net", "azurecontainer.io", "azurecr.io", "azuredatalakeanalytics.net", "azuredatalakestore.net", 
			"azureedge.net", "azurehdinsight.net", "azurefd.net", "azurehealthcareapis.com", "azureiotcentral.com", "azurewebsites.net", "batch.azure.com",
			"blob.core.windows.net", "cloudapp.azure.com", "cloudapp.net", "core.windows.net", "database.windows.net", "p.azurewebsites.net", "redis.cache.windows.net", 
			"search.windows.net", "service.signalr.net", "servicebus.windows.net", "trafficmanager.net", "visualstudio.com"]):

			if findNX(CNAME):
				outcome = ["Azure", domain, CNAME]

	return outcome
