#!/usr/bin/python
#
# 	TimeZoneUpdater.py
#
# 	Copyright (c) 2021  IanSav.  All rights reserved.
#
# 	GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
#
# 	This program is free software: you can redistribute it and/or
# 	modify it under the terms of the GNU General Public License as
# 	published by the Free Software Foundation.  It is open source,
# 	you are allowed to use and modify it so long as you attribute
# 	and acknowledge the source and original author.  That is, the
# 	license, original author and this message must be retained at
# 	all times.
#
# 	This code was developed as open source software it should not
# 	be commercially distributed or included in any commercial
# 	software or used for commercial benefit.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	See <https://www.gnu.org/licenses/>.

from six import PY2
from sys import argv
from time import gmtime, strftime
try:
	from urllib.request import urlopen
except ImportError:
	from urllib2 import urlopen
from xml.etree.cElementTree import ParseError, fromstring
from babel import languages

TIMEZONEDB_FETCH = "http://api.timezonedb.com/v2.1/list-time-zone?key=%s&format=xml&fields=countryCode,countryName,zoneName,gmtOffset,dst"
OUTPUT_FILE = "timezone.xml"
TIMEZONEBASE = "GMT"  # Some prefer "UTC".
FILE_HEADER = """<?xml version="1.0" encoding="UTF-8"?>

<!--
	This data has been extracted from the official IANA data
	as distributed by TimezonesDB (https://timezonedb.com) on
	%s by the program TimeZoneUpdater written by IanSav.

	IMPORTANT NOTE: It is preferred that this file not be edited
	except to bring it into line with future IANA updates.  If this
	file must be edited please ensure that all zone entries are
	unique.  If there are *any* duplicated zone entries the Enigma2
	ConfigSelection UI control can/will fail!
-->

"""
nameReMap = (
	"Antarctica",
	"Argentina",
	"Australia",
	"Brazil",
	"Canada",
	"Chile",
	"China",
	"Cyprus",
	"Democratic Republic of the Congo",
	"Ecuador",
	"French Polynesia",
	"Germany",
	"Greenland",
	"Indonesia",
	"Kazakhstan",
	"Kiribati",
	"Malaysia",
	"Marshall Islands",
	"Mexico",
	"Micronesia",
	"Mongolia",
	"New Zealand",
	"Palestinian Territory",
	"Papua New Guinea",
	"Portugal",
	"Russia",
	"Spain",
	"Ukraine",
	"United States",
	"Uzbekistan",
)
zoneNameReMap = {
	"Antarctica/DumontDUrville": "Antarctica: Dumont d'Urville",
	"Antarctica/Macquarie": "Australia: Macquarie Island",
	"Atlantic/Canary": "Spain: Canary Islands",
	"Australia/Currie": "Australia: Currie (Deprecated use Hobart)",
	"Australia/Lindeman": "Australia: Lindeman Island",
	"Australia/Lord_Howe": "Australia: Lord Howe Island",
	"Pacific/Chatham": "New Zealand: Chatham Islands",
	"Pacific/Galapagos": "Ecuador: Galapagos Islands",
	"Pacific/Gambier": "French Polynesia: Gambier Islands",
	"Pacific/Marquesas": "French Polynesia: Marquesas Islands",
	"Pacific/Midway": "United States Minor Outlying Islands: Midway Islands",
	"Pacific/Pitcairn": "Pitcairn Islands",
	"Pacific/Wake": "United States Minor Outlying Islands: Wake Island",
}

print("TimeZoneUpdater version 1.2  -  Copyright (C) 2021  IanSav.\n")
print("This program comes with ABSOLUTELY NO WARRANTY.")
print("This is free software, and you are welcome to redistribute it under")
print("certain conditions.  See source code and GNUv3 for details.\n")
if len(argv) < 2:
	print("Usage: %s TimeZoneDBAccessKey [TimezoneOutputFile]" % argv[0])
	exit(1)
timeZoneKey = argv[1]
outputFile = argv[2] if len(argv) > 2 else OUTPUT_FILE
print("Fetching time zone data from '%s'..." % (TIMEZONEDB_FETCH % "<HIDDEN>"))
try:
	timeZoneData = urlopen(TIMEZONEDB_FETCH % timeZoneKey).read()
except Exception as err:
	print("Error: Unable to fetch current time zone data! (%s)" % str(err))
	exit(2)
timeZoneDom = fromstring(timeZoneData)
status = timeZoneDom.find("status").text
if status != "OK":
	message = timeZoneDom.find("message").text
	print("Error: Status of fetch is not OK! (%s): %s" % (status, message))
	exit(3)
timeZoneDom = timeZoneDom.find("zones")
timeZoneData = {}
print("Preparing time zone file...")
for zoneElement in timeZoneDom.findall("zone"):
	countryCode = zoneElement.find("countryCode").text
	languageCode = "en"
	for l in languages.get_official_languages(countryCode, de_facto=True):
		languageCode = l
		break
	localeCode = "%s_%s" % (languageCode, countryCode)
	countryName = zoneElement.find("countryName").text
	zoneName = zoneElement.find("zoneName").text
	gmtOffset = zoneElement.find("gmtOffset").text
	dst = zoneElement.find("dst").text.lower() in ("1", "true", "yes")  # API documentation says "0"/"1" but currently sends "false"/"true"!
	if countryName in nameReMap:
		zones = zoneName.split("/")
		if len(zones) == 3 and countryName != zones[-2]:
			countryName = "%s: %s; %s" % (countryName, zones[-2].replace("_", " "), zones[-1].replace("_", " "))
		else:
			countryName = "%s: %s" % (countryName, zones[-1].replace("_", " "))
	nameReplacement = zoneNameReMap.get(zoneName, None)
	if nameReplacement:
		countryName = nameReplacement
	gmtOffset = float(gmtOffset) - 3600.0 if dst else float(gmtOffset)
	data = str(gmtOffset / 3600.0).split(".")
	if len(data) == 2:
		data[1] = float("0.%s" % data[1]) * 60.0
	else:
		data.append("0")
	offset = "%+03d:%02d" % (int(data[0]), int(data[1]))
	if offset == "+00:00":
		offset = ""
	timeZoneData["%06d%s" % (gmtOffset + 100000, countryName)] = "\t<zone name=\"(%s%s) %s\" zone=\"%s\" countryCode=\"%s\" languageCode=\"%s\" localeCode=\"%s\" />" % (TIMEZONEBASE, offset, countryName, zoneName, countryCode, languageCode, localeCode)
timeZones = []
for timeZoneItem in sorted(list(timeZoneData.keys())):
	timeZones.append(timeZoneData[timeZoneItem])
print("Creating and writing time zone file...")
try:
	with open(outputFile, "w") as fd:
		fd.write(FILE_HEADER % strftime("%B %Y", gmtime()))
		fd.write("<timezone>\n")
		fd.write("\n".join(timeZones).encode("UTF-8", errors="ignore") if PY2 else "\n".join(timeZones))
		fd.write("\n</timezone>\n")
except (IOError, OSError) as err:
	print("Error %d: Unable to create time zone file '%s'!  (%s)" % (err.errno, outputFile, err.strerror))
	exit(4)
print("Time zone file '%s' created successfully." % outputFile)
exit(0)
