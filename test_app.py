import unittest
import app as tested_app


class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        tested_app.app.config["TESTING"] = True
        self.app = tested_app.app.test_client()

    def test_ping_endpoint(self):
        r = self.app.get("/ping")
        self.assertEqual(r.data.decode("UTF-8"), "Hello There!!")


if __name__ == "__main__":
    unittest.main()
