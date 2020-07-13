from django.test import TestCase
from sign.models import Guest, Event
from django.contrib.auth.models import User


# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=2, name='华为Mate40发布会', status=True, limit=2000, address='山西',
                             start_time='2020-08-01 12:00:00')
        Guest.objects.create(id=1, event_id='2', realname='离散风', phone='15235514553', email='zhangbo@qq.com',
                             sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='华为Mate40发布会')
        self.assertEqual(result.address, '山西')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='15235514553')
        self.assertEqual(result.realname, '离散风')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):
    '''测试登陆动作'''

    def setUp(self):
        User.objects.create_user('zhangbo1', 'zhangbo_dcits@163.com', 'qqw123456')

    def test_add_admin(self):
        '''测试添加用户'''
        user = User.objects.filter(username='zhangbo1')
        # for i in user:
        #     print(i, 1111111111)
        self.assertEqual(user[0].username, 'zhangbo1')
        self.assertEqual(user[0].email, 'zhangbo_dcits@163.com')

    def test_login_action_username_password_null(self):
        '''用户密码为空'''
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        print(response)
        self.assertEqual(response.status_code, 200)
        # print('111111111111111111111', response.content, 111111111111111111)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_username_password_error(self):
        '''用户密码为空'''
        test_data = {'username': 'aaa', 'password': 'ccccccccccccccccc'}
        response = self.client.post('/login_action/', data=test_data)
        print(response)
        self.assertEqual(response.status_code, 200)
        # print('111111111111111111111', response.content, 111111111111111111)
        self.assertIn(b'username or password error!', response.content)

    def test_login_action_success(self):
        '''用户密码为空'''
        test_data = {'username': 'zhangbo1', 'password': 'qqw123456'}
        response = self.client.post('/login_action/', data=test_data)
        print('1111111', response, '1111111')
        print(response.status_code, 1111111111)
        self.assertEqual(response.status_code, 301)
        # print('111111111111111111111', response.content, 111111111111111111)

    class EventManageTest(TestCase):
        '''发布会管理'''

        def setUp(self):
            User.objects.create_user('zhangbo', 'zhangbo_dcits@163.com', 'qqw123456')
