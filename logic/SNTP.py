from ntplib import NTPClient, NTPException
from time import ctime
from logger import get_logger
from logic.Settings import ntpURL

logger = get_logger("SNTP")

class SNTP:
    def __init__(self):
        # initialize ntp client
        ntp_client = NTPClient()
        try:
            response = ntp_client.request(ntpURL)
        except NTPException as e:
            logger.error(e)
            raise
        self.timestamp = ctime(response.tx_time)
        logger.info("Time taken from %s server : %s", ntpURL, self.timestamp)