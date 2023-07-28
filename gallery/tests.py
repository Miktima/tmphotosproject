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
        # test home page
        response = self.client.get(reverse('home'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'gallery/index.html')

    def test_image_url(self):
        # test friendly urls of hires images
        photo_ins = Photo.objects.order_by('pk').all()
        for p in photo_ins:
            response = self.client.get(reverse('url_image', 
                        kwargs={'url_image': p.url}))
            # test status code
            self.assertEqual(response.status_code, 200)

    def test_image_tmb_url(self):
        # test friendly urls of thumbnails
        photo_ins = Photo.objects.order_by('pk').all()
        for p in photo_ins:
            response = self.client.get(reverse('image_tmb_url', 
                        kwargs={'url_tmb': p.url_min}))
            # test status code
            self.assertEqual(response.status_code, 200)

    def test_stocks_page(self):
        # test stocks page
        response = self.client.get(reverse('stocks'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'gallery/stocks.html')

    def test_genre_image(self):
        # test genre page with a hires image
        genre_ins = Genre.objects.order_by('pk').all()
        photo_ins = Photo.objects.order_by('pk').all()
        for g in genre_ins:
            # reduce genre to the slag type
            link_genre = g.genre.lower()
            link_genre = link_genre.replace(' ', '-')
            for p in photo_ins:
                # test for every images and genres
                response = self.client.get(reverse('genre_image', 
                        kwargs={'genre': link_genre, 'image': p.url}))
                # test status code
                self.assertEqual(response.status_code, 200)

    def test_genre(self):
        # test genre page with a hires image
        genre_ins = Genre.objects.order_by('pk').all()
        for g in genre_ins:
            # reduce genre to the slag type
            link_genre = g.genre.lower()
            link_genre = link_genre.replace(' ', '-')
            # test for every genres
            response = self.client.get(reverse('genre_content', 
                                    kwargs={'genre': link_genre}))
            # test status code
            self.assertEqual(response.status_code, 200)
            if 'is_paginated' in response.context:
            # Pagination is set to 9 photos
                self.assertEqual(len(response.context['page_obj']), 9)
                resp2 = self.client.get(reverse('genre_content')+'?page=2')
                self.assertEqual(resp2.status_code, 200)
                self.assertTrue('is_paginated' in resp2.context)
                self.assertTrue(resp2.context['is_paginated'] == True)
                # must be 2 photos or more
                self.assertGreaterEqual(len(response.context['page_obj']), 2)
