from django.test import TestCase
from managephotos.models import Genre, Keywords, Photo, Pubstars
from django.db.models import Avg
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
                url = "Friendly-URL-" + str(i) + "-" + intitle + "-photo-DSC_0503.jpg",
                url_min = "Friendly-URL-" + str(i) + "-" + intitle + "-tmb-DSC_0503_tn.jpg",
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
        # test for 404 error
        photo_rnd = Photo.objects.order_by('?').first()
        revurl = reverse('url_image', kwargs={'url_image': photo_rnd.url})
        # remove center letter
        revurl = revurl[:int(len(revurl)/2)] + revurl[int(len(revurl)/2)+1:]
        # check response
        response = self.client.get(revurl)
        self.assertEqual(response.status_code, 404)

    def test_image_tmb_url(self):
        # test friendly urls of thumbnails
        photo_ins = Photo.objects.order_by('pk').all()
        for p in photo_ins:
            response = self.client.get(reverse('image_tmb_url', 
                        kwargs={'url_tmb': p.url_min}))
            # test status code
            self.assertEqual(response.status_code, 200)
        # test for 404 error
        photo_rnd = Photo.objects.order_by('?').first()
        revurl = reverse('image_tmb_url', kwargs={'url_tmb': photo_rnd.url_min})
        # remove center letter
        revurl = revurl[:int(len(revurl)/2)] + revurl[int(len(revurl)/2)+1:]
        # check response
        response = self.client.get(revurl)
        self.assertEqual(response.status_code, 404)

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
        # test for 404 error
        # pure genre
        genre_rnd = Genre.objects.order_by('?').first()
        link_genre = genre_rnd.genre.lower()
        link_genre = link_genre.replace(' ', '-')
        # remove center letter
        url404 = link_genre[:int(len(link_genre)/2)] + link_genre[int(len(link_genre)/2)+1:]
        # check response
        response = self.client.get(url404)
        self.assertEqual(response.status_code, 404)
        # genre with image
        photo_rnd = Photo.objects.order_by('?').first()
        url404i = reverse('genre_image', kwargs={'genre': link_genre, 'image': photo_rnd.url})
        url404i = link_genre[:int(len(url404i)/2)] + link_genre[int(len(url404i)/2)+1:]
        response = self.client.get(url404i)
        self.assertEqual(response.status_code, 404)

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
    
    def test_stars(self):
        # test internal and public stars
        photo_rnd = Photo.objects.order_by('?').first()
        genre_ins = photo_rnd.genre.first()
        pkphoto = photo_rnd.pk
        link_genre = genre_ins.genre.lower()
        link_genre = link_genre.replace(' ', '-')
        # internal stars
        url = reverse('genre_image', kwargs={'genre': link_genre, 'image': photo_rnd.url})
        int_stars = photo_rnd.star
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        photo = response.context["photo"]
        n1 = (photo["stars"]).count(1)
        self.assertEqual(n1, int_stars)
        # 5 public stars
        for i in range(5):
            # add public star
            rnd_star = random.randrange(1, 5)
            payload = str(pkphoto) + "__" + str(rnd_star)
            response = self.client.post('/save_star.html', {'star': payload})
            self.assertEqual(response.status_code, 200)
            # get image
            url = reverse('genre_image', kwargs={'genre': link_genre, 'image': photo_rnd.url})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)           
            # check internal stars and public star
            photo = response.context["photo"]
            n1 = (photo["stars"]).count(1)
            n0 = (photo["stars"]).count(0)
            # Среднее по публичному голосованию, если результатов нет, то возвращаем, то, что присвоено фотографии
            avgPubstars = Pubstars.objects.filter(photoid=photo_rnd.pk).aggregate(Avg("star", default=photo_rnd.star))
            avgStars = (avgPubstars['star__avg'] + photo_rnd.star)/2
            if n0 > 0:
                self.assertLess(n1, avgStars)
            else:
                self.assertEqual(n1, avgStars)
            self.assertGreater(n1+1, avgStars)
