from bs4 import BeautifulSoup
import re
import requests
import json
import time
import os


def get_token(url):
    url_re=re.compile(r'\d*.shtm')
    old_aid=url_re.findall(url)[0].split('.')[0]
    url_token='https://max.book118.com/index.php?g=Home&m=NewView&a=index&aid='+str(old_aid)
    token_get=requests.get(url_token)
    token_data=BeautifulSoup(token_get.text,'lxml')
    token_text=token_data.text
    pagenum_re=re.compile('preview: parseInt\(\'(\d*)\'\)')
    pagenum=int(pagenum_re.findall(token_text)[0])
    pid_re=re.compile('project_id: (\d*)')
    pid=pid_re.findall(token_text)[0]
    aid_re=re.compile(r'aid: parseInt\(\'(\S*)\'\)')
    aid=aid_re.findall(token_text)[0]
    token_re=re.compile(r'view_token: \'(.*)\'')
    token=token_re.findall(token_text)[0]
    return old_aid,pagenum,pid,aid,token

def get_pnglist(pagenum,pid,aid,token):
    preview_json_dict={}
    time.sleep(3)
    for i in range(1,pagenum,6):
        preview_url='https://openapi.book118.com/getPreview.html?&project_id='+str(pid)+'&aid='+str(aid)+'&view_token='+str(token)+'&page='+str(i)
        preview_data=requests.get(preview_url).text
        json_re=re.compile(r'jsonpReturn\((.*)\)')
        json_data=json_re.findall(preview_data)[0]
        preview_json=json.loads(json_data).get('data')
        print(preview_json)
        preview_json_dict.update(preview_json)
        time.sleep(2)
    return preview_json_dict

def get_png(old_aid,preview_json_dict):
    os.makedirs('./'+old_aid)
    for index in preview_json_dict:
        png_url='http:'+str(preview_json_dict[index])
        png = requests.get(png_url)
        with open('./'+old_aid+'/'+index+'.png', 'wb') as f:
            f.write(png.content)

def userapi():
    url=input('请输入网址，完成后按回车：')
    old_aid,pagenum,pid,aid,token=get_token(url)
    pnglist=get_pnglist(pagenum,pid,aid,token)
    get_png(old_aid,pnglist)

userapi()



