#!/usr/bin/python

import sys

import util

# BaseCommand.json
# Stage.json
# Task.json
# TransitionPo.json

rc = util.configReader.ReadConf()
jsonDir = rc.getJsonDir()
nodeJson = jsonDir + rc.getNodeJson()
serviceJson = jsonDir + rc.getServiceJson()
roleJson = jsonDir + rc.getRoleJson()

serivce_type_list = ["ZOOKEEPER", "HDFS", "YARN", "HYPERBASE", "HDFSNAMESERVICE", "INCEPTOR_SQL", "GUARDIAN", "INCEPTOR_ML"]
args = sys.argv
this = args[0]
if len(args) > 1:
    serivce_type_list = []
    for a in args:
        serivce_type_list.append(a)

# node infos
nis = util.jsonParser.getNodeInfo(nodeJson)
# Format ouput
header = ["roleType", "hostName", "status"]

# Log
logger_str = ""
myLogger = util.logWriter.Logger(logName="root").getLogger()

for sts in serivce_type_list:
    # service infos
    sis = util.jsonParser.getServiceInfo(sts, serviceJson)
    for si in sis:
        content_list = []
        titleName = si[u"sid"]
        # role infos
        ris = util.jsonParser.getRoleInfo(si[u"id"], roleJson)
        for ri in ris:
            # Add role's hostName
            for ni in nis:
                if ri[u"nodeId"] == ni[u"id"]:
                    ri[u"hostName"] = ni[u"hostName"]
                    break
            # Get content
            ri_list = []
            for t in header:
                for ri_key in ri.keys():
                    if ri_key == t:
                        ri_list.append(ri[ri_key])
            content_list.append(ri_list)

        # Log
        myLogger.info("sid: " + titleName + ", status: " + si[u"status"])
        for ri2 in ris:
            for t in header:
                logger_str += str(t) + ": " + str(ri2[t]) + ", "
            myLogger.info(logger_str[0:int(int(len(logger_str)) - 2)] if logger_str.endswith(", ") else logger_str)
            logger_str = ""

        # Format output
        fos = util.outputFormatter.Formatter().formatted_output(titleName, ["ROLE", "NODE", "STATE"], content_list)
        print "Formatted output string:\n", fos
