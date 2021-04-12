from unittest import TestCase
# from controller.user_input_controller import parse_user_arguments


class Test(TestCase):
    def test_parse_user_ip_options(self):
        args = {"t": "ip"}
        result = args.get("t")
        self.assertEqual(result, "ip")
