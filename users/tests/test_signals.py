from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from users.models import Profile

class TestCreateProfileSignal(TestCase):
    def test_profile_creation_and_email(self):
        # Creează un utilizator
        user = User.objects.create_user(
            username='testuser',
            email='adamion03@gmail.com',
            first_name='Test',
            password='testpassword123'
        )

        # Verifică dacă profilul a fost creat
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.email, user.email)

        # Verifică dacă un email a fost trimis
        self.assertEqual(len(mail.outbox), 1)  # Trebuie să existe un singur email trimis

        # Verificăm conținutul emailului trimis
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'welcom to devsearch ')
        self.assertEqual(email.body, 'we are glad you are here!')
        self.assertEqual(email.to, [user.email])
