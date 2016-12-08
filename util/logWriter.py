import logging.config
import util.configReader as cr

class Logger:

    rc = cr.ReadConf("conf/logSettings.conf")

    def __init__(self, conf=rc.getLogConf(), name=rc.getLogName()):
        self.conf = conf
        self.name = name

    def getLogger(self):
        """Returns object logger.
        """
        logging.config.fileConfig(self.conf)
        return logging.getLogger(self.name)
