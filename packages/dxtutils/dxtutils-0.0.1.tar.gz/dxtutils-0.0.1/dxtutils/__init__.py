import time
import re
import requests
import os
import sys
import csv
import random
import pypinyin
import hashlib
from fake_useragent import UserAgent
from collections import defaultdict
from pypinyin import pinyin,lazy_pinyin
def generate_user_agent():
    """动态生成User-Agent"""
    ua = UserAgent()
    return ua.random
def  filter_html(html):
    """过滤html标签"""
    pattern = re.compile(r'<[^>]+>',re.S)
    result = pattern.sub('', html)
    return result
def get_now_time():
    """获取当前时间"""
    now_time = time.strftime("%Y-%m-%d", time.localtime()) 
    return now_time
def write_to_csv(filename, data):
    """将数据写入CSV文件"""
    with open(filename, 'a+', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
def search_matching(req,html,n):
    """正则搜索匹配"""
    text = re.search(req,html)
    if text:
        data = text.group(n)
    else:
        data = 'no'
    return data 
def check_contain_chinese(check_str):
    """判断字符串是否包含中文，1为包含，0为不包含"""
    chinese_code = 0
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            chinese_code = 1
    return chinese_code 
def get_include_file(filename):
    """查看当前目录是否存在某个文件"""
    file = os.path.exists(filename)
    return file     
def get_html_content(url,headers,proxies):
    """请求网页获取内容"""
    maxTryNum = 3 # 定义最大尝试请求次数
    for tries in range(maxTryNum):
        try:
            html = requests.get(url, headers=headers,timeout=60,proxies=proxies)
            html.encoding = html.apparent_encoding
            return html
        except:
            if tries < (maxTryNum - 1):
                continue
            else:
                print("请求失败！已经尝试%d次请求%s\n" % (maxTryNum, url))
                break
def check_sensitive(word):
    """检查内容是否包含违禁词"""
    sensitive = ['敏感词1','敏感词2'] # 敏感词库
    # 用于存放敏感词
    sensitive_find = []
    # 遍历敏感词库
    for item in sensitive:
        # 将至少出现一次的敏感词放到sensitive_find中
        if word.count(item)>0:
            sensitive_find.append(item+':'+str(word.count(item))+'次')
    return sensitive_find
def request_json(url):
    """请求json数据"""
    req = requests.get(url,timeout=30)
    try:
        jsondata = req.json()
        return jsondata
    except:
        print("请求接口失败")
def get_content_wordnumber(html):
    """计算网页长度"""
    text = re.sub("[+/_,$%^*(+\"]+|[+——！，:：。？、~@#￥%……&*（）“”《》]+", "",html)
    text2 = re.sub('<[^>]*?>','',text)
    words_number = len(text2)
    return words_number
def get_md5(str):
    """生成md5"""
    m2 = hashlib.md5()
    m2.update(str.encode('utf8'))
    return m2.hexdigest()
def eachFile(filepath):
    """获取目录下所有文件路径"""
    file_pash_list = []
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s\%s' % (filepath, allDir))
        file_pash_list.append(child)
    return file_pash_list
def get_line_by_txt(txt_url_name):
    """获取文件的第一条数据"""
    str = open(sys.path[0]+'/'+txt_url_name).readline().strip()
    return str
def get_lines_by_txt(txt_url_name):
    """获取文件的多条数据"""
    results = open(sys.path[0]+'/'+txt_url_name,encoding='UTF-8').readlines()
    return results
def sogou_site_count(content):
    """提取搜狗搜索结果数量"""
    matches = re.findall(r'<p class="num-tips">搜狗已为您找到约([\d,]+)条相关结果</p>', content)
    if matches:
        return str(matches[0]).replace(',', '')
    else:
        return '0'   
    
def read_cookies_from_txt(file_path):
    """从txt文件读取cookies"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Cookie file not found at {file_path}")

    cookie_dict = defaultdict(str)
    
    with open(file_path, 'r') as f:
        for line in f.readlines():
            # 去除末尾换行符，并按等号分割键和值
            pair = line.strip().split('=', 1)
            if len(pair) == 2:
                # 对于每个键值对，添加到字典中，同时考虑到多个同名Cookie的情况
                cookie_dict[pair[0].strip()] += '=' + pair[1].strip() + ';'

    # 将字典转换为适合requests库的Cookie格式
    cookie_string = ''.join([f"{k}={v}" for k, v in cookie_dict.items()])
    return {"cookie": cookie_string}

def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str =''
    base_str ='abcdefghigklmnopqrstuvwxyz0123456789'
    length =len(base_str) -1
    for i in range(randomlength):
        random_str +=base_str[random.randint(0, length)]
    return random_str
def getQuanPin(ori_str):
    """根据中文获取全拼"""
    return ''.join(lazy_pinyin(ori_str, style = pypinyin.NORMAL))
def getJianPin(ori_str):
    """根据中文获取简拼"""
    first_letter_list = pinyin(ori_str, style = pypinyin.FIRST_LETTER)
    return ''.join([i[0] for i in first_letter_list])