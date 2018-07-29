import pytest

from visma.models import User


class TestUser:

    def test_list_users(self):

        users = User.objects.all()

        assert len(users) is not 0


