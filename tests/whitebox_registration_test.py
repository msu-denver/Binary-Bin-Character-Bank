import unittest
from src.app.routes import register_user

class TestRegistration(unittest.TestCase):
    def test_empty_username(self):
        msg, success = register_user("", "Password123")
        self.assertFalse(success)
        self.assertEqual(msg, "Missing data")

    def test_empty_password(self):
        msg, success = register_user("new_user", "")
        self.assertFalse(success)
        self.assertEqual(msg, "Missing data")

    def test_existing_username(self):
        msg, success = register_user("existing_user", "Password123")
        self.assertFalse(success)
        self.assertEqual(msg, "Username already taken")

    def test_new_user(self):
        msg, success = register_user("unique_user", "Password123")
        self.assertTrue(success)
        self.assertEqual(msg, "User registered")

if __name__ == "__main__":
    unittest.main()
