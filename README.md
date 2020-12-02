# pi_mcu

## 抽帧服务

+ ### 依赖环境
    #### 1. opencv 
    最好自己编译，因为apt-get安装的opencv版本比较低，而且默认使用ffmage，并没有使用gstreamer。如果想让opencv使用gstreamer，就需要在编译的时候添加相应的参数。当然 ，如果不想用gstreamer，并且对opencv版本没有要求，那可以直接选择apt-get大法安装。
    #### 2. ffmpeg
    可以默认安装，也可以自己编译。
    #### 3. gstreamer
    - 安装
    sudo apt-get install libgstreamer1.0-dev
    sudo apt-get install libgstreamer-plugins-bad1.0-dev
    sudo apt-get install gstreamer1.0-tools
+ ### 使用
    ```python
    Camera = CameraService(
        name = "your user name",
        pwd = "your user password",
        ip = "your ip address:554",
        camera_brand = "HIKVISION"
    )

    Camera.start()
    while True:
        frame = Camera.get_frame()
        cv2.imshow('test', frame)
        key = cv2.waitKey(10)
        if key == 27:
            break
    ```