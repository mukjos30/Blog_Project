import unittest
from app.models import Subscriber

class TestSubscriber(unittest.TestCase):
    """
    This is the class I will use to test the subscriber
    """
    def setUp(self):
        """
        This will create a new sub before each test
        """
        self.new_sub = Subscriber(email = "mukjos30@gmail.com")

    def tearDown(self):
        """
        This will clear the db after each test
        """
        Subscriber.query.delete()

    def test_is_instance(self):
        """
        This will test whether the new sub is an instance of the Subscriber class
        """
        self.assertTrue(isinstance(self.new_sub, Subscriber))

    def test_init(self):
        """
        This will test whether the sub is instantiated correctly
        """
        self.assertTrue(self.new_sub.email == "mukjos30@gmail.com")

    def test_save_sub(self):
        """
        This will test whether the sub is added to the db
        """
        self.new_sub.save_subscriber()
        self.assertTrue(len(Subscriber.query.all()) > 0)
        
