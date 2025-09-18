from imports import *

def createObj():
    sccmObj = helper_hygieneclasses.hygieneCategory
    sccmObj.name = "sccm"
    sccmObj.sensors = [
                            {"Filter": "", "Sensor" : "SCCM Client Communication Days Old", "FileName" : "sccmcomm.csv"},
                            {"Filter": "", "Sensor" : "SCCM Client Installed", "FileName" : "sccminstalled.csv"},
                            {"Filter": "", "Sensor" : "SCCM Client Running", "FileName" : "sccmrunning.csv"},
                            {"Filter": "", "Sensor" : "SCCM Client Version", "FileName" : "sccmversion.csv"},
                            {"Filter": "", "Sensor" : "SCCM WMI Health", "FileName" : "sccmwmi.csv"},
                            {"Filter": "", "Sensor" : "Online", "FileName" : "isonline.csv"}
    ]
    return sccmObj

def processData(obj, prs, PPTXFileName):

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [SCCM] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."

    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    ##############################
    #Load Files into Panda Objects

    #get all SCCM COMM Data
    try:
        sCOMMDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', '::SCCM Not Installed::', 'None']
        for nValue in noiseArr:
            sCOMMDF = cleanNoise(sCOMMDF,'SCCM Client Communication Days Old',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']

    #get all SCCM Install Data
    try:
        sINSTDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            sINSTDF = cleanNoise(sINSTDF,'SCCM Client Installed',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']

    #get all SCCM Running Data
    try:
        sRUNDF = pd.read_csv(os.path.join("DATA", obj.sensors[2]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            sRUNDF = cleanNoise(sRUNDF,'SCCM Client Running',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[2]['FileName']

    #get all SCCM Version Data
    try:
        sVERDF = pd.read_csv(os.path.join("DATA", obj.sensors[3]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', '::SCCM Not Installed::', 'SCCM or WMI error']
        for nValue in noiseArr:
            sVERDF = cleanNoise(sVERDF,'Version Description',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[3]['FileName']

    #get all SCCM WMI Health Data
    try:
        sWMIDF = pd.read_csv(os.path.join("DATA", obj.sensors[4]['FileName']))

        #clean
        noiseArr = ['TSE', '[no results]', '[current result unavailable]', '::SCCM Not Installed::', 'SCCM or WMI error']
        for nValue in noiseArr:
            sWMIDF = cleanNoise(sWMIDF,'SCCM WMI Health',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[4]['FileName']

    #get online Data
    try:
        oDF = pd.read_csv(os.path.join("DATA", obj.sensors[5]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', 'N/A']
        for nValue in noiseArr:
            oDF = cleanNoise(oDF,'Online',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[5]['FileName']

    ##############
    #General Stats
    ##############

    #online Count
    #multiple tests required because output from question "true" may be interprested differently by Pandas depending on output
    try:
        oDF1 = oDF.loc[oDF['Online'] == True]
        isOnlineCount1 = oDF1['Count'].sum()
        if (isOnlineCount1 == 0):
            try:
                oDF2 = oDF.loc[oDF['Online'] == 'TRUE']
                isOnlineCount2 = oDF2['Count'].sum()
                if (isOnlineCount2 == 0):
                    try:
                        oDF3 = oDF.loc[oDF['Online'] == 'True']
                        isOnlineCount3 = oDF3['Count'].sum()
                        if (isOnlineCount3 != 0):
                            isOnlineCount = isOnlineCount3
                    except:
                        errorMsg()
                        isOnlineCount = "0"
                        pass
                else:
                    isOnlineCount = isOnlineCount2
            except:
                errorMsg()
                isOnlineCount = "0"
                pass
        else:
            isOnlineCount = isOnlineCount1
    except:
        errorMsg()
        isOnlineCount = "0"
        pass

    ######################
    #SCCM CSV Calculations
    ######################

    #max days old comm
    #remove all non numeric values and get max days old
    try: 
        sCOMMMaxDF = sCOMMDF.drop('SCCM Client Communication Days Old', axis=1).\
                join(sCOMMDF['SCCM Client Communication Days Old'].apply(pd.to_numeric, errors='coerce'))

        sCOMMMaxDF = sCOMMMaxDF[~sCOMMMaxDF['SCCM Client Communication Days Old'].isnull().apply(np.any, axis=0)]
    except:
        pass

    #if there are no Comm Problems, set Comm Problems to 0
    try:
        if (len(sCOMMMaxDF) > 0):
            sCOMMMax = int(sCOMMMaxDF['SCCM Client Communication Days Old'].max())
        else:
            sCOMMMax = 0
    except:
        errorMsg()
        sCOMMMax = "0"
        pass

    #number of Endpoint with Comm Problems
    #removing endpoints with no comm problems
    try: 
        sCOMMMaxEPDF = sCOMMDF.loc[sCOMMDF['SCCM Client Communication Days Old'] != '0']
    except: 
        pass
        
    #getting all other endpoints with comm problems
    try:
        sCOMMMaxEP = sCOMMMaxEPDF['Count'].sum()
    except:
        errorMsg()
        sCOMMMaxEP = "0"
        pass

    #Number of Endpoints where SCCM Missing
    try:
        sINSTDF = sINSTDF.loc[sINSTDF['SCCM Client Installed'] != 'Yes']
    except:
        pass
    
    try:
        sMiss = sINSTDF['Count'].sum()
    except:
        errorMsg()
        sMiss = "0"
        pass

    #Number of Endpoints SCCM NotRunning
    try:
        sRUNDF = sRUNDF.loc[sRUNDF['SCCM Client Running'] != 'Yes']
    except: 
        pass
        
    try:
        sNRun = sRUNDF['Count'].sum()
    except:
        errorMsg()
        sNRun = "0"
        pass

    #SCCM Version Data

    #number of Distinct SCCM Versions
    try:
        sVERCount = len(sVERDF['Version Description'])
    except:
        errorMsg()
        sVERCount = "0"
        pass

    #latest version
    try:
        sVERMax = sVERDF['Version Description'].max()
    except:
        errorMsg()
        sVERMax = "0"
        pass

    #number of endpoints running an old version of SCCM
    try:
        sVEROldDF = sVERDF.loc[sVERDF['Version Description'] != sVERMax ]
        sVerOldCount = sVEROldDF['Count'].sum() 
    except:
        errorMsg()
        sVerOldCount = "0"
        pass

    #WMI Errors
    try:
        sWMIDF = sWMIDF.loc[sWMIDF['SCCM WMI Health'] != 'OK' ]
        sWMIErr = sWMIDF['Count'].sum()
    except:
        errorMsg()
        sWMIErr = "0"
        pass

    #Total SCCM Remediation
    try:
        sTotalRem = int(sWMIErr) + int(sVerOldCount) + int(sNRun) + int(sMiss) + int(sCOMMMaxEP)
    except:
        errorMsg()
        sTotalRem = "0"
        pass
        
    ######################
    #SCCM Statistics Slide

    sccmArray = [
        "Total Number of Machines Scanned for SCCM Statistics", str(isOnlineCount), 
        "Longest Number of Days a Client Has Not Registered into SCCM", str(sCOMMMax), 
        "Number of Endpoints Reporting Communication/Registration Issues", str(sCOMMMaxEP), 
        "Number of Endpoints with SCCM Not Installed", str(sMiss), 
        "Number of Distinct SCCM Client Versions Installed", str(sVERCount), 
        "Number of Endpoints Running Older SCCM Versions (latest: " + str(sVERMax) + ")", str(sVerOldCount), 
        "Number of Endpoints where SCCM is Not Running", str(sNRun), 
        "Number of Endpoints Reporting WMI Errors", str(sWMIErr), 
        "Total Potential Actions Required to Remediate SCCM Across Endpoints", "~" + str(sTotalRem)
    ]

    title_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, sccmArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)