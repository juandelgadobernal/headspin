#!/usr/bin/env python3
import time

from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from datetime import datetime
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.action_chains import ActionChains
from subprocess import check_call, check_output

#Create Desired capabilities
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['udid'] = 'emulator-5554'
desired_caps['androidNaturalOrientation	'] = 'false'
#Create driver
driver = webdriver.Remote("http://127.0.0.1:4724/wd/hub", desired_caps)
driver.implicitly_wait(10)

photo_name = "test5.jpeg"
email_to_send = "juandedios.delgadobernal@gmail.com"
email_subject = "This is a code challenger"
email_compose = "Please find below the image attached"


def photo_resoiurce_id_xpath(file_created_timestamp):
    HH = ""

    file_creation_date = file_created_timestamp[0:10]
    file_creation_date_format = datetime.strptime(file_creation_date, '%Y-%m-%d').date()
    file_creation_date_format = file_creation_date_format.strftime("%b %d, %Y")

    file_creation_time = file_created_timestamp[11:19]
    file_creation_time_format = datetime.strptime(file_creation_time, '%H:%M:%S').time()
    file_creation_time_format = file_creation_time_format.strftime("%I:%M:%S %p")
    HH_0 = file_creation_time_format[0:1]
    MM_SS_TZ = file_creation_time_format[2:11]
    if HH_0 == "0":
        HH = file_creation_time_format[0:2]
        HH = HH.replace("0", "")
    else:
        HH = file_creation_time_format[0:2]
    file_creation_time_format_final = HH + MM_SS_TZ
    file_xpath = file_creation_date_format + " " + file_creation_time_format_final
    print("Xpath date in photo: {}".format(file_xpath))
    file_xpath_full = "Photo taken on " + file_xpath

    return file_xpath_full

def appium_swipe_right_left(driver):

    # landscape
    lstartx2 = 500
    lendx2 = 1385
    lstarty2 = 1272
    lendy2 = 450

    actions = ActionChains(driver)

    swipe_left = ActionChains(driver)
    swipe_left.w3c_actions = ActionBuilder(driver)
    swipe_left.w3c_actions.pointer_action.move_to_location(lstartx2, lstarty2)
    swipe_left.w3c_actions.pointer_action.pointer_down()
    swipe_left.w3c_actions.pointer_action.pause(2)
    swipe_left.w3c_actions.pointer_action.move_to_location(lendx2, lendy2)
    swipe_left.w3c_actions.pointer_action.release()
    swipe_left.perform()


def appium_click_by_coordinates(driver, val_x, val_y ):
    #actions = ActionChains(driver)
    coordinate_x = val_x
    coordinate_y = val_y

    click_coordinates = ActionChains(driver)
    click_coordinates.w3c_actions = ActionBuilder(driver)
    click_coordinates.w3c_actions.pointer_action.move_to_location(coordinate_x, coordinate_y).click()
    click_coordinates.perform()
    time.sleep(2)

def appium_push_file(driver, photo_name):
    """

    :return:
    """
    xp_photo_resource_id =""
    file_name = photo_name
    dut_path = 'sdcard/Download/' + file_name
    filepath = '/Users/juandelgado/PycharmProjects/projectHeadspin/test.jpeg'
    with open(file=filepath, mode='rb') as myfile:
        import base64
        encoded_file = base64.b64encode(myfile.read())
    # We need to decode to get rid of the b'' bytes literal for the upload to work
    if driver.push_file(dut_path, encoded_file.decode()):
        print("File Name: {} has been send successfully".format(file_name))
        output = check_output(['adb', 'shell', 'stat', '-c %y', dut_path])
        lines = output.splitlines()
        file_created_timestamp_date = lines[0].split()[0]
        file_created_timestamp_time = lines[0].split()[1]
        file_created_timestamp_date = file_created_timestamp_date.decode('ascii')
        file_created_timestamp_time = file_created_timestamp_time.decode('ascii')
        file_created_timestamp = file_created_timestamp_date + " " + file_created_timestamp_time
        print("file_created_timestamp: {}".format(file_created_timestamp))
        xp_photo_resource_id = photo_resoiurce_id_xpath(file_created_timestamp)
        print("Full Xpath date photo with resource_id to use: {}".format(xp_photo_resource_id))
    return xp_photo_resource_id

def appium_open_image(driver, file_name):
    photo_name = file_name

    driver.press_keycode(3)
    time.sleep(3)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Files")').click()
    time.sleep(3)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("'+photo_name+'")').click()
    time.sleep(3)
    driver.press_keycode(3)

def launch_photos(driver, str_xp_photo_resource_id, file_name):
    photo_name = file_name

    # Launch Photos App
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Photos")').click()
    #time.sleep(5)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Not now")').click()
    #time.sleep(5)

    #Photos App -> Library
    #appium_click_by_coordinates(driver, 1260, 2280)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Library")').click()

    #Photos App -> Library -> Click Folder
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Download")').click()
    #Photos App -> Library -> Click Photo
    driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="'+str_xp_photo_resource_id+'"]').click()
    time.sleep(3)
    #Landscape
    driver.orientation = "LANDSCAPE"
    time.sleep(3)
    #appium_click_by_coordinates(driver, 2475, 181)
    driver.find_element(AppiumBy.XPATH,'//android.widget.ImageView[@content-desc="More options"]').click()

    time.sleep(3)
    appium_swipe_right_left(driver)

    #Validate Photo Name
    element = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")

    flag_image_found = False
    for x in element:
        name_image = x.text
        #print(name_image)
        if name_image.find(photo_name) != -1:
            photo_name_found_path = name_image
            print(photo_name_found_path)
            flag_image_found = True

    if flag_image_found:
        print("Image found in Photos App", photo_name)
    else:
        print("Photo does not exist")

def send_phot_email(driver,email_to_send, email_subject, email_compose, str_xp_photo_resource_id):

    email = email_to_send
    email_sub = email_subject
    email_comp = email_compose

    driver.orientation = "portrait"
    driver.press_keycode(3)
    time.sleep(1)

    #Gmail
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Gmail")').click()
    time.sleep(15)

    #Compose email
    #appium_click_by_coordinates(driver, 1150, 2055)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Compose")').click()
    time.sleep(5)


    #Enter eMail
    to = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText')
    to.set_value(email)
    time.sleep(2)
    driver.press_keycode(66)
    time.sleep(2)

    comp = driver.find_element(AppiumBy.ID, "com.google.android.gm:id/subject")
    comp.set_value(email_sub)
    time.sleep(2)
    driver.press_keycode(66)
    time.sleep(2)

    #Attach File
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'UiSelector().description("Attach file")').click()
    time.sleep(2)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Attach file")').click()
    time.sleep(3)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Photos")').click()
    time.sleep(3)
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Download")').click()
    time.sleep(3)

    #Select Photo
    #appium_click_by_coordinates(driver, 1333, 183)
    driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="'+str_xp_photo_resource_id+'"]').click()
    time.sleep(3)

    #driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Today")').click()
    #time.sleep(3)
    #driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'text("Today")').click()
    driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Done"]').click()
    time.sleep(3)

    compose = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@text=""]')
    compose.set_value(email_comp)
    time.sleep(2)

    #Send mail
    send = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Send"]')
    send.click()
    time.sleep(2)

#---------------------------------------------------------------------------

if __name__ == "__main__":

    str_xp_photo_resource_id = appium_push_file(driver, photo_name)
    appium_open_image(driver, photo_name)
    launch_photos(driver, str_xp_photo_resource_id, photo_name)
    send_phot_email(driver, email_to_send, email_subject, email_compose, str_xp_photo_resource_id)