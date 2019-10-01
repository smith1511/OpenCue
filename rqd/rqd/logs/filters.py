import logging, platform
import rqutil

class HostnameFilter(logging.Filter):
    hostname = rqutil.getHostname()
    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True
