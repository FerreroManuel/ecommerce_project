import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AWKEzlQqiQIfM8fuJvQdCRcC0zlLYZEuwst6o9xNDtseEUpa2tXfagpeN2MJewu-QUBHXkBgN4E3F7U0"
        self.client_secret = "EGPsXFdI25bhfu4YeJ4cVQ6AZXoc-7kZIF91Q5lfgWEZwJ0Nl-MHzKXqd876Wz7m6sZ8DCHaiSYAf8-Q"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)