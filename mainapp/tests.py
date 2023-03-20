from django.test import TestCase
from django.urls import reverse
from django import setup
import os
#from .sis_data import get_depts


# Create tests here.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
setup()

class LandingPageTestCase(TestCase):
  
    def test_correct_home_page(self):
      
        response = self.client.post(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/landing_page.html')

    def test_dept_list_pulled_correctly(self):
      
        depts = self.client.post(reverse('department_list'))
        
        self.assertGreater(len(depts.context["mnemonics"]), 0)
        self.assertTrue("APMA" in depts.context["mnemonics"])
        self.assertTrue("PHYS" in depts.context["mnemonics"])
