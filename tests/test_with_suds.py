from suds.cache import NoCache
from suds.client import Client

from .base import SpyneServerTestCase


class SudsClientTest(SpyneServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(SudsClientTest, cls).setUpClass()

        url = "http://%s:%s/?wsdl" % (cls.host, cls.port)
        cls.client = Client(url, cache=NoCache())

        cls.service = cls.client.sd[0].service
        cls.chicken_type = cls.client.sd[0].types[0][0]
        cls.cow_type = cls.client.sd[0].types[1][0]

        cls.methods = [
            str(x) for x in cls.client.wsdl.services[0].ports[0].methods]

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        super(SudsClientTest, cls).tearDownClass()

    def test_wsdl_service_name(self):
        self.assertEqual(self.service.name, "FarmService")

    def test_types_namespace(self):
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
            cow_result, "{spyne.delegate.farm}sayMooh -> Supercow overridden")

        another_result = self.client.service.generateName('Mooh')
        self.assertEqual(
            another_result, "{spyne.delegate.farm}generateName -> Mooh")
