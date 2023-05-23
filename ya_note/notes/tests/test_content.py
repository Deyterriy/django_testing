from django.contrib.auth import get_user_model

from django.shortcuts import reverse
from django.test import TestCase

from notes.models import Note

User = get_user_model()


class TestNotesForm(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='',
            author=cls.author,
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.add_url = reverse('notes:add')
        cls.user = User.objects.create(username='AA')
        cls.note2 = Note.objects.create(
            title='Заголовок2',
            text='Текст2',
            slug='слаг',
            author=cls.user,
        )

    def test_note_in_context(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)
        self.assertNotIn(self.note2, object_list)

    def test_edit_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.edit_url)
        self.assertIn('form', response.context)

    def test_add_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)
