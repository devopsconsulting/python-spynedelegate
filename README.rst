==============
Spyne Delegate
==============

Extension for spyne so you can easy override services using delegate classes.

Example usage:

.. code:: python

    import logging
    from wsgiref.simple_server import make_server

    from spyne import Application, Unicode
    from spyne.model.complex import ComplexModel
    from spyne.protocol.soap.soap11 import Soap11
    from spyne.util.wsgi_wrapper import WsgiMounter
    from spynedelegate.meta import DelegateBase, ExtensibleServiceBase, rpc


    logging.basicConfig(level=logging.DEBUG)


    # models
    class Chicken(ComplexModel):
        __namespace__ = "spyne.delegate.chicken"
        name = Unicode


    class Cow(ComplexModel):
        __namespace__ = "spyne.delegate.cow"
        name = Unicode


    # delegates
    class ChickenDelegate(DelegateBase):
        @rpc(Chicken, _returns=Chicken.customize(max_occurs='unbounded'))
        def multiplyChickens(self, chicken):  # noqa
            return [chicken, chicken]


    class CowDelegate(DelegateBase):
        @property
        def method_request_string(self):
            # you can access the context with self.ctx
            return self.ctx.method_request_string

        def gen_name(self, name):
            # and you can use self as well
            return "%s -> %s" % (self.method_request_string, name)

        @rpc(Cow, _returns=Unicode)
        def sayMooh(self, cow):  # noqa
            return self.gen_name(cow.name)


    # inheritance
    class FarmDelegate(ChickenDelegate, CowDelegate):
        pass


    # service
    class FarmService(ExtensibleServiceBase):
        delegate = FarmDelegate


    farm_application = Application(
        [FarmService],
        tns='spyne.delegate.farm',
        name='farm-application',
        in_protocol=Soap11(validator='lxml'),
        out_protocol=Soap11()
    )


    wsgi_mounter = WsgiMounter({
        'farm': farm_application,
    })

    server = make_server('0.0.0.0', 8000, wsgi_mounter)
    server.serve_forever()

