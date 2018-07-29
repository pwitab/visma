import datetime

import pytest

from visma.api import VismaClientException
from visma.models import Project


class TestProject:

    @pytest.fixture()
    def last_project(self):

        projects = Project.objects.all().order_by('number')

        list_of_project = list()
        for project in projects:
            list_of_project.append(project)

        yield list_of_project[-1]

    @pytest.fixture()
    def project(self, last_project):
        new_number = int(last_project.number) + 1
        project = Project(name='TestProject', number=str(new_number),
                          start_date='2018-02-02')
        project.save()

        yield project

    def test_list_projects(self, project):
        projects = Project.objects.all()

        assert len(projects) is not 0

    def test_get_projects(self, last_project):
        project = Project.objects.get(last_project.id)

        assert project.id == last_project.id

    def test_create_project(self):
        # Done in fixture. Can't delete so no need to create alot if extras.
        pass

    def test_update_project(self, last_project):
        new_desc = datetime.datetime.now().isoformat()[-10:-1]
        last_project.notes = new_desc
        last_project.save()

        updated_project = Project.objects.get(last_project.id)

        assert updated_project.notes == new_desc

    def test_delete_project(self, last_project):

        with pytest.raises(VismaClientException):
            last_project.delete()


