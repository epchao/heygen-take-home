"""
Small client library that interacts with our server and is used to get the status of the job.
"""

import logging
import time
import random
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Client:
    """
    The client hitting the server endpoint.
    """

    def __init__(
            self,
            base_url="http://localhost:5000",
            initial_delay=1,
            max_delay=60,
            backoff_factor=2,
            max_retries=5
    ):
        self.base_url = base_url
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.max_retries = max_retries

    def get_status(self):
        """
        Make HTTP call to /status endpoint and wrap errors. Retry when requests fail and increase
        delays while this occurs to reduce the server load.
        """
        url = f"{self.base_url}/status"
        delay = self.initial_delay
        retries = 0

        while retries < self.max_retries:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                result = data.get("result")
                message = data.get("message")
                if message:
                    logging.info(message)
                    raise requests.RequestException
                return result
            except requests.RequestException as e:
                logging.info("Retrying connection due to error: %s.", e)
                if retries >= self.max_retries - 1:
                    break

                time.sleep(delay)
                delay = min(delay * self.backoff_factor, self.max_delay)
                delay *= (random.random() * 0.5 + 0.75)
                retries += 1
        return "error"
