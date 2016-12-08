import fileOpener as fo

class ReadConf:

    res = {}

    def __init__(self, confFile="conf/configurations.conf"):
        """Init.

        Convert file to dictionary."""
        cf = fo.openFile(confFile)
        for line in cf:
            line = line.replace("\n", "")
            if "#" not in line and "=" in line:
                kv = line.split("=")
                self.res[kv[0]] = kv[1]
            del line
        fo.closeFile(cf)

    def get(self, key):
        return self.res[key]

    def getLogConf(self, key="log_conf"):
        return self.res[key]

    def getLogName(self, key="log_name"):
        return self.res[key]

    def getJsonDir(self, key="json_dir"):
        return self.res[key]

    def getNodeJson(self, key="node_json"):
        return self.res[key]

    def getServiceJson(self, key="service_json"):
        return self.res[key]

    def getRoleJson(self, key="role_json"):
        return self.res[key]
