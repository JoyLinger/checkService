import os

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
    :param logName: logger in file: conf/logger.conf
    :param cmdPath:
    :param zkCliPath:
    """
    for fp in os.listdir(cmdPath):
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            commands = [kinit]
            zkcli = "%s/zkCli.sh -server %s:2181" % (zkCliPath, host)
            for cmd in cmdList:
                commands.append("echo %s | %s" % (cmd, zkcli))
            contents = runCmd.run_all_check_command(commands, logName)
            # for i in range(1, len(contents)):
            #     contents[i][0] = cmds[i - 1]
            res = opf.Formatter().formatted_output("ZooKeeper on %s" % host, header, contents)
            print res


def testHdfs(kinit, header, hosts, logName="hdfs", cmdPath="cmd/hdfs"):
    """To test HDFS and print test result."""
    for fp in os.listdir(cmdPath):
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            commands = [kinit]
            for cmd in cmdList:
                commands.append(cmd)
            contents = runCmd.run_all_check_command(commands, logName)
            res = opf.Formatter().formatted_output("Active NameNode on %s" % host, header, contents)
            print res


def testYarn(kinit, header, hosts, logName="yarn", cmdPath="cmd/yarn"):
    """To test YARN and print test result."""
    for fp in os.listdir(cmdPath):
        cmdList = getCmdsFromFile(path="%s/%s" % (cmdPath, fp))
        for host in hosts:
            commands = [kinit]
            for cmd in cmdList:
                commands.append(cmd)
            contents = runCmd.run_all_check_command(commands, logName)
            res = opf.Formatter().formatted_output("Yarn on %s" % host, header, contents)
            print res


# def testHbase(this_host, header, rc, logName):
#     """To test HyperBase and print test result."""
#     cmds = getCmdsFromFile(path="cmd/hyperbase")
#     hosts = str(rc.get(key="HYPERBASE_MASTER")).split(",")
#     kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % this_host
#     for h in hosts:
#         commands = [kinit]
#         hbaseShell = "hbase --hosts %s shell |grep -v \"SLF4J\"|grep -v '^$'|grep -v \"row(s) in\"" % h
#         for cmd in cmds:
#             commands.append("echo %s | %s" % (cmd, hbaseShell))
#         contents = c.run_all_check_command(commands, logName)
#         res = opf.Formatter().formatted_output("HyperBase on %s" % h, header, contents)
#         print res

def testHyperbase(kinit, header, hosts, logName="hbase", cmdPath="cmd/hyperbase"):
    """To test HyperBase and print test result."""
    files = os.listdir(cmdPath)
    if len(files) == 0 or files:
        print "No command to run. Please check your CMD-FILES in path '%s'" % cmdPath
        return
    for h in hosts:
        commands = [kinit]
        hbaseShell = "hbase --hosts %s shell" % h
        for f in files:
            commands.append("%s %s/%s" % (hbaseShell, cmdPath, f))
        contents = runCmd.run_all_check_command(commands, logName)
        res = opf.Formatter().formatted_output("HyperBase on %s" % h, header, contents)
        print res


def testInceptorServer2(kinit, header, hosts, logName="hive", cmdPath="cmd/inceptor", database="default", realm="TDH"):
    """To test InceptorServer2 and print test result."""
    files = os.listdir(cmdPath)
    for h in hosts:
        commands = [kinit]
        beeline = "beeline -u \"jdbc:hive2://%s:10000/%s;principal=hive/%s@%s\"" % (h, database, h, realm)
        for f in files:
            commands.append("%s -f %s/%s" % (beeline, cmdPath, f))
        contents = runCmd.run_all_check_command(commands, logName)
        res = opf.Formatter().formatted_output("InceptorServer on %s" % h, header, contents)
        print res
