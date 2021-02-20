from PIL import Image
import PIL
import os
import math
import  cv2
import time
import random
import threading
from cv2 import VideoCapture
from cv2 import imwrite
from tqdm import tqdm
import numpy as np

import json
'''
bottom_high1=137
bottom_high2=77
'''

# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image, addr, num):
    #cv2.namedWindow("Image")
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    #img=PIL.Image.fromarray(image)#3.8#3.64 0.04
    #img.show()
    address = addr + str(num)+'.jpg'
    print(address)
    #imwrite(address, image)
    cv2.imencode('.jpg', image)[1].tofile(address)

def videoToImg(name,bottom_high1,bottom_high2):
    video_path = "video/"+name+"[00].mp4"  # 视频路径
    out_path = "img/test_"  # 保存图片路径+名字

    # 读取视频文件
    #videoCapture
    video= VideoCapture(video_path)

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    high = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    is_all_frame = False  # 是否取所有的帧
    sta_frame = 600  # 开始帧
    end_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # 结束帧
    print('总帧数：',end_frame)

    ######
    time_interval = 36  # 时间间隔

    # 读帧
    success, frame = video.read()
    if success:
        print("读取视频成功")
    else:
        print("读取视频失败")
        exit(0)
    #print(frame)

    #save_image(frame, out_path, 111)

    i = -1
    j = 0
    if is_all_frame:
        time_interval = 1

    pix=None
    n=0
    s_num=0
    tar=Image.new('RGB',(width,(bottom_high1-bottom_high2)*30))

    pbar = tqdm(total=end_frame, desc='截取进度', leave=True, ncols=100, unit='frame', unit_scale=True)
    while success:
        i = i + 1
        if (i % time_interval == 0):
            if is_all_frame == False:
                if i >= sta_frame and i <= end_frame:
                    j = j + 1
                    #print('save frame:', i)
                    ######save_image(frame, out_path, j)
                    ####################################
                    ######
                    last = pix
                    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = PIL.Image.fromarray(frame)
                    pix = img.load()
                    #img2 = img.crop((0, high - bottom_high1, width, high-bottom_high2))
                    #img2.show()
                    diff = 0
                    if (last):
                        for y in range(high - bottom_high1, high - bottom_high2 + 1):
                            for x in range(852):
                                if (pix[x, y][0] >= 240 and pix[x, y][1] >= 240 and pix[x, y][2] >= 240):
                                    diff = diff + abs(pix[x, y][0] - last[x, y][0]) + abs(
                                        pix[x, y][1] - last[x, y][1]) + abs(pix[x, y][2] - last[x, y][2])
                    #print(diff)
                    if (diff > 120000):
                        img2 = img.crop((0, high-bottom_high1, width, high-bottom_high2))
                        #img2.show()
                        tar.paste(img2,(0,(bottom_high1-bottom_high2)*n,width,(bottom_high1-bottom_high2)*(n+1)))
                        n=n+1
                        if(n==30):
                            #tar = tar.convert('L')
                            tar.save("img/"+name+str(s_num)+".jpg")
                            s_num=s_num+1
                            tar=Image.new('RGB',(width,(bottom_high1-bottom_high2)*30))
                            n=0

                elif i > end_frame:
                    break
        success, frame = video.read()
        pbar.update(1)
    #tar.show()
    if(n!=0):
        tar=tar.crop((0,0,width,(bottom_high1-bottom_high2)*(n)))
        tar.save("img/"+ name + str(s_num) + ".jpg")

def download(name,addr):
    print("下载 ",name," 开始")
    dir=os.getcwd()
    print('you-get  --format=dash-flv720 -o='+dir+'"video" -O='+name+' '+addr)
    os.system('you-get  --format=dash-flv720 -o='+dir+'"video" -O='+name+' '+addr)
    print("下载结束")

def get_file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        #print(files)
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L
# 加载原始图片
def caijian(addr):
    tar=Image.new('RGB',(852,28*len(addr)))
    for i in range(len(addr)):
        img = Image.open(addr[i])
        width=img.size[0]
        high=img.size[1]
        # 从左上角开始 剪切 200*200的图片
        img2 = img.crop((0, high-63, width, high-35))
        tar.paste(img2,(0,28*i,width,28*(i+1)))
    tar.show()
    tar.save('newt1/res6.jpg')

def quchong():
    #addr=get_file_name('img')9399 9056 9376 4332 4478 2763
    addr=[]
    pix=None
    path=get_file_name('t0')
    for t in range(0,1000):
        last=pix
        a_addr=path[t]
        img=Image.open(a_addr)#0 305
        pix=img.load()
        width = img.size[0]
        high = img.size[1]
        diff=0
        if(last):
            for y in range(high - 63, high - 35 + 1):
                for x in range(852):
                    if (pix[x, y][0] >= 240 and pix[x, y][1] >= 240 and pix[x, y][2] >= 240):
                        diff=diff+abs(pix[x,y][0]-last[x,y][0])+abs(pix[x,y][1]-last[x,y][1])+abs(pix[x,y][2]-last[x,y][2])
        if(diff>120000):
            print(path[t],'  ',diff)
            addr.append(path[t])
    return addr
'''
                if(pix[x,y][0]>=240 and pix[x,y][1]>=240 and pix[x,y][2]>=240):
                    #print((pix[x,y]))
                    white_sum=white_sum+1
        #print(t," ",white_sum)
        now_sum=white_sum
        if(is_add):
            addr.append(a_addr)
            is_add=False
        elif(now_sum-last_sum>400 and now_sum>400):
            is_add=True
    return addr
        '''

def pingjie():
    addr=get_file_name('newimg')
    tar=Image.new('RGB',(1920,60*len(addr)))
    for i in range(len(addr)):
        print(i)
        img=Image.open(addr[i])
        tar.paste(img,(0,60*i,1920,60*(i+1)))
    tar.show()

def pic_show(img2):
    img2.show()

if __name__ == '__main__':
    sta=time.time()
    dirs1='video'
    if not os.path.exists(dirs1):
        os.makedirs(dirs1)
    dirs2='img'
    if not os.path.exists(dirs2):
        os.makedirs(dirs2)
    # addr=quchong()
    # print(addr)
    # caijian(addr)
    #pingjie()
    #get_file_name('D:\\2021寒假项目\\爬虫进阶\\video')

    flag=1
    is_download=1
    name=input('请输入视频标题：')
    for root, dirs, files in os.walk(dirs1):
        for file in files:
            if(file[:-8]==name):
                is_download=0
                break
    # if(is_download):
    #     url=input('请输入下载视频的链接：')
    #     download(name,url)


    #'''
    #download('【逸语道破】要组建第三政党？特朗普能拯救美国吗','https://www.bilibili.com/video/BV1bo4y197Ad')
    if(name[:6]=="【逸语道破】"):
        bottom_high1=111
        bottom_high2=75
        flag=0
    elif os.path.exists('video/history.json'):
            f_his=open('video/history.json', 'r')
            his=json.load(f_his)
            if name in his:
                bottom_high1=his[name][0]
                bottom_high2=his[name][1]
                print(bottom_high1)
                flag=0
                f_his.close()

    while(flag):
        video_path = dirs1+"/" + name + "[00].mp4"  # 视频路径
        video = VideoCapture(video_path)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        high = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_time=random.randint(0, int(video.get(cv2.CAP_PROP_FRAME_COUNT)) )
        print(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))
        print(frame_time)

        bottom_high1=int(input('请输入字幕上边距距离底部的距离（像素为单位）：'))
        bottom_high2=int(input('请输入字幕下边距距离底部的距离（像素为单位）：'))
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_time - 1)
        success, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = PIL.Image.fromarray(frame)
        pix = img.load()
        img2 = img.crop((0, high - bottom_high1, width, high-bottom_high2))
        threa_show=threading.Thread(target=pic_show, args=(img2,))
        threa_show.start()
        flagstr=(input('是否截取正确，正确输入1，不正确输入0：'))
        if(flagstr=='1'):
            break
    if(flag==1):
        info={name:(bottom_high1,bottom_high2)}
        info_json=json.dumps(info,sort_keys=False, indent=4, separators=(',', ': '))
        f = open('video/history.json', 'a')
        f.write(info_json)
        f.close()
    videoToImg(name,bottom_high1,bottom_high2)
    print(time.time()-sta)
    #'''