import datetime
import random
import re
import time
from socket import socket
from typing import Union

import requests
import urllib3
from tqdm import tqdm

from citi_login import USTCPassportLogin
from sms_utils import send_sms


class USTCGymAppointment(object):
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.login_bot = USTCPassportLogin()
        self.sess = self.login_bot.sess
        self.event_list_url = 'https://ichangtou.zhidieyun.com/api/event/getEventList'
        self.token_url = 'https://cgyy.ustc.edu.cn/api/user/login'
        self.join_cancel_url = 'https://ichangtou.zhidieyun.com/api/event/joinCancelEvent'
        self.event_detail_url = 'https://ichangtou.zhidieyun.com/api/event/getEventDetail'
        self.token = ''
        self.member_id = ''
        self._login(phone_number)
    def _get_event_list(self):
        payload = {
            'token': self.token,
            'offset': '1000',
            'page': '1'
        }
        response = self.sess.post(self.event_list_url, payload, allow_redirects=False, timeout=5)
        return response.json()
    def _get_event_detail(self, event_id):
        payload = {
            'token': self.token,
            'memberid': self.member_id,
            'eventid': event_id,
            'from': 'false'
        }
        response = self.sess.post(self.event_detail_url, payload, allow_redirects=False, timeout=5)
        return response.json()
    def _join_cancel(self, event_id):
        payload = {
            'token': self.token,
            'memberid': self.member_id,
            'eventid': event_id
        }
        response = self.sess.post(self.join_cancel_url, payload, allow_redirects=False, timeout=5)
        return response.json()

    def _login(self, username):
        """
        登录,需要提供用户名、密码，顺便返回后续表单需要提供的token
        """
        self.token = ''
        user_info = self.login_bot.login(username)['data']
        print(user_info)
        self.token = user_info['Token']
        self.member_id = user_info['Memberid']


    def check_activity(self, pattern):
        while (1):
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            try:
                event_id = self.get_target_event_id(pattern)
            except TimeoutError:
                print('time out')
            except urllib3.exceptions.MaxRetryError:
                print('MaxRetryError')
            except requests.exceptions.ConnectTimeout:
                print('ConnectTimeout')
            except requests.exceptions.RequestException:
                print('RequestException')
            if event_id != '':
                send_sms(self.phone_number, pattern + '活动开始啦')
                return event_id
            else:
                print('活动未开始。')
            time.sleep(random.uniform(1, 5))

    def appointment(self, pattern):
        event_id = self.check_activity(pattern)
        count = 1;
        while (1):
            try:
                devet_detail = self._get_event_detail(event_id)
            except TimeoutError:
                time.sleep(random.uniform(30, 200))
                print('time out')
            except urllib3.exceptions.MaxRetryError:
                print('MaxRetryError')
            except requests.exceptions.ConnectTimeout:
                print('MaxRetryError')
            except requests.exceptions.RequestException:
                print('RequestException')

            msg = devet_detail['message']
            print('第' + str(count) + '次轮询: ' + msg)
            count = count + 1
            if (msg == '立即报名'):
                result = self._join_cancel(event_id)
                print(result)
                if result['message'] == '报名成功':
                    print('报名成功')
                    send_sms(self.phone_number, pattern + "报名成功")
                    return
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            time.sleep(random.uniform(15, 50))

    def test(self):
        self._login('17396245416')
        payload = {
            'token': self.token,
            'memberid': '688385839196240713',
            'eventid': '1037710619316326400'
        }
        response = self.sess.post(self.join_cancel_url, payload, allow_redirects=False, timeout=5)
        print(response.json())
        if (response.json()['message'] == '报名成功'):
            print('报名成功')


    def invalid_date(self, date_str):
        # now_time = time.strftime('%Y-%m-%d %H:%M', time.localtime())
        now_time = datetime.datetime.now()
        format_date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        return now_time < format_date


    def str_match(self, str, pattern):
        match = re.search(pattern, str)
        if match:
            return True
        else:
            return False
    def grab_event(self, event, pattern):
        return (event['club'] == '羽毛球俱乐部') & self.invalid_date(event['date']) & self.str_match(event['name'], pattern)


    def get_target_event_id(self, pattern):
        found = False
        response = self._get_event_list()
        if (response['code'] == 200):
            event_list = response['data']
            for event in tqdm(event_list):
                if self.grab_event(event, pattern):
                    print(event)
                    found = True
                    return event['id']
        if not found:
            return ""


    def test_get_event_list(self):
        response = self._get_event_list()
        target_event = ''
        if(response['code'] == 200):
            event_list = response['data']
            for event in tqdm(event_list):
                if self.grab_event(event, '华体汇'):
                    print(event)
                    target_event = event
                    break


