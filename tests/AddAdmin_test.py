from AddAdmin import AddAdmin
from main import bot
from db_manager.UsersDB import UsersDB

test_db = UsersDB("test.db")


class Test_Databases (unittest.TestCase):
    def test_set_admin(self):
        pass
