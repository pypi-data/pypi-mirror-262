'''
通过将可能的明文密码转换为散列值，并与Wireshark捕获的散列值进行比较，从而找到匹配项。
这种方法通常被称为“散列碰撞”或“彩虹表攻击”，它是基于尝试许多不同的可能的密码，直到找到一个其散列值与捕获的散列值相匹配的密码。

下面是一个简化的流程描述：

你有一个Wireshark捕获的加密（散列）的密码，例如MD5、SHA1、SHA256等。
你创建一个包含可能明文密码的列表。
对于列表中的每个明文密码，你使用相同的散列算法生成散列值。
将生成的散列值与Wireshark捕获的散列值进行比较。
如果某个生成的散列值与捕获的散列值相匹配，那么你可以假设相应的明文密码就是原始密码。
这种方法的有效性取决于你的密码列表是否包含了正确的密码。如果列表中没有正确的密码，你将无法找到匹配的散列值。
此外，如果使用了强散列函数和/或额外的安全措施（如盐值），即使你有正确的密码，也可能无法找到匹配的散列值。

'''

import base64
import hashlib

class PasswordHashTester:
    def __init__(self, hash_algorithms=None):
        """
        初始化密码散列测试器类。

        :param hash_algorithms: 一个字典，键为散列算法的名称，值为对应的散列函数。如果为None，则使用默认算法集。
        """
        if hash_algorithms is None:
            self.hash_algorithms = {
                'MD5': hashlib.md5,
                'SHA1': hashlib.sha1,
                'SHA224': hashlib.sha224,
                'SHA256': hashlib.sha256,
                'SHA384': hashlib.sha384,
                'SHA512': hashlib.sha512,
                # 可以添加更多的算法
            }
        else:
            self.hash_algorithms = hash_algorithms

    @staticmethod
    def decode_base64(encoded_str):
        """
        对base64编码的字符串进行解码。

        :param encoded_str: base64编码的字符串。
        :return: 解码后的bytes，如果解码失败则返回None。
        """
        try:
            decoded_bytes = base64.b64decode(encoded_str)
            return decoded_bytes
        except base64.binascii.Error as e:
            print(f"解码错误: {e}")
            return None

    def test_password_hash(self, captured_hash, passwords_to_test):
        """
        测试一系列明文密码与不同的散列算法是否与已捕获的散列密码匹配。

        :param captured_hash: Wireshark捕获的十六进制散列密码字符串。
        :param passwords_to_test: 要测试的明文密码列表。
        :return: None
        """
        for password in passwords_to_test:
            for hash_name, hash_func in self.hash_algorithms.items():
                hash_value = hash_func(password.encode()).hexdigest()
                if hash_value == captured_hash:
                    print(f"找到匹配项，算法：{hash_name}, 密码：{password}")
                    return
        print("没有找到匹配项。")


# 使用示例
if __name__ == "__main__":
    tester = PasswordHashTester()

    # 示例：base64编码的密码和Wireshark捕获的十六进制散列密码
    encoded_pass = "c2FsdF8xMXhsayE1MjAxMDA="
    captured_passwd = "b3aa4ca75ecb6681f9a543674d8e3c88"
    passwords_to_test = ['password123', 'letmein', '123456', 'xlk!520100']


    # 解码base64编码的密码
    decoded_pass = tester.decode_base64(encoded_pass)

    # 测试密码散列是否与捕获的散列匹配
    tester.test_password_hash(captured_passwd, passwords_to_test)

