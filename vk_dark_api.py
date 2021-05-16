import requests
import Exceptions
import re

token = 'VK_API_TOKEN'

vk_api_url = "https://api.vk.com/method/"

v = '5.130'


class Main:
    def __init__(self):
        self.url = None
        self.key = None
        self.server = None
        self.ts = None
        self.session = requests.Session()

    def listen(self):
        payload = {
            'v': v,
            'group_id': '145807659',
            'access_token': token
        }
        r = requests.get(
            url=vk_api_url + "groups.getLongPollServer",
            params=payload
        )
        response = r.json()
        response_data = response['response']
        self.ts = response_data['ts']
        self.key = response_data['key']
        self.server = response_data['server']
        payload = {
            'act': 'a_check',
            'key': str(self.key),
            'wait': '5',
            'ts': str(self.ts)
        }
        r = requests.post(url=self.server, data=payload)
        response_data = response['response']
        self.ts = response_data['ts']
        if r.json().get('updates'):
            if func := r.json().get('updates')[0]:
                return func


class methods(object):
    __slots__ = '_method'

    def __init__(self, method=None):
        self._method = method

    def __getattr__(self, method):
        return methods(method=f'{self._method}.{method}')

    def __call__(self, **kwargs):
        """
        :param method: Метод выполняемый в вк апи
        :param kwargs: Аргументы для этого метода
        :return: https://vk.com/dev/methods
        """
        if self._method is None:
            self.return_traceback('Method not entered')
        kwargs['v'] = v
        kwargs['access_token'] = token
        rw = requests.get(vk_api_url + self._method[74:], params=kwargs)
        if rw.json().get('error'):
            text_s = rw.json()["error"]["error_msg"]
            self.return_traceback(text_s)
        return rw.json()

    def return_traceback(self, text_s):
        raise Exceptions.MethodError(text_s)


class message_handler(object):
    def connect_to_methods(self):
        print('methods connected!')
        return methods(self)
