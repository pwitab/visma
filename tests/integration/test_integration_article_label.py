import pytest

from visma.api import VismaAPIException
from visma.models import ArticleLabel


class TestCRUDArticleLabel:

    @pytest.fixture()
    def article_label(self):

        label = ArticleLabel(name='Test')
        label.save()
        yield label
        label.delete()

    def test_list_article_labels(self, article_label):

        so_there_is_at_least_one_lable = article_label

        labels = ArticleLabel.objects.all()

        assert len(labels) is not 0

    def test_create_article_labels(self):

        new_label = ArticleLabel(name='Test L', description='A description')
        new_label.save()

        assert new_label.id is not None

        new_label.delete()

    def test_read_article_labels(self, article_label):

        read_label = ArticleLabel.objects.get(article_label.id)

        assert read_label.id == article_label.id

    def test_update_article_labels(self, article_label):
        article_label.name = 'Updated Name'
        article_label.save()

        updated_label = ArticleLabel.objects.get(article_label.id)

        assert updated_label.name == 'Updated Name'

    def test_delete_article_labels(self):
        new_label = ArticleLabel(name='To Delete')
        new_label.save()

        to_delete = ArticleLabel.objects.get(new_label.id)
        to_delete.delete()

        with pytest.raises(VismaAPIException):
            should_raise = ArticleLabel.objects.get(new_label.id)

