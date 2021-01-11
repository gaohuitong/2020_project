import requests
from bs4 import BeautifulSoup
import pprint
import json
old_pages_indexs=range(1997,2000,1)
new_pages_indexs=range(2000,2022,1)

#将每年的debian安全网页下载下来
def download_all_htmls(pages_indexs):
    htmls=[]
    for idx in pages_indexs:
        url=f"https://www.debian.org/security/{idx}"
        print("craw html:",url) 
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
        try:
            r = requests.get(url,headers=headers,timeout=10)
            if r.status_code != 200:
                raise Exception("浏览器无法访问")
        except:
            print('服务器无响应')
            try:
                r = requests.get(url,headers=headers,timeout=10)
                if r.status_code != 200:
                    raise Exception("浏览器无法访问")
            except:
                print('服务器无响应2')
                try:
                    r = requests.get(url,headers=headers,timeout=10)
                    if r.status_code != 200:
                        raise Exception("浏览器无法访问")
                except:
                    print('服务器无响应3')
        htmls.append(r.text)
    return htmls

old_htmls = download_all_htmls(old_pages_indexs)
new_htmls = download_all_htmls(new_pages_indexs)

def download_html(url):
    print("craw html:",url)
    try:
        r = requests.get(url,timeout=10)
        if r.status_code != 200:
            raise Exception("浏览器无法访问")
    except:
        print('服务器无响应1')
        try:
            r = requests.get(url,timeout=10)
            if r.status_code != 200:
                raise Exception("浏览器无法访问")
        except:
            print('服务器无响应2')
            try:
                r = requests.get(url,timeout=10)
                if r.status_code != 200:
                    raise Exception("浏览器无法访问")
            except:
                print('服务器无响应3')    
    html = r.text
    return html

#爬旧版本网页并返回一个字典列表
def old_parse_single_html(html):
    soup = BeautifulSoup(html,'html.parser')
    article_date = soup.find("h1").get_text().replace("Security Advisories from ","")
    article_dts = (
        soup.find("div",id="content")
            .find("dl")
            .find_all("dt")
    )
    datas = []
    for article_item in article_dts:
        date=article_item.find("tt").get_text()
        name=article_item.find("strong").find("a").get_text()
        info_indexs=article_item.find("strong").find("a")["href"].replace(".","")
        url=f"https://www.debian.org/security/"+article_date+info_indexs
        subhtml = download_html(url)
        subsoup = BeautifulSoup(subhtml,'html.parser')
        security_advisory = subsoup.find("h2").get_text()
        article_dds = (
        subsoup.find("div",id="content")
            .find("dl")
            .find_all("dd")
        )
        affected_packages = article_dds[1].get_text()
        vulnerable = article_dds[2].get_text()
        security_database_references = article_dds[3].get_text()
        more_information = article_dds[4].get_text()
        if len(article_dds) > 5:
            fixed_in = article_dds[5].get_text()
        else:
            fixed_in = ""
        datas.append({
            "date":date,
            "name":name,
            "security_advisory":security_advisory,
            "affected_packages":affected_packages,
            "vulnerable":vulnerable,
            "security_database_references":security_database_references,
            "more_information":more_information,
            "fixed_in":fixed_in
        })  
    return datas

#爬新版本网页并返回一个字典列表
def new_parse_single_html(html):
    soup = BeautifulSoup(html,'html.parser')
    article_date = soup.find("h1").get_text().replace("Security Advisories from ","")
    article_tts = (
        soup.find("div",id="content")
            .find_all("tt")
    )
    article_strongs = (
        soup.find("div",id="content")
            .find_all("strong")
    )
    datas = []
    for i in range(len(article_tts)):
        date=article_tts[i].get_text()
        name=article_strongs[i].get_text()
        info_indexs=article_strongs[i].find("a")["href"].replace(".","")
        url=f"https://www.debian.org/security/"+article_date+info_indexs
        subhtml = download_html(url)
        subsoup = BeautifulSoup(subhtml,'html.parser')
        security_advisory = subsoup.find("h2").get_text()
        article_dds = (
        subsoup.find("div",id="content")
            .find("dl")
            .find_all("dd")
        )
        if len(article_dds) > 4:
            affected_packages = article_dds[1].get_text()
            vulnerable = article_dds[2].get_text()
            security_database_references = article_dds[3].get_text()
            more_information = article_dds[4].get_text()
            if len(article_dds) > 5:
                fixed_in = article_dds[5].get_text()
            else:
                fixed_in = ""
        else:
            affected_packages = ""
            vulnerable = article_dds[1].get_text()
            security_database_references = article_dds[2].get_text()
            more_information = article_dds[3].get_text()
            fixed_in = ""
        datas.append({
            "date":date,
            "name":name,
            "security_advisory":security_advisory,
            "affected_packages":affected_packages,
            "vulnerable":vulnerable,
            "security_database_references":security_database_references,
            "more_information":more_information,
            "fixed_in":fixed_in
        })  
    return datas

all_datas=[]
for html in old_htmls:
    all_datas.extend(old_parse_single_html(html))
for html in new_htmls:
    all_datas.extend(new_parse_single_html(html))

#将字典列表数据放入Excel中
from openpyxl  import Workbook
def inputexcel(inputdata,outputfile):
    wb = Workbook()
    sheet = wb.active
    fd = inputdata[0]
    for zm,i in list(zip([chr(letter).upper() for letter in range(65, 91)],range(len(list(fd.keys()))))):
        sheet[zm+str(1)].value = list(fd.keys())[i]
    j = 2
    for item in inputdata:
        for zm, key in list(zip([chr(letter).upper() for letter in range(65, 91)], list(fd.keys()))):
            sheet[zm+str(j)] = item[key]
        j += 1
    wb.save(outputfile)
inputexcel(all_datas,'debian_data.xlsx')
