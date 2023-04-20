from django.test import TestCase
from managephotos.models import Genre, Keywords, Photo
from django.core.files import File
from django.urls import reverse
import random
import string
from django.contrib.auth.models import User
from managephotos import views

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
                place = "Place #" + str(i)            
            )
            pp.genre.add(g_sel)
            pp.keywords.add(k1, k2)

    def setUp(self):
        # Add user
        test_user = User.objects.create_user(username='testuser', password='1X!ISRUkw+tuK')
        test_user.save()
        
    def test_guest_redirect(self):
        # test redirect for unlogged user
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/managephotos/accounts/login/?next=/managephotos/')

    def test_login(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('index'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'managephotos/index.html')
        
    def test_pagination_first(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('index'))
        # print (response.context)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # Pagination is set to 3 photos
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_pagination_second(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        # 5 photos is available, so 2 photos are on the second page
        self.assertEqual(len(response.context['page_obj']), 2)

class ManagephotosAddPhotoViewTests(TestCase):
    
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

    def setUp(self):
        # Add user
        test_user = User.objects.create_user(username='testuser', password='1X!ISRUkw+tuK')
        test_user.save()
        
    def test_guest_redirect(self):
        # test redirect for unlogged user
        response = self.client.get(reverse('add_photo'))
        self.assertRedirects(response, 
                             '/managephotos/accounts/login/?next=/managephotos/add_photo/')

    def test_login(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('add_photo'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'managephotos/upload_photo.html')

    def test_base_form(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')        
        f = open("test_files/DSC_0503.jpg", 'rb')
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        genre_instace = Genre.objects.get(genre = "Nature")
        response = self.client.post('/managephotos/add_photo/', {
            'src': f,
            'src_min': f_tn,
            'star': 2,
            'title': 'This is a title',
            'genre': genre_instace
        })
        # print("src: ", response.context['src'])
        # print("src_min: ", response.context['src_min'])
        # print("star: ", response.context['star'])
        # print("title: " , response.context['title'])
        # print("genre: " , response.context['genre'])
        # print("place: " , response.context['place'])
        # print("url: " , response.context['url'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, views.add_photo)
        print (response.json())
        

