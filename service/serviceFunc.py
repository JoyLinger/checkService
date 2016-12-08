import util.cmd as c
import util.formatOutput as fo

def testZookeeper(this_host, header, rc):
    hosts = str(rc.get("ZOOKEEPER")).split(",")
    zk_kinit = "kinit zookeeper/%s -kt /etc/zookeeper1/zookeeper.keytab" % this_host
    cmd1 = "ls /"
    cmd2 = "create /zk-test zookeeper-test"
    cmd3 = "get /zk-test"
    cmd4 = "set /zk-test zk_test"
    cmd5 = "delete /zk-test"
    cmd6 = "ls /"
    cmds = [cmd1, cmd2, cmd3, cmd4, cmd5, cmd6]
    for host in hosts:
        zk_commands = [zk_kinit]
        zkcli = "/usr/lib/zookeeper/bin/zkCli.sh -server %s:2181" % host
        for cmd in cmds:
            zk_commands.append("echo %s | %s" % (cmd, zkcli))
        zk_contents = c.run_all_check_command(zk_commands)
        zk_res = fo.Formatter().formatted_output("ZooKeeper on %s" % host, header, zk_contents)
        print zk_res

def testHdfs():
    pass

def testYarn():
    pass

def testHbase(this_host, header, rc):
    hosts = str(rc.get("HYPERBASE_MASTER")).split(",")
    kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % this_host
    for h in hosts:
        commands = [kinit, "hbase --hosts %s shell %s |grep -v \"SLF4J\"|grep -v '^$'|grep -v \"row(s) in\"" % (h, "cmds/hbase")]
        contents = c.run_all_check_command(commands)
        res = fo.Formatter().formatted_output("HyperBase on %s" % h, header, contents)
        print res

def testHive2(this_host, header, rc):
    pass

def testDiscover(this_host, header, rc):
    pass

