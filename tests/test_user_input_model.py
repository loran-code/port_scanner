from unittest import TestCase

from model.user_input_model import *


class TestUserInputModel(TestCase):

    def test_check_port(self):
        result = UserInputModel.check_port(None)
        self.assertEqual(result, 1000)
        # self.fail()


class Test(TestCase):
    def test_user_input_model(self):
        self.fail()
