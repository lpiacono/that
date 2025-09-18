import requests
from bs4 import BeautifulSoup

# disable python from generating a .pyc file
#sys.dont_write_bytecode = True

def getAdobeShockwaveTotalVulCount():
    #content url
    url = "http://www.cvedetails.com/product/6670/Adobe-Shockwave-Player.html"
    r = requests.get(url)

    #soupify it
    soup = BeautifulSoup(r.content, "lxml")

    #find table with versions from website
    souptable = soup.body.find(text='Total').parent
    #get total from TD next to it
    totalvul = souptable.find_next_sibling('td')
    #cleanup
    totalvul = totalvul.string.replace("\t", "").replace("\n", "")

    return totalvul