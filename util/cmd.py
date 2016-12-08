import os
import time

import commands as cmds
import util.logWriter as lw

def run_all_check_command(command_list):
    contentList = []
    for c in command_list:
        array = cmds.getstatusoutput(c)
        contentList.append(check_status(c, array[0], array[1]))
    return contentList

def check_status(command, stat, out):
    lw.Logger().getLogger().info("COMMAND: " + command + ", STATUS: " + str(stat) + ", OUTPUT: " + out)
    list = [command, "SUCCEEDED" if stat == 0 else "FAILED"]
    return list

def createDir(dirPath):
    if os.path.exists(dirPath):
        newDirPath = "/tmp/check_hdfs_%s/" % time.strftime("%Y%m%d%H%M%s")
        createDir(newDirPath)
    else:
        os.mkdir(dirPath)
