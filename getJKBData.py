#!/usr/bin/env python
# coding: utf-8
# %%

# %%


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, pprint, os
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import pandas as pd
from pprint import pprint


# %%


def create_instance(target_url):
    options = Options()
    options.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # ChromeDriver 83.0.4103.14
    webdriver_path = os.getcwd()+"\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get(target_url)
    driver.maximize_window()
    return driver


# %%


def open_browser_and_login(url, elm_username_name, elm_password_name, username, password, elm_submit_xpath):
    driver = create_instance(url)
    user_element = driver.find_element_by_id(elm_username_name)
    password_element = driver.find_element_by_id(elm_password_name)
    user_element.send_keys(username)
    password_element.send_keys(password)
    driver.find_element_by_xpath(elm_submit_xpath).click()
    time.sleep(1)
    return driver


# %%


def open_tab(driver, tab_number, url):
    driver.execute_script("window.open('about:blank', '"+tab_number+"');")
    driver.switch_to.window(tab_number)
    driver.get(url)
    time.sleep(1)


# %%


def enterStartTime(startTime):
    timezone = driver.find_element_by_xpath("//span[@ng-show='!custom_time_state']").click()
    time.sleep(1)
    js = "$('input[data-id=taskdetail_timeone]').removeAttr('readonly')"
    js = "$('input[data-id=taskdetail_timeone]').attr('readonly',false)"
    driver.execute_script(js)
    driver.find_element_by_xpath("//input[@data-id='taskdetail_timeone']").clear()
    driver.find_element_by_xpath("//input[@data-id='taskdetail_timeone']").send_keys(startTime)
    time.sleep(1)
    driver.find_element_by_xpath("//button[@class='ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all']").click()
    time.sleep(1)


# %%


def enterEndTime(endTime):
    js = "$('input[data-id=taskdetail_timetwo]').removeAttr('readonly')"
    js = "$('input[data-id=taskdetail_timetwo]').attr('readonly',false)"
    driver.execute_script(js)
    driver.find_element_by_xpath("//input[@data-id='taskdetail_timetwo']").clear()
    driver.find_element_by_xpath("//input[@data-id='taskdetail_timetwo']").send_keys(endTime)
    time.sleep(1)
    driver.find_element_by_xpath("//button[@class='ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all']").click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[@class='ng-binding']").click()


# %%


def getTabsURLandFileName():
    # read urls
    with open(os.getcwd()+"\\jkbURLs.txt",'r+') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    fileNameList = content[0::2]
    # delete comments
    del content[0::2]
    # create a list for storing urls
    index = 0
    china_area_url= list(range(0, len(content)))
    for url in content:
        china_area_url[index] = url
        index +=1
    # create a list for storing tabs
    index = 0
    tabList = list(range(0, len(content)))
    for tab in tabList:
        tabList[index] = 'tab' + str(tab)
        index +=1
    return [tabList, china_area_url, fileNameList]


# %%


def organizePageAndGetPageLen():
    driver.find_element_by_xpath("//*[@id='order_check_time']/span[2]").click()#the early time
    time.sleep(1)
    driver.find_element_by_xpath("//option[@value='100']").click()#display 100 list
    time.sleep(1)
    length = driver.find_elements_by_xpath("//div[@class='page_container']//div[@class='pages']//a")#page
    return length


# %%


def clickPageAndGetSinglePageData(pageNumber):
    page = driver.find_element_by_link_text(pageNumber).click()
    time.sleep(1)
    info = driver.find_elements_by_id('snapshotlist')[0].text
    time.sleep(1)
    return info


# %%


def getAllPagesData(length):
    AlldataList = []
    for count in length:
        pageData = clickPageAndGetSinglePageData(count.text)
        add_n = (pageData  + '\n')
        row_type = ''.join(add_n)
        replace_name = row_type.replace(' ', ',').replace('不可用','no available').replace('测试成功', 'success').replace('可用', 'available').replace('数据包全部丢弃','packet not found')
        split_n = replace_name.split('\n')
        split_n.pop()
        AlldataList += split_n 
    return AlldataList


# %%


def combineAllCSVtoOneXLSX():
    # get path where csv files locate
    newdir = os.getcwd()+"\\CSVFILE" 
    # list csv file names and put into a list
    names = os.listdir(newdir)
    writer = pd.ExcelWriter('combined.xlsx')
    for name in names:
        path = os.path.join(newdir, name)
        data = pd.read_csv(path, encoding="utf8", index_col=0)
        data.to_excel(writer, sheet_name=name)
    writer.save()


# %%


'''
data2 format is 
{"username": "value", 
 "password": "value", 
 "url": "value", 
 "element_username_id": "value", 
 "element_password_id": "value", 
 "element_submit_xpath": "value"
}

'''

# JKB use id for element of username and password
data2 = { "JKB_data": {"username": "your_username",
                       "password": "your_password",
                       "url": "https://monitoring.cloudwise.com/users/login",
                       "element_username_id": "email",
                       "element_password_id": "pwd",
                       "element_submit_xpath":  "//button[@id='sigin_btn']"}  
        }


# %%


# main driver
driver = open_browser_and_login(data2["JKB_data"]["url"], 
                       data2["JKB_data"]["element_username_id"], 
                       data2["JKB_data"]["element_password_id"], 
                       data2["JKB_data"]["username"], 
                       data2["JKB_data"]["password"], 
                       data2["JKB_data"]["element_submit_xpath"]
                      )


# %%


tabsURLsAndFileNamesList = getTabsURLandFileName()


# %%


# enter star time and end time
IP = tk.Tk()
IP.withdraw()

#start time
startTime = simpledialog.askstring(title="Start time", prompt="Please enter a time ex:2020-03-01 21:00")
messagebox.showinfo(title="START TIME",message="The start time is: " + startTime)

#end time
endTime = simpledialog.askstring(title="End time", prompt="Please enter a time ex:2020-03-02 21:00")
messagebox.showinfo(title="END TIME",message="The end time is : " + endTime)


# %%


# create a document
try:
    os.mkdir(os.getcwd()+"\\CSVFILE")
except os.error:
    pass


# %%


try:
    for x in range(0, len(tabsURLsAndFileNamesList[0])):
        open_tab(driver, str(tabsURLsAndFileNamesList[0][x]), tabsURLsAndFileNamesList[1][x])
        enterStartTime(startTime)
        enterEndTime(endTime)
        time.sleep(2)
        length = organizePageAndGetPageLen()
        allPagesData = getAllPagesData(length)
        result = pd.DataFrame(allPagesData)
        result.to_csv(os.getcwd() + "\\CSVFILE\\" + tabsURLsAndFileNamesList[2][x] + '.csv',index=False, header=False)
    #combine all csv to one
    combineAllCSVtoOneXLSX()
    driver.quit()
    messagebox.showinfo(title="Completed",message="The process has been completed successfully!!")
except Exception as e:
    print("The erro message is below: \n"+ e)
    driver.quit()
    messagebox.showerror(title="Failed!!!",message="The erro message is as below: \n" + e)

