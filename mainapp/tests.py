from django.test import TestCase
from django.urls import reverse
from django import setup
import os
from .sis_data import get_depts

# Create your tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
setup()

class LandingPageTestCase(TestCase):
  
    def test_correct_home_page(self):
      
        response = self.client.post(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor-link/landing_page.html')

    def test_dept_list_pulled_correctly(self):
      
        depts = get_depts("https://tutor-link.herokuapp.com/api/")
        
        self.assertGreater(len(depts), 0)
        self.assertTrue("APMA" in depts)
        self.assertTrue("PHYS" in depts)


