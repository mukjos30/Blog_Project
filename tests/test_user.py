import unittest
from app.models import User,Post
from app import db
class TestUSer(unittest.TestCase):
    """
    This is the class we will be using to test the users
    """

    def setUp(self):
        """
        This will create a new user before each test
        """
        self.new_user = User(username = "josee",bio = "haha",password ="mukarange")

    def tearDown(self):
        """
        This will clear the db after each test
        """
        User.query.delete()
        Post.query.delete()

    def test_is_instance(self):
        """
        This will test whether the user created is an instance of the User class
        """
        self.assertTrue(isinstance(self.new_user, User))

    def test_init(self):
        """
        This will test whether the user is instantiated correctly
        """
        self.assertTrue(self.new_user.username == "josee")
        self.assertTrue(self.new_user.bio == "haha")

    def test_pass_generate(self):
        """
        This will test whether a new password is generated for the user
        """
        self.assertTrue(self.new_user.user_pass is not None)
    
    def test_hash_generate(self):
        """
        This will test whether the password generated is not equal to the original password
        """
        self.assertTrue(self.new_user.user_pass is not "josee")
    
    def test_save_user(self):
        """
        This will test whether the user is saved to the db
        """
        self.new_user.save_user()
        self.assertTrue(len(User.query.all()) == 1)
