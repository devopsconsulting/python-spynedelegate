from unittest import TestCase

from spyne._base import MethodDescriptor

from .application import Chicken, ChickenDelegate, ChickenService


class MetaClassTestCase(TestCase):

    def test_spyne_method_wrapper(self):
        """We can still call the original function of a SpyneMethodWrapper"""
        delegate = ChickenDelegate()
        method_wrapper = delegate._spyne_cls_dict['multiplyChickens']
        chicken = Chicken(name='toktok')

        # call it
        result = method_wrapper(delegate.ctx, chicken)
        self.assertEqual(result[0].name, "toktok")
        self.assertEqual(result[1].name, "toktok")

    def test_service_class(self):
        """See if the service meta class is doing its magic"""
        service = ChickenService()

        # it should put all functions of a delegate class in my public methods
        self.assertIn('multiplyChickens', service.public_methods)

        # and see if we have a spyne MethodDescriptor
        self.assertEqual(
            type(service.multiplyChickens.descriptor), MethodDescriptor)

        # call it to see if it returns something.
        chicken = Chicken(name='toktok')
        result = service.multiplyChickens(None, chicken)
        self.assertTrue(type(result[0]), Chicken)
