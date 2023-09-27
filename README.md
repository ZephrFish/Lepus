[![GitHub License](https://img.shields.io/badge/License-BSD%203--Clause-informational.svg)](https://github.com/GKNSB/Lepus/blob/master/LICENSE)
[![GitHub Python](https://img.shields.io/badge/Python-%3E=%203.9.5-informational.svg)](https://www.python.org/)
[![GitHub Version](https://img.shields.io/badge/Version-3.5.0-green.svg)](https://github.com/GKNSB/Lepus)
<a href="https://www.buymeacoffee.com/gknsb"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a beer&emoji=🍺&slug=gknsb&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" align="right" style="height: 40px !important;width: 108 !important;"/></a>

<br></br>
# Lepus

**Lepus** is a tool for enumerating subdomains, checking for subdomain takeovers and perform port scans - and boy, is it fast!

#### Basic Usage

```
lepus.py yahoo.com
```

## Summary
* [Enumeration modes](#Enumeration-modes)
* [Subdomain Takeover](#Subdomain-Takeover)
* [Port Scan](#Port-Scan)
* [Installation](#Installation)
* [Arguments](#Arguments)


## Enumeration modes
The enumeration modes are different ways lepus uses to identify sudomains for a given domain. These modes are:

* [Collectors](#Collectors)
* [Dictionary](#Dictionary)
* [Permutations](#Permutations)
* [Expand](#Expand)
* [Enrich](#Enrich)
* [Reverse DNS](#ReverseDNS)
* [Markov](#Markov)
* [ChatGPT](#ChatGPT)
* [Regulator](#Regulator)

Moreover:
* For all methods, lepus checks if the given domain or any generated potential subdomain is a *wildcard* domain or not.
* After identification, lepus collects ASN and network information for the identified domains that resolve to public IP Addresses.


### Collectors
The Collectors mode collects subdomains from the following services:

|Service|API Required|
|---|:---:|
|[AlienVault OTX](https://otx.alienvault.com/)|No|
|[Anubis-DB](https://jonlu.ca/anubis/)|No|
|[Bevigil](https://bevigil.com/)|Yes|
|[BinaryEdge](https://www.binaryedge.io/)|Yes|
|[BufferOver](https://tls.bufferover.run/)|Yes|
|[C99](https://api.c99.nl/)|Yes|
|[Censys](https://censys.io/)|Yes|
|[CertSpotter](https://sslmate.com/certspotter/)|No|
|[Columbus Elmasy](https://columbus.elmasy.com/)|No|
|[CommonCrawl](https://index.commoncrawl.org/)|No|
|[CRT](https://crt.sh/)|No|
|[DNSDumpster](https://dnsdumpster.com/)|No|
|[DNSRepo](http://dnsrepo.noc.org/)|Yes|
|[DNSTrails](https://securitytrails.com/dns-trails/)|Yes|
|[Digitorus](https://certificatedetails.com/)|No|
|[Farsight DNSDB](https://www.farsightsecurity.com/solutions/dnsdb/)|Yes|
|[FOFA](https://fofa.so/)|Yes|
|[Fullhunt](https://fullhunt.io/)|Yes|
|[HackerTarget](https://hackertarget.com/)|No|
|[HunterIO](https://hunter.io/)|Yes|
|[IntelX](https://intelx.io/)|Yes|
|[LeakIX](https://leakix.net/)|Yes|
|[Maltiverse](https://maltiverse.com/)|No|
|[Netlas](https://netlas.io/)|Yes|
|[PassiveTotal](https://www.riskiq.com/products/passivetotal/)|Yes|
|[Project Discovery Chaos](https://chaos.projectdiscovery.io/)|Yes|
|[Qianxin Hunter](https://hunter.qianxin.com/)|Yes|
|[RapidDNS](https://rapiddns.io/)|No|
|[ReconCloud](https://recon.cloud/)|No|
|[Redhunt Labs](https://redhuntlabs.com/)|Yes|
|[Riddler](https://riddler.io/)|Yes|
|[Robtex](https://www.robtex.com/)|Yes|
|[SecurityTrails](https://securitytrails.com/)|Yes|
|[Shodan](https://www.shodan.io/)|Yes|
|[SiteDossier](http://www.sitedossier.com/)|No|
|[ThreatBook](https://www.threatbook.cn/)|Yes|
|[ThreatCrowd](https://www.threatcrowd.org/)|No|
|[ThreatMiner](https://www.threatminer.org/)|No|
|[URLScan](https://urlscan.io/)|Yes|
|[VirusTotal](https://www.virustotal.com/)|Yes|
|[Wayback Machine](https://archive.org/web/)|No|
|[Webscout](https://webscout.io/)|No|
|[WhoisXMLAPI](https://www.whoisxmlapi.com/)|Yes|
|[ZoomEye](https://www.zoomeye.org/)|Yes|

You can add your API keys in the `config.ini` file.

The Collectors module will run by default on lepus. If you do not want to use the collectors during a lepus run (so that you don't exhaust your API key limits), you can use the `-nc` or `--no-collectors` argument.

### Dictionary
The dictionary mode can be used when you want to provide lepus a list of subdomains. You can use the `-w` or `--wordlist` argument followed by the file. A custom list comes with lepus located at `lists/subdomains.txt`. An example run would be:

```
lepus.py -w lists/subdomains.txt yahoo.com
```

### Permutations
The Permutations mode performs changes on the list of subdomains that have been identified. For each subdomain, a number of permutations will take place based on the `lists/words.txt` file. You can also provide a custom wordlist for permutations with the `-pw` or `--permutation-wordlist` argument, followed by the file name. An example run would be:

```
lepus.py --permutate yahoo.com
```

or

```
lepus.py --permutate -pw customsubdomains.txt yahoo.com
```

### Expand
The expansion mode performs brute-force of subdomains similar to the dictionary mode, but on subdomains of the root. For instance considering the following already identified findings:

```
dev.test.example.com
qa.test.example.com
```

In such a case, with a default depth of 1, Lepus would use a dictionary against `test.example.com`. You can use the `-ed` or `--expand-depth` to control the depth of subdomains to brute-force. Moreover, the wordlist to use can be changed with the `-ew` or `--expand-wordlist` flag. An example run would be:

```
lepus.py --expand yahoo.com
```

or

```
lepus.py --expand yahoo.com -ed 2 -ew lists/subdomains-top5000.txt
```

### Enrich
The enrichment mode identifies strings in already identified subdomains and uses these as an input wordlist similarly to the previously mentioned permutations module. Using the flag `-el` or `--enrich-length` the minimum length of the strings extracted can be changed from the default value of 2. An example run of this module would be:

```
lepus.py --enrich yahoo.com
```

or

```
lepus.py --enrich yahoo.com -el 3
```

### ReverseDNS
The ReverseDNS mode will gather all IP addresses that were resolved and perform a reverse DNS on each one in order to detect more subdomains. For example, if `www.example.com` resolves to `1.2.3.4`, lepus will perform a reverse DNS for `1.2.3.4` and gather any other subdomains belonging to `example.com`, e.g. `www2`,`internal` or `oldsite`.

To run the ReverseDNS module use the `--reverse` argument. Additionally, `--ripe` (or `-ripe`) can be used in order to instruct the module to query the RIPE database using the second level domain for potential network ranges. Moreover, lepus supports the `--ranges` (or `-r`) argument. You can use it to make reverse DNS resolutions against CIDRs that belong to the target domain.

By default this module will take into account all previously identified IPs, then defined ranges, then ranges identified through the RIPE database. In case you only want to run the module against specific or RIPE identified ranges, and not against all already identified IPs, you can use the `--only-ranges` (`-or`) argument.

An example run would be:

```
lepus.py --reverse yahoo.com
```

or

```
lepus.py --reverse -ripe -r 172.216.0.0/16,183.177.80.0/23 yahoo.com
```

or only against the defined or identified from RIPE

```
lepus.py --reverse -or -ripe -r 172.216.0.0/16,183.177.80.0/23 yahoo.com
```

Hint: lepus will identify `ASNs` and `Networks` during enumeration, so you can also use these ranges to identify more subdomains with a subsequent run.

### Markov
With this module, Lepus will utilize Markov chains in order to train itself and then generate subdomain based on the already known ones. The bigger the general surface, the better the tool will be able to train itself and subsequently, the better the results will be.

The module can be activated with the `--markovify` argument. Parameters also include the Markov state size, the maximum length of the generated candidate addition, and the quantity of generated candidates. Predefined values are 3, 5 and 5 respectively. Those arguments can be changed with `-ms` (`--markov-state`), `-ml` (`--markov-length`) and `-mq` (`--markov-quantity`) to meet your needs. Keep in mind that the larger these values are, the more time Lepus will need to generate the candidates.

It has to be noted that different executions of this module might generate different candidates, so feel free to run it a few times consecutively. Keep in mind that the higher the `-ms`, `-ml` and `-mq` values, the more time will be needed for candidate generation.

```
lepus.py --markovify yahoo.com
```

or

```
lepus.py --markovify -ms 5 -ml 10 -mq 10
```

### ChatGPT
By enabling this module with the `--gpt` argument, Lepus will utilize OpenAI's ChatGPT in order to generate more subdomains. By default, the prompt looks like the following:

```
Please generate 100 subdomains similar to <list of 10 subdomains already identified>"
```

You can use `-gg` (`--gpt-give`) and `-gr` (`--gpt-receive`) to control the ammount of subdomains you either ask for in each query, or the ammount of hostnames you provide it with. Moreover, `-gc` or `--gpt-concurrent` can be used to control concurrent queries made, and `-gl` or `--gpt-loop` can be used to loop over the same query more than once. An example run would be the following:

```
lepus.py --gpt yahoo.com
```

or

```
lepus.py --gpt yahoo.com -gg 10 -gr 200 -gc 8 -gl 4
```

### Regulator
This module's goal is to be able to automagically learn regexes that capture idiosyncratic features of observed DNS data. Using these learned patterns, Lepus will attempt to synthesize new subdomains that follow the same language patterns. This module utilizes the power of regular language ranking via the `dank` (https://github.com/cramppet/dank) library.

The module can be enabled with the `--regulate` flag. Moreover, the following additional flags can be provided to fine-tune the parameters and execution if needed:

* `-rt` or `--reg-threshold` 
* `-rmr` or `--reg-max-ratio`
* `-rml` or `--reg-max-length`
* `-rdl` or `--reg-dist-low`
* `-rdh` or `--reg-dist-high`

The module is a port of `Regulator` (https://github.com/cramppet/regulator) and more information can be found on the author's blog (https://cramppet.github.io/regulator/index.html).

An example exeuction of this module would be like the following:

```
lepus.py --regulate yahoo.com
```

or

```
lepus.py --regulate yahoo.com -rt 500 -rmr 25 -rml 1000 -rdl 2 -rdh 10
```

### Subdomain Takeover
Lepus has a list of signatures in order to identify if a domain can be taken over. You can use it by providing the `--takeover` argument. This module also supports Slack notifications, once a potential takeover has been identified, by adding a Slack token in the `config.ini` file. The checks are made against the following services:

* Acquia
* Activecampaign
* Aftership
* Aha!
* Airee
* Amazon AWS/S3
* Apigee
* Azure
* Bigcartel
* Bitbucket
* Brightcove
* Campaign Monitor
* Cargo Collective
* Desk
* Feedpress
* Fly[]().io
* Getresponse
* Ghost[]().io
* Github
* Hatena
* Helpjuice
* Helpscout
* Heroku
* Instapage
* Intercom
* JetBrains
* Kajabi
* Kayako
* Launchrock
* Mashery
* Maxcdn
* Moosend
* Ning
* Pantheon
* Pingdom
* Readme[]().io
* Simplebooklet
* Smugmug
* Statuspage
* Strikingly
* Surge[]().sh
* Surveygizmo
* Tave
* Teamwork
* Thinkific
* Tictail
* Tilda
* Tumblr
* Uptime Robot
* UserVoice
* Vend
* Webflow
* Wishpond
* Wordpress
* Zammad
* Zendesk

### Port Scan
The port scan module will check open ports against a target and log them in the results. You can use the `--portscan` argument which by default will scan ports 80, 443, 8000, 8080, 8443. You can also use custom ports or choose a predefined set of ports.

|Ports set|Ports|
|---|---|
|small|80, 443|
|medium (default)|80, 443, 8000, 8080, 8443|
|large|80, 81, 443, 591, 2082, 2087, 2095, 2096, 3000, 8000, 8001, 8008, 8080, 8083, 8443, 8834, 8888, 9000, 9090, 9443|
|huge|80, 81, 300, 443, 591, 593, 832, 981, 1010, 1311, 2082, 2087, 2095, 2096, 2480, 3000, 3128, 3333, 4243, 4567, 4711, 4712, 4993, 5000, 5104, 5108, 5800, 6543, 7000, 7396, 7474, 8000, 8001, 8008, 8014, 8042, 8069, 8080, 8081, 8088, 8090, 8091, 8118, 8123, 8172, 8222, 8243, 8280, 8281, 8333, 8443, 8500, 8834, 8880, 8888, 8983, 9000, 9043, 9060, 9080, 9090, 9091, 9200, 9443, 9800, 9943, 9980, 9981, 12443, 16080, 18091, 18092, 20720, 28017|

An example run would be:

```
lepus.py --portscan yahoo.com
```

or

```
lepus.py --portscan -p huge yahoo.com
```

or

```
lepus.py --portscan -p 80,443,8082,65123 yahoo.com
```

### Frontable Domains
The identification module for frontable domains uses a list of signatures in order to identify potential domains of interest that can be used for your domain fronting needs. This module is activated using the `--front` flag. This module also supports Slack notifications, once a potential takeover has been identified, by adding a Slack token in the `config.ini` file. The checks are made against the following services:

* Cloudfront
* Google
* Azure
* Akamai
* Level3
* Cloudflare
* Unbounce
* Incapsula
* Fastly


## Installation

1. Normal installation:

	```
	$ python3 -m pip install -r requirements.txt
	```

2. Preferably install in a virtualenv:

	```
	$ pyenv virtualenv 3.9.5 lepus
	$ pyenv activate lepus
	$ pip install -r requirements.txt
	```


## Arguments

```
usage: lepus.py [-h] [-w WORDLIST] [-hw] [-hf] [-t THREADS] [-nc] [-zt] [--permutate]
                [-pw PERMUTATION_WORDLIST] [--expand] [-ed EXPAND_DEPTH] [-ew EXPAND_WORDLIST] [--enrich]
                [-el ENRICH_LENGTH] [--gpt] [-gg GPT_GIVE] [-gr GPT_RECEIVE] [-gc GPT_CONCURRENT]
                [-gl GPT_LOOP] [--reverse] [-ripe] [-r RANGES] [-or] [--markovify] [-ms MARKOV_STATE]
                [-ml MARKOV_LENGTH] [-mq MARKOV_QUANTITY] [--regulate] [-rt REG_THRESHOLD]
                [-rmr REG_MAX_RATION] [-rml REG_MAX_LENGTH] [-rdl REG_DIST_LOW] [-rdh REG_DIST_HIGH]
                [--portscan] [-p PORTS] [--takeover] [--front] [-f] [-v]
                domain

Infrastructure OSINT

positional arguments:
  domain                domain to search

optional arguments:
  -h, --help            show this help message and exit
  -w WORDLIST, --wordlist WORDLIST
                        wordlist with subdomains
  -hw, --hide-wildcards
                        hide wildcard resolutions
  -hf, --hide-findings  hide all findings from all modules (only write to db and files)
  -t THREADS, --threads THREADS
                        number of threads [default is 100]
  -nc, --no-collectors  skip passive subdomain enumeration
  -zt, --zone-transfer  attempt to zone transfer from identified name servers
  --permutate           perform permutations on resolved domains
  -pw PERMUTATION_WORDLIST, --permutation-wordlist PERMUTATION_WORDLIST
                        wordlist to perform permutations with [default is lists/words.txt]
  --expand              expand subdomains from a subdomain level
  -ed EXPAND_DEPTH, --expand-depth EXPAND_DEPTH
                        level of subdomains to start from
  -ew EXPAND_WORDLIST, --expand-wordlist EXPAND_WORDLIST
                        wordlist to perform expansions with [default is lists/subdomains-top5000.txt]
  --enrich              perform enrichment permutations on resolved domains
  -el ENRICH_LENGTH, --enrich-length ENRICH_LENGTH
                        min length of strings used [default is 2]
  --gpt                 use ChatGPT to generate potential subdomains
  -gg GPT_GIVE, --gpt-give GPT_GIVE
                        how many of subdomains to give ChatGPT as an example [default is 10]
  -gr GPT_RECEIVE, --gpt-receive GPT_RECEIVE
                        how many of subdomains to request from ChatGPT [default is 100]
  -gc GPT_CONCURRENT, --gpt-concurrent GPT_CONCURRENT
                        ChatGPT concurrent qury count [default is 4]
  -gl GPT_LOOP, --gpt-loop GPT_LOOP
                        how many times to run each query [default is 1]
  --reverse             perform reverse dns lookups on resolved public IP addresses
  -ripe, --ripe         query ripe database with the 2nd level domain for networks to be used for reverse
                        lookups
  -r RANGES, --ranges RANGES
                        comma seperated ip ranges to perform reverse dns lookups on
  -or, --only-ranges    use only ranges provided with -r or -ripe and not all previously identified IPs
  --markovify           use markov chains to identify more subdomains
  -ms MARKOV_STATE, --markov-state MARKOV_STATE
                        markov state size [default is 3]
  -ml MARKOV_LENGTH, --markov-length MARKOV_LENGTH
                        max length of markov substitutions [default is 5]
  -mq MARKOV_QUANTITY, --markov-quantity MARKOV_QUANTITY
                        max quantity of markov results per candidate length [default is 5]
  --regulate            use regular language ranking to identify more subdomains
  -rt REG_THRESHOLD, --reg-threshold REG_THRESHOLD
                        Threshold to start performing ratio test [default is 500]
  -rmr REG_MAX_RATION, --reg-max-ratio REG_MAX_RATION
                        Ratio test parameter R: len(Synth)/len(Obs) < R [default is 25]
  -rml REG_MAX_LENGTH, --reg-max-length REG_MAX_LENGTH
                        Maximum rule length for global search [default is 1000]
  -rdl REG_DIST_LOW, --reg-dist-low REG_DIST_LOW
                        Lower bound on string edit distance range [default is 2]
  -rdh REG_DIST_HIGH, --reg-dist-high REG_DIST_HIGH
                        Upper bound on string edit distance range [default is 10]
  --portscan            scan resolved public IP addresses for open ports
  -p PORTS, --ports PORTS
                        set of ports to be used by the portscan module [default is medium]
  --takeover            check identified hosts for potential subdomain take-overs
  --front               check identified hosts for potentially frontable domains
  -f, --flush           purge all records of the specified domain from the database
  -v, --version         show program's version number and exit
```

The following command flushes all database entries for a specific domain:
```
./lepus.py python.org --flush
```