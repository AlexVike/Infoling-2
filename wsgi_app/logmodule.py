import logging
import logging.handlers
import os


def getLogger(name, file=None, loglevel=logging.DEBUG, maxBytes=None, logformat='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s') -> logging.Logger:
    """Erstellt einen Logger oder gibt einen bereits existenten zurück.

    Der Logger wird mit dem angegebenen Namen und Loglevel erstellt.
    Die Loglevel sind untergliedert in:
        * DEBUG: Detailed information, typically of interest only when diagnosing problems.
        * INFO: Confirmation that things are working as expected.
        * WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
        * ERROR: Due to a more serious problem, the software has not been able to perform some function.
        * CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
        Auszug von https://docs.python.org/3/howto/logging.html.

    Args:
        name (str): Name des Loggers
        file (str, optional): File for logging. Defaults to None and logs to console.
        loglevel (logging.level, optional): Sets the log-Level. Defaults to logging.DEBUG.
        maxBytes (int, optional): Max. Size of the Log-File. Defaults to None and writes infinitely (Disk-Overflow !!!).
        logformat (str, optional): log-format. Defaults to '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s'
    Returns:
        logging.Logger: Object of class logging.Logger
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(loglevel)
    handler = None
    if file is None:
        handler = logging.StreamHandler()
    else:
        if not os.path.isfile(file):
            print("File does not yet exist")
            try:
                with open(file, 'w') as logfile:
                    logfile.write("File created")
            except Exception as e:
                print(e)
                print("Setting default console handler")
                handler = logging.StreamHandler()
        if handler == None:
            if maxBytes == None:
                print("setting normal file handler")
                handler = logging.FileHandler(file)
            else:
                print("setting RotatingFileHandler")
                handler = logging.handlers.RotatingFileHandler(file, maxBytes = maxBytes, backupCount=1)
    
    handler.setFormatter(logging.Formatter(logformat))
    logger.addHandler(handler)
    return logger

if __name__ == "__main__":
    logger = getLogger("test", file=os.getcwd()+'/logs/test.log')
    logger.debug("Test")
