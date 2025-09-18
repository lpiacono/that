import requests
from bs4 import BeautifulSoup

# disable python from generating a .pyc file
#sys.dont_write_bytecode = True

def getJavaJRETotalVulCount():
    #content url
    url = "http://www.cvedetails.com/product/19117/Oracle-JRE.html"
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