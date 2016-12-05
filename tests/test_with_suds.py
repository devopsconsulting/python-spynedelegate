import logging

import multiprocessing

from unittest import TestCase

from wsgiref.simple_server import make_server
from wsgiref.validate import validator

from spyne.server.wsgi import WsgiApplication

from suds.cache import NoCache
from suds.client import Client

from .application import farm_application

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

host = '127.0.0.1'
port = 9876


def spyne_server(queue):
    wsgi_application = WsgiApplication(farm_application)
    wsgi_server = make_server(host, port, validator(wsgi_application))

    logger.info('Starting server at %s:%s.' % (host, port))
    logger.info('WSDL is at: /?wsdl')

    queue.put('server started')
    wsgi_server.serve_forever()


class SpyneClientTestBase(TestCase):
    @classmethod
    def setUpClass(cls):

        q = multiprocessing.Queue()
        cls.server = multiprocessing.Process(target=spyne_server, args=(q,))
        cls.server.start()

        # wait for wsgi server to start
        q.get('server started')

        url = "http://%s:%s/?wsdl" % (host, port)
        cls.client = Client(url, cache=NoCache())

        cls.service = cls.client.sd[0].service
        cls.chicken_type = cls.client.sd[0].types[0][0]
        cls.cow_type = cls.client.sd[0].types[1][0]

        cls.methods = [
            str(x) for x in cls.client.wsdl.services[0].ports[0].methods]

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()

    def test_wsdl_service_name(self):
        self.assertEqual(self.service.name, "FarmService")

    def test_wsdl_types(self):
        self.assertEqual(self.service.name, "FarmService")
        self.assertEqual(
            self.chicken_type.namespace()[1], "spyne.delegate.chicken")
        self.assertEqual(
            self.cow_type.namespace()[1], "spyne.delegate.cow")

    def test_wsdl_methods(self):
        self.assertTrue('multiplyChickens' in self.methods)
        self.assertTrue('sayMooh' in self.methods)
        self.assertTrue('thisStillWorks' in self.methods)

        chicken = self.client.factory.create("ns0:Chicken")
        chicken.name = "toktok"
        chicken_results = self.client.service.multiplyChickens(chicken)
        self.assertEqual(len(chicken_results), 2)
        self.assertEqual(chicken_results[0].name, "toktok")
        self.assertEqual(chicken_results[1].name, "toktok")

        cow = self.client.factory.create("ns1:Cow")
        cow.name = "Supercow"
        cow_result = self.client.service.sayMooh(cow)
        self.assertEqual(
            cow_result, "{spyne.delegate.farm}sayMooh -> Supercow")
