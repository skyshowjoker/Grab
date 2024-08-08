# Recovery code
# X78G7Y6Z8RVPMSF3SJ28E8QH

from twilio.rest import Client

# 用你的账号 SID 和授权令牌替换下面的值
account_sid = 'AC8cea36046449788eccd6a654d29fd22e'
auth_token = '7593aa97825d93cef885e656f1ce1def'

# 初始化客户端
client = Client(account_sid, auth_token)

def send_sms(to_phone_number, message):
    try:
        # 发送短信
        message = client.messages.create(
            body=message,
            from_='+18577545620',  # 替换为你在 Twilio 上的号码
            to=to_phone_number   # 收信人的手机号码
        )
        print(f"短信已发送，SID: {message.sid}")
    except Exception as e:
        print(f"发送短信失败: {e}")





