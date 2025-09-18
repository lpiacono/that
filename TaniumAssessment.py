#############################################
#         Tanium Hygiene Assessment         #
#   Written by: leandro.iacono@tanium.com   #
#############################################

#imports
from imports import *

#Hygiene Assessment Step Web Service
def haWS(cX, tAM, eSTEP):
    requests.get('http://hygieneassessment.azurewebsites.net/hastats.php?exec=' + eSTEP + ' &cx=' + cX + '&t=' + tAM +'')
    return 0

#current version of this script
version = 816

#space between initial execution line and Application
print ""
print "*********************************************************"
print ""
print "                TANIUM HYGIENE ASSESSMENT"
print "                  HTTP://WWW.TANIUM.COM"
print "                      VERSION: " + str(version) + ""
print ""
print "*********************************************************"
print ""

#check for internet connection
internet = False
try:
    requests.get('https://www.google.com')
    internet = True
except:
    print "//////////////////////////////////////////////////////////////////////////"
    print "/ WARNING: INTERNET CONNECTIVITY CHECK FAILED!                           /"
    print "/ Internet Connectivity is NOT Required for Tanium Data Download (CSVs); /"
    print "/ However it is required for Complete Data Analysis (PPTX Report).       /"
    print "/ For Assistance with this Warning, contact your TAM.                    /"
    print "//////////////////////////////////////////////////////////////////////////"
    cinternet = helper_prompt.ask("(Y/N) - Continue without an Internet Connection? ")
    if (cinternet != True):
        print ""
        print "Exiting... "
        print ""
        sys.exit()

# Following code intended to notify TAM of new version of Framework exists/published.

if (internet == True):
    #check version published online
    try:
        cversion = requests.get('http://hygieneassessment.azurewebsites.net/v.php')

        #log START - HA WS
        haWS('', '', 'prestart')

    except:
        cversion = False
        print ""
        print "////////////////////////////////////////////////////////////"
        print "/ WARNING: Unable to check for new version of the Toolset. /"
        print "/ Script Execution will Proceed ...                        /"
        print "////////////////////////////////////////////////////////////"
        print ""
        pass

    #compare published version with current script version
    if (cversion != False):
        if (int(version) < int(cversion.text)):
            print ""
            print "///////////////////////////////////////////////////////////"
            print "/ WARNING: A Newer Hygiene Assessment Version Exists: " + str(cversion.text) + " /"
            print "/ Current Hygiene Assessment Version: " + str(version) + "                 /"
            print "/ For Assistance with this Warning, contact your TAM.     /"
            print "///////////////////////////////////////////////////////////"
            print ""
            newversion = helper_prompt.ask('(Y/N) - CONTINUE HYGIENE ASSESSMENT EXECUTION? ')
            if (newversion == True):
                print ""
                pass
            else:
                print "Exiting..."
                sys.exit()

#try to load config json file
try:
    configfile = json.load(open("config.json"))
except:
    configfile = False
    print ""
    print "///////////////////////////////////////////////////////"
    print "/ WARNING: Couldn't find/load config.json             /"
    print "/ Script Execution Will Ask User for Required Values. /"
    print "///////////////////////////////////////////////////////"
    print ""

#Get Assessment Information
print ""
print "************************"
print " ASSESSMENT INFORMATION "
print "************************"
print "" 

#Customer Name
if (configfile and len(configfile['customername']) > 0):
    cX = configfile['customername']
    print "[SUCCESS][JSON] Using Customer Name: " + cX
else:
    cX = raw_input('Customer Name: ')

#TAM Name 
if (configfile and len(configfile['tam']) > 0):
    tAM = configfile['tam']
    print "[SUCCESS][JSON] Using TAM Name: " + tAM
else:
    tAM = raw_input('TAM Name: ')

#check if we should extract data from tanium
if (configfile and len(configfile['extractdatafromtanium']) > 0):
    if (configfile['extractdatafromtanium'] == "1"):
        print "[SUCCESS][JSON] Extract Tanium Data: 1 - Executing Tanium Data Extraction."
        tExtract = True
    else:
        print "[ERROR][JSON] Extract Tanium Data: <Unexpected Value> - Skipping Tanium Data Extraction."
        tExtract = False
else:
    tExtract = helper_prompt.ask("(Y/N) - EXTRACT DATA FROM TANIUM SERVER? ")

#check if we should analyze data from tanium
if (configfile and len(configfile['analyzedata']) > 0):
    if (configfile['analyzedata'] == "1"):
        print "[SUCCESS][JSON] Analyze Tanium Data: 1 - Executing Tanium Data Analysis."
        tAnalyze = True
    else:
        print "[ERROR][JSON] Analyze Tanium Data: <Unexpected Value> - Skipping Tanium Data Analysis." 
        tAnalyze = False
else:
    tAnalyze = helper_prompt.ask("(Y/N) - ANALYZE CSV DATA (GENERATE PPTX)? ")

#log start, CX and TAM info - HA WS
try:
    haWS(cX, tAM, 'start')
except:
    pass

if (tAnalyze == True or tExtract == True):

    #Get list of sensor files to process
    catInDir = [os.path.basename(x) for x in glob.glob(bundle_dir + '/sensors_*')]
    #remove taniumstats as its manually processed at the end
    catInDir.remove('sensors_taniumstats.py')
    #remove file name extensions
    catInDir = [element[:-3] for element in catInDir]
    #get categories to download/Process data for
    answerGrid = []
    for cat in catInDir:
        if helper_prompt.ask("(Y/N) - [EXTRACT/ANALYZE] " + cat.upper() + " DATA? ") == True:
            answerGrid.append(cat)
            

#if extraction and analysis were not selected, exiting script.
elif (tAnalyze == False and tExtract == False):
    print ""
    print "**************************************************"
    print "*                    [ERROR]                     *"
    print "* [TANIUM DATA EXTRACTION AND ANALYSIS DISABLED] *"
    print "*    [NOTHING MORE TO DO - EXITING SCRIPT...]    *"
    print "**************************************************"
    sys.exit()

#if no sensors selected for processing, exiting script
elif (len(answerGrid) == 0):
    print ""
    print "***********************************************"
    print "*                  [ERROR]                    *"
    print "* [NO TANIUM SENSORS SELECTED FOR PROCESSING] *"
    print "*   [NOTHING MORE TO DO - EXITING SCRIPT...]  *"
    print "***********************************************"
    sys.exit()

#Dictonary to store Login Data to Tanium Console for Pytan Export
tConsoleLogin = {}

#Check if we want to Export Data from Tanium Console
if (tExtract == True):
    print ""
    print "**********************************"
    print " TANIUM CONSOLE LOGIN INFORMATION "
    print "**********************************"
    print ""

    #user + domain
    if (configfile and len(configfile['consoleusername']) > 0 and len(configfile['consoledomain']) > 0):
        domuser = str(configfile['consoledomain']) + "\\" + str(configfile['consoleusername'])
        print "[SUCCESS][JSON] Using Console Username: " + domuser
        tConsoleLogin['user'] = domuser
    else:
        tConsoleLogin['user'] = raw_input('Tanium Console Username (Domain\User): ')
        
    #password    
    if (configfile and len(configfile['consolepassword']) > 0):
        tConsoleLogin['pw'] = configfile['consolepassword']
        print "[SUCCESS][JSON] Using Console Password: *****"
    else:
        tConsoleLogin['pw'] = getpass.getpass(prompt='Tanium Console User Password: ')
    
    #host
    if (configfile and len(configfile['consolehost']) > 0):
        print "[SUCCESS][JSON] Using Console Host: " + configfile['consolehost']
        tConsoleLogin['host'] = configfile['consolehost']
    else:
        tConsoleLogin['host'] = raw_input('Tanium Server Address/IP: ')

    #port
    if (configfile and len(configfile['consoleport']) > 0):
        print "[SUCCESS][JSON] Using Console Port: " + configfile['consoleport']
        tConsoleLogin['port'] = configfile['consoleport']
    else:
        tConsoleLogin['port'] = raw_input('Tanium Server Console Port Number (<ENTER> for 443): ')
        if (len(tConsoleLogin['port']) == 0):
            tConsoleLogin['port'] = 443

    #Question Completion Percentage (JSON)
    if (configfile and len(configfile['questionpercent']) > 0):
        try:
            cPCT = int(configfile['questionpercent'])
            if (cPCT > 0 and cPCT < 101):
                print "[SUCCESS][JSON] Using Question Completion Percentage: " + str(cPCT)
            else:
                print "[ERROR][JSON] Question Completion Percentage: <Unexpected Value>."
                cPCT = raw_input('Tanium Question Completion Percentage (<Enter> for Default 90%): ')
                if (len(cPCT) == 0):
                    cPCT = 90
                else:
                    cPCT = int(cPCT)
        except:
            print "[ERROR][JSON] Question Completion Percentage: <Unexpected Value>."
            cPCT = int(raw_input('Tanium Question Completion Percentage (<Enter> for Default 90%): '))
            if (len(cPCT) == 0):
                cPCT = 90   
    else:
        cPCT = raw_input('Tanium Question Completion Percentage (<Enter> for Default 90%): ')
        if (len(cPCT) == 0):
            cPCT = 90
        else:
            cPCT = int(cPCT)

#Declaring Question Statistics Array in case its needed
qTimeArr = []

#If we want to extract data and the credentials were supplied, go get the data
if (len(tConsoleLogin) == 4 and tExtract == True):
    print ""  
    print "*****************************"
    print " REQUESTING DATA FROM TANIUM "
    print "*****************************"
    print "" 

    #if we specified to gather question stats
    if (configfile and configfile['questionstats'] == "1"):
        for cat in answerGrid:        
            obj = eval(cat).createObj()
            for query in obj.sensors:
                start = time.time()
                try:
                    helper_getdata.getData(tConsoleLogin['user'], tConsoleLogin['pw'], tConsoleLogin['host'], tConsoleLogin['port'], query['Filter'] , query['Sensor'], query['FileName'], int(cPCT))
                except:
                    print "[ERROR] Failed to Process Sensor: " + query['Sensor'] + " - " + query['Filter']
                    print "[ERROR] Check connectivity to Tanium Server and Username/Password."
                    print "[ERROR] Sensor content must exists in Tanium for Query to Complete."
                    print "[ERROR] Attempting to capture remaining sensor data..."
                    print "--------------------------------------------------------------------------"
                    pass
                end = time.time()
                qSecs = int(end - start)
                print "Number of Seconds to Complete Question Execution: " + str(qSecs) 
                qTimeArr.append(qSecs)
    
        #write question stats to csv file
        qcsv = os.path.join("DATA", "qstats.csv")
        file = open(qcsv, "w")
        numq = len(qTimeArr)
        avgq = sum(qTimeArr)/len(qTimeArr)
        qstats = str(numq) + "," + str(avgq)
        lines_of_text = ["numq,avgq\n", qstats]
        file.writelines(lines_of_text)
        file.close()

    #else no question stats in json, just get the data
    else:
        for cat in answerGrid:        
            obj = eval(cat).createObj()
            for query in obj.sensors:
               try:
                    helper_getdata.getData(tConsoleLogin['user'], tConsoleLogin['pw'], tConsoleLogin['host'], tConsoleLogin['port'], query['Filter'] , query['Sensor'], query['FileName'], int(cPCT))
               except:
                    print "[ERROR] Failed to Process Sensor: " + query['Sensor'] + " - " + query['Filter']
                    print "[ERROR] Check connectivity to Tanium Server and Username/Password."
                    print "[ERROR] Sensor content must exists in Tanium for Query to Complete."
                    print "[ERROR] Attempting to capture remaining sensor data..."
                    print "--------------------------------------------------------------------------"
                    pass

    #CSV DATA ZIP FILENAME
    zipTS = (time.strftime("%H%M%S-%m%d%Y"))
    zipFN = zipTS + " - DATA - " + str(version)
    shutil.make_archive(zipFN, 'zip', 'DATA')

    #log data extracted - HA WS
    try:
        haWS(cX, tAM, 'dataEX')
    except:
        pass

    print ""
    print "========================================================================="
    print "  Question DATA Download to CSV Completed (/DATA)                        "
    print "  Ensure any changes to CSV DATA are made now before proceeding.         "
    print "  CSV ZIP Created: " + zipFN + ".zip                                     "
    print "========================================================================="
    print "-=                     Press <ENTER> to continue.                      =-"
    print "========================================================================="
    raw_input('')


#if analyze data, process CSV Data in /DATA Folder'
if (tAnalyze == True):

    #PPTX Template to be used 
    templatePPTXDir = 'PPTXTEMPLATES'
    templatePPTXFileName ='PPTX-18FontEmbedded.pptx'

    #File Name of Completed Presentation
    PPTXFileNameDateTime = (time.strftime("%H%M%S-%m%d%Y"))
    PPTXFileName = PPTXFileNameDateTime + " - " + cX + " Hygiene Assessment.pptx"

    #################
    #PPTX BUILD LOGIC

    #build path to PPTX Template
    templateFilePath = os.path.join(bundle_dir, os.path.join(templatePPTXDir, templatePPTXFileName))

    #load PPTX Template into new Flat PPTX where data will be placed.
    prs = Presentation(templateFilePath)
    prs.save(PPTXFileName)

    #################
    #PPTX Build Logic
    #################

    #Template Master Slide List
    # [0] - Tanium Face/Main Logo
    # [1] - Presentation Title
    # [2] - Hygiene Assessment Overview
    # [3] - Custom / Blank Slide if Additional Information want to be added manually
    # [4] - Closing Slide
    # [5] - Windows Patch Statistics
    # [6] - SCCM Statistics
    # [7] - Java Statistics
    # [8] - Adobe Statistics
    # [9] - Tanium Statistics
    # [10] - McAfee Statistics

    #Adding Tanium Face Slide, Presentation Title, Hygiene Assessment Overview and Custom Slide (in case additional information is wanted/needeD)
    prs.slides.add_slide(prs.slide_layouts[0])
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    #Adding Presentation Slide Title
    slide.placeholders[0].text = cX + " Hygiene Assessment"

    #Tanium TAM Name
    slide.placeholders[1].text = tAM

    #Adding Date to Slide Title
    slide.placeholders[10].text = str("Prepared on " + time.strftime("%d/%m/%Y"))

    #Adding Hygiene Assessment Overview Slide
    slide = prs.slides.add_slide(prs.slide_layouts[2])

    #Empty Slide for Additional Content
    slide = prs.slides.add_slide(prs.slide_layouts[3])
    prs.save(PPTXFileName)

    print ""  
    print "**********************"
    print " PROCESSING CSV DATA"
    print "**********************"
    print "" 

    for cat in answerGrid:
        obj = eval(cat).createObj()
        eval(cat).processData(obj, prs, PPTXFileName)

    #process last Tanium Stats slide
    if (configfile):
        if (len(configfile['NumEndpointsSystemStatusPage']) > 0 or len(configfile['NumUnmanagedAssets']) > 0 or len(configfile['NumQuestionHistory']) > 0 or len(configfile['NumActionHistory']) > 0):
            sensors_taniumstats.processData('', prs, PPTXFileName, configfile)
        else:
            sensors_taniumstats.processData('', prs, PPTXFileName, '')
    else:
        sensors_taniumstats.processData('', prs, PPTXFileName, '')

#Adding Closing Slide 
prs.slides.add_slide(prs.slide_layouts[4])
#final slide save
prs.save(PPTXFileName)

#log pptx created - HA WS
try:
    haWS(cX, tAM, 'pptx')
except:
    pass


print ""
print "********************************************** "
print "************ [EXECUTION COMPLETE] ************ "
print "********************************************** "