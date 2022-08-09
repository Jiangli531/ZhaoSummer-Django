import binascii
import pyDes


class DesSecret:

    def __init__(self):
        self.KEY = 'ZHAOZHAO'  # 八位密钥

    # 加密
    def des_en(self, text):
        iv = secret_key = self.KEY
        k = pyDes.des(secret_key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = k.encrypt(text, padmode=pyDes.PAD_PKCS5)
        # data.进制返回文本字符串.解码字符串
        return binascii.b2a_hex(data).decode()

    # 解密
    def des_de(self, text):
        iv = secret_key = self.KEY
        k = pyDes.des(secret_key, pyDes.CBC, iv, pad=None, padmode=pyDes.PAD_PKCS5)
        data = k.decrypt(binascii.a2b_hex(text), padmode=pyDes.PAD_PKCS5)
        return data.decode()


#  使用举例
#
# input_text = '8'
#
# DS = DesSecret()
# encode_str = DS.des_en(input_text.encode())
# print('加密后：', encode_str)
#
# decode_str = DS.des_de(encode_str)
# print('解密后：', decode_str)
