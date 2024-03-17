"""
SurrealDB helpers
"""

import atexit
import os

from subprocess import Popen, PIPE, TimeoutExpired


class SurrealServer:
    """A helper to launch a local surrealDB server"""

    def __init__(self, url, bind="0.0.0.0:8000"):
        self.url = url
        self.bind = bind
        self.proc = None

    def start(self):
        """starts surreal process and register a callback is anything goes wrong"""
        os.makedirs(self.url, exist_ok=True)
        # launch server
        self.proc = Popen(
            [
                "surreal",
                "start",
                "--bind",
                f"{self.bind}",
                "--user",
                "root",
                "--pass",
                "root",
                f"file://{self.url}",
            ],
            stdout=PIPE,
            stderr=PIPE,
        )
        # give sometime to communicate with process
        # so server will be ready or we get some error feedback
        try:
            stdout, stderr = self.proc.communicate(timeout=0.5)
            print(stdout)
            print(stderr)
            raise RuntimeError()  # something was wrong
        except TimeoutExpired:
            pass

        # stop process when parent process may die
        atexit.register(self.stop)

    def stop(self):
        """stops child process and unregister callback"""
        self.proc.terminate()
        atexit.unregister(self.stop)
