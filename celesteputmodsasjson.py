from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException 
import time
# Functions

def convert_k_to_number(num):
    return int(1000*(float(num.rstrip(num[-1]))))

def format_date(date):
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    return "{d}/{m}/{y}".format(d=day,m=month,y=year)
    
def detect_difficulties(input_text):
    # Detects difficulties (Beginner, Intermediate, Advanced, Expert, Grandmaster) and return all diffs detected
    diffs_to_detect = ['green beginner', 'yellow beginner', 'red beginner', 'green intermediate', 'yellow intermediate', 'red intermediate', 'green advanced', 'yellow advanced', 'red advanced', 'green expert', 'yellow expert', 'red expert', 'green grandmaster', 'yellow grandmaster', 'red grandmaster', 'green gm', 'yellow gm', 'red gm']
    diffs_to_detect_basic = ["beginner", "intermediate", "advanced", "expert", "grandmaster", "gm", "gm+1"]
    diffs_detected = []
    input_text = input_text.lower()
    for diff in diffs_to_detect:
        if diff in input_text:
            diffs_detected.append(diff)
    if diffs_detected == []:
        for diff in diffs_to_detect_basic:
            if diff in input_text:
                diffs_detected.append(diff)
    return diffs_detected

def min_diff(diffs):
    diffs_to_detect = ['green beginner', 'yellow beginner', 'red beginner',"beginner", 'green intermediate', 'yellow intermediate', 'red intermediate',"intermediate", 'green advanced', 'yellow advanced', 'red advanced',"advanced", 'green expert', 'yellow expert', 'red expert',"expert", 'green grandmaster', 'yellow grandmaster', 'red grandmaster',"grandmaster", 'green gm', 'yellow gm', 'red gm','gm',"gm+1"]
    diffs_indexes = []
    for diff in diffs:
        diffs_indexes.append(diffs_to_detect.index(diff))
    return diffs_to_detect[min(diffs_indexes)]
    
def max_diff(diffs):
    diffs_to_detect = ['green beginner', 'yellow beginner', 'red beginner',"beginner", 'green intermediate', 'yellow intermediate', 'red intermediate',"intermediate", 'green advanced', 'yellow advanced', 'red advanced',"advanced", 'green expert', 'yellow expert', 'red expert',"expert", 'green grandmaster', 'yellow grandmaster', 'red grandmaster',"grandmaster", 'green gm', 'yellow gm', 'red gm',"gm","gm+1"]
    diffs_indexes = []
    for diff in diffs:
        diffs_indexes.append(diffs_to_detect.index(diff))
    return diffs_to_detect[max(diffs_indexes)]

with open("C:/Users/ethan/Desktop/celestemods.txt","r") as cmods:
    all_mods = cmods.readlines()
    
p = 0
for mod in all_mods:
    all_mods[p] = mod[:-1]
    p+=1
print(all_mods)

with open("C:/Users/ethan/Desktop/celestemapclassed.json","a") as cmodsclass :
    cmodsclass.write("[")

driver = webdriver.Firefox()

all_jsons = []

unicode_encode_error = []

for site in all_mods:
    driver.get(site)

    driver.implicitly_wait(2)

    title_element = driver.find_element(by=By.ID,value="PageTitle")
    title = title_element.get_attribute("innerText")
    title = title.removesuffix("\n- A Mod for Celeste.")
    try :
        li_like = driver.find_element(By.CLASS_NAME,"LikeCount.CountStat")
        likes = li_like.get_attribute("innerText")
        if "k" in likes : likes = convert_k_to_number(likes)
    except NoSuchElementException:
        likes = "not found"

    try :
        li_download = driver.find_element(By.CLASS_NAME,"DownloadCount.CountStat")
        downloads = li_download.get_attribute("innerText")
        if "k" in downloads : downloads = convert_k_to_number(downloads)
    except NoSuchElementException:
        downloads = "not found"

    try:
        li_views = driver.find_element(By.CLASS_NAME,"ViewCount.CountStat")
        views = li_views.get_attribute("innerText")
        if "k" in views : views = convert_k_to_number(views)
    except NoSuchElementException:
        views = "not found"

    try : 
        li_dateadded = driver.find_element(By.CLASS_NAME,"DateAdded.TimeStat")
        time_dateadded = li_dateadded.find_element(By.TAG_NAME,"time")
        date_added = time_dateadded.get_attribute("datetime")
        date_added = format_date(date_added)
    except NoSuchElementException:
        date_added = "not found"

    try :
        content_flow_element = driver.find_element(By.ID,"ItemProfileModule")
        richtext = content_flow_element.find_element(By.TAG_NAME,"article")
        description = richtext.get_attribute("innerText")
    except NoSuchElementException:
        description = "not found"

    diffs = detect_difficulties(description)
    if diffs != []:
        mini_diff = min_diff(diffs)
        maxi_diff = max_diff(diffs)
    else : 
        mini_diff = "not found"
        maxi_diff = "not found"

    map_json = """
        "name" : "{title}",
        "likes" : "{likes}",
        "downloads" : "{downloads}",
        "views" : "{views}",
        "date added" : "{date_added}",
        "difficulties detected" : "{diffs_detected}",
        "min diff" : "{min_diff}",
        "max diff" : "{max_diff}",
        "link" : "{site}"
        """.format(title=title, likes=likes, downloads=downloads, views=views, date_added=date_added, description=description, diffs_detected = diffs, min_diff=mini_diff, max_diff = maxi_diff,site=site)
    map_json = "{" + map_json + "},"
    all_jsons.append(map_json)
    print(map_json)
    try : 
        with open("C:/Users/ethan/Desktop/celestemapclassed.json","a") as cmodsclass :
            cmodsclass.write("%s\n" % map_json)
    except UnicodeEncodeError:
        print(site + " can't be written into file, skipped")
        unicode_encode_error.append(site)

with open("C:/Users/ethan/Desktop/celestemapclassed.json","a") as cmodsclass :
    cmodsclass.write("]")
    
print(unicode_encode_error)
# with open("celestemapclassed.txt","w") as cmodsclass :
#     for mod in all_jsons:
#         cmodsclass.write("%s" % mod)