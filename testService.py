#!/usr/bin/python
import commands
import os
import time

import util
import service.serviceFunc as sf
import util.cmd as uc

this_host = commands.getoutput("hostname")
rc = util.configReader.ReadConf("conf/test-cluster.conf")
header = str(rc.get("HEADER")).split(",")
# myLog = util.logWriter.Logger().getLogger()
# Zookeeper
sf.testZookeeper(this_host, header, rc)

# HBASE
sf.testHbase(this_host, header, rc)

# HDFS

# active_nn_host = rc.get("HDFS_ACTIVENAMENODE")
# port = rc.get("PORT")
# nameservice = rc.get("NAMESERVICE")
#
# hdfs_path = "/tmp/check_hdfs/"
# file_name = "checkHdfsStatus.txt"
# uc.createDir(hdfs_path)
# # Don't make "xxx" + "xxx" in method commands.getstatusoutput(), otherwise, you'll get an ERROR like below:
# #   sh: -c: line 0: unexpected EOF while looking for matching `''
# #   sh: -c: line 1: syntax error: unexpected end of file
# write_words = "echo 'Generate this text file to check status for TDH-cluster-service: hdfs1' > " + hdfs_path + file_name
# os.system(write_words)
#
# hdfs_kinit = "kinit hdfs/" + this_host + " -kt /etc/hdfs1/hdfs.keytab"
# cmd1 = "hdfs dfs -mkdir -p " + hdfs_path
# cmd2 = "hdfs dfs -put " + hdfs_path + file_name + " " + hdfs_path
# cmd3 = "hdfs dfs -put /etc/hosts " + hdfs_path
# cmd4 = "hdfs dfs -get " + hdfs_path + file_name + " /tmp"
# cmd5 = "hdfs dfs -ls " + hdfs_path
# cmd6 = "hdfs dfs -cat " + hdfs_path + "hosts"
# cmd7 = "hdfs dfs -rm -R " + hdfs_path
#
# hdfs_commands = [hdfs_kinit, cmd1, cmd2, cmd3, cmd4, cmd5, cmd6, cmd7]
#
# hdfs_contents = uc.run_all_check_command(hdfs_commands)
# hdfs_res = util.formatOutput.Formatter().formatted_output("HDFS", header, hdfs_contents)
# print hdfs_res
# os.remove(hdfs_path)

# # YARN
# yarn_command = ["kinit yarn/" + host + " -kt /etc/yarn1/yarn.keytab", "yarn application -list -appStates ALL"]
# yarn_contents = run_all_check_command(yarn_command)
# yarn_res = util.formatOutput.Formatter().formatted_output("YARN", header, yarn_contents)
#
# # Hbase
# hbase_command = ["kinit hbase/" + host + " -kt /etc/hyperbase1/hbase.keytab", "echo 'list_namespace' | hbase shell"]
# hbase_contents = run_all_check_command(hbase_command)
# hbase_res = util.formatOutput.Formatter().formatted_output("HBase", header, hbase_contents)
#
# # Inceptor
# inceptor_command = ['echo "show databases;" | beeline -u "jdbc:hive2://tw-suse2204:10000/default;principal=hive/tw-suse2204@TDH"', 'echo "show tables;" | beeline -u "jdbc:hive2://tw-suse2204:10000/default;principal=hive/tw-suse2204@TDH"']
# inceptor_contents = run_all_check_command(inceptor_command)
# inceptor_res = util.formatOutput.Formatter().formatted_output("Inceptor", header, inceptor_contents)

# Discover
# discover_command = []
# discover_contents = run_all_check_command(discover_command)

# print yarn_res
# print hbase_res
# print inceptor_res

