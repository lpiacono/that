from imports import *

def processData(obj, prs, PPTXFileName, configfile):

    ########################
    #Tanium Statistics Slide
    ########################

    try: 
        qStatDF = pd.read_csv(os.path.join("DATA", "qstats.csv"))
        qStat = True
        qTotal = qStatDF['numq'].sum()
        qAverage = qStatDF['avgq'].sum()
    except:
        qStat = False

    #check if Tanium Stats are in Config File
    if (len(configfile) > 0):
        #if they are load them in Array
        taniumstatsArray = [
            "Total Number Endpoints Registering into Tanium", configfile['NumEndpointsSystemStatusPage'], 
            "Total Number of Unmanaged Assets Discovered", configfile['NumUnmanagedAssets'], 
            "Total Number of Questions Asked to Date", configfile['NumQuestionHistory'], 
            "Total Number of Actions Deployed to Endpoints to Date", configfile['NumActionHistory'] 
        ]

        print "Using Total Number Endpoints Registering into Tanium: " + configfile['NumEndpointsSystemStatusPage']
        print "Using Total Number of Unmanaged Assets Discovered: " + configfile['NumUnmanagedAssets']
        print "Using Total Number of Questions Asked to Date: " + configfile['NumQuestionHistory']
        print "Using Total Number of Actions Deployed to Endpoints to Date: " + configfile['NumActionHistory'] 
        
        #check if we are analyzing question performance. If so, add to array
        if (qStat):
            taniumstatsArray.append("Number of Questions Extracted Programmatically for this Report")
            taniumstatsArray.append(str(qTotal))
            taniumstatsArray.append("Average Number of Seconds To Process Each Question for this Report")
            taniumstatsArray.append(str(qAverage))
    
    #else, just ask user for numbers
    else:
        print ""
        print "------ Following Data Must be Entered Manually -------"
        print ""

        taniumstatsArray = [
            "Total Number Endpoints Registering into Tanium", raw_input('Number of Endpoints on System Page: '), 
            "Total Number of Unmanaged Assets Discovered", raw_input('Number of Unmanaged Assets in Discover: '), 
            "Total Number of Questions Asked to Date", raw_input('Number of Questions in Question History: '), 
            "Total Number of Actions Deployed to Endpoints to Date", raw_input('Number of Actions in Action History: ')
        ]

    title_slide_layout = prs.slide_layouts[9]
    slide = prs.slides.add_slide(title_slide_layout)

    for placeholder, aItem in zip(slide.placeholders, taniumstatsArray):
        placeholder.text = aItem

    prs.save(PPTXFileName)