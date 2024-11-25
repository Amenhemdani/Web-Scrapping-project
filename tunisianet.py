from selenium import webdriver
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.chrome.options import Options
from csv import writer
import time
import json


def to_json(data):
    json_object = json.dumps(data)
    with open("pc.json", "a") as outfile: 
        outfile.write(json_object + ",\n")

def add_to_csv(data):
    with open('pc.csv', 'a') as f_object:
        dictwriter_object = writer(f_object)
        dictwriter_object.writerow(data)
        f_object.close()

def initialize_csv_file():
    with open('pc.csv', 'w') as f_object:
        data = ["category","title","price","reference","description","image","disponibility","Operating_system","Processor","Ref_Processor","Memory","Hard_Drive","Graphics_Card","ref_Graphics_Card","Screen_Size","Screen_Type","Touch_screen","Network","Camera","Guarantee","Color"]
        dictwriter_object = writer(f_object)
        dictwriter_object.writerow(data)
        f_object.close()   

def initialize_json():
    with open('pc.json', 'w') as f_object:
        f_object.write('[')

def final_json():
    with open('pc.json', 'a') as f_object:
        f_object.write(']')

def to_dict(list_description):
    dict_description = {}
    for i in range(0,len(list_description)-1,2):
        dict_description[list_description[i]] = list_description[i+1]
    return dict_description


options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")


def main(driver,url,category):
    number_of_pages = driver.find_element(By.XPATH, '//ul[@class="page-list clearfix"]/li[5]').text
    for i in range(1,int(number_of_pages)+1):
        driver.get(f"{url}?page={i}&order=product.price.asc")

        elements = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-title')))

        links = []
        article_title = []
        for elem in elements:
            links.append(WebDriverWait(elem,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2.product-title > a[href]"))).get_attribute("href"))
            article_title.append(WebDriverWait(elem,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"h2.product-title > a[href]"))).text.replace("Pc Portable ",""))

        for link,title in zip(links,article_title):
            driver.get(link)
            description_text = driver.find_element(By.CLASS_NAME, 'prodes').text.replace("\n"," ")
            ref = driver.find_element(By.CLASS_NAME, 'product-reference').text.replace("Référence : ","")
            price = driver.find_element(By.CLASS_NAME, 'current-price').text
            image = driver.find_element(By.CLASS_NAME, 'selected').get_attribute("src")
            dispo = driver.find_element(By.ID, 'stock_availability').text.replace("Disponibilté : ","")
            
            item = {"category":category,"title":title,"price":price,"reference":ref,"description":description_text,"image":image,"disponibility":dispo}

            descriptions = driver.find_element(By.CLASS_NAME, 'data-sheet').text

            while len(descriptions) == 0:
                show_details = driver.find_element(By.LINK_TEXT,'Détails').click()
                descriptions = driver.find_element(By.CLASS_NAME, 'data-sheet').text

            list_of_description = descriptions.split("\n")
            dict_description = to_dict(list_of_description)
            item.update(dict_description)
            data = item.values()
            add_to_csv(data)
            to_json(item)
    

if __name__ == "__main__":
    driver = webdriver.Chrome(options=options)
    urls = ["https://www.tunisianet.com.tn/301-pc-portable-tunisie","https://www.tunisianet.com.tn/681-pc-portable-gamer","https://www.tunisianet.com.tn/703-pc-portable-pro"]
    initialize_csv_file()
    initialize_json()
    categories = ["pc_portable","pc_portable_gamer","pc_portable_pro"] 
    for category,url in zip(categories,urls):
        driver.get(url)
        main(driver,url,category)
    final_json()
    driver.quit()