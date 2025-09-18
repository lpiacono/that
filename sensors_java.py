from imports import *

def createObj():
    javaObj = helper_hygieneclasses.hygieneCategory
    javaObj.name = "java"
    javaObj.sensors = [
                            {"Filter": "", "Sensor" : "Installed Applications, that contains:java", "FileName" : "java.csv"},
                            {"Filter": "", "Sensor" : "Installed Java Runtimes", "FileName" : "jre.csv"},
                            {"Filter": "Installed Applications, that contains:java", "Sensor" : "Target", "FileName" : "javatargets.csv"}
    ]
    return javaObj

def processData(obj, prs, PPTXFileName):

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [Java] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."
    
    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    #Vulnerabilities Count of CVEDetails.com
    from helper_getLatestJavaJREVulVersion import getLatestJavaJREVulVersion
    from helper_getJavaJRETotalVulCount import getJavaJRETotalVulCount

    ##############################
    #Load Files into Panda Objects

    #get all Java Installed data
    try:
        jDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', 'Java not installed']
        for nValue in noiseArr:
            jDF = cleanNoise(jDF,'Name',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']

    #get all JRE data
    try:
        jREDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', 'Java not installed']
        for nValue in noiseArr:
            jREDF = cleanNoise(jREDF,'JRE',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']

    #Adobe Targets
    try:
        jTargetsDF = pd.read_csv(os.path.join("DATA", obj.sensors[2]['FileName']))
    except:
        print""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[2]['FileName']

    
    ######################
    #Java CSV Calculations
    
    #total number endpoints reporting any Java product installed
    try:
        jTotalTargets = jTargetsDF.loc[jTargetsDF['Target'] == 'Target', 'Count'].sum()
    except: 
        errorMsg()
        jTotalTargets = 0
        pass

    #get total count of java products installed across endpoints
    try:
        jProductCount = len(jDF['Name'].unique())
    except: 
        errorMsg()
        jProductCount = "0"
        pass

    #get total number of times java products installed across all endpoints
    try:
        jInstallCount = jDF['Count'].sum()
    except: 
        errorMsg()
        jInstallCount = "0"
        pass

    #average install per endpoint given number of machines reporting adobe product installed
    try:
        if (jTotalTargets > 0):
            if (float(jInstallCount) / float(jTotalTargets)) < 1:
                jInstallAvg = int(math.ceil(float(jInstallCount) / float(jTotalTargets)))
            elif (float(jInstallCount) / float(jTotalTargets)) >= 1:
                jInstallAvg = int(float(jInstallCount) / float(jTotalTargets))
        else:
            jInstallAvg = 0
    except: 
        errorMsg()
        jInstallAvg = "0"
        pass

    #############
    #JRE Specific
    #############

    #get total count of JRE versions installed across endpoints
    try:
        jREProductCount = len(jREDF['Version'].unique())
    except: 
        errorMsg()
        jREProductCount = "0"
        pass

    #get total count of JRE installs across endpoints
    try:
        jREInstallCount = jREDF['Count'].sum()
    except: 
        errorMsg()
        jREInstallCount = "0"
        pass

    #Total Known JRE Vulnerabilities from CVEDetails.com
    try:
        jRETotalVulCount = getJavaJRETotalVulCount()
    except: 
        errorMsg()
        jRETotalVulCount = "0"
        pass

    #Latest known JRE Vulnerable Version from CVE Data
    try:
        latestJavaJREVulVersion = getLatestJavaJREVulVersion()
    except: 
        errorMsg()
        latestJavaJREVulVersion = "0"
        pass

    #Approximate Total Number of Vulnerable Installs on Endpoints (Compare latest version Across Endpoints to CVE Data)
    try:
        jREVulEndpoints = jREDF.loc[jREDF['Version'] <= latestJavaJREVulVersion, 'Count'].sum()
    except:
        errorMsg()
        jREVulEndpoints = "0"
        pass

    #Approximate Total Number of Vulnerable Endpoints (Compare latest version Across Endpoints to CVE Data)
    try:
        if (jInstallAvg > 0):
            jREPercentVulInstalls = int (math.ceil((int(jREVulEndpoints) * 100) / int(jREInstallCount)))
        else:
            jREPercentVulInstalls = 0
    except: 
        errorMsg()
        jREPercentVulInstalls = "0"
        pass
        
    ######################
    #Java Statistics Slide

    javaArray = [
        "Total Number of Distinct Java Products/Versions Found", str(jProductCount),
        "Total Install Count of Java Products Across All Endpoints", str(jInstallCount),
        "Average Number of Java Products Installed Per Endpoint", str(jInstallAvg),
        "Total Number of Endpoints with Java Products Installed", str(jTotalTargets),
        "Number of Distinct Java Runtime Versions Detected", str(jREProductCount), 
        "Count of Java Runtime Installs Across All Endpoints", str(jREInstallCount), 
        "Number of Known Java Runtime Vulnerabilities (source: cvedetails.com)", str(jRETotalVulCount), 
        "Approximate Percentage of Installed Java Runtime Versions Affected by Vulnerabilities", "~" + str(jREPercentVulInstalls) + "%", 
        "Approximate Number of Non-Vulnerable Installations of Java Runtime", "~" + str(int(jREInstallCount) - int(jREVulEndpoints))
    ] 

    title_slide_layout = prs.slide_layouts[7]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, javaArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)