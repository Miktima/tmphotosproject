from django.test import TestCase
from managephotos.forms import KeywordsForm, KeywordsEditForm, PhotoEditForm
import random
import string

class ManagephotosFormTests(TestCase):
    
    def setUp(self):
        random.seed()

    def test_keywords_add_form(self):
        testString = ""
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters + string.digits + 
                        string.punctuation, k=7)
            testString += "".join(random_text)
            if k < 6:
                testString += ", "
        form = KeywordsForm(data={'keywords_bulk': testString})
        print("before: ", testString)
        self.assertTrue(form.is_valid())
        self.assertRegex(form.cleaned_data["keywords_bulk"], '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]')
        print("after: ", form.cleaned_data["keywords_bulk"])

    def test_keywords_edit_form(self):
        testString = ""
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters + string.digits + 
                        string.punctuation, k=7)
            testString += "".join(random_text)
            if k < 6:
                testString += ", "
        form = KeywordsEditForm(data={'keywords_bulk': testString})
        print("before: ", testString)
        self.assertTrue(form.is_valid())
        self.assertRegex(form.cleaned_data["keywords_bulk"], '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]')
        print("after: ", form.cleaned_data["keywords_bulk"])

    def test_photoEditForm_template(self):
        form = PhotoEditForm()
        print(form.default_renderer)
