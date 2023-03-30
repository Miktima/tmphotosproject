from django.test import TestCase
from managephotos.forms import KeywordsForm, KeywordsEditForm, KeywordsCheckboxSelectMultiple
import random
import string

class ManagephotosFormTests(TestCase):
    
    def setUp(self):
        random.seed()
        string_list = []
        for i in range(0, 10):
            s = ""
            for k in range(0, 7):
                random_text = random.choices(string.ascii_letters + string.digits + 
                        string.punctuation, k=7)
                s += random_text
                if k < 6:
                    s += ", "
            string_list.append(s)

    def test_keywords_add_form(self):
        form = KeywordsForm




