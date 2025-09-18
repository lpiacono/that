from imports import *

def createObj():
    patchObj = helper_hygieneclasses.hygieneCategory
    patchObj.name = "patch"
    patchObj.sensors = [
                            {"Filter": "", "Sensor" : "Has Patch Tools", "FileName" : "haspatchtools.csv"},
                            {"Filter": "", "Sensor" : "Available Patches", "FileName" : "patches.csv"},
                            {"Filter": "", "Sensor" : "Available Patch Status", "FileName" : "patchstatus.csv"},
                            {"Filter": "", "Sensor" : "Reboot Required", "FileName" : "patchreboot.csv"}
    ]
    return patchObj

def processData(obj, prs, PPTXFileName):

    ##############################
    #Load Files into Panda Objects

    def errorMsg():
        print ""
        print "[ERROR] Encountered Unexpected Data in [Patch] CSV."
        print "[ERROR] Review value/s 0 in PPTX output for more information on falied datapoint."
        print "[ERROR] Provide Tanium a copy of the ZIP CSV DATA Folder for further Triage."

    def cleanNoise(DFName,Column,nValue):
        DFName = DFName[~DFName[Column].astype(str).str.startswith(nValue)]
        return DFName

    #has patch tools data
    try:
        ptDF = pd.read_csv(os.path.join("DATA", obj.sensors[0]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]']
        for nValue in noiseArr:
            ptDF = cleanNoise(ptDF,'Has Patch Tools',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[0]['FileName']

    #get all patch data
    try:
        wpDF = pd.read_csv(os.path.join("DATA", obj.sensors[1]['FileName']))

        #clean
        noiseArr = ['TSE', 'Error', '[no results]', '[current result unavailable]', 'N/A on Mac', 'N/A on Solaris', 'N/A on Linux', 'N/A on AIX']
        for nValue in noiseArr:
            wpDF = cleanNoise(wpDF,'Title',nValue)

    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[1]['FileName']

    #More than 5 Critical Patches data
    try:
        pStatusDF = pd.read_csv(os.path.join("DATA", obj.sensors[2]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[2]['FileName']

    #Reboot Required data
    try:
        pRebootDF = pd.read_csv(os.path.join("DATA", obj.sensors[3]['FileName']))
    except:
        print ""
        print "[ERROR] Could Not Load or Find File: " + obj.sensors[3]['FileName']

    ###############################
    #Windows Patch CSV Calculations

    #has patch tools DF
    try:
        hasPatchToolsCount = ptDF.loc[ptDF['Has Patch Tools'] == 'Yes', 'Count'].values[0]
    except: 
        errorMsg()
        hasPatchToolsCount = "0"
        pass

    #Removing as not relevant
    #Reparse Date Column correctly (remove time from Date field)
    #wpDF['Available Patches:Date'] = wpDF['Available Patches:Date'].apply(lambda x: x.strftime('%Y-%m'))

    #Any Severity Patch Total Count
    try:
        wpDFPatchTotalCount = wpDF.loc[:,'Title'].count()
    except: 
        errorMsg()
        wpDFPatchTotalCount = "0"
        pass

    #Critical Patch Total Count
    try:
        wpDFPatchCriticalCount = wpDF.loc[wpDF['Severity'] == 'Critical', 'Title'].count()
    except: 
        errorMsg()
        wpDFPatchCriticalCount = "0"
        pass

    #Total Required Across Endpoints
    try:
        wpDFRequiredTotalCount = wpDF.loc[:,'Count'].sum()
    except: 
        errorMsg()
        wpDFRequiredTotalCount = "0"
        pass

    #Total Critical Required Across Endpoints
    try:
        wpDFRequiredCriticalCount = wpDF.loc[wpDF['Severity'] == 'Critical', 'Count'].sum()
    except: 
        errorMsg()
        wpDFRequiredCriticalCount = "0"
        pass

    #Required Patch Count AVG Across all Endpoints
    try:
        wpDFRequiredAVGCount = wpDF.loc[:,'Count'].mean()
    except: 
        errorMsg()
        wpDFRequiredAVGCount = "0"
        pass

    #Required Patch Count AVG per Endpoint
    try:
        wpAvgPatchCountEP = (wpDFRequiredTotalCount * wpDFPatchTotalCount) / (wpDFPatchTotalCount * hasPatchToolsCount)
    except: 
        errorMsg()
        wpAvgPatchCountEP = "0"
        pass

    #Required Critical Patch Count AVG per Endpoint
    try:
        wpAvgCriticalPatchCountEP = (wpDFRequiredCriticalCount * wpDFPatchTotalCount) / (wpDFPatchTotalCount * hasPatchToolsCount)
    except: 
        errorMsg()
        wpAvgCriticalPatchCountEP = "0"
        pass

    #Oldest Date Any Severity Patch
    try:
        wpDFPatchDateMin = wpDF.loc[:,'Date'].min()
    except: 
        errorMsg()
        wpDFPatchDateMin = "0"
        pass

    #Number of Products Affected (Unique Product Count)
    try:
        wpDFProds = wpDF['Filename'].str.replace(r'\-kb.*', '').unique()
    except: 
        errorMsg()
        wpDFProds = "0"
        pass

    #More than 5 Critical Patches
    try:
        pStatusDF = pStatusDF[pStatusDF['Available Patch Status'] == 'More than 5 Critical Patches Required']
        pStatus5Critical = pStatusDF['Count'].sum()
    except: 
        errorMsg()
        pStatus5Critical = "0"
        pass

    #Reboot Required
    try:
        pRebootDF = pRebootDF[pRebootDF['Reboot Required'] == 'Yes']
        pReboot = pRebootDF['Count'].sum()
    except: 
        errorMsg()
        pReboot = "0"
        pass

    ###############################
    #Windows Patch Statistics Slide
    ###############################

    wpArray = [
        "Total Number of Machines Scanned for Patches", "~" + str(hasPatchToolsCount), 
        "Total Unique Missing Patches (Any Severity)", str(wpDFPatchTotalCount), 
        "Total Unique Missing Critical Patches", str(wpDFPatchCriticalCount), 
        "Approximate Number of Microsoft Products Affected", str("~" + str(len(wpDFProds))), 
        "Total Count of Missing Patches Across All Endpoints (Any Severity)", str(wpDFRequiredTotalCount), 
        "Total Count of Missing Critical Patches Across All Endpoints", str(wpDFRequiredCriticalCount), 
        "Number of Endpoints Requiring 5 or More Critical Patches", str(pStatus5Critical), 
        "Oldest Missing Patch Date Detected Across Endpoints", str(wpDFPatchDateMin), 
        "Number of Endpoints Requiring Reboot", str(pReboot)
    ]

    title_slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, wpArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)