from django.shortcuts import reverse
from django.conf import settings
import pytest
from news.models import News, Comment

pytestmark = pytest.mark.django_db


def test_news_count(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(all_news, client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    ordered_news = News.objects.order_by('-date')[: len(object_list)]
    all_dates_news = [news.date for news in ordered_news]
    all_dates = [news.date for news in object_list]
    assert all_dates_news == all_dates


def test_comments_order(all_comments, client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    comments_sorted = Comment.objects.order_by('created')
    all_dates_comments = [comment.created for comment in comments_sorted]
    all_dates = [comment.created for comment in all_comments]
    assert all_dates_comments == all_dates


@pytest.mark.parametrize(
    'parametrized_client, is_allowed',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    ),
)
def test_author_client_has_form(parametrized_client, is_allowed, comment):
    url = reverse('news:detail', args=(comment.pk,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is is_allowed
