import pytest
import datetime

from visma.models import CostCenter, CostCenterItem


class TestCostCenter:

    def test_list_cost_center(self):

        cc = CostCenter.objects.all()
        length = len(cc)  # to evaluate the queryset

        if length == 0:
            raise Exception('Is there any Cost Centers in the app?')

    def test_update_cost_center(self):
        cc1 = CostCenter.objects.all().first()

        new_name = datetime.datetime.now().isoformat()[-10:-1]
        cc1.name = new_name
        _id = cc1.id
        cc1.save()

        new_cc = CostCenter.objects.filter(id=_id).first()

        assert new_cc.name == new_name
        assert new_cc.id == _id


class TestCostCenterItems:

    @pytest.fixture()
    def cost_center(self):
        cc = CostCenter.objects.all().first()

        yield cc

    def test_create_cost_center_item(self, cost_center):

        cost_center_item = CostCenterItem(cost_center_id=cost_center.id,
                                          name='TestCostCenter',
                                          short_name='TCC')

        cost_center_item.save()

        assert cost_center_item.id is not None

    def test_get_cost_center_item(self, cost_center):
        cost_center_item = cost_center.items[0]
        cci = CostCenterItem.objects.get(cost_center_item.id)

        assert cci.id == cost_center_item.id

    def test_update_cost_center_item(self, cost_center):
        new_name = datetime.datetime.now().isoformat()[-10:-1]
        cost_center_item = CostCenterItem.objects.get(cost_center.items[0].id)

        cost_center_item.name = new_name
        cost_center_item.save()

        cci = CostCenterItem.objects.get(cost_center_item.id)

        assert cci.name == new_name

