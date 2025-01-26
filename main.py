from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time
from consts import FORM_URL, DATABASE_PATH


def load_database():
    return pd.read_csv(DATABASE_PATH)

def is_valid_selection(selection, data_options):
    return 0 <= selection < len(data_options)

def select_record(data_options):
    print("Registros disponibles:")
    for idx, name in enumerate(data_options['name']):
        print(f"{idx + 1}. {name}")
    
    selection = -1
    while not is_valid_selection(selection, data_options):
        try:
            selection = int(input("\nSeleccione el número del registro a utilizar: ")) - 1
            if not is_valid_selection(selection, data_options):
                print("Selección fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
            selection = -1
    
    return data_options.iloc[selection]

def start_driver():
    chrome_install = ChromeDriverManager().install()

    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")
    service = ChromeService(chromedriver_path)
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fill_input_field(web_driver_wait, field_id, value):
    input_element = web_driver_wait.until(EC.element_to_be_clickable((By.ID, field_id)))
    input_element.clear()
    input_element.send_keys(str(value))

def fill_address(web_driver_wait, data):
    address_input = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_20")))
    
    web_driver_wait.until(
        lambda driver: driver.execute_script(
            'return document.querySelector("#input_1_20").getAttribute("class").includes("pac-target-input")'
        )
    )

    address_input.clear()
    address_input.send_keys(data['address'])
    web_driver_wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "pac-container"))
    )
    
    address_input.send_keys(Keys.RETURN)

def fill_text_fields(web_driver_wait, data):
    fill_input_field(web_driver_wait, "input_1_1_3", data['name'])
    fill_input_field(web_driver_wait, "input_1_2", data['email'])
    fill_input_field(web_driver_wait, "input_1_5", data['phone'])
    
    fill_address(web_driver_wait, data)

def fill_select_field(web_driver_wait, field_id, value):
    select_element = web_driver_wait.until(EC.element_to_be_clickable((By.ID, field_id)))
    select_element.click()
    select_element.send_keys(str(value))
    select_element.send_keys(Keys.RETURN)
    time.sleep(1)

def fill_select_fields(web_driver_wait, data):
    fill_select_field(web_driver_wait, "input_1_24", data['structureType'])
    
    if data['structureType'] == 'Techo' or data['structureType'] == 'Carport':
        fill_select_field(web_driver_wait, "input_1_26", data['roofType'])
        
        if 'Otro' in data['roofType']:
            fill_input_field(web_driver_wait, "input_1_29", data['roofType'].split('-')[1])
        
        if data['structureType'] == 'Techo':
            fill_select_field(web_driver_wait, "input_1_25", data['roofInclination'])
            
    fill_select_field(web_driver_wait, "input_1_34", data['reference'])

def fill_slider(web_driver_wait, data):
    slider = web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "noUi-handle")))
    slider_container = web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "noUi-base")))
    
    total_width = slider_container.size['width']
    min_value = float(slider.get_attribute("aria-valuemin"))
    max_value = float(slider.get_attribute("aria-valuemax"))
    target_value = float(data['accountCost'])
    current_value = float(slider.get_attribute("aria-valuenow"))
    
    target_percentage = (target_value - min_value) / (max_value - min_value)
    current_percentage = (current_value - min_value) / (max_value - min_value)
    
    pixel_difference = int((target_percentage - current_percentage) * total_width)
    
    action = webdriver.ActionChains(web_driver_wait._driver)
    action.click_and_hold(slider)
    action.move_by_offset(pixel_difference, 0)
    action.release()
    action.perform()

def upload_file(web_driver_wait, data):
    if 'fileRoute' in data and not pd.isna(data['fileRoute']):
        file_path = os.path.join('data', 'uploadFiles', data['fileRoute'])
        file_input = web_driver_wait.until(EC.presence_of_element_located((By.ID, "input_1_27")))
        file_input.send_keys(os.path.abspath(file_path))

def fill_form(driver, data):
    try:
        wait = WebDriverWait(driver, 10)
        
        wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        fill_text_fields(wait, data)
        fill_select_fields(wait, data)
        fill_slider(wait, data)
        upload_file(wait, data)

    except Exception as e:
        print(f"Error al rellenar el formulario: {str(e)}")

def main():
    data_options = load_database()
    selected_data = select_record(data_options)
    
    try:
        driver = start_driver()
        driver.get(FORM_URL)
        
        fill_form(driver, selected_data)
        
        input("\nPresione Enter para cerrar el navegador...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()