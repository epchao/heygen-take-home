"""
Spins up server and uses client library to demonstrate usage and log printing.
"""
import unittest
import threading
import time
from server import app
from server import DELAY_TIME
from client import Client


class IntegrationTest(unittest.TestCase):
    """
    Integration tests for the client-server relationship.
    """
    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(
            target=app.run, kwargs={'port': 5000})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)

    def test_client_server_interaction(self):
        """
        Test one /status request to get pending status, another one to get pending status, and
        finally the last one to get a completed status.
        """
        client = Client(initial_delay=0.5, max_delay=2, backoff_factor=1.5)

        # Testing initial pending
        status = client.get_status()
        self.assertEqual(status, "pending")
        time.sleep(DELAY_TIME // 2)

        # Testing second pending
        status = client.get_status()
        self.assertEqual(status, "pending")
        time.sleep(DELAY_TIME // 2)

        status = client.get_status()
        self.assertEqual(status, "completed")

    def test_concurrent_clients(self):
        """
        Create NUM_CLIENTS and concurrently request to this endpoint to stress-test it and to test
        the retrying multiple times and the exponential backoff to reduce server load.
        """
        num_clients = 500
        results = []

        def client_task():
            client = Client()
            status = client.get_status()
            results.append(status)

        threads = []
        for _ in range(num_clients):
            thread = threading.Thread(target=client_task)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        pending_count = results.count("pending")
        completed_count = results.count("completed")
        error_count = results.count("error")
        self.assertTrue(pending_count + completed_count +
                        error_count == num_clients)
        self.assertTrue(pending_count > 0 or completed_count > 0)


if __name__ == '__main__':
    unittest.main()
