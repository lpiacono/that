from imports import *

def createObj():
    mcafeeObj = helper_hygieneclasses.hygieneCategory
    mcafeeObj.name = "mcafee"
    mcafeeObj.sensors = [
                            {"Filter": "", "Sensor" : "VirusScan Enterprise Version, that lt:8.7", "FileName" : "mcafeeunsupported.csv"},
                            {"Filter": "VirusScan Enterprise DAT Days Old, that gt:2", "Sensor" : "VirusScan Enterprise DAT Version", "FileName" : "mcafeedat.csv"},
                            {"Filter": "", "Sensor" : "VirusScan Enterprise On-Access Scan State, that contains:Disabled", "FileName" : "mcafeeonaccessstate.csv"},
                            {"Filter": "", "Sensor" : "Installed Applications, that contains:mcafee", "FileName" : "mcafee.csv"},
    ]
    return mcafeeObj

def processData(obj, prs, PPTXFileName):

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [McAfee] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."

    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    ##############################
    #Load Files into Panda Objects

    #get all McAfee Data
    try:
        mcafeeUnSupportedDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            mcafeeUnSupportedDF = cleanNoise(mcafeeUnSupportedDF,'VirusScan Enterprise Version',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']

    #get all McAfee DAT Versions
    try:
        mcafeeDATDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))
    
        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            mcafeeDATDF = cleanNoise(mcafeeDATDF,'VirusScan Enterprise DAT Version',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']

    #get McAfee OnAccess State
    try:
        mcafeeOnAccessDF = pd.read_csv(os.path.join("DATA", obj.sensors[2]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[2]['FileName']

    #get all McAfee Data
    try:
        mcafeeInstalledDF = pd.read_csv(os.path.join("DATA", obj.sensors[3]['FileName']))

        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            mcafeeInstalledDF = cleanNoise(mcafeeInstalledDF,'Name',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[3]['FileName']

    ##############
    #McAfee Stats
    ##############

    #Total Number of Scanned Endpoints for McAfee Products
    try:
        mcafeeTotalNum = mcafeeDATDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeTotalNum = "0"
        pass

    #McAfee Not Installed
    try:
        mcafeeNotInstalledDF = mcafeeDATDF.loc[mcafeeDATDF['VirusScan Enterprise DAT Version'] == 'VirusScan Enterprise Not Installed']
        mcafeeNotInstalled = mcafeeNotInstalledDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeNotInstalled = "0"
        pass

    #Number of Unsupported Versions
    try:
        mcafeeUnSupportedDF = mcafeeUnSupportedDF.loc[mcafeeUnSupportedDF['VirusScan Enterprise Version'] != 'Not Installed']
        mcafeeNumUnSupportedVer =  len(mcafeeUnSupportedDF['VirusScan Enterprise Version'])
    except: 
        errorMsg()
        mcafeeNumUnSupportedVer = "0"
        pass

    #number of installs across endpoints with unsupported versions
    try:
        mcafeeInstallsUnsupportedVer = mcafeeUnSupportedDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeInstallsUnsupportedVer = "0"
        pass

    #Outdated mcAfee Dat Versions
    try:
        mcafeeOutdatedDats = len(mcafeeDATDF['VirusScan Enterprise DAT Version'])
    except: 
        errorMsg()
        mcafeeOutdatedDats = "0"
        pass

    #Total Endpoints Running OutDated Dat version
    try:
        mcafeeOutdatedDatEP = mcafeeDATDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeOutdatedDatEP = "0"
        pass

    #Total Number of Endpoints with OnAccess Disabled State
    try:
        mcafeeOnAccessDF = mcafeeOnAccessDF.loc[mcafeeOnAccessDF['VirusScan Enterprise On-Access Scan State'] == 'Disabled']
        mcafeeOnAccessNum = mcafeeOnAccessDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeOnAccessNum = "0"
        pass

    #Total Number of McAfee Products
    try:
        mcafeeInstalledProds = len(mcafeeInstalledDF['Name'])
    except: 
        errorMsg()
        mcafeeInstalledProds = "0"
        pass
        
    #Total McAfee Install Count
    try:
        mcafeeInstallCount = mcafeeInstalledDF['Count'].sum()
    except: 
        errorMsg()
        mcafeeInstallCount = "0"
        pass

    ######################
    #McAfee Statistics Slide

    McAfeeArray = [
        "Total Number of Endpoints Scanned", str(mcafeeTotalNum), 
        "Total Number Distinct McAfee Products/Versions Detected", str(mcafeeInstalledProds),
        "Total Number McAfee Installations Across Endpoints", str(mcafeeInstallCount),
        "Number of Unsupported McAfee VirusScan Versions (older than v8.7)", str(mcafeeNumUnSupportedVer), 
        "Number of Unsupported McAfee VirusScan Installs Across Endpoints", str(mcafeeInstallsUnsupportedVer),
        "Number of Endpoints without McAfee VirusScan Installed", str(mcafeeNotInstalled),
        "Number of Outdated McAfee VirusScan DAT Versions (Greater than 3 Days)", str(mcafeeOutdatedDats),
        "Number of Endpoints with Outdated McAfee VirusScan DAT Versions", str(mcafeeOutdatedDatEP),
        "Number of Endpoints with McAfee VirusScan On-Access Scanning Disabled", str(mcafeeOnAccessNum)
        
    ]

    title_slide_layout = prs.slide_layouts[10]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, McAfeeArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)