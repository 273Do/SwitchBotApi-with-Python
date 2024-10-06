import time
import hashlib
import hmac
import base64
import uuid
import requests
import pprint

from dotenv import load_dotenv
import os

# .envファイルの内容を読み込見込む

load_dotenv()


def make_secret(secret_key):
    secret_key = bytes(secret_key, 'utf-8')
    return secret_key


def make_sign(secret_key, t, nonce):
    string_to_sign = '{}{}{}'.format(token, t, nonce)
    string_to_sign = bytes(string_to_sign, 'utf-8')
    sign = base64.b64encode(
        hmac.new(secret_key, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign


def make_t():
    t = int(round(time.time() * 1000))
    return str(t)


def make_nonce():
    nonce = str(uuid.uuid4())
    return nonce


if __name__ == "__main__":

    # SwitchBotアプリから取得
    secret_key = os.environ['SECRET_TOKEN']  # 文字列で入力
    token = os.environ['SB_TOKEN']   # 文字列で入力

    # Requestパラメータ作成
    secret_key = make_secret(secret_key)
    t = make_t()
    nonce = make_nonce()
    sign = make_sign(secret_key, t, nonce)

    # URL指定
    url = "https://api.switch-bot.com/v1.1/devices"

    # APIHeader作成
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": t,
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf-8"
    }

    # requests処理
    response = requests.get(url, headers=headers)

    pprint.pprint(response.json())

    """
    出力例
    {'body': {'deviceList': [{'deviceId': 'AAAAAAAAAAAA',
                            'deviceName': 'プラグミニ(JP) E6',
                            'deviceType': 'Plug Mini (JP)',
                            'enableCloudService': True,
                            'hubDeviceId': ''}],
    'infraredRemoteList': []},
    'message': 'success',
    'statusCode': 100}
    """
