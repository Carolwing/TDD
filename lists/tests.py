from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

from lists.views import home_page # (2)

class HomePageTest(TestCase):

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    
    def test_uses_home_template(self):
        # request = HttpRequest() # 1
        # response = home_page(request) # 2

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        # html = response.content.decode('utf8') # 3
        # self.assertTrue(html.startswith('<html>')) # 4
        # self.assertIn('<title>To-Do lists</title>', html) # 5
        # self.assertTrue(html.strip().endswith('</html>')) # 4
        # expected_html = render_to_string('home.html')
        # self.assertEqual(html, expected_html)
        # self.assertTemplateUsed(response, 'home.html')

#class SmokeTest(TestCase):
    
    # def test_bad_maths(self):
       # self.assertEqual(1+1, 3)

class ListAndItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
     
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
 
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
  
        response = self.client.get('/lists/the-only-list-in-the-world/')
  
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
  
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
       
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text':'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

# Create your tests here.