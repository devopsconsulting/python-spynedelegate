import logging
import thread
import time
from unittest import TestCase

from wsgiref.simple_server import make_server
from wsgiref.validate import validator

from spyne.server.wsgi import WsgiApplication

import suds
from suds.cache import NoCache

from .application import farm_application


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

host = '127.0.0.1'
port = 9876


def spyne_server():
    wsgi_application = WsgiApplication(farm_application)
    server = make_server(host, port, validator(wsgi_application))

    logger.info('Starting server at %s:%s.' % (host, port))
    logger.info('WSDL is at: /?wsdl')
    server.serve_forever()


class SpyneClientTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        def run_server():
            spyne_server()

        thread.start_new_thread(run_server, ())
        time.sleep(1)
        cls.client = suds.client.Client(
            'http://127.0.0.1:9876/?wsdl', cache=NoCache())

        cls.service = cls.client.sd[0].service
        cls.chicken_type = cls.client.sd[0].types[0][0]
        cls.cow_type = cls.client.sd[0].types[1][0]

        cls.methods = cls.client.wsdl.services[0].ports[0].methods.values()

    def test_wsdl_service_name(self):
        self.assertEqual(self.service.name, "FarmService")

    def test_wsdl_types(self):
        self.assertEqual(self.service.name, "FarmService")
        self.assertEqual(
            self.chicken_type.namespace()[1], "spyne.delegate.chicken")
        self.assertEqual(
            self.cow_type.namespace()[1], "spyne.delegate.cow")

    def test_wsdl_methods(self):
        self.assertEqual(self.methods[0].name, 'multiplyChickens')
        self.assertEqual(self.methods[1].name, 'sayMooh')

        chicken = self.client.factory.create("ns0:Chicken")
        chicken.name = "toktok"
        result = self.client.service.multiplyChickens(chicken)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "toktok")
        self.assertEqual(result[1].name, "toktok")

        cow = self.client.factory.create("ns1:Cow")
        cow.name = "Supercow"
        result = self.client.service.sayMooh(cow)
        self.assertEqual(result, "{spyne.delegate.farm}sayMooh -> Supercow")
