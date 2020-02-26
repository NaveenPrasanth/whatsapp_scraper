"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import configparser
import json
import re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = configparser.RawConfigParser()
    config_file_path = 'settings.txt'
    config_parser.read(config_file_path)

    browser = config_parser.get('config', 'BROWSER')
    browser_path = config_parser.get('config', 'BROWSER_PATH')
    page = config_parser.get('config', 'PAGE')

    settings = {
        'browser': browser,
        'browser_path': browser_path,
        'page': page
    }
    return settings


def load_driver(settings):
    """
    Load the Selenium driver depending on the browser
    (Edge and Safari are not running yet)
    """
    driver = ''
    if settings['browser'] == 'firefox':
        firefox_profile = webdriver.FirefoxProfile(settings['browser_path'])
        driver = webdriver.Firefox(firefox_profile)
    elif settings['browser'] == 'edge':
        pass
    elif settings['browser'] == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-data-dir=" +
                                    settings['browser_path'])
        driver = webdriver.Chrome(chrome_options=chrome_options)
    elif settings['browser'] == 'safari':
        pass

    return driver


def get_path_hierarchy(element, path_list):

    if 'html' == element.tag_name:
        path_list.append(element.tag_name)
        return
    else:
        path_list.append(element.tag_name)
        print(path_list)
        get_path_hierarchy(element.find_element_by_xpath(".."), path_list)
        return path_list


def scroll_till_full_two_days_available(driver, chat_window):
    current_string = chat_window.text
    result = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{4}', current_string)
    today_only_reference = re.search(r'.*Messages you send to this chat and calls.*', current_string)
    days_result = re.findall(r'.*DAY\n', current_string)
    today = "TODAY\n"
    yesterday = "YESTERDAY\n"
    if today in days_result:
        days_result.remove(today)
    if yesterday in days_result:
        days_result.remove(yesterday)

    if result is None and len(days_result) < 1 and today_only_reference is None:
        driver.execute_script("arguments[0].scrollTop = -250", chat_window)
        scroll_till_full_two_days_available(driver, chat_window)
        return chat_window
    else:
        return chat_window


def find_images_and_download_with_time(driver, chat_text):
    images_list = []
    #class name of images inside chat
    for img_element in chat_text.find_elements_by_class_name("_18vxA"):
        try:
            driver.execute_script("arguments[0].scrollIntoView()", img_element)
            img_element.click()
            try:
                img_element.click()

            except:
                pass
        #classname of images after enlarged
            img = driver.find_element_by_xpath("/html/body/div[1]/div/span[3]/div/div/div[2]/div[2]/div[2]/div/div/img")
            close_button = driver.find_element_by_xpath("//div[@role='button' and @title='Close']")
            close_button.click()
            images_list.append(img.screenshot_as_base64)
        except:
            pass

    return images_list


def fetch_msg_for_chatset(driver, settings):
    element = driver.find_element_by_xpath("//div[@tabindex='-1' and @data-tab='3']")
    print(element)
    all_chat_names = []

    for cache_element in element.find_elements_by_class_name("X7YrQ"):
        all_chat_names.append(cache_element.text)

    chat_dict = {}
    visited = []
    current_elements = element.find_elements_by_class_name("X7YrQ")

    while current_elements:
        visited_set = set(visited)
        current_elements_set = set(current_elements)
        current_elements = list(current_elements_set.difference(visited_set))
        if len(current_elements) < 1:
            break
        ele = current_elements[0]
        visited.append(ele)
        print(chat_dict)
        print("parsing element:", ele.text)
        #driver.execute_script("arguments[0].scrollIntoView()", ele)
        try:
            ele.click()
        except:
            continue
        chat_window = driver.find_element_by_class_name("_1_keJ")
        chat_text = scroll_till_full_two_days_available(driver, chat_window)
        all_images = find_images_and_download_with_time(driver, chat_text)
        chat_name = ele.text.split("\n")[0]
        #chat_dict[chat_name] = chat_text.text
        chat_dict[chat_name] = {}
        chat_dict[chat_name]["text"] = chat_text.text
        chat_dict[chat_name]["images"] = all_images

        current_elements = element.find_elements_by_class_name("X7YrQ")
    return chat_dict

    #path = get_path_hierarchy(test_ele, [])
    #print(path)

    #element.find_elements_by_class_name("X7YrQ")
    #driver.execute_script("arguments[0].scrollTop = 720", element[0].find_element_by_xpath(".."))
    #driver.execute_script("return document.body.scrollHeight")


def scroll_tester(driver, settings):
    left_side_pane = driver.find_element_by_xpath("//div[@id='pane-side']")


def search_chatter(driver, settings):
    """
    Function that search the specified user and activates his chat
    """

    while True:
        for chatter in driver.find_elements_by_xpath("//div[@class='X7YrQ']"):
            chatter_name = chatter.find_element_by_xpath(
                ".//span[@class='_19RFN']").text
            if chatter_name == settings['name']:
                chatter.find_element_by_xpath(
                    ".//div[contains(@class,'_2UaNq')]").click()
                return


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    settings = load_settings()
    driver = load_driver(settings)
    driver.implicitly_wait(10)

    driver.get(settings['page'])
    #scroll_tester(driver, settings)

    chat_dict = fetch_msg_for_chatset(driver, settings)
    with open('./result.json', 'w') as fp:
        json.dump(chat_dict, fp)
    # search_chatter(driver, settings)
    #
    # previous_in_message = None
    # while True:
    #     last_in_message, emojis = read_last_in_message(driver)
    #
    #     if previous_in_message != last_in_message:
    #         print last_in_message, emojis
    #         previous_in_message = last_in_message
    #
    #     time.sleep(1)


if __name__ == '__main__':
    main()
