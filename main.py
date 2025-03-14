import time
from selenium import webdriver

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import data


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    taxi_button = (By.CLASS_NAME, "button round")
    set_rote = (By.CLASS_NAME, "dst-picker")
    comfort_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    select_phone_insert = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    number = (By.XPATH, '//*[@id="phone"]')
    next_button = (By.XPATH, '//*[text()="Siguiente"]')
    click_code = (By.ID, 'code_input')
    code = (By.ID, 'code')
    select_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    phone_send_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    payment_method = (By.CLASS_NAME, "pp-button")
    card_add_button = (By.CLASS_NAME, "pp-plus")
    credit_click = (By.CLASS_NAME, 'card-number-input')
    add_credit_card = (By.XPATH, '//*[@id="number"]')
    card_cvv = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code"]')
    agree_card = (By.XPATH, '//*[text()="Agregar"]')
    x_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    cell_next = (By.XPATH, '//*[text()="Confirmar"]')
    driver_message = (By.XPATH, '//*[@id="comment"]')
    write_message = (By.CSS_SELECTOR, "#comment")
    requests_button = (By.CLASS_NAME, "reqs-head")
    blanket_and_scarves = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    ice_cream_counter = (By.CLASS_NAME, "counter-plus")
    taxi_search_button = (By.CLASS_NAME, "smart-button-main")
    modal_taxi = (By.CLASS_NAME, "order-details")  # cambiar a Class name

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def select_taxi_button(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.select_taxi).click()

    def select_comfort_rate(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.comfort_button).click()

    def select_number_button(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.select_phone_insert).click()

    def add_phone_number(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.number).send_keys(data.phone_number)

    def set_phone(self):
        self.driver.implicitly_wait(30)
        self.select_number_button()
        self.driver.implicitly_wait(30)
        self.add_phone_number()

    def the_next_button(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.next_button).click()

    def send_cell_info(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.cell_next).click()

    def get_phone(self):
        return self.driver.find_element(*self.phone_input).get_property('value')

    def code_click(self):
        self.driver.find_element(*self.click_code).click()

    def code_number(self):
        self.driver.implicitly_wait(20)
        phone_code = retrieve_phone_code(driver=self.driver)
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.code).send_keys(phone_code)

    def get_code(self):
        return self.driver.find_element(*self.code).get_property('value')

    def pay_click(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.payment_method).click()

    def add_click(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.card_add_button).click()

    def click_card(self):
        self.driver.implicitly_wait(30)
        self.pay_click()
        self.driver.implicitly_wait(30)
        self.add_click()

    def number_click(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.credit_click).click()

    def number_input(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.add_credit_card).send_keys(data.card_number)

    def card_input(self):
        self.driver.implicitly_wait(20)
        self.number_click()
        self.driver.implicitly_wait(20)
        self.number_input()

    def get_card_input(self):
        return self.driver.find_element(*self.add_credit_card).get_property('value')

    def cvv_add(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.card_cvv).click()

    def code_card_input(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.card_cvv).send_keys(data.card_code)

    def cvv_code(self):
        self.driver.implicitly_wait(20)
        self.code_card_input()

    def get_cvv_card(self):
        return self.driver.find_element(*self.card_cvv).get_property('value')

    def registered_card(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.agree_card).click()

    def add_card(self):
        self.driver.implicitly_wait(30)
        self.card_input()
        self.driver.implicitly_wait(30)
        self.cvv_code()
        self.driver.implicitly_wait(30)
        self.registered_card()

    def close_window(self):
        self.driver.implicitly_wait(30)
        self.driver.find_element(*self.x_button).click()

    def write_drive_message(self, message):
        self.driver.implicitly_wait(20)
        message_field = self.driver.find_element(*self.driver_message)
        message_field.send_keys(message)

    def get_message(self):
        return self.driver.find_element(*self.driver_message).get_property('value')

    def request_blanket_and_tissues(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.blanket_and_scarves).click()

    def get_blanket_and_scarves(self):
        return self.driver.find_element(*self.blanket_and_scarves).get_property('value')

    def request_ice_cream(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.ice_cream_counter).click()
        self.driver.find_element(*self.ice_cream_counter).click()

    def get_ice_cream(self):
        return self.driver.find_element(*self.ice_cream_counter).get_property('value')

    def search_taxi(self):
        self.driver.implicitly_wait(20)
        self.driver.find_element(*self.taxi_search_button).click()

    def get_taxi(self):
        return self.driver.find_element(*self.taxi_search_button).get_property('value')

    def wait_for_driver_info(self):
        self.driver.implicitly_wait(120)
        self.driver.find_element(*self.modal_taxi)
        self.driver.implicitly_wait(120)


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        time.sleep(10)
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_full_taxi_request_process(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # 1.Configurar la dirección
    def test_set_route(self):
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(10)  # cambio del timeslep
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # 2.Seleccionar la tarifa Comfort.
    def test_pick_comfort(self):
            routes_page.select_taxi_button()

        # 3. Rellenar el número de teléfono
    def test_set_phone_number(self):
        phone_number = data.phone_number
        self.driver.implicitly_wait(10)  # Cambio de time.sleep a implicitly_wait
        routes_page.set_phone(phone_number)  # Pasar el número como argumento
        assert routes_page.get_phone() == phone_number

        # 4.Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
            self.routes_page.validate_card_number(data.card_number)

        # 5.Escribir un mensaje para el controlador
    def test_set_message(self):
        message = data.message_for_driver
        routes_page.write_drive_message(message)
        assert routes_page.get_message() == data.message_for_driver  # agregar assert

        # 6.Pedir una manta y pañuelos
    def test_set_requirements(self):
        self.driver.implicitly_wait(20)  # cambio del timeslep
        routes_page.request_blanket_and_tissues()
        assert routes_page.get_blanket_and_scarves() == routes_page.request_blanket_and_tissues()  # agregar assert

        # 7.Pedir 2 helados
     def test_call_taxi(self):
        self.driver.implicitly_wait(20)  # cambio del timeslep
        routes_page.request_ice_cream()
        assert routes_page.get_ice_cream() == routes_page.request_ice_cream()  # agregar Assert

        # 8.Aparece el modal para buscar un taxi.
    def test_wait_driver_details(self):
        self.driver.implicitly_wait(50)  # cambio del timeslep
        routes_page.search_taxi()

        # 9.Esperar a que aparezca la información del conductor en el modal (Esta prueba es opcional)
    def test_wait_for_driver_info(self):
        self.driver.implicitly_wait(50)  # aumentar tiempo
        routes_page.wait_for_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()