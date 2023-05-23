from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import Client, TestCase

from notes.forms import WARNING
from notes.models import Note

from pytils.translit import slugify

User = get_user_model()


class TestNotesCreation(TestCase):
    SLUG_TEXT = 'SlagoviySlug'
    NOTE_TEXT = 'Текстовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Зеленый')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.url = reverse('notes:add')
        cls.url_done = reverse('notes:success')
        cls.form_data = {
            'title': 'Заголовок',
            'text': cls.NOTE_TEXT,
            'slug': cls.SLUG_TEXT,
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_notes(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_done)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.slug, self.SLUG_TEXT)
        self.assertEqual(note.author, self.author)

    def test_slug_transit(self):
        no_slug_data = {
            'title': 'ЗаголовокТранслит',
            'text': 'text',
            'slug': '',
        }
        self.auth_client.post(self.url, data=no_slug_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        new_note = Note.objects.get()
        expected_slug = slugify(new_note.title)
        self.assertEqual(new_note.slug, expected_slug)


class TestNoteEditDelete(TestCase):
    TITLE = 'Заголовок'
    TEXT = 'Текст'
    SLUG_TEXT = 'Slug'
    NEW_TITLE = 'Заголовочный заголовок'
    NEW_TEXT = 'Текстовый текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Зеленый')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            slug=cls.SLUG_TEXT,
            author=cls.author,
        )
        note_slug = cls.note.slug
        cls.url = reverse('notes:add')
        cls.success_url = reverse('notes:success')
        cls.edit_url = reverse('notes:edit', args=(note_slug,))
        cls.delete_url = reverse('notes:delete', args=(note_slug,))
        cls.author2 = User.objects.create(username='Синий')
        cls.auth2_client = Client()
        cls.auth2_client.force_login(cls.author2)
        cls.form_data = {
            'title': cls.TITLE,
            'text': cls.TEXT,
            'slug': cls.SLUG_TEXT,
        }
        cls.edit_form_data = {
            'title': cls.NEW_TITLE,
            'text': cls.NEW_TEXT,
            'slug': cls.SLUG_TEXT,
        }

    def test_unique_slug(self):
        bad_data = {
            'title': self.TITLE,
            'text': self.TEXT,
            'slug': self.SLUG_TEXT,
        }
        response = self.auth_client.post(self.url, data=bad_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=(self.note.slug + WARNING),
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_delete_notes(self):
        response = self.auth_client.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.auth2_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.auth_client.post(
            self.edit_url, data=self.edit_form_data
        )
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_TITLE)
        self.assertEqual(self.note.text, self.NEW_TEXT)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.auth2_client.post(
            self.edit_url, data=self.edit_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.TITLE)
        self.assertEqual(self.note.text, self.TEXT)
