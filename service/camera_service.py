# coding=utf-8

"""
Source: wufujun 2020-08-21
"""

import cv2

import queue
import time
import threading


class CameraService:
    """
    CameraService
    """

    def __init__(self, name="", pwd="", ip="", channel=101, camera_brand=""):

        self.__name = name
        self.__pwd = pwd
        self.__ip = ip
        self.__channel = channel
        self.__camera_brand = camera_brand

        self.__frame_queue = queue.Queue(maxsize=4)
        

        self.camera_connect()
    
    
    def camera_connect(self):
        """
        网络摄像机品牌（capture_brand）现适配：HIKVISION,DaHua；适配摄像头以外的参数都会尝试调取本机摄像头
        大华（DaHua）摄像头的rtsp地址还没有经过测试，需要在用到的时候再确认一下最新的地址格式
        """

        if self.__camera_brand == "HIKVISION":
            self.cap = cv2.VideoCapture(
                "rtsp://%s:%s@%s/Streaming/Channels/%d?transportmode=unicast" % (
                    self.__name, self.__pwd, self.__ip, self.__channel
                )
            )
        
        elif self.__camera_brand == "DaHua":
            self.cap = cv2.VideoCapture(
                "rtsp://%s:%s@%s/cam/realmonitor?channel=%d&subtype=0" % (
                    self.__name, self.__pwd, self.__ip, self.__channel
                )
            )
        
        else:
            # self.cap = cv2.VideoCapture(0)
            self.cap = cv2.VideoCapture(
                "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
            )


        try:
            if self.cap.isOpened() == False:
                ex = Exception('[%s] Camera open failed' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                raise ex

        except Exception as re:
            print(re)

        else:
            print('[%s] Camera open success' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    
    
    def put_frame(self):
        """
        将摄像头画面帧并推送至队列。
        """

        while True:
            ret, frame = self.cap.read()
            if ret:
                self.__frame_queue.put(frame)
                self.__frame_queue.get() if self.__frame_queue.qsize() > 2 else time.sleep(0.01)

            else:
                # 当出现断流或者取帧失败的情况，释放摄像机重新连接
                print('[%s] Failed to get frame, Camera reconnection...' % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                self.cap.release()
                self.camera_connect()
            

    def get_frame(self):
        """
        获取摄像头画面帧
        """

        return self.__frame_queue.get()
    
    
    def start(self):
        """
        开启服务
        """
        
        thread = threading.Thread(target=self.put_frame)
        thread.daemon = True
        thread.start()
        #thread.join()



