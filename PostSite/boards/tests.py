from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from .models import Board
from .views import home,board_topics

# Create your tests here.




class HomeTest(TestCase):
    #Testing the status code of the response
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    #Test if Django will return the correct view function for the requested URL
    def test_home_url_resolves_home_view(self):
        try:
            view = resolve('/')
            self.assertEquals(view.func,home)
        except Resolver404:
            self.fail("Couldn't not resolve URL")

#The test_board_topics_view_success_status_code method: is testing if Django is returning a status code 200 (success) for an existing Board.
#The test_board_topics_view_not_found_status_code method: is testing if Django is returning a status code 404 (page not found) 
#for a Board that doesn’t exist in the database.
#The test_board_topics_url_resolves_board_topics_view method: is testing if Django is using the correct view function to render the topics.

class BoardTopicsTest(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description ='Django board.')
    def test_board_topics_views_success_status_code(self):
        url =reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
    def test_board_topics_views_not_found_status_code(self):
        url =reverse('board_topics', kwargs={'pk':99})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)
    #This test failed, instead of the visitor seeing a 505 internal error we adjust the board_topics view to display a 404 page
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func,board_topics)

