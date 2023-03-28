from django.test import TestCase
from .models import Genre, Keywords, Photo
from pathlib import Path
from django.core.files import File

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
    
    def test_add_photos(self):
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
        # Проверяем значение по умолчанию
        self.assertEqual(3, p.star)
        # Проверяем title
        self.assertEqual("This is a title", p.title)
        # Максимальное добавление полей
        g_nature = Genre.objects.get(genre="Nature")
        g_other = Genre.objects.get(genre="Other")
        k1 = Keywords.objects.create(keyword="first")
        k2 = Keywords.objects.create(keyword="second")
        pp = Photo.objects.create(
            
        )

