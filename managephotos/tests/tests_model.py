from django.test import TestCase
from managephotos.models import Genre, Keywords, Photo
import os
from django.core.files import File
from datetime import date

class ManagephotosModelTests(TestCase):

    def setUp(self):
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
    
    def test_add_min_photos(self):
        # Минимальное добавление полей
        g_landscape = Genre.objects.get(genre="Landscape")
        k = Keywords.objects.create(keyword="keyword")
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        p = Photo.objects.create(
            src = image,
            src_min = image_tn,
            title = "This is a title"
        )
        p.genre.add(g_landscape)
        p.keywords.add(k)
        # Проверяем наличие добавленных значений при соотношении many-to-many
        self.assertIn("Landscape", p.genre.values_list('genre', flat=True))
        self.assertIn("keyword", p.keywords.values_list('keyword', flat=True))
        # Проверяем название файлов
        self.assertIn("DSC_0503", p.src.url)
        self.assertIn("DSC_0503_tn", p.src_min.url)
        # Проверяем, что путь соответствует дате
        td = date.today()
        upload_path = "photo/" + td.strftime("%Y/%m/%d/")
        self.assertIn(upload_path, p.src.url)
        self.assertIn(upload_path, p.src_min.url)
        # Проверяем значение по умолчанию
        self.assertEqual(3, p.star)
        # Проверяем title
        self.assertEqual("This is a title", p.title)

    def test_add_max_photos(self):
        # Максимальное добавление полей
        f = open("test_files/DSC_0503.jpg", 'rb')
        image = File(f)
        f_tn = open("test_files/DSC_0503_tn.jpg", 'rb')
        image_tn = File(f_tn)
        g_nature = Genre.objects.get(genre="Nature")
        g_other = Genre.objects.get(genre="Other")
        k1 = Keywords.objects.create(keyword="first")
        k2 = Keywords.objects.create(keyword="second")
        pp = Photo.objects.create(
            src = image,
            src_min = image_tn,
            url = "Friendly-URL-of-the-photo-test-files-DSC_0503.jpg",
            url_min = "Friendly-URL-of-the-thumbnail-test-files-DSC_0503.jpg",
            title = "Title with question? and!",
            star = 1,
            place = "Place of the photo"            
        )
        pp.genre.add(g_nature, g_other)
        pp.keywords.add(k1, k2)
        # Проверяем наличие добавленных значений при соотношении many-to-many
        self.assertIn("Nature", pp.genre.values_list('genre', flat=True))
        self.assertIn("Other", pp.genre.values_list('genre', flat=True))
        self.assertIn("first", pp.keywords.values_list('keyword', flat=True))
        self.assertIn("second", pp.keywords.values_list('keyword', flat=True))
        # Проверяем название файлов
        self.assertIn("DSC_0503", pp.src.url)
        self.assertIn("DSC_0503_tn", pp.src_min.url)
        # Проверяем, что путь соответствует дате
        td = date.today()
        upload_path = "photo/" + td.strftime("%Y/%m/%d/")
        self.assertIn(upload_path, pp.src.url)
        self.assertIn(upload_path, pp.src_min.url)
        # Проверяем значение star
        self.assertEqual(1, pp.star)
        # Проверяем title и place
        self.assertEqual("Title with question? and!", pp.title)
        self.assertEqual("Place of the photo", pp.place)
        # Проверяем friendly urls
        self.assertEqual("Friendly-URL-of-the-photo-test-files-DSC_0503.jpg", pp.url)
        self.assertEqual("Friendly-URL-of-the-thumbnail-test-files-DSC_0503.jpg", pp.url_min)
        # Удаление Записи в Photo
        # начальное число записей
        n_genre = Genre.objects.count()
        n_keywords = Keywords.objects.count()
        n_photos = Photo.objects.count()
        self.assertGreater(n_photos, 0)
        # Удаляем файлы
        for ph in Photo.objects.all(): 
            os.remove(ph.src.path)
            os.remove(ph.src_min.path)
        # Удаляем все записи в Photo
        photos = Photo.objects.all()
        photos.delete()
        # Число записей после удаление (должно обнулиться только в Photo)
        self.assertEqual(Photo.objects.count(), 0)
        self.assertEqual(Keywords.objects.count(), n_keywords)
        self.assertEqual(Genre.objects.count(), n_genre)





