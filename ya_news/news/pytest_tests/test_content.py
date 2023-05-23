from django.shortcuts import reverse
from django.conf import settings
import pytest


@pytest.mark.django_db
def test_news_count(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(all_news, client):
    home_url = reverse('news:home')
    response = client.get(home_url)
    object_list = response.context['object_list']
    first_news_date = object_list[0].date
    all_dates = [news.date for news in object_list]
    assert first_news_date == max(all_dates)


@pytest.mark.django_db
def test_comments_order(all_comments, client, news):
    detail_url = reverse('news:detail', args=[news.id])
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, comment):
    url = reverse('news:detail', args=(comment.pk,))
    response = author_client.get(url)
    assert 'form' in response.context


@pytest.mark.django_db
def test_anon_client_has_not_form(client, comment):
    url = reverse('news:detail', args=(comment.pk,))
    response = client.get(url)
    assert 'form' not in response.context
