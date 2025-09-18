===================================
=-  Hygiene Assessment Package  -=
===================================

************************************
Change Log:

11/30/16 (v816)
- Fixed Incorrect Symantec Vertical showing
- Fixed Date order (day/month -> month/day)

11/28/16 (v815)
- Fixed Default Value for Question Percentage Error

11/22/2016 (v814)
- Ability to specify Question Percentage Completion
- Misc Data Calculation Fixes
- Internet Check Logic Fix

11/17/2016 (v813)
- Changed Executable Name (TaniumAssessment.exe)
- Misc User Prompt Fixes
- Misc Data Calculation Fixes

11/16/16 - (v812)
- Improved Error Handling
- Misc Fixes to Data Processing

10/25/16 - (v811)
- Includes Security Vertical
- Includes Simple Error Handling
- Includes automatic ZIP CSV/DATA folder for historical data captures and easier copying/email to TAM
- Includes Misc Fixes to Data Processing

10/22/16 - (v807)
- Includes Hygiene Assessment Package Online Version Checker
- Includes config.json file to pre-configure Assessment Package
- Includes McAfee vertical
- Includes Hygiene Assessment Question Stats (hidden Option)
- Misc Bug Fixes

============
=- HOW TO -=
============

Prerequisites:
==============
- Internet connectivity is Not Required for Tanium Sensor Data Extraction (ask question and download to CSV).
-- Internet Connection is required to check for New Version of Assesment Tool
-- Internet Connection is required to download latest CVE statistics off CVEDETAILS.COM
-- It is HIGHLY recommended to run the toolset on a machine with Internet connectivity.

-No other software pre-requiste required. The toolset .EXE file self contains all needed pre-reqs for execution.
-Currently runs on Windows Only (working on MAC support!)


Execution:
==========
0) Package can be executed on Tanium Server (POC/PROD) or on a seperate Windows PC
that can reach the Tanium Console through the browser (HTTP connectivity to Tanium Console).

1) Extract ZIP file contents to same Directory on FileSystem

2) Consider editing config.json if you would like to pre-configre the Hygiene Assessment questions:
2.1 All items in config.json must be answered for proper use.
2.2 If the config.json is not properly configured, we may not use the conifg.json or prompt the user to re-input incorrect data. 
2.3 For Instructions on filling out config.json see CONFIG.JSON section below.

3) Open Command Prompt / Powershell Window as Administrator

4) Execute TaniumAssessment.exe

5) Follow instructions on screen

6) PPTX will output to same directory as TaniumAssessment.exe

7) RAW Data from Tanium (CSV) will be downloaded to "/DATA" folder in directory as TaniumAssessment.exe
7.1 You can bypass DATA Analysis and only download CSV Data from Tanium Server for later DATA Analysis offline on TAM Machine or on a different Machine by selecting YES on "Extract Data form Tanium Server?" but selectin NO on "Analyze CSV Data?"
7.2 Likewise you can bypass DATA Download from Tanium Server and only execute data analysis to PPTX if all CSV files already exist in DATA folder. CSV files must be named the same way the package names them on download.


CONFIG.JSON
===========
The config.json file allows you to preconfigure the Script exection so that you don't have to answer the same questions over and over in case you need to execute the scripts a few times before getting things right.

If a certain value does not fall within expected range, the script will tell you on execution, or revert back to asking the user to input correct information.

Configured Values must be inside quotes (including quotes).

{
"customername": "", -> Name of Customer / Expected Value: Any
"tam": "", -> Name of TAM / Expected Value: Any
"extractdatafromtanium": "", -> Do you want to Get Data from Tanium Server / "1" = Yes. Anything Else = No
"analyzedata": "", -> Enable Data Analysis (CSV Files to PPTX) / "1" = Yes. Anything Else = No
"consoledomain": "", -> Domain name (Domain\) of the user account to be used / Expected Value: Any
"consoleusername": "", -> Username to Access Console / Expected Value: Any
"consolepassword": "", -> Password to Access Console / Expected Value: Any
"consolehost": "", -> Hostname to Access Console / Expected Value: Any
"consoleport": "",-> Port to Access Console / Expected Value: Any
"NumEndpointsSystemStatusPage": "", -> Number of Endpoints in System Status Page / Expected Value: Any
"NumUnmanagedAssets": "", -> Number of Unmanaged Assets in Discover / Expected Value: Any
"NumQuestionHistory": "", -> Number of Questions in Question History Page / Expected Value: Any
"NumActionHistory": "", -> Number of Actions in Action History Page / Expected Value: Any
"questionstats": "" -> Include Hygiene Assessment Question Statistics in PPTX / Expected Value: Any
"questionpercent": "" -> Specify Sensor completion percentage. Default "90" percent.
}

Example JSON:
*************
{
"customername": "Contoso",
"tam": "Leandro Iacono",
"extractdatafromtanium": "1",
"analyzedata": "1",
"consoledomain": "ACME", 
"consoleusername": "administrator",
"consolepassword": "Tanium2016!",
"consolehost": "192.168.1.1",
"consoleport": "443",
"NumEndpointsSystemStatusPage": "9583",
"NumUnmanagedAssets": "6831",
"NumQuestionHistory": "64803",
"NumActionHistory": "34982",
"questionstats": "1",
"questionpercent": "90"
}

Known Issues:
=============
- Why doesn't this execute on MAC?! ...Coming Soon!
- Powerpoint complains about embedded font file?! This is a known "Office for MAC" issue. The Font for the PPTX is in /FONT. Install the Font on your machine for better UI experience with PPTX.

- Questions/issues? leandro.iacono@tanium.com - #hygiene-assessment slack channel

