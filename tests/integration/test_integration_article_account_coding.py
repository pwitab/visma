import pytest

from visma.models import ArticleAccountCoding


class TestArticleAccountCodings:

    @pytest.fixture()
    def article_account_coding_id(self):
        coding = ArticleAccountCoding.objects.all()[0]
        yield coding.id

    def test_list_article_account_codings(self):
        codings = ArticleAccountCoding.objects.all()

        assert codings is not None

    def test_get_article_account_codings(self, article_account_coding_id):
        coding = ArticleAccountCoding.objects.get(article_account_coding_id)
        assert coding is not None

