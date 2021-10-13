# Hello，大家好我是ZDLAY
# 欢迎大家使用这个录屏截图功能，可以用它录屏然后截图进行标注
# author ZDLAY
# email chinadlay@163.com

# install 安装
# pip install pyside2 pyautogui threading numpy opencv time pyqt5_tools pyqt5 random

# 模块引用部分
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
import pyautogui
import threading
import numpy as np
import cv2 as cv
import time
import random

# 引用全局变量
from lib.function import DLAY

# cv的帧率
cv.CAP_PROP_FPS = 30

# 间隔
op = 0.5


# 类
class Win_Main:

    def __init__(self):

        unix = time.time()

        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('main.ui')

        # 绑定监听
        self.ui.start.clicked.connect(self.on_start)

        # 绑定监听
        self.ui.stop.clicked.connect(self.on_stop)

    # 开始录屏事件
    def on_start(self):
        print("点击了开始录屏")
        if DLAY.InStart:
            print("录屏已经开始")
        else:
            print("开始录屏")
            DLAY.InStart = True
            DLAY.Stop = False

            # 创建新的线程去执行发送方法，
            # 服务器慢，只会在新线程中阻塞
            # 不影响主线程
            thread = threading.Thread(target=self.threadSend)
            thread.start()

    # 新线程入口函数
    def threadSend(self):
        try:
            while not DLAY.Stop and DLAY.InStart:

                # 获取每一帧截图
                img = pyautogui.screenshot()

                # 转换为numpy数组
                frame = np.array(img)

                # 因为cv读取的话可能会出现颜色不对的情况
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                # 获取当前时间戳
                unix = time.time()

                # 间隔，越高可能会变卡
                time.sleep(op)
                
                # 获取随机数因为时间戳1秒可能重复很多
                rand = random.random()

                # 文件保存目录和图片文件名
                path = './data/' + str(int(unix)) + str(rand) + '.jpg'

                # 控制台输出
                print("正在录屏,当前文件：{}".format(path, {}))

                # gui界面输出
                self.ui.text.setText("状态：正在录屏, 当前文件：{}".format(path, {}))

                # cv 写入图片
                cv.imwrite(path, frame)

                # cv 显示
                cv.imshow('result', frame)

                # cv 等待
                if cv.waitKey(1) & 0xFF == DLAY.Stop:
                    print("停止")
                    self.ui.text.setText("状态：停止录屏 ,文件保存到data目录请查看")
                    break
        # 异常输出代码
        except:
            print("非正在录屏")
            self.ui.text.setText("状态：开启录屏失败")
            DLAY.InStart = False
            DLAY.Stop = False

    # 停止录屏事件
    def on_stop(self):
        if DLAY.InStart:

            # 设置变量让while退出循环
            DLAY.Stop = True

            # 不在录屏中
            DLAY.InStart = False

            # 设置间隔因为可能while循环结束有延时
            time.sleep(0.5)

            # 设置输出
            self.ui.text.setText("状态：停止录屏,文件保存到data目录请查看")

            # 输出
            print("停止录屏,文件保存到data目录请查看")

        else:

            # 当录屏没有开始的输出
            print("录屏没有开始")
            self.ui.text.setText("状态：录屏没有开始")

# 主程序入口
app = QApplication([])
DLAY.Main = Win_Main()
DLAY.Main.ui.show()
app.exec_()

cv.destroyAllWindows()
