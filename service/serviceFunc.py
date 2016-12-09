import util.cmd as c
import util.formatOutput as fo
import util.configReader as cr

def getCmdsFromFile(path):
    return cr.ReadConf(path).getCmdList(key="cmd")

def testZookeeper(this_host, header, rc):
    cmds = getCmdsFromFile("cmd/zookeeper")
    hosts = str(rc.get("ZOOKEEPER")).split(",")
    kinit = "kinit zookeeper/%s -kt /etc/zookeeper1/zookeeper.keytab" % this_host
    for host in hosts:
        commands = [kinit]
        zkcli = "/usr/lib/zookeeper/bin/zkCli.sh -server %s:2181" % host
        for cmd in cmds:
            commands.append("echo %s | %s" % (cmd, zkcli))
        contents = c.run_all_check_command(commands)
        # for i in range(1, len(contents)):
        #     contents[i][0] = cmds[i - 1]
        res = fo.Formatter().formatted_output("ZooKeeper on %s" % host, header, contents)
        print res

def testHdfs():
    pass

def testYarn():
    pass

def testHbase(this_host, header, rc):
    cmds = getCmdsFromFile(path="cmd/hbase")
    hosts = str(rc.get("HYPERBASE_MASTER")).split(",")
    kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % this_host
    for h in hosts:
        commands = [kinit]
        hbaseShell = "hbase --hosts %s shell |grep -v \"SLF4J\"|grep -v '^$'|grep -v \"row(s) in\"" % h
        for cmd in cmds:
            commands.append("echo %s | %s" % (cmd, hbaseShell))
        contents = c.run_all_check_command(commands)
        res = fo.Formatter().formatted_output("HyperBase on %s" % h, header, contents)
        print res

def testHive2(this_host, header, rc):
    pass

def testDiscover(this_host, header, rc):
    pass

