# MLH Hackathon Scraper
#
# MLH's webpage listing all the hackathons going on in a particular year [0]
# does not list the hackathons in the order in which they are announced.
# Meaning, it's difficult to see know which hackathons just appeared on the
# list. It'd be nice to know which hackathon you haven't yet looked at. Well,
# that's what this script does.
# [0]: https://mlh.io/seasons/na-2017/events
#
# Author:  Kevin Dong (https://www.github.com/kevindong)
# License: MIT License
# Date:    September 8, 2016
# Source:  https://www.github.com/kevindong/MLH_Hackathon_Tracker

import requests
import time
import fnmatch
import os
from sys import exit
from lxml import html

print("Please note that VERY little testing has been done on this script.\n")

print("Attempting to download page... "),
page = requests.get("https://mlh.io/seasons/na-2017/events")
if page.status_code != 200:
	print("Error")
	exit(1)
else:
	print("Done")

print("Attempting to save downloaded page... ")
if not (os.path.exists('Hackathons')):
	print("\tThe \"Hackathons\" directory was not found. Creating now...")
	os.makedirs("Hackathons")
currentTime = time.strftime("%Y%m%d_at_%H%M%S")
webpageFile = open("Hackathons/" + currentTime + '.html', 'w')
webpageFile.write(page.text.encode('utf8'))
webpageFile.close()
print("\tDone writing to: " + currentTime + '.html')

print("Attempting to parse downloaded page... "),
htmlTree = html.fromstring(page.content)
hackathons = htmlTree.xpath('//h3[@itemprop="name"]/text()')
print("Done")

print("Attempting to save parsed data... ")
hackathonsFile = open("Hackathons/" + currentTime + '.txt', 'w')
for item in hackathons:
	hackathonsFile.write("%s\n" % item)
hackathonsFile.close()
print("\tDone writing to: " + currentTime + '.txt')

print("Detecting if previous runs exist...")
hackathonsDirectory = os.listdir("Hackathons")
hackathonsDirectory.sort()
for item in hackathonsDirectory:
	if ('.txt' not in item):
		hackathonsDirectory.remove(item)
if (len(hackathonsDirectory) > 1):
	print("\tAssumed this program has been previously run...")
else:
	print("\tAssumed this program has not been previously run...")
	exit(0)

print("Attempting to open previous record: " + hackathonsDirectory[-2] + '...'),
previousHackathonFile = open("Hackathons/" + hackathonsDirectory[-2], 'r')
print("Done\n\n")

print("Parsing previous record now...")
previousHackathonList = [line.rstrip('\n') for line in previousHackathonFile]
newHackathons = []
for item in hackathons:
	if item not in previousHackathonList:
		newHackathons.append(item)
if len(newHackathons) == 0:
	print("No new hackathons were detected. :(")
	os.remove("Hackathons/" + currentTime + '.txt')
	os.remove("Hackathons/" + currentTime + '.html')
	print("The files generated during this run were deleted.");
else:
	print("The following hackathons are new: ")
	for item in newHackathons:
		print(item)
	print("\nHappy hacking!")
