# coding=utf-8

"""
Source: wufujun 2020-11-25
"""
import cv2

from service.camera_service import CameraService


Camera = CameraService(
    name = "your user name",
    pwd = "your user password",
    ip = "your ip address:554",
    camera_brand = "HIKVISION"
)

#Camera = CameraService()
Camera.start()
while True:
    frame = Camera.get_frame()
    cv2.imshow('test', frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
