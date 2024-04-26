from django.test import TestCase, Client, LiveServerTestCase
from django.urls import reverse
import os
from .models import *
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile

#Web Driver
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

#Keys and By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):

        self.creator = Creator.objects.create(
            name="Test Man",
            email="TestEmail@test.com",
            user=User.objects.create(username="testuser")
        )

        self.test_video_content = b"fake video content"
        self.test_video_file = SimpleUploadedFile(
            "test_video.mp4",
            self.test_video_content,
            content_type = "video/mp4"
        )

        self.capsule = Capsule.objects.create(
            title="Capsule Title",
            is_primary=True,
            synopsis="Test Synopsis",
            video=self.test_video_file,
            education="Test Education",
            profession="Test Profession",
            fav_book="Test Book",
            fav_movie="Test Movie",
            fav_quote="Test Quote",
            creator=self.creator
        )

    def test_creator_creation(self):
        self.assertEqual(self.creator.name, "Test Man")
        self.assertEqual(self.creator.email, "TestEmail@test.com")
        self.assertEqual(self.creator.get_absolute_url(), "/creator/1")

    def test_capsule_creation(self):
        self.assertEqual(self.capsule.title, "Capsule Title")
        self.assertTrue(self.capsule.is_primary)
        self.assertEqual(self.capsule.synopsis, "Test Synopsis")
        self.assertEqual(os.path.basename(self.capsule.video.name), "test_video.mp4")
        self.assertEqual(self.capsule.video.size, len(b"fake video content"))
        self.assertEqual(self.capsule.education, "Test Education")
        self.assertEqual(self.capsule.profession, "Test Profession")
        self.assertEqual(self.capsule.fav_book, "Test Book")
        self.assertEqual(self.capsule.fav_movie, "Test Movie")
        self.assertEqual(self.capsule.fav_quote, "Test Quote")
        self.assertEqual(self.capsule.creator, self.creator)
        self.assertEqual(self.capsule.get_absolute_url(), "/capsules/1")

    def tearDown(self):
        self.capsule.video.delete()

class FormsTestCase(TestCase):

    def setUp(self):

        self.creator = Creator.objects.create(
            name="Test Man",
            email="TestEmail@test.com",
            user=User.objects.create(username="testuser")
        )

        self.test_video_content = b"fake video content"
        self.test_video_file = SimpleUploadedFile(
            "test_video.mp4",
            self.test_video_content,
            content_type = "video/mp4"
        )

        self.capsule = Capsule.objects.create(
            title="Capsule Title",
            is_primary=True,
            synopsis="Test Synopsis",
            video=self.test_video_file,
            education="Test Education",
            profession="Test Profession",
            fav_book="Test Book",
            fav_movie="Test Movie",
            fav_quote="Test Quote",
            creator=self.creator
        )
    
    def tearDown(self):
        self.capsule.video.delete()
    
    class CreatorForm(ModelForm):
        class Meta:
            model = Creator
            fields = '__all__'
            exclude = ('user',)

    def test_valid_creator_data(self):
        data = {'name': 'Test Man', 'email': 'Test@email.com'}
        form = CreatorForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_creator_data(self):
        data={}
        form = CreatorForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    class CapsuleForm(ModelForm):
        class Meta:
            model = Capsule
            fields = '__all__'
            exclude = ('creator',)

    def test_valid_capsule_data(self):
        data = {'title':  'Capsule Title'}
        form = CapsuleForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_capsule_data(self):
        data={}
        form = CapsuleForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)


class ViewsTestCase(TestCase):

    def setUp(self):

        self.creator = Creator.objects.create(
            name="Test Man",
            email="TestEmail@test.com",
            user=User.objects.create(username="testuser")
        )

        self.test_video_content = b"fake video content"
        self.test_video_file = SimpleUploadedFile(
            "test_video.mp4",
            self.test_video_content,
            content_type = "video/mp4"
        )

        self.capsule = Capsule.objects.create(
            title="Capsule Title",
            is_primary=True,
            synopsis="Test Synopsis",
            video=self.test_video_file,
            education="Test Education",
            profession="Test Profession",
            fav_book="Test Book",
            fav_movie="Test Movie",
            fav_quote="Test Quote",
            creator=self.creator
        )

    def tearDown(self):
        self.capsule.video.delete()

    def test_index_view_valid(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'capsule_app/index.html')

    def test_authentication_view_invalid(self):
        client = Client()
        response = client.get(reverse('create-capsule',args=[1]))
        self.assertEqual(response.status_code, 302)

class SeleniumTests(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):

        self.creator = Creator.objects.create(
            name="Test Man",
            email="TestEmail@test.com",
            user=User.objects.create(username="testuser")
        )

        self.test_video_content = b"fake video content"
        self.test_video_file = SimpleUploadedFile(
            "test_video.mp4",
            self.test_video_content,
            content_type = "video/mp4"
        )

        self.capsule = Capsule.objects.create(
            title="Capsule Title",
            is_primary=True,
            synopsis="Test Synopsis",
            video=self.test_video_file,
            education="Test Education",
            profession="Test Profession",
            fav_book="Test Book",
            fav_movie="Test Movie",
            fav_quote="Test Quote",
            creator=self.creator
        )
    
    def testHomePage(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/nav/div/div/ul/li[1]/a").click()

    def testCreators(self):
        self.browser.get(self.live_server_url)
        time.sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/nav/div/div/ul/li[2]/a").click()

    def testViewCreator(self):
        self.browser.get(self.live_server_url + reverse('creators'))
        time.sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/div/div/ul/div[1]/div/a").click()

    def testCreateNewCapsule(self):
        self.browser.get(self.live_server_url + reverse('creator-detail', args=[self.creator.id]))
        time.sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/div/div/a[2]").click()


    def tearDown(self):
        self.capsule.video.delete()
