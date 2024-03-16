import logging

TRACE = 5
logging.TRACE = TRACE

# Add the TRACE level to the logging module
logging.addLevelName(TRACE, "TRACE")


class CustomLogger(logging.Logger):

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)
