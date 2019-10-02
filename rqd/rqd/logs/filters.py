import logging, platform
import rqutil

class HostnameFilter(logging.Filter):
    """Injects the RQD instance hostname or IP"""
    hostname = rqutil.getHostname()

    def filter(self, record):
        """Sets LogRecord.hostname to the current hostname or IP.
        The hostname can then be accessed via the LogRecord or
        formatters.
        """
        record.hostname = HostnameFilter.hostname
        return True
