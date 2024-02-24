import unittest
from usermap import UserMap, PasswordError

class TestUserMap(unittest.TestCase):
    def setUp(self):
        self.um = UserMap()
        self.um.add_user("Spiderkid423", "Azeem423")

    def test_add_user(self):
        self.assertIn("Spiderkid423", self.um)
        with self.assertRaises(RuntimeError):
            self.um.add_user("Spiderkid423", "Azeem423")
        self.um.add_user("himmy", "Azeem423")
        self.assertIn("himmy", self.um)

    def test_get_item(self):
        self.assertEqual(self.um["Spiderkid423"].username, "Spiderkid423")
        with self.assertRaises(KeyError):
            _ = self.um["user3"]

    def test_update_password(self):
        self.um.update_password("Spiderkid423", "Azeem423", "Zeemie$")
        with self.assertRaises(PasswordError):
            self.um.update_password("Spiderkid423", "Zeemie?", "Zmoney2")

    def test_len(self):
        self.assertEqual(len(self.um), 1)
        self.um.add_user("himmy", "Azeem423")
        self.assertEqual(len(self.um), 2)

    def test_double(self):
        for i in range(3, 10):
            self.um.add_user(f"user{i}", "Azeem423")
        self.assertEqual(len(self.um), 8)
        self.assertEqual(self.um._num_buckets, 16)

if __name__ == '__main__':
    unittest.main()
