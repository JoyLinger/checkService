#!/usr/bin/python
import sys

import util
import service.serviceFunc as sf
import util.cmdRunner as cmd

# zookeeper
def zk():
    kinit = "kinit zookeeper/%s -kt /etc/zookeeper1/zookeeper.keytab" % manager
    hosts = str(rc.get(key="ZOOKEEPER")).split(",")
    sf.testZookeeper(kinit, header, hosts, logName="zk", cmdPath="cmd/zookeeper")

# HDFS
def hdfs():
    path = rc.get(key="path")
    originFile = rc.get(key="originFile")
    getFromHdfs_file = rc.get(key="getFromHdfs_file")
    write_words = rc.get(key="words")
    cmd.prepareTestHdfs(path, write_words, originFile)
    kinit = "kinit hdfs/%s -kt /etc/hdfs1/hdfs.keytab" % manager
    hosts = str(rc.get(key="HDFS_ACTIVENAMENODE")).split(",")
    sf.testHdfs(kinit, header, hosts, logName="hdfs", cmdPath="cmd/hdfs")
    cmd.compare("%s/%s" % (path, originFile), "%s/%s" % (path, getFromHdfs_file))
    cmd.deleteDir(path)

# YARN
def yarn():
    kinit = "kinit yarn/%s -kt /etc/yarn1/yarn.keytab" % manager
    hosts = str(rc.get(key="YARN_RESOURCEMANAGER")).split(",")
    sf.testYarn(kinit, header, hosts, logName="yarn", cmdPath="cmd/yarn")

# HBASE
# sf.testHbase(this_host, header, rc, logName)
def hyperbase():
    kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % manager
    hosts = str(rc.get(key="HYPERBASE_MASTER")).split(",")
    sf.testHyperbase(kinit, header, hosts, logName="hbase", cmdPath="cmd/hyperbase")

# Inceptor
def inceptor():
    kinit = "kinit hive/%s -kt /etc/inceptorsql1/hive.keytab" % manager
    hosts = str(rc.get(key="INCEPTOR_SERVER")).split(",")
    sf.testInceptorServer2(kinit, header, hosts, logName="hive", cmdPath="cmd/inceptor", database=rc.get(key="DATABASE"), realm=rc.get(key="REALM"))


rc = util.configReader.ReadConf("conf/test-cluster.conf")
header = str(rc.get("HEADER")).split(",")
manager = rc.get("MANAGER")
supportServiceList = ["ZK", "ZOOKEEPER", "HDFS", "YARN", "HYPERBASE", "INCEPTOR"]
argList = sys.argv
if len(argList) == 1:
    print "No argument, test all services commands."
    zk()
    hdfs()
    yarn()
    hyperbase()
    inceptor()
elif len(argList) > 1:
    print "Start test services below:"
    args = ""
    for i in range(1, len(argList)):
        arg = str(argList[i]).upper()
        if arg == "ZK" or arg == "ZOOKEEPER":
            zk()
        elif arg == "HDFS":
            hdfs()
        elif arg == "YARN":
            yarn()
        elif arg == "HBASE" or arg == "HYPERBASE":
            hyperbase()
        elif arg == "HIVE" or arg == "INCEPTOR":
            inceptor()
        else:
            print "Sorry,", "'" + argList[i] + "'", "is not supported for cmd test."
