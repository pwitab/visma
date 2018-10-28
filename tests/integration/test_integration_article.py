import pytest

from visma.api import VismaClientException
from visma.models import Article, ArticleAccountCoding, Unit


class TestCRUDArticle:

    @pytest.fixture()
    def article(self):
        article = Article.objects.all()[0]
        yield article

    @pytest.fixture()
    def coding(self):
        coding = ArticleAccountCoding.objects.all()[0]
        yield coding

    @pytest.fixture()
    def unit(self):
        unit = Unit.objects.all()[0]
        yield unit

    def test_list_articles(self):
        articles = Article.objects.all()

        assert len(articles) is not 0

    def test_create_article(self, coding, unit):
        # article = Article(number=100, name='test article', coding_id=coding.id, unit_id=unit.id)
        # article.save()

        # assert article.id is not None

        # Since we cannot delete articles we don't want to keep on creating new ones.
        pass

    def test_read_article(self, article):
        read_article = Article.objects.get(article.id)

        assert read_article.id == article.id

    def test_update_article(self, article):
        article.net_price = 50
        article.save()

        updated_article = Article.objects.get(article.id)

        assert updated_article.net_price == 50

        updated_article.net_price = 10
        updated_article.save()

    def test_delete_article(self, article):
        # Not allowed
        # TODO: raise more explaining exception
        with pytest.raises(VismaClientException):
            article.delete()
