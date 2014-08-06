from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from utils import create_deck
from models import Card, Player
from django.test import TestCase
from forms import EmailUserCreationForm
from test_utils import run_pyflakes_for_package, run_pep8_for_package

__author__ = 'TTruong'


class BasicMathTestCase(TestCase):
    def test_math(self):
        a = 1
        b = 1
        self.assertEqual(a + b, 2)

        # def test_failing_case(self):
        # a = 1
        #     b = 1
        #     self.assertEqual(a+b, 1)


class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)


# class ModelTestCase(TestCase):
#     def test_get_ranking(self):
#         """Test that we get the proper ranking for a card"""
#         card = Card.objects.create(suit=Card.CLUB, rank="jack")
#         self.assertEqual(card.get_ranking(), 11)


class ModelTestCase(TestCase):
    def setUp(self):
        self.card = Card.objects.create(suit=Card.CLUB, rank="jack")

    def test_get_ranking(self):
        """Test that we get the proper ranking for a card"""
        self.assertEqual(self.card.get_ranking(), 11)


class ResultTestCase(TestCase):

    def test_get_war_result_greater(self):
        """Test dealer and user card"""
        first_card = Card.objects.create(suit=Card.DIAMOND, rank='five')
        second_card = Card.objects.create(suit=Card.DIAMOND, rank='four')
        self.assertEqual(first_card.get_war_result(second_card), 1)

    def test_get_war_result_equal(self):
        """Test dealer and user card"""
        first_card = Card.objects.create(suit=Card.DIAMOND, rank='five')
        second_card = Card.objects.create(suit=Card.DIAMOND, rank='five')
        self.assertEqual(first_card.get_war_result(second_card), 0)

    def test_get_war_result_less(self):
        """Test dealer and user card"""
        first_card = Card.objects.create(suit=Card.DIAMOND, rank='four')
        second_card = Card.objects.create(suit=Card.DIAMOND, rank='five')
        self.assertEqual(first_card.get_war_result(second_card), -1)


class FormTestCase(TestCase):
    def test_clean_username_exception(self):
        Player.objects.create_user(username='test-user')

        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}

        with self.assertRaises(ValidationError):
            form.clean_username()

    def test_clean_username(self):

        form = EmailUserCreationForm()
        form.cleaned_data = {'username': 'test-user'}
        self.assertEquals(form.clean_username(), 'test-user')

#
# class ViewTestCase(TestCase):
#     def setUp(self):
#         create_deck()
#
#     def test_home_page(self):
#         response = self.client.get(reverse('home'))
#         self.assertIn('<p>Suit: spade, Rank: two</p>', response.content)
#         self.assertEqual(response.context['cards'].count(), 52)


class ViewTestCase(TestCase):
          def setUp(self):
              create_deck()
    
          def test_faq_page(self):
              response = self.client.get(reverse('faq'))
              self.assertIn('<p>Q: Can I win real money on this website?</p>', response.content)

          def test_filters_page(self):
                response = self.client.get(reverse('filters'))
                self.assertIn('52', response.content)
                self.assertEqual(response.context['cards'].count(), 52)

# class ViewTestCase(TestCase):
#
#     def test_register_page(self):
#         username = 'new-user'
#         data = {
#             'username': username,
#             'email': 'test@test.com',
#             'password1': 'test',
#             'password2': 'test'
#         }
#         response = self.client.post(reverse('register'), data)
#
#         # Check this user was created in the database
#         self.assertTrue(Player.objects.filter(username=username).exists())
#
#         # Check it's a redirect to the profile page
#         self.assertIsInstance(response, HttpResponseRedirect)
#         self.assertTrue(response.get('location').endswith(reverse('profile')))
#
#
#     def create_war_game(self, user, result=WarGame.LOSS):
#         WarGame.objects.create(result=result, player=user)

    #
    # def test_profile_page(self):
    #     # Create user and log them in
    #     password = 'passsword'
    #     user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
    #     self.client.login(username=user.username, password=password)
    #
    #     # Set up some war game entries
    #     self.create_war_game(user)
    #     self.create_war_game(user, WarGame.WIN)
    #
    #     # Make the url call and check the html and games queryset length
    #     response = self.client.get(reverse('profile'))
    #     self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
    #     self.assertEqual(len(response.context['games']), 2)


class SyntaxTest(TestCase):
    def test_syntax(self):
        """
        Run pyflakes/pep8 across the code base to check for potential errors.
        """
        packages = ['cards']
        warnings = []
        # Eventually should use flake8 instead so we can ignore specific lines via a comment
        for package in packages:
            warnings.extend(run_pyflakes_for_package(package, extra_ignore=("_settings",)))
            warnings.extend(run_pep8_for_package(package, extra_ignore=("_settings",)))
        if warnings:
            self.fail("{0} Syntax warnings!\n\n{1}".format(len(warnings), "\n".join(warnings)))