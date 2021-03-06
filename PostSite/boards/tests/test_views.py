from django.urls import reverse
from django.test import TestCase
from django.urls import resolve
from ..models import Board,Topic,Post
from ..views import home,board_topics,new_topic
from django.contrib.auth.models import User
from ..forms import NewTopicForm

# Create your tests here.



#Observe that now we added a setUp method for the HomeTests as well. 
# That’s because now we are going to need a Board instance and also we moved the url and response to the setUp, 
# so we can reuse the same response in the new test.
class HomeTest(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django',description='Django Board')
        url = reverse('home')
        self.response = self.client.get(url)

    #Testing the status code of the response
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code,200)

    #Test if Django will return the correct view function for the requested URL
    def test_home_url_resolves_home_view(self):
        try:
            view = resolve('/')
            self.assertEquals(view.func,home)
        except Resolver404:
            self.fail("Couldn't not resolve URL")

    #The new test here is the test_home_view_contains_link_to_topics_page.
    #  Here we are using the assertContains method to test if the response body contains a given text. 
    # The text we are using in the test, is the href part of an a tag. 
    # So basically we are testing if the response body has the text href="/boards/1/".
    #Changed the code in home.html from {{ board.name }} to <a href="{% url 'board_topics' board.pk %}">{{ board.name }}</a>
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url=reverse('board_topics',kwargs={'pk':self.board.pk})
        self.assertContains(self.response,'href="{0}"'.format(board_topics_url))

    


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

    def test_board_topics_view_contains_links_back_to_homepage(self):
        board_topics_url=reverse('board_topics',kwargs={'pk': 1})
        response=self.client.get(board_topics_url)
        homepage_url=reverse('home')
        self.assertContains(response,'href="{0}"'.format(homepage_url))


    #Test user new topic page
    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url=reverse('board_topics',kwargs={'pk':1})
        homepage_url=reverse('home')
        new_topic_url=reverse('new_topic',kwargs={'pk':1})

        response=self.client.get(board_topics_url)
        self.assertContains(response,'href="{0}'.format(homepage_url))
        self.assertContains(response,'href="{0}'.format(new_topic_url))


#setUp: creates a Board instance to be used during the tests
#test_new_topic_view_success_status_code: check if the request to the view is successful
#test_new_topic_view_not_found_status_code: check if the view is raising a 404 error when the Board does not exist
#test_new_topic_url_resolves_new_topic_view: check if the right view is being used
#test_new_topic_view_contains_link_back_to_board_topics_view: ensure the navigation back to the list of topics
class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        #Added for the new topic view
        User.objects.create_user(username='John',email='john@gmail.com',password='1234')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func,new_topic)

    def test_new_topic_view_contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
    #New Test for New Topic Page:

    #Up: included the User.objects.create_user to create a User instance to be used in the tests
    #test_csrf: since the CSRF Token is a fundamental part of processing POST requests, we have to make sure our HTML contains the token.
    #test_new_topic_valid_post_data: sends a valid combination of data and check if the view created a Topic instance and a Post instance.
    #test_new_topic_invalid_post_data: here we are sending an empty dictionary to check how the application is behaving.
    #test_new_topic_invalid_post_data_empty_fields: similar to the previous test, but this time we are sending some data. 
    #The application is expected to validate and reject empty subject and message
    def test_crf(self):
        url=reverse('new_topic',kwargs={'pk':1})
        response=self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())


    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)
    
    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())



    def test_contains_form(self):  # <- new test
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)



