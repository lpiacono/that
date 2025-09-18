from imports import *

def createObj():
    adobeObj = helper_hygieneclasses.hygieneCategory
    adobeObj.name = "Adobe"
    adobeObj.sensors = [
                            {"Filter": "", "Sensor" : "Installed Applications, that contains:adobe", "FileName" : "adobe.csv"},
                            {"Filter": "Installed Applications, that contains:adobe", "Sensor" : "Target", "FileName" : "adobetargets.csv"}
    ]
    return adobeObj


def processData(obj, prs, PPTXFileName):

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [Adobe] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."
    
    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    #Latest Java and Adobe Vulnerable Version
    from helper_getLatestAdobeFlashVulVersion import getLatestAdobeFlashVulVersion
    from helper_getLatestAdobeShockwaveVulVersion import getLatestAdobeShockwaveVulVersion

    #Total Adobe and Java Vul Count
    from helper_getAdobeFlashTotalVulCount import getAdobeFlashTotalVulCount
    from helper_getAdobeShockwaveTotalVulCount import getAdobeShockwaveTotalVulCount

    ##############################
    #Load Files into Panda Objects

    #Adobe Data
    try:
        aDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            aDF = cleanNoise(aDF,'Name',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']
        pass

    #Adobe Targets
    try:
        aTargetsDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']
        pass
    
    #######################
    #Adobe CSV Calculations
    #######################

    #total number endpoints reporting any adobe product installed
    try:
        aTotalTargets = aTargetsDF.loc[aTargetsDF['Target'] == 'Target', 'Count'].sum()
    except: 
        errorMsg()
        aTotalTargets = "0"
        pass

    #get total count of adobe products installed across endpoints
    try:
        aProductCount = len(aDF['Name'].unique())
    except:
        errorMsg()
        aProductCount = "0"
        pass

    #get total number of times adobe products installed across all endpoints
    try:
        aInstallCount = aDF['Count'].sum()
    except:
        errorMsg()
        aInstallCount = "0"
        pass

    #average install per endpoint given number of machines reporting adobe product installed
    try:
        if (aTotalTargets > 0):
            if (float(aInstallCount) / float(aTotalTargets)) < 1:
                aInstallAvg = int(math.ceil(float(aInstallCount) / float(aTotalTargets)))
            elif (float(aInstallCount) / float(aTotalTargets)) >= 1:
                aInstallAvg = int(float(aInstallCount) / float(aTotalTargets))
        else:
            aInstallAvg = 0
    except:
        errorMsg()
        aInstallAvg = "0"
        pass

    #########################
    #Adobe Shockwave Specific
    #########################

    #Number of Shockwave Products Installed
    try:
        aDFShockwave = aDF[aDF['Name'].str.contains("Shockwave Player")]
        aShockwaveCount = len(aDFShockwave['Version'].unique())
    except: 
        errorMsg()
        aShockwaveCount = "0"
        pass

    #Shocwave Vulnerability Count from CVEDetails.com 
    try:
        aShockwaveTotalVulCount = getAdobeShockwaveTotalVulCount()
    except:
        errorMsg()
        aShockwaveTotalVulCount = "0"
        pass

    #Latest known Shockwave Vulnerable Version from CVEDetails.com
    try:
        latestAdobeShockwaveVulVersion = getLatestAdobeShockwaveVulVersion()
    except:
        errorMsg()
        latestAdobeShockwaveVulVersion = "0"
        pass

    #Approximate Total Number of Vulnerable Endpoints (Compare latest version Across Endpoints to CVE Data)
    try:
        aShockwaveVulEndpoints = aDFShockwave.loc[aDFShockwave['Version'] <= latestAdobeShockwaveVulVersion, 'Count'].sum()
    except:
        errorMsg()
        aShockwaveVulEndpoints = "0"
        pass

    #####################
    #Adobe Flash Specific
    #####################

    #Number of Flash Products Installed
    try:
        aDFFlash = aDF[aDF['Name'].str.contains("Flash Player")]
        aFlashCount = len(aDFFlash['Version'].unique())
    except:
        errorMsg()
        aFlashCount = "0"
        pass

    #Flash Vulnerability Count from CVEDetails.com 
    try:
        aFlashTotalVulCount = getAdobeFlashTotalVulCount()
    except:
        errorMsg()
        aFlashTotalVulCount = "0"
        pass

    #Latest known Flash Vulnerable Version from CVEDetails.com
    try:
        latestAdobeFlashVulVersion = getLatestAdobeFlashVulVersion()
    except:
        errorMsg()
        latestAdobeFlashVulVersion = "0"
        pass

    #Approximate Total Number of Vulnerable Installations (Compare latest version Across Endpoints to CVE Data)
    try:
        aFlashVulInstalls = aDFFlash.loc[aDFFlash['Version'] <= latestAdobeFlashVulVersion, 'Count'].sum()
    except:
        errorMsg()
        aFlashVulInstalls = "0"
        pass


    #######################
    #Adobe Statistics Slide

    adobeArray = [
        "Total Number of Distinct Adobe Products/Versions Found", str(aProductCount), 
        "Total Install Count of Adobe Products Across All Endpoints", str(aInstallCount), 
        "Average Number of Adobe Products Installed Per Endpoint", str(aInstallAvg), 
        "Number of Distinct Adobe Shockwave Versions Installed", str(aShockwaveCount), 
        "Number of Known Adobe Shockwave Vulnerabilities (source: cvedetails.com)", str(aShockwaveTotalVulCount), 
        "Approximate Number of Vulnerable Installations of Adobe Shockwave", str(aShockwaveVulEndpoints), 
        "Number of Distinct Adobe Flash Versions Installed", str(aFlashCount), 
        "Number of Known Adobe Flash Vulnerabilities (source: cvedetails.com)", str(aFlashTotalVulCount), 
        "Approximate Number of Vulnerable Installations of Adobe Flash", str(aFlashVulInstalls)
    ]

    title_slide_layout = prs.slide_layouts[8]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, adobeArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)