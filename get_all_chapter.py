import os.path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

import D2wnloader

"""
获取动漫主页的url
"""

class AgeGetUrl:
    def __init__(self,url,path):
        ch_opthions=Options()
        # ch_opthions.add_argument("--headless")
        self.driver = webdriver.Chrome(options=ch_opthions)
        self.driver.set_page_load_timeout(10)  # 页面加载超时时间
        self.driver.set_script_timeout(10)
        self.url=url
        self.path=path
        self.Animate_name=''
        self.Chapter_Urls=[]
        self.request_times=5   #重复请求次数5次

    def Get_All_Chapter_Url(self):
        for i in range(0, self.request_times):
            try:
                list = self.driver.find_element(By.ID,'stab_1_71').find_elements(By.CSS_SELECTOR,'li')
                list = reversed(list)
                #返回的是包含字典的列表
                #例  [{'url':"sadsad','filenamne':'asda'},{...},{...}]
                Chapter_Urls=[]
                for i in list:
                    filename = i.text
                    print("正在获取"+filename+'url')
                    url = i.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
                    print(url)
                    url_dict={}
                    url_dict['url']=url
                    url_dict['filename']=filename
                    #如果不是是备份的视频才加入
                    if(filename.find("备用")==-1):
                        Chapter_Urls.append(url_dict)
                return Chapter_Urls
            except:
                print("获取集数url失败")

    def Get_Animate_name(self):
        time.sleep(1)
        for i in range(0, self.request_times):
            try:
                Animate_name = self.driver.find_element(By.CLASS_NAME,'name').text
                print("下载视频:"+ Animate_name)
                return Animate_name
            except:
                print("动漫名获取错误")

    def Get_chapter_src(self):

        for i in range(0, self.request_times):
            try:
                for i in self.Chapter_Urls:
                    print("正在获取"+i['filename']+'src')
                    url=i['url']
                    self.driver.get(url)
                    time.sleep(1)
                    iframe1=self.driver.find_element(By.ID,'playiframe')
                    self.driver.switch_to.frame(iframe1)
                    iframe2=self.driver.find_element(By.ID,'playiframe')
                    self.driver.switch_to.frame(iframe2)
                    src = self.driver.find_element(By.CSS_SELECTOR,'video').get_attribute('src')
                    print(src)
                    i['src'] =src
                break
            except:
                print("获取src失败")

    def down_src(self):

        for i in range(0,self.request_times):

            try:
                for i in self.Chapter_Urls:
                    src=i['src']
                    filename=i['filename']+'.mp4'
                    path=self.path+'\\'+self.Animate_name
                    #判断文件是否存在
                    if os.path.isfile(path+'\\'+filename):
                        print(self.Animate_name+'---'+filename+'---已下载')
                    else:
                        down = D2wnloader.D2wnloader(src, filename, path)
                        down.start()
                        time.sleep(5)
                break
            except:
                    print("下载失败")

    def run(self):
        for i in range(0,self.request_times):
            try:
                print("正在连接到动漫集数页面")
                self.driver.get(self.url)
                break
            except:
                print('get '+self.url+ '失败')

        self.Animate_name=self.Get_Animate_name()
        self.Chapter_Urls = self.Get_All_Chapter_Url()
        self.Get_chapter_src()
        self.down_src()
        self.driver.close()

if __name__ == '__main__':
    #下载多个动漫
    urlist=[
        'http://www.agefans.top/acg/66196/',
        'http://www.agefans.top/mov/16961/'
    ]
    #保存的文件路径,空为当前工作路径 格式为 C:\Users\Faith\Desktop\FileRecv 即保存在FileRecv中
    path='D:\Animate\看'
    for i in urlist:
        down = AgeGetUrl(i,path)
        down.run()
        time.sleep(10)
