from django.test import Client, TestCase

from model_bakery import baker

from users.models import User


class ListBattlesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email="eduardavercosa@vinta.com.br", password="admin")
        self.user.set_password("admin")
        self.user.save()

    def test_create_battle(self):
        self.client.login(username=self.user.email, password="admin")
        battles = baker.make("battling.Battle", creator=self.user, _quantity=2)
        response = self.client.get("/battle/list/")
        response_qs = response.context_data.get("battle_list")
        self.assertCountEqual(battles, response_qs)
