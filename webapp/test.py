from django.test import TestCase
from django.urls import reverse
from .models import Bitacora
from django.contrib.auth.models import User

class BitacoraMiddlewareTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='Hola123-')
        self.client.login(username='admin', password='Hola123-')

    def test_bitacora_creates_entry(self):
        response = self.client.get(reverse('index'))  # 'some_view' debe ser una vista existente en tu aplicación
        self.assertEqual(response.status_code, 200)
        print("Checking if Bitacora entry was created...")
        self.assertEqual(Bitacora.objects.count(), 1)
        bitacora_entry = Bitacora.objects.first()
        self.assertEqual(bitacora_entry.user.username, 'admin')
