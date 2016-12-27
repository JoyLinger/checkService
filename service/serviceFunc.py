import os
import sys

import util.cmdRunner as runCmd
import util.configReader as cr
import util.outputFormatter as opf


def getCmdsFromFile(path):
    """Return commands as list."""
    return cr.ReadConf(path).getCmdList(key="cmd")


def testZookeeper(kinit, header, hosts, logName="zk", cmdPath="cmd/zookeeper", zkCliPath="/usr/lib/zookeeper/bin"):
    """To test ZK and print test result.
    :param kinit:
    :param header:
    :param hosts:
    :param logName: which logger in file 'conf/logger.conf'
    :param cmdPath:
    :param zkCliPath:
    """
    for fp in os.listdir(cmdPath):
        sickNum = 0
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            if sickNum > len(hosts) / 2:
                print "\033[31mZookeeper is not healthy, stop current test.\033[0m"
                sys.exit(0)
            commands = [kinit]
            zkcli = "%s/zkCli.sh -server %s:2181" % (zkCliPath, host)
            for cmd in cmdList:
                commands.append("echo %s | %s" % (cmd, zkcli))
            contents, status = runCmd.run_all_check_command(commands, logName)
            if status == "SICK":
                sickNum += 1
            for i in range(1, len(contents)):
                contents[i][0] = commands[i - 1]
            res = opf.Formatter().formatted_output("ZooKeeper on %s: %s" % (host, status), header, contents)
            print res


def testHdfs(kinit, header, hosts, paDirName, logName="hdfs", cmdPath="cmd/hdfs"):
    """To test HDFS and print test result."""
    for fp in os.listdir(cmdPath):
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            commands = [kinit]
            for cmd in cmdList:
                commands.append(str(cmd).replace("check_hdfs", paDirName))
            contents, status = runCmd.run_all_check_command(commands, logName)
            res = opf.Formatter().formatted_output("Active NameNode on %s: %s" % (host, status), header, contents)
            print res


def testYarn(kinit, header, hosts, logName="yarn", cmdPath="cmd/yarn"):
    """To test YARN and print test result."""
    for fp in os.listdir(cmdPath):
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            commands = [kinit]
            for cmd in cmdList:
                commands.append(cmd)
            contents, status = runCmd.run_all_check_command(commands, logName)
            res = opf.Formatter().formatted_output("Yarn on %s: %s" % (host, status), header, contents)
            print res


def testHyperbase(kinit, header, hosts, logName="hbase", cmdPath="cmd/hyperbase"):
    """To test HyperBase and print test result."""
    files = os.listdir(cmdPath)
    if len(files) == 0 or files:
        print "No command to run. Please check your CMD-FILES in path '%s'" % cmdPath
        return
    for host in hosts:
        commands = [kinit]
        hbaseShell = "hbase --hosts %s shell" % host
        for f in files:
            commands.append("%s %s/%s" % (hbaseShell, cmdPath, f))
        contents, status = runCmd.run_all_check_command(commands, logName)
        res = opf.Formatter().formatted_output("HyperBase on %s: %s" % (host, status), header, contents)
        print res


def testInceptorServer2(kinit, header, hosts, logName="hive", cmdPath="cmd/inceptor", database="default", realm="TDH"):
    """To test InceptorServer2 and print test result."""
    files = os.listdir(cmdPath)
    for host in hosts:
        commands = [kinit]
        beeline = "beeline -u \"jdbc:hive2://%s:10000/%s;principal=hive/%s@%s\"" % (host, database, host, realm)
        for f in files:
            commands.append("%s -f %s/%s" % (beeline, cmdPath, f))
        contents, status = runCmd.run_all_check_command(commands, logName)
        res = opf.Formatter().formatted_output("InceptorServer on %s: %s" % (host, status), header, contents)
        print res
