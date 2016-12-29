#!/usr/bin/python
import sys
import getopt
import time
import os

import service.serviceFunc as sf
import util.configReader as cr
import util.cmdRunner as runCmd


# zookeeper
def zk(conf_file, rc, header, manager):
    # print "\032[31m [ Start test zookeeper ] \032[0m"
    kinit = "kinit zookeeper/%s -kt /etc/zookeeper1/zookeeper.keytab" % manager
    hosts = str(rc.get(key="ZOOKEEPER")).split(",")
    if len(hosts) == 0 or (len(hosts) == 1 and hosts[0] == ""):
        print "Please check the value of the key 'ZOOKEEPER' in your configure-file '%s'" % conf_file
        return
    zkCliPath = rc.get("ZKCLI_PATH")
    sf.testZookeeper(kinit, header, hosts, logName="zookeeper", cmdPath="cmd/zookeeper", zkCliPath=zkCliPath)


# HDFS
def hdfs(conf_file, rc, header, manager):
    hosts = str(rc.get(key="HDFS_ACTIVENAMENODE")).split(",")
    if len(hosts) == 0 or (len(hosts) == 1 and hosts[0] == ""):
        print "Please check the value of the key 'HDFS_ACTIVENAMENODE' in your configure-file '%s'" % conf_file
        return
    # print "\033[31m [ Start test hdfs ] \033[0m"
    path = rc.get(key="path")
    path += "_%s/" % time.strftime("%Y%m%d%H%M%s")
    paths = str(path).split("/")
    originFile = rc.get(key="originFile")
    getFromHdfs_file = rc.get(key="getFromHdfs_file")
    write_words = rc.get(key="words")
    runCmd.prepareTestHdfs(path, write_words, originFile)
    kinit = "kinit hdfs/%s -kt /etc/hdfs1/hdfs.keytab" % manager
    sf.testHdfs(kinit, header, hosts, paths[len(paths) - 2], logName="hdfs", cmdPath="cmd/hdfs")
    runCmd.compare("%s/%s" % (path, originFile), "%s/%s" % (path, getFromHdfs_file))
    runCmd.deleteDir(path)


# YARN
def yarn(conf_file, rc, header, manager):
    # print "\033[31m [ Start test yarn ] \033[0m"
    kinit = "kinit yarn/%s -kt /etc/yarn1/yarn.keytab" % manager
    hosts = str(rc.get(key="YARN_RESOURCEMANAGER")).split(",")
    if len(hosts) == 0 or (len(hosts) == 1 and hosts[0] == ""):
        print "Please check the value of the key 'YARN_RESOURCEMANAGER' in your configure-file '%s'" % conf_file
        return
    sf.testYarn(kinit, header, hosts, logName="yarn", cmdPath="cmd/yarn")


# HYPERBASE
# sf.testHbase(this_host, header, rc, logName)
def hyperbase(conf_file, rc, header, manager):
    # print "\033[31m [ Start test hyperbase ] \033[0m"
    kinit = "kinit hbase/%s -kt /etc/hyperbase1/hbase.keytab" % manager
    hosts = str(rc.get(key="HYPERBASE_MASTER")).split(",")
    if len(hosts) == 0 or (len(hosts) == 1 and hosts[0] == ""):
        print "Please check the value of the key 'HYPERBASE_MASTER' in your configure-file '%s'" % conf_file
        return
    sf.testHyperbase(kinit, header, hosts, logName="hbase", cmdPath="cmd/hyprtbase")


# Inceptor
def inceptor(conf_file, rc, header, manager):
    # print "\033[31m [ Start test inceptor ] \033[0m"
    kinit = "kinit hive/%s -kt /etc/inceptorsql1/hive.keytab" % manager
    hosts = str(rc.get(key="INCEPTOR_SERVER")).split(",")
    if len(hosts) == 0 or (len(hosts) == 1 and hosts[0] == ""):
        print "Please check the value of the key 'INCEPTOR_SERVER' in your configure-file '%s'" % conf_file
        return
    sf.testInceptorServer2(kinit, header, hosts, logName="hive", cmdPath="cmd/inceptor", database=rc.get(key="DATABASE"), realm=rc.get(key="REALM"))


def main(this, argv):
    help_msg = """Usage: %s [options...] arguments...

    -c,--cluster <cluster name>     Specify the cluster. The valid cluster
                                    name can be one of the following:
                                    BABYLON,OLYMPUS,TEST
    -s,--service <service name>     Specify the services to test. The valid
                                    service name can be one or more than one
                                    of the following: ALL,ZOOKEEPER,HDFS,
                                    YARN,HBASE,INCEPTOR. But ALL must be used
                                    all alone.
    -h,--help                       Print help information."""\
               % str(this).split("/")[len(str(this).split("/")) - 1]
    cluster = ""
    services = ""
    conf_file = "%s/conf/" % os.getcwd()
    # supportServiceList = ["ZOOKEEPER", "HDFS", "YARN", "HYPERBASE", "INCEPTOR"]
    try:
        opts, args = getopt.getopt(argv, "c:s:h", ["cluster=", "service=", "help"])
    except getopt.GetoptError:
        print help_msg
        sys.exit(1)
    if len(opts) == 0:
        print help_msg
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--cluster"):
            cluster = arg
        elif opt in ("-s", "--service"):
            services += arg
        elif opt in ("-h", "--help"):
            print help_msg
            sys.exit(0)
    upCluster = str(cluster).upper()
    # my own test-cluster
    if upCluster == "MINE":
        conf_file += "my-centos-cluster.conf"
    # transwarp test-cluster
    elif upCluster == "XH":
        conf_file += "xh-cluster.conf"
    else:
        print "Unknown cluster, Exit."
        sys.exit(3)
    if services == "" or services.upper() == "ALL":
        serviceList = ["ZOOKEEPER", "HDFS", "YARN", "HYPERBASE", "INCEPTOR"]
    elif services.upper().__contains__("ALL"):
        print "ALL cannot be used with other arguments. Exit"
        sys.exit(4)
    else:
        serviceList = services.split(",")
    rc = cr.ReadConf(conf_file)
    header = str(rc.get("HEADER")).split(",")
    manager = rc.get("MANAGER")
    print "Start test services below:"
    print serviceList
    for s in serviceList:
        arg = str(s).upper()
        if arg == "ZOOKEEPER":
            zk(conf_file, rc, header, manager)
        elif arg == "HDFS":
            hdfs(conf_file, rc, header, manager)
        elif arg == "YARN":
            yarn(conf_file, rc, header, manager)
        elif arg in ("HBASE", "HYPERBASE"):
            hyperbase(conf_file, rc, header, manager)
        elif arg in ("HIVE", "INCEPTOR"):
            inceptor(conf_file, rc, header, manager)
        else:
            print "Sorry,", "'" + s + "'", "is not supported in current version."

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
