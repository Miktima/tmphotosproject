from django.test import TestCase, RequestFactory
from managephotos.models import Genre, Keywords, Photo
from django.core.files import File
from django.urls import reverse
import random
import string
import random
import os
from django.contrib.auth.models import User
from managephotos.MpClass import MpClass
from managephotos.views import add_photo, edit_photo

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
        self.test_user = User.objects.create_user(username='testuser', password='1X!ISRUkw+tuK')
        self.test_user.save()
        # добавление полей
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_nature = Genre.objects.get(genre="Nature")
        g_other = Genre.objects.get(genre="Other")
        test_photo = Photo.objects.create(
            src = image,
            src_min = image_tn,
            title = "This is a title",
            star = 2,
            place = "Place of the photo"            
        )
        test_photo.genre.add(g_nature, g_other)
        random.seed()

    def test_guest_redirect(self):
        # test redirect for unlogged user
        response = self.client.get(reverse('add_photo'))
        self.assertRedirects(response, 
                             '/managephotos/accounts/login/?next=/managephotos/add_photo/')

    def test_login_get(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('add_photo'))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'managephotos/upload_photo.html')

    def test_login_post(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.post(reverse('add_photo'))
        # test status code
        self.assertEqual(response.status_code, 200)

    def test_friendly_urls(self):
        # Проверка создания ЧПУ     
		# Получаем последнее записанное значение
        photo_row = Photo.objects.last()
        mptool = MpClass()
		# Создаем ЧПУ для фото и эскиза
        f_url = mptool.convertUrl(str(photo_row.src.url), str(photo_row.title))
        f_url_min = mptool.convertUrl(str(photo_row.src_min.url), str(photo_row.title))
        self.assertRegex(f_url, "^This_is_a_title_DSC_0503\w*.jpg$")
        self.assertRegex(f_url_min, "^This_is_a_title_DSC_0503_tn\w*.jpg$")
        test_list = []
        # Заполняем список для формирования заголовка
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters, k=7)
            testString = "".join(random_text)
            test_list.append(testString)
        f_url = mptool.convertUrl(str(photo_row.src.url), " ".join(test_list))
        f_url_min = mptool.convertUrl(str(photo_row.src_min.url), " ".join(test_list))
        result_str = test_list[0] + "_" + test_list[1] + "_" + test_list[2] + "_"
        for i in test_list:
            print(i)
        self.assertRegex(f_url, "^" + result_str + "DSC_0503\w*.jpg$")
        self.assertRegex(f_url_min, "^" + result_str + "DSC_0503_tn\w*.jpg", f_url_min)        
        # Заполняем список для формирования заголовка с артиклями
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters, k=7)
            testString = "".join(random_text)
            test_list.append(testString)
        f_url = mptool.convertUrl(str(photo_row.src.url), "The " + " ".join(test_list))
        f_url_min = mptool.convertUrl(str(photo_row.src_min.url), "A " + " ".join(test_list))
        result_str = test_list[0] + "_" + test_list[1] + "_" + test_list[2] + "_"
        self.assertRegex(f_url, "^" + result_str + "DSC_0503\w*.jpg$")
        self.assertRegex(f_url_min, "^" + result_str + "DSC_0503_tn\w*.jpg", f_url_min)        

    def test_keywords_parsing(self):
        # Проверка разбора ключевых слов
        # Инстанс RequestFactory 
        factory = RequestFactory()
        # Заполняем двумя словами таблицу Keywords
        Keywords.objects.create(keyword = "one")
        Keywords.objects.create(keyword = "two")
        # Данные для записи в таблицу Photo
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_other = Genre.objects.get(genre="Other")
        kw_list = []
        # Заполняем список ключевых слов
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters, k=7)
            kwString = "".join(random_text)
            kw_list.append(kwString)
        data = {
            "src": image, 
            "src_min" : image_tn, 
            "title": "The title", 
            "star": 4, 
            "place": "Place of the photo",
            "genre": g_other.pk,
            "keywords_bulk": ", ".join(kw_list) + ", one"
            }
        request = factory.post(reverse('add_photo'), data=data)
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.        
        request.user = self.test_user
        response = add_photo(request)
        # You need to add a client to the response object
        response.client = self.client
        # Устанавливаем fetch_redirect_response=False, так как 
        # не авторизованного пользователя редиректит дальше
        self.assertRedirects(response, '/managephotos/', fetch_redirect_response=False)
        # Проверяем, что в таблице Keywords и Photo записаны все ключевые слова
        for kw in kw_list:
            n = Keywords.objects.filter(keyword=kw).count()
            m = Photo.objects.filter(keywords__keyword = kw).count()
            self.assertEqual(n, 1)
            self.assertEqual(m, 1)
        # Проверяем, что one есть в Photo
        m = Photo.objects.filter(keywords__keyword = "one").count()
        self.assertEqual(m, 1)
        # А слова two - нет
        m = Photo.objects.filter(keywords__keyword = "two").count()
        self.assertEqual(m, 0)

class ManagephotosEditPhotoViewTests(TestCase):
    
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
        self.test_user = User.objects.create_user(username='testuser', password='1X!ISRUkw+tuK')
        self.test_user.save()
        # добавление полей
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_landscape = Genre.objects.get(genre="Landscape")
        self.test_photo = Photo.objects.create(
            src = image,
            src_min = image_tn,
            title = "This is a title",
            star = 2,
            place = "Place of the photo"            
        )
        self.test_photo.genre.add(g_landscape)
        random.seed()

    def test_guest_redirect(self):
        # test redirect for unlogged user
        response = self.client.get(reverse('edit_photo',
                                   kwargs={'photo_id': self.test_photo.pk}))
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('edit_photo',
                                           kwargs={'photo_id': self.test_photo.pk}))
        # test status code
        self.assertEqual(response.status_code, 200)
        # test template
        self.assertTemplateUsed(response, 'managephotos/edit_photo.html')

    def test_login_get_404(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('edit_photo',
                                           kwargs={'photo_id': 999}))
        # test status code
        self.assertEqual(response.status_code, 404)

    def test_login_post(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.post(reverse('edit_photo',
                                            kwargs={'photo_id': self.test_photo.pk}))
        # test status code
        self.assertEqual(response.status_code, 200)

    def test_view_edit(self):
        # Проверка разбора ключевых слов
        # Инстанс RequestFactory 
        factory = RequestFactory()
        # Заполняем двумя словами таблицу Keywords
        Keywords.objects.create(keyword = "white")
        Keywords.objects.create(keyword = "black")
        # Данные для записи в таблицу Photo
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_other = Genre.objects.get(genre="Other")
        kw_list = []
        # Заполняем список ключевых слов
        for k in range(0, 7):
            random_text = random.choices(string.ascii_letters, k=7)
            kwString = "".join(random_text)
            kw_list.append(kwString)
        data = {
            "src_min" : image_tn, 
            "title": "The title in the edit view", 
            "star": 1, 
            "genre": g_other.pk,
            "keywords_bulk": ", ".join(kw_list) + ", white"
            }
        request = factory.post(reverse('edit_photo',
                                       kwargs={'photo_id': self.test_photo.pk}), data=data)
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.        
        request.user = self.test_user
        response = edit_photo(request, self.test_photo.pk)
        # You need to add a client to the response object
        response.client = self.client
        # Устанавливаем fetch_redirect_response=False, так как 
        # не авторизованного пользователя редиректит дальше
        self.assertRedirects(response, '/managephotos/', fetch_redirect_response=False)
        # Проверяем, что в таблице Keywords и Photo записаны все ключевые слова
        for kw in kw_list:
            n = Keywords.objects.filter(keyword=kw).count()
            m = Photo.objects.filter(keywords__keyword = kw).count()
            self.assertEqual(n, 1)
            self.assertEqual(m, 1)
        # Проверяем, что white есть в Photo
        m = Photo.objects.filter(keywords__keyword = "white").count()
        self.assertEqual(m, 1)
        # А слова black - нет
        m = Photo.objects.filter(keywords__keyword = "black").count()
        self.assertEqual(m, 0)

class ManagephotosRemovePhotoViewTests(TestCase):
    
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
        self.test_user = User.objects.create_user(username='testuser', password='1X!ISRUkw+tuK')
        self.test_user.save()
        # добавление полей
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_architecture = Genre.objects.get(genre="Architecture")
        self.test_photo = Photo.objects.create(
            src = image,
            src_min = image_tn,
            title = "This is a title of removing photo",
            star = 1,
        )
        self.test_photo.genre.add(g_architecture)
        random.seed()

    def test_guest_redirect(self):
        # test redirect for unlogged user
        response = self.client.get(reverse('remove_photo',
                                   kwargs={'photo_id': self.test_photo.pk}))
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        main_path = self.test_photo.src.path
        min_path = self.test_photo.src.path
        # Проверяем, что пути указывают на существующие файлы до удаления
        self.assertTrue(os.path.exists(main_path))
        self.assertTrue(os.path.exists(min_path))
        response = self.client.get(reverse('remove_photo',
                                           kwargs={'photo_id': self.test_photo.pk}))
        # test redirect
        self.assertRedirects(response, '/managephotos/')
        # Проверяем, что файлы удалены
        self.assertFalse(os.path.exists(main_path))
        self.assertFalse(os.path.exists(min_path))

    def test_login_get_404(self):
        # user login
        login = self.client.login(username='testuser', password='1X!ISRUkw+tuK')
        response = self.client.get(reverse('remove_photo',
                                           kwargs={'photo_id': 999}))
        # test status code
        self.assertEqual(response.status_code, 404)

