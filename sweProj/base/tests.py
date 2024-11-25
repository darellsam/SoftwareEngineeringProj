
# Create your tests here.
from django.test import TestCase
from base.models import User, Post
from base.forms import MyUserCreationForm

class UserModelTest(TestCase):
    def setUp(self):
        # Set up a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_user_creation(self):
        # Check if the user is created successfully
        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.name, 'Test User')

    def test_user_str_method(self):
        # Test the __str__ method of the user model
        self.assertEqual(str(self.user), 'test@example.com')




class UserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = MyUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'email': '',
            'name': 'Test User',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = MyUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Email is required, so this should fail




class PostTest(TestCase):
    def setUp(self):
        # Set up a user for testing
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test User'
        )

        self.post = Post.objects.create(
            heading = "Test Heading",
            content = "test test test",
            author = self.user
        )

    def test_post_creation(self):
        post = Post.objects.get(heading = "Test Heading")
        self.assertEqual(post.content, "test test test")
        self.assertEqual(post.author, self.user)

    def test_post_str_method(self):
        # Test the __str__ method of the Post model
        self.assertEqual(str(self.post), "Test Heading")

    
