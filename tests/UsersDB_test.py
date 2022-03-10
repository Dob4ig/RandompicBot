import unittest
from db_manager import UsersDB

test_db = UsersDB.UsersDB("test.db")


class Test_Databases (unittest.TestCase):
    def test_add_user(self):
        self.assertTrue(type(test_db.add_user(1111, "Test")) is str)

    def test_get_fullname(self):
        self.assertTrue(type(test_db.get_fullname(1111)) is str)

    def test_set_admin(self):
        self.assertTrue(type(test_db.set_admin(1111)) is str)

    def test_del_admin(self):
        self.assertTrue(type(test_db.del_admin(1111)) is str)

    def test_ban_user(self):
        self.assertTrue(type(test_db.ban_user(1111)) is str)

    def test_unban_user(self):
        self.assertTrue(type(test_db.unban_user(1111)) is str)

    def test_add_channel(self):
        self.assertTrue(type(test_db.add_channel(1111, 2222)) is str)

    def test_get_channel(self):
        self.assertTrue(type(test_db.get_channel(1111)) is str)

    def test_del_channel(self):
        self.assertTrue(type(test_db.del_channel(1111, 2222)) is str)

    def test_get_users(self):
        self.assertTrue(type(test_db.get_users("user")) is set)
