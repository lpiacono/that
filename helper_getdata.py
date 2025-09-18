def getData(user, pw, host, port, filter, sensor, FName, cPCT):

    #import pytan
    from lib import *
    from lib.pytan import *
    from lib.requests import *
    from lib.taniumpy import *

    # create a dictionary of arguments for the pytan handler
    handler_args = {}

    # establish our connection info for the Tanium Server
    handler_args['username'] = user
    handler_args['password'] = pw
    handler_args['host'] = host
    handler_args['port'] = port

    # optional, level 0 is no output except warnings/errors
    # level 1 through 12 are more and more verbose
    handler_args['loglevel'] = 1

    # optional, use a debug format for the logging output (uses two lines per log entry)
    handler_args['debugformat'] = False

    # optional, this saves all response objects to handler.session.ALL_REQUESTS_RESPONSES
    # very useful for capturing the full exchange of XML requests and responses
    handler_args['record_all_requests'] = True

    # instantiate a handler using all of the arguments in the handler_args dictionary
    #print "...CALLING: pytan.handler() with args: {}".format(handler_args)
    handler = pytan.Handler(**handler_args)

    # print out the handler string
    #print "...OUTPUT: handler string: {}".format(handler)

    # setup the arguments for the handler() class
    kwargs = {}
    kwargs["complete_pct"] = cPCT
    kwargs["question_filters"] = filter
    kwargs["sensors"] = sensor
    kwargs["qtype"] = u'manual'

    #print "...CALLING: handler.ask with args: {}".format(kwargs)
    response = handler.ask(**kwargs)

    #print "...OUTPUT: Type of response: ", type(response)

    #print "...OUTPUT: Pretty print of response:"
    #print pprint.pformat(response)

    #print "...OUTPUT: Equivalent Question if it were to be asked in the Tanium Console: "
    print response['question_object'].query_text

    if response['question_results']:
        # call the export_obj() method to convert response to CSV and store it in out
        export_kwargs = {}
        export_kwargs['obj'] = response['question_results']
        export_kwargs['export_format'] = 'csv'

        #print "...CALLING: handler.export_obj() with args {}".format(export_kwargs)
        #out = handler.export_obj(**export_kwargs)

        # trim the output if it is more than 15 lines long
        #if len(out.splitlines()) > 15:
        #    out = out.splitlines()[0:15]
        #    out.append('..trimmed for brevity..')
        #    out = '\n'.join(out)

        #print "...OUTPUT: CSV Results of response: "
        #print out
        csvpath = os.path.join('DATA', FName)
        handler.export_to_report_file(report_file = csvpath, **export_kwargs)