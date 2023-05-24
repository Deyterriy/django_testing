from http import HTTPStatus

from django.shortcuts import reverse
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING

from news.models import Comment

from random import choice

pytestmark = pytest.mark.django_db


def test_user_can_create_comment(author_client, author, form_data, news):
    url = reverse('news:detail', args=[news.id])
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    comments_count = 0
    comments_count += Comment.objects.count()
    assert comments_count == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author


def test_anon_cant_create_comment(client, form_data, news):
    url = reverse('news:detail', args=[news.id])
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    comment_count = 0
    comment_count += Comment.objects.count()
    assert comment_count == 0


def test_bad_word_warning(author_client, comment, form_data, news):
    url = reverse('news:detail', args=[news.id])
    form_data['text'] = f'Какой-то текст, {choice(BAD_WORDS)}, еще текст'
    response = author_client.post(url, data=form_data)
    assertFormError(
        response,
        'form',
        'text',
        errors=WARNING,
    )
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(author_client, form_data, comment, news):
    url = reverse('news:edit', args=(comment.pk,))
    detail_url = reverse('news:detail', args=[news.id])
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_other_user_cant_edit_comment(admin_client, form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(pk=comment.pk)
    assert comment.text == comment_from_db.text


def test_author_can_delete_comment(author_client, pk_for_args, news):
    url = reverse('news:delete', args=[pk_for_args])
    detail_url = reverse('news:detail', args=[news.id])
    response = author_client.post(url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 0


def test_other_user_cant_delete_comment(admin_client, form_data, pk_for_args):
    url = reverse('news:delete', args=[pk_for_args])
    response = admin_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
