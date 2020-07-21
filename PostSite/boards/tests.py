from django.urls import reverse
from django.test import TestCase
from django.urls import resolve

from .views import home

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