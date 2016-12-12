import logging

import multiprocessing

from unittest import TestCase

from wsgiref.simple_server import make_server
from wsgiref.validate import validator

from spyne.server.wsgi import WsgiApplication


from .application import farm_application

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SpyneServerTestCase(TestCase):
    host = '127.0.0.1'
    port = 9876

    @classmethod
    def spyne_server(cls, queue):
        wsgi_application = WsgiApplication(farm_application)
        wsgi_server = make_server(
            cls.host, cls.port, validator(wsgi_application))

        logger.info('Starting server at %s:%s.' % (cls.host, cls.port))
        logger.info('WSDL is at: /?wsdl')

        queue.put('server started')
        wsgi_server.serve_forever()

    @classmethod
    def setUpClass(cls):
        queue = multiprocessing.Queue()
        cls.server = multiprocessing.Process(
            target=cls.spyne_server, args=(queue,))
        cls.server.start()

        # wait for wsgi server to start
        queue.get('server started')

        super(SpyneServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        super(SpyneServerTestCase, cls).tearDownClass()
