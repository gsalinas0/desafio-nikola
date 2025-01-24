from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
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

def fill_form(driver, data):
    """Rellena el formulario con los datos seleccionados"""
    try:
        # Esperar a que los elementos del formulario estén presentes
        wait = WebDriverWait(driver, 10)
        
        # Rellenar nombre
        nombre_input = wait.until(EC.presence_of_element_located((By.NAME, "nombre")))
        nombre_input.send_keys(data['nombre'])
        
        # Rellenar email
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(data['email'])
        
        # Rellenar teléfono
        telefono_input = driver.find_element(By.NAME, "telefono")
        telefono_input.send_keys(data['telefono'])
        
        # No enviamos el formulario automáticamente para permitir revisión
        print("\nFormulario rellenado. Por favor, revise los datos antes de enviar manualmente.")
        
    except Exception as e:
        print(f"Error al rellenar el formulario: {str(e)}")

def main():
    data_options = load_database()
    selected_data = select_record(data_options)
    
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Abrir la página
        driver.get(FORM_URL)
        
        # Rellenar el formulario
        # fill_form(driver, selected_data)
        
        # Mantener la ventana abierta hasta que el usuario decida cerrarla
        input("\nPresione Enter para cerrar el navegador...")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()