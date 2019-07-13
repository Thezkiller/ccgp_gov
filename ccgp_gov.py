# -*- coding: utf-8 -*-
import os
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from multiprocessing.dummy import Pool as ThreadPool
from selenium.common.exceptions import NoSuchElementException

def sub_crawler(website_list):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  #无头chrome
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(website_list)
    # time.sleep(0.8)
    print(website_list)  #检错

    try:
        item_name = driver.find_element_by_xpath("//*[@id='detail']/div[2]/div/div[2]/div/div[1]/h2").text
        budget_amount = driver.find_element_by_xpath("//*[@id='detail']/div[2]/div/div[2]/div/div[2]/table/tbody/tr[11]/td[2]").text
        admin_area = driver.find_element_by_xpath("//*[@id='detail']/div[2]/div/div[2]/div/div[2]/table/tbody/tr[5]/td[2]").text
        with open("{}/project.csv".format(os.getcwd()), "a") as csv:
            csv.write("{}\t{}\t{}\t{}\n".format(item_name, budget_amount, admin_area, website_list)) 
        print ("已爬取{}\n{}\n{}\n{}\n".format(item_name, budget_amount, admin_area, website_list))

    except NoSuchElementException as msg:
        print ("{}: 页面非正常表格格式，需手动标注".format(msg))
        with open("{}/project.csv".format(os.getcwd()), "a") as csv:
            csv.write("{}\t{}\t{}\t{}\n".format("异常版面，需手动标注", "异常版面，需手动标注", "异常版面，需手动标注", website_list)) 
        print ("已爬取{}\n{}\n".format("异常版面，需手动标注", website_list))

    driver.quit()

def crawler(url,page_num,threadNum):
    # driver = webdriver.Chrome()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  #无头chrome
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)

    driver.maximize_window()
    driver.get(url)

    # 开始爬信息 (第一页)
    website_list = [elemente.get_attribute("href")for elemente in driver.find_elements_by_css_selector("a[style='line-height:18px']")]
    # time.sleep(0.3)
    left_page = page_num - 1
    # 剩余页 爬信息
    while left_page > 0:
        driver.find_element_by_css_selector("a[class='next']").click()
        for elemente in driver.find_elements_by_css_selector("a[style='line-height:18px']"):
            website_list.append(elemente.get_attribute("href"))
        print("剩余{}页地址爬取，{}页地址信息分析中".format(left_page,left_page+1),end='\r')
        # time.sleep(0.5)
        left_page -= 1

    print(len(website_list)) # 爬到的信息条数
    crawls_num = len(website_list)
    source_num = int(driver.find_element_by_xpath("/html/body/div[5]/div[1]/div/p[1]/span[2]").text) # 检索信息条数

    
    # 
    if crawls_num == source_num:
        print("爬取的信息条数与检索信息条数一致")
        driver.quit()
        with open("{}/project.csv".format(os.getcwd()), "w") as csv:
            csv.write("采购项目名称\t预算金额\t行政区域\t网址\n")
        pool = ThreadPool(processes=threadNum)
        pool.map(sub_crawler,website_list)
        pool.close()
        pool.join()
    
    else:
        print("爬取的信息条数与检索信息条数不一致,请检查")

    


if __name__ == "__main__":


    page_num =  48
    threadNum = 8
    # url要事先把选项选好，还有页数记好
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=++0&bidType=1&dbselect=bidx&kw=%E8%88%B9%E8%88%B6&start_time=2018%3A01%3A01&end_time=2019%3A01%3A01&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='

    crawler(url,page_num,threadNum)
