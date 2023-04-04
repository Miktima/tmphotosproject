from django.test import TestCase
from managephotos.models import Genre, Keywords, Photo
from django.core.files import File
from django.urls import reverse
import random
import string

class ManagephotosIndexViewTests(TestCase):
    
    @classmethod
    def setUpTestData(cls):
    # Инициализируем жанры
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
            db = Genre.objects.create(genre=g)
        # Делаем 5 записей в таблицу Photo
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        random.seed()
        for i in range(0, 5):
            ngenre = random.randrange(1, len(genres)+1)        
            g_sel = Genre.objects.get(id=ngenre)
            random_text = random.choices(string.ascii_letters, k=7)
            k1 = Keywords.objects.create(keyword=random_text)
            random_text = random.choices(string.ascii_letters, k=7)
            k2 = Keywords.objects.create(keyword=random_text)
            rnd_star = random.randrange(1, 5)
            pp = Photo.objects.create(
                src = image,
                src_min = image_tn,
                url = "Friendly_URL_" + str(i) + "_photo/DSC_0503.jpg",
                url_min = "Friendly_URL_" + str(i) + "_thumbnail/DSC_0503.jpg",
                title = "Title with number " + str(i),
                star = rnd_star,
                place = "Place #" + + str(i)            
            )
            pp.genre.add(g_sel)
            pp.keywords.add(k1, k2)

    def test_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'managephotos/index.html')
        
