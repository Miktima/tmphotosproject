from django.test import TestCase
from managephotos.forms import KeywordsForm, KeywordsEditForm, PhotoEditForm, KeywordsCheckboxSelectMultiple
from managephotos.models import Genre, Keywords, Photo
import random
import string
from django.core.files import File

class ManagephotosFormTests(TestCase):
    
    def setUp(self):
        random.seed()

    def test_keywords_add_form(self):
        # Проверка удаления символов в форме KeywordsForm
        testString = ""
        # Заполняем строку символами, включая специальные символы
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters + string.digits + 
                        string.punctuation, k=7)
            testString += "".join(random_text)
            if k < 6:
                testString += ", "
        form = KeywordsForm(data={'keywords_bulk': testString})
        # Проверяем, что форма валидная
        self.assertTrue(form.is_valid())
        # Проверяем, что специальных символов кроме , и & нет
        self.assertRegex(form.cleaned_data["keywords_bulk"], '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]')

    def test_keywords_edit_form(self):
        # Проверка удаления символов в форме KeywordsEditForm
        testString = ""
        # Заполняем строку символами, включая специальные символы
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters + string.digits + 
                        string.punctuation, k=7)
            testString += "".join(random_text)
            if k < 6:
                testString += ", "
        form = KeywordsEditForm(data={'keywords_bulk': testString})
        # Проверяем, что форма валидная
        self.assertTrue(form.is_valid())
        # Проверяем, что специальных символов кроме , и & нет
        self.assertRegex(form.cleaned_data["keywords_bulk"], '[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]')

    def test_photoEditForm_template(self):
        # Заполняем таблицу жанров
        genres = [
            "Landscape",
            "Nature",
            "Water",
            "Still life",
            "Minimalism",
            "Abstraction",
            "Architecture",
            "Other"
        ]
        for g in genres:
            Genre.objects.create(genre=g)
        # Заполняем таблицу ключевых слов
        keywords_list = [
            "one",
            "two",
            "three",
            "four",
            "five"
        ]
        for kw in keywords_list:
            Keywords.objects.create(keyword=kw)
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_abstraction = Genre.objects.get(genre="Abstraction")
        k1 = Keywords.objects.get(keyword="one")
        k2 = Keywords.objects.get(keyword="two")
        pp = Photo.objects.create(
            src = image,
            src_min = image_tn,
            title = "Title test",
        )
        pp.genre.add(g_abstraction)
        pp.keywords.add(k1, k2)
        form = PhotoEditForm(instance=pp)
        # Жанры в форме должны быть выбранные и не выбранные
        self.assertIn("Landscape</option>", form.as_table())
        self.assertIn("Nature</option>", form.as_table())
        self.assertIn("selected>Abstraction</option>", form.as_table())
        # Ключевые слова должны быть только зачеканные
        self.assertIn("id_keywords_0", form.as_table()) 
        self.assertIn("id_keywords_1", form.as_table())
        self.assertNotIn("id_keywords_2", form.as_table()) 
        self.assertNotIn("id_keywords_3", form.as_table()) 
        self.assertNotIn("id_keywords_4", form.as_table()) 
 
