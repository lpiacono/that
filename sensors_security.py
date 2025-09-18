from imports import *

def createObj():
    secObj = helper_hygieneclasses.hygieneCategory
    secObj.name = "security"
    secObj.sensors = [
                            {"Filter": "", "Sensor" : "Online", "FileName" : "isonline.csv"},
                            {"Filter": "", "Sensor" : "UAC Status", "FileName" : "uacstatus.csv"},
                            {"Filter": "", "Sensor" : "Windows Credential Security Settings", "FileName" : "wincredssettings.csv"},
                            {"Filter": "", "Sensor" : "Local Account Last Password Change Days Ago ", "FileName" : "lapwchange.csv"}

    ]
    return secObj

def processData(obj, prs, PPTXFileName):

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [Security] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."

    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    ##############################
    #Load Files into Panda Objects

    #get online Data
    try:
        oDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', 'N/A']
        for nValue in noiseArr:
            oDF = cleanNoise(oDF,'Online',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']
        pass

    #get UAC Stats
    try:
        sUACStatusDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']
        pass

    #get Windows Cred Settings
    try:
        sWinCredsDF = pd.read_csv(os.path.join("DATA", obj.sensors[2]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[2]['FileName']
        pass

    #get Local Account Last Password Change Days Ago
    #sLAPWChangeDF = pd.read_csv(os.path.join("DATA", obj.sensors[3]['FileName']))

    ##############
    #General Stats

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

    ##############################
    #Security Stats

    #UAC Stats
    #Do we even care that UAC is disabled anymore?
    try:
        sUACDisabled = sUACStatusDF.loc[sUACStatusDF['UAC Status'] == 'Disabled', 'Count'].sum()
    except: 
        errorMsg()
        sUACDisabled = "0"
        pass

    #WinCreds- LM Hash Disabled
    try:
        sLMHashDF = sWinCredsDF.loc[sWinCredsDF['Setting Name'] == 'LM Hash is prevented from being stored']
        sLMHash = sLMHashDF.loc[sLMHashDF['Setting Value'] == 'Disabled', 'Count'].sum()
    except: 
        errorMsg()
        sLMHash = "0"
        pass

    #WinCreds- LSA Auditing
    #What is auditing vs Enabled?
    #should we be doing 'Run LSASS as protected process light (PPL)' instead?
    #if so, what is PPL 'light' anyways?
    try:
        sLSAAuditDF = sWinCredsDF.loc[sWinCredsDF['Setting Name'] == 'Protected LSA Auditing']
        sLSAAudit = sLSAAuditDF.loc[sLSAAuditDF['Setting Value'] == 'Disabled', 'Count'].sum()
    except: 
        errorMsg()
        sLSAAudit = "0"
        pass

    #WinCreds- Cached Logons Count
    #were these actual cached logons? Is this accurate or aproximate data?
    try:
        sCachedLogonsDF = sWinCredsDF.loc[sWinCredsDF['Setting Name'] == 'Cached logons count']
        sCachedLogons = sCachedLogonsDF['Count'].sum()
    except: 
        errorMsg()
        sCachedLogons = "0"
        pass  
    
    #WinCreds- KB2871997 Enhanced Credential Security update
    try:
        sKB2871997DF = sWinCredsDF.loc[sWinCredsDF['Setting Name'] == 'KB2871997 Enhanced Credential Security update']
        sKB2871997 = sKB2871997DF.loc[sKB2871997DF['Setting Value'] == 'Missing', 'Count'].sum()
    except: 
        errorMsg()
        sKB2871997 = "0"
        pass
    
    ######################
    #Java Statistics Slide

    secArray = [
        "Total Number of Machines Scanned for Security Statistics", str(isOnlineCount),
        "Total Number of Endpoints with UAC Disabled", str(sUACDisabled),
        "Number of Endpoints where Hashed LAN Manager Credentials can be Stored", str(sLMHash),
        "Number of Endpoints with Protected LSA Auditing Disabled", str(sLSAAudit),
        "Number of Logons with Cached Credentials Across Endpoints", str(sCachedLogons), 
        "Number of Endpoints Missing KB2871997 - Enhanced Credential Security Update", str(sKB2871997)
    ] 

    title_slide_layout = prs.slide_layouts[11]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, secArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)