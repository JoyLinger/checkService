#!/usr/bin/python
import sys

import service.serviceFunc as sf
import util.configReader as cr
import util.cmdRunner as runCmd


# zookeeper
def zk():
    print "\033[31m [ Start test zookeeper ] \033[0m"
    kinit = "kinit zookeeper/%s -kt /etc/zookeeper1/zookeeper.keytab" % manager
    hosts = str(rc.get(key="ZOOKEEPER")).split(",")
    zkCliPath = rc.get("ZKCLI_PATH")
    sf.testZookeeper(kinit, header, hosts, logName="zk", cmdPath="cmd/zookeeper", zkCliPath=zkCliPath)


# HDFS
def hdfs():
    print "\033[31m [ Start test hdfs ] \033[0m"
    path = rc.get(key="path")
    originFile = rc.get(key="originFile")
    getFromHdfs_file = rc.get(key="getFromHdfs_file")
    write_words = rc.get(key="words")
    runCmd.prepareTestHdfs(path, write_words, originFile)
    kinit = "kinit hdfs/%s -kt /etc/hdfs1/hdfs.keytab" % manager
    hosts = str(rc.get(key="HDFS_ACTIVENAMENODE")).split(",")
    sf.testHdfs(kinit, header, hosts, logName="hdfs", cmdPath="cmd/hdfs")
    runCmd.compare("%s/%s" % (path, originFile), "%s/%s" % (path, getFromHdfs_file))
    runCmd.deleteDir(path)


# YARN
def yarn():
    print "\033[31m [ Start test yarn ] \033[0m"
    kinit = "kinit yarn/%s -kt /etc/yarn1/yarn.keytab" % manager
    hosts = str(rc.get(key="YARN_RESOURCEMANAGER")).split(",")
    sf.testYarn(kinit, header, hosts, logName="yarn", cmdPath="cmd/yarn")


# HYPERBASE
# sf.testHbase(this_host, header, rc, logName)
def hyperbase():
    print "\033[31m [ Start test hyperbase ] \033[0m"
    kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % manager
    hosts = str(rc.get(key="HYPERBASE_MASTER")).split(",")
    sf.testHyperbase(kinit, header, hosts, logName="hbase", cmdPath="cmd/hyperbase")


# Inceptor
def inceptor():
    print "\033[31m [ Start test inceptor ] \033[0m"
    kinit = "kinit hive/%s -kt /etc/inceptorsql1/hive.keytab" % manager
    hosts = str(rc.get(key="INCEPTOR_SERVER")).split(",")
    sf.testInceptorServer2(kinit, header, hosts, logName="hive", cmdPath="cmd/inceptor", database=rc.get(key="DATABASE"), realm=rc.get(key="REALM"))


# rc = cr.ReadConf("conf/test-cluster.conf")
rc = cr.ReadConf("conf/my-centos-cluster.conf")
header = str(rc.get("HEADER")).split(",")
manager = rc.get("MANAGER")
# supportServiceList = ["ZOOKEEPER", "HDFS", "YARN", "HYPERBASE", "INCEPTOR"]
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
            print "Sorry,", "'" + argList[i] + "'", "is not supported in current version."
