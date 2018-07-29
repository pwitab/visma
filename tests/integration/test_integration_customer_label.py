import datetime

import pytest

from visma.api import VismaAPIException
from visma.models import CustomerLabel


class TestCustomerLabel:

    @pytest.fixture()
    def customer_label(self):
        label = CustomerLabel(name='TestLabel4', description='')
        label.save()

        yield label

        label.delete()

    def test_list_customer_labels(self, customer_label):
        # customer_label is there to ensure the list is not empty
        labels = CustomerLabel.objects.all()

        assert len(labels) is not 0

    def test_create_customer_label(self):
        name = datetime.datetime.now().isoformat()[-10:-1]
        label = CustomerLabel(name=name, description='')
        label.save()

        assert label.id is not None

        label.delete()

    def test_get_customer_label(self, customer_label):
        lable2 = CustomerLabel.objects.get(customer_label.id)

        assert lable2.id == customer_label.id

    def test_update_customer_label(self, customer_label):
        new_name = 'Updated Name'
        customer_label.name = new_name
        customer_label.save()

        updated_label = CustomerLabel.objects.get(customer_label.id)

        assert updated_label.name == new_name

    def test_delete_customer_label(self):
        label = CustomerLabel(name='TestLabel3', description='')
        label.save()

        to_delete = CustomerLabel.objects.get(label.id)
        to_delete.delete()

        with pytest.raises(VismaAPIException):
            l = CustomerLabel.objects.get(label.id)