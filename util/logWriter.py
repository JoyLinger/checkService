import logging.config


class Logger:
    def __init__(self, logName, logConf="conf/logger.conf"):
        self.conf = logConf
        self.name = logName

    def getLogger(self):
        """Returns object logger.
        """
        logging.config.fileConfig(self.conf)
        return logging.getLogger(self.name)
