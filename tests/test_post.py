import unittest
from app.models import Post,User

class TestPost(unittest.TestCase):
    """
    This is the class I will use to test the posts
    """

    def setUp(self):
        """
        This will create a new post before each test
        """
        self.new_post = Post(title = "Haha")

    def tearDown(self):
        """
        This will clear the db after every test
        """
        Post.query.delete()
        User.query.delete()

    def test_is_instance(self):
        """
        This will test whether the new_post created is an instance of the Post class
        """
        self.assertTrue(isinstance(self.new_post, Post))

    def test_init(self):
        """
        This will test whether the post is initialized correctly
        """
        self.assertTrue(self.new_post.title == "Haha")

    def test_save_user(self):
        """
        THis will test whether the pitch is added to the db
        """
        self.new_post.save_post()
        self.assertTrue(len(Post.query.all()) > 0)

    def test_user_relation(self):
        """
        This will test whether the post is correctly linked to the user
        """
        new_user = User(username = "Marvin")
        test_post = Post(title = "J", user = new_user)
        self.assertTrue(test_post.user.username == "Marvin")
    