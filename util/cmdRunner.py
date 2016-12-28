import commands as cmds
import os
import sys

import util.logWriter as lw


def run_all_check_command(command_list, logName):
    """Run commands, return command && result list."""
    contentList = []
    status = "HEALTHY"
    for c in command_list:
        array = cmds.getstatusoutput(c)
        if array[0] != 0:
            status = "SICK"
        list, logFilePath = check_status(c, array[0], array[1], logName)
        contentList.append(list)
    return contentList, status, logFilePath


def check_status(command, stat, out, logName):
    """Write into log file and return every command && result as list"""
    logFilePath = lw.Logger(logName).getLogger().handlers[0].baseFilename
    if stat == 0:
        lw.Logger(logName).getLogger().info("COMMAND: %s" % command)
        lw.Logger(logName).getLogger().info("OUTPUT : %s" % out)
    else:
        lw.Logger(logName).getLogger().error("FAILED_COMMAND: %s" % command)
        lw.Logger(logName).getLogger().error("ERROR_MESSAGE : %s" % out)
    # get cmd which runs in shell without 'echo' and '| xxx'
    # if command.__contains__("echo"):
    #     command = command.split("echo")[1].split("|")[0]
    list = [command.strip(), "SUCCEEDED" if stat == 0 else "FAILED"]
    return list, logFilePath


def createDir(dirPath):
    """Create directories for hdfs test."""
    if os.path.exists(dirPath):
        print "Local path", "'" + dirPath + "'", "already exists."
        sys.exit(3)
    else:
        os.mkdir(dirPath)


def prepareTestHdfs(path, writeWords, fileName):
    """Prepare sth for hdfs test"""
    createDir(path)
    os.system("echo %s > %s/%s" % (writeWords, path, fileName))


def compare(originFile, getFromHdfs_file):
    """Use md5sum to compare."""
    op1 = cmds.getoutput("md5sum %s" % originFile).split("  ")[0]
    op2 = cmds.getoutput("md5sum %s" % getFromHdfs_file).split("  ")[0]
    if op1 == op2:
        print "The command 'hdfs dfs -get' is ok."
    else:
        print "Something is wrong with the command 'hdfs dfs -get'."


def deleteDir(path):
    if os.path.exists(path):
        os.system("rm -r %s" % path)
