import requests
from bs4 import BeautifulSoup
import re

# disable python from generating a .pyc file
#sys.dont_write_bytecode = True

def getLatestJavaJREVulVersion():

    #content url
    url = "http://www.cvedetails.com/version-list/93/19117/1/Oracle-JRE.html"
    r = requests.get(url)

    #soupify it
    soup = BeautifulSoup(r.content, "lxml")

    #find table with versions from website
    souptable = soup.find('table', attrs={'class':'listtable'})

    #declare empty arrays for data
    data = []
    versions = []

    #for each row in table, place it inside data array
    for row in souptable.findAll("tr"):
        cells = row.findAll("td")
        if len(cells) > 0:
            data.append(cells)

    #for each td in table, extract data into an array
    for ele in data:
        #text cleanup from HTML obfuscation
        test = ele[0].string.replace("\t", "").replace("\n", "")
        
        #make sure its a version number, not an application name
        if test[0].isdigit() == True:
        
            #create sub version array
            subversion = []
            #get first 5 columns
            for td in ele[:3]:
                #cleanup html some more
                td = td.string.replace("\t", "").replace("\n", "")

                #make sure cell is not empty
                if len(td) > 0:
                    #make sure cell isn't text
                    if td[0].isdigit() == True or td[0].startswith("U"):
                        td = re.sub(r"[^.0-9]+", "",td)
                        subversion.append(td)

            versions.append(subversion)

    newversions = []

    for version in versions:
        if len(version) > 1:
            version = '.'.join(version)
            version = version[2:]
            newversions.append(version)

    return sorted(newversions, reverse=True)[0]

#print getLatestJavaJREVulVersion() 