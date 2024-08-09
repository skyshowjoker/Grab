import requests



class USTCPassportLogin(object):
    def __init__(self):
        self.passport = "https://ichangtou.zhidieyun.com/api/member/wxlogin"
        self.sess = requests.session()
        self.sess.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

    def _get_open_id(self):
        """
        获取登录时需要提供的验证字段
        """
        url = 'https://ichangtou.zhidieyun.com/api/member/getOpenId'
        data = {
            'code': '0d38Qm000W47yS18ut200bJSOy48Qm0M'
        }
        response = self.sess.post(url, data)

        return response.json()

    def login(self, phoneNumber):
        """
        登录,需要提供用户名、密码
        """
        self.sess.cookies.clear()
        try:
            user_info = self._get_open_id()['data']
            login_data = {
                'username': phoneNumber,
                'openid': user_info['openid'],
                'sessionkey': user_info['sessionkey'],
                'unionid': user_info['unionid'],
            }

            instance_data = {
                'username': '17396245416',
                'openid': 'ojXSe5PdNSrN6PEgiTwqjrVd3l6M',
                'sessionkey': 'gq+yKgrHH9uybsp0dmoyKg==',
                'unionid': 'oP1u65y5cuI36qqwn_JD7UD6ExGE',
            }
            result = self.sess.post(self.passport, instance_data, allow_redirects=False)
            print(result)
            return result.json()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    login_bot = USTCPassportLogin()
    result = login_bot._get_open_id()
    print(result)
