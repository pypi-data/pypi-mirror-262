# Builtin modules
import os, unittest
from time import monotonic
from http import HTTPStatus
# Third party modules
from fsLogger import SimpleLogger, Logger
from fsSignal import Signal, SoftSignal
# Local modules
from .. import Client
# Program
class ClientTest(unittest.TestCase):
	signal:Signal
	@classmethod
	def setUpClass(cls) -> None:
		if os.environ.get("DEBUG") == "1":
			SimpleLogger("TRACE")
		cls.signal = Signal()
		return None
	def test_request(self) -> None:
		rootClient = Client(
			"TCPv4:HTTP:JSONRPC-2",
			("api.fusionexplorer.io", 443),
			ssl=True,
			disableCompression=True,
			log=Logger("Client"),
			signal=SoftSignal()
		)
		r = rootClient.request("ping")
		self.assertEqual(r.isDone(), False)
		self.assertEqual(r.isSuccess(), True)
		self.assertEqual(r.isDone(), True)
		self.assertGreater(r.getDelay(), 0)
		self.assertIsInstance(r.get(), str)
		with rootClient as c:
			r = c.request("ping")
			self.assertEqual(r.isDone(), False)
			self.assertEqual(r.isSuccess(), True)
			self.assertEqual(r.isDone(), True)
			self.assertIsInstance(r.get(), str)
			r = c.request("ping", id=88)
			self.assertEqual(r.getID(), 88)
			r = c.request("ping", [0])
			self.assertEqual(r.isSuccess(), False)
			self.assertEqual(r.isDone(), True)
			self.assertEqual(r.get(), {
				"code": -32602,
				"data": "ping() takes 0 positional argument but 1 were given",
				"message": "Invalid params"
			})
			assert(r.getHTTPStatus() == HTTPStatus.OK)
			r = c.request("surenoteexists")
			self.assertEqual(r.isSuccess(), False)
			self.assertEqual(r.isDone(), True)
			self.assertEqual(r.get(), {"code": -32601, "data": "surenoteexists", "message": "Method not found"})
			r0 = c.request("ping", id="asd")
			r1 = c.request("ping", id="dsa")
			self.assertIsInstance(r0.get(), str)
			self.assertIsInstance(r1.get(), str)
		with rootClient as c:
			r0 = c.request("ping", id="asd")
			r1 = c.request("ping", id="dsa")
			self.assertIsInstance(r0.get(), str)
			self.assertIsInstance(r1.get(), str)
	def test_retry(self) -> None:
		rootClient = Client(
			"TCPv4:HTTP:JSONRPC-P",
			("api.fusionexplorer.io", 443),
			ssl=False,
			disableCompression=True,
			retryCount=2,
			retryDelay=1,
			log=Logger("Client"),
			signal=SoftSignal(),
		)
		s = monotonic()
		r = rootClient.request("ping")
		try:
			r.get()
		except:
			pass
		self.assertGreater(monotonic()-s, 1.0)
	def test_binance(self) -> None:
		with Client(
			"TCPv4:HTTP:REST",
			("fapi.binance.com", 443),
			ssl=True,
			log=Logger("Client"),
			signal=SoftSignal(),
		) as clnt:
			clnt.request(httpMethod="GET", path="/fapi/v1/premiumIndex").get()
