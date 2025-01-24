from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from consts import FORM_URL, DATABASE_PATH

# TODO: Separar funciones en archivos

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

def fill_basic_info(wait_driver_wait, data):
    
    nombre_input = wait_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_1_3")))
    email_input = wait_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_2")))
    telefono_input = wait_driver_wait.until(EC.element_to_be_clickable((By.ID, "input_1_5")))
    
    nombre_input.clear()
    nombre_input.send_keys(data['name'])
    
    email_input.clear()
    email_input.send_keys(data['email'])
    
    telefono_input.clear()
    telefono_input.send_keys(str(data['phone']))
    
    
def fill_form(driver, data):
    """Rellena el formulario con los datos seleccionados"""
    try:
        wait = WebDriverWait(driver, 10)
        
        wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        fill_basic_info(wait, data)
        
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