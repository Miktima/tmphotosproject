from django.test import TestCase
from managephotos.models import Genre, Keywords, Photo
from django.core.files import File
import random
import string
from django.urls import reverse


class GalleryIndexViewTests(TestCase):
    
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
        # Делаем 15 записей в таблицу Photo, при этом 11 в один жанр, чтобы проверить пагинацию
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        # Получаем первый номер индекса
        first = Genre.objects.first()
        random.seed()
        ngenre = random.randrange(first.pk, first.pk + len(genres))
        for i in range(0, 15):
            if i > 10:
                ngenre = random.randrange(first.pk, first.pk + len(genres))   
            g_sel = Genre.objects.get(pk=ngenre)
            random_text = random.choices(string.ascii_letters, k=7)
            k1 = Keywords.objects.create(keyword=random_text)
            random_text = random.choices(string.ascii_letters, k=7)
            k2 = Keywords.objects.create(keyword=random_text)
            random_text = random.choices(string.ascii_letters, k=7)
            k3 = Keywords.objects.create(keyword=random_text)
            intitle = "".join(random.choices(string.ascii_letters, k=5))
            rnd_star = random.randrange(1, 5)
            pp = Photo.objects.create(
                src = image,
                src_min = image_tn,
                url = "Friendly_URL_" + str(i) + "_" + intitle + "_photo_DSC_0503.jpg",
                url_min = "Friendly_URL_" + str(i) + "_" + intitle + "_tmb_DSC_0503_tn.jpg",
                title = "Title with number " + str(i),
                star = rnd_star,
                place = "Place #" + str(i)            
            )
            pp.genre.add(g_sel)
            pp.keywords.add(k1, k2, k3)

    def test_home(self):
        response = self.client.get(reverse('home'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'gallery/index.html')
        
    # def test_pagination_first(self):
    #     response = self.client.get(reverse('index'))
    #     # print (response.context)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     # Pagination is set to 3 photos
    #     self.assertEqual(len(response.context['page_obj']), 3)

    # def test_pagination_second(self):
    #     response = self.client.get(reverse('index')+'?page=2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('is_paginated' in response.context)
    #     self.assertTrue(response.context['is_paginated'] == True)
    #     # 5 photos is available, so 2 photos are on the second page
    #     self.assertEqual(len(response.context['page_obj']), 2)

