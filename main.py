from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from consts import FORM_URL, DATABASE_PATH
from time import sleep
from selenium.webdriver.common.keys import Keys

# TODO: Separar funciones en archivos
# TODO: juntar el como se rellenan los campos parecidos
# TODO: Ver que el driver se cierra correctamente
# TODO: Asegurarnos de que existe el documento

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
    name_input = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_1_3")))
    email_input = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_2")))
    phone_input = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_5")))
    
    name_input.clear()
    name_input.send_keys(data['name'])
    
    email_input.clear()
    email_input.send_keys(data['email'])
    
    phone_input.clear()
    phone_input.send_keys(str(data['phone']))
    
    fill_address(web_driver_wait, data)

def fill_select_fields(web_driver_wait, data):
    structure_select = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_24")))
    structure_select.click()
    structure_select.send_keys(data['structureType'])
    structure_select.send_keys(Keys.RETURN)
    
    if data['structureType'] == 'Techo' or data['structureType'] == 'Carport':
        roof_material_select = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_26")))
        roof_material_select.click()
        roof_material_select.send_keys(data['roofType'])
        roof_material_select.send_keys(Keys.RETURN)
        
        if data['structureType'] == 'Techo':
            roof_type_select = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_25")))
            roof_type_select.click()
            roof_type_select.send_keys(data['roofInclination'])
            roof_type_select.send_keys(Keys.RETURN)
            
    reference_select = web_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_34")))
    reference_select.click()
    reference_select.send_keys(data['reference'])
    reference_select.send_keys(Keys.RETURN)
    
def fill_slider(web_driver_wait, data):
    # NO BORRES ESTE COMENTARIO
    # slider = web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "noUi-handle")))

    # min_value = float(slider.get_attribute("aria-valuemin"))
    # max_value = float(slider.get_attribute("aria-valuemax"))
    # target_value = float(data['accountCost'])
    
    # percentage = (target_value - min_value) / (max_value - min_value)
    
    # offset = int(slider.size['width'] * percentage)
    
    # print(offset)
    
    # webdriver.ActionChains(web_driver_wait._driver).drag_and_drop_by_offset(slider, offset, 0).perform()
    
    
    web_driver_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "noUi-target")))
    target_value = float(data['accountCost'])
    
    script = f"document.querySelector('.noUi-target').noUiSlider.set({target_value})"
    web_driver_wait._driver.execute_script(script)

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
    
    driver = start_driver()
    
    try:
        driver.get(FORM_URL)
        
        fill_form(driver, selected_data)
        
        # Mantener la ventana abierta hasta que el usuario decida cerrarla
        input("\nPresione Enter para cerrar el navegador...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()