from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

def display_options(lst):
    """Show all the options from a list.
    Make the user to choose a valid option."""
    print("OPTIONS")
    print("---------")
    while True:
        for i in range(len(lst)):
            print(f"{i + 1}- {lst[i]}")
        user_input = int(input("> ")) - 1
        try:
            return lst[user_input]
        except IndexError:
            continue
class Apartments:
    def __init__(self, chromedriver_path, **kwargs):
        """Initialize the attributes."""
        try:
            self.lang = kwargs["lang"].lower()
        except KeyError:
            pass
        else:
            if self.lang == "spanish":
                self.min_price, self.max_price, self.min, self.max = self.get_filters_spanish()
            else:
                self.min_price, self.max_price, self.min, self.max = self.get_filters_english()
        self.location = kwargs["usa_city"]
        self.chromedriver_path = chromedriver_path
        self.URL = "https://www.apartments.com/"
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path)

    def __str__(self):
        return f"{self.URL}"

    @classmethod
    def get_filters_english(cls):
        """Get user inputs. It will be easier to add the filters
         on the search bar."""
        min_price = input("Prices starts from: ")
        max_price = input("Price ends at: ")
        beds_min_options = ["No Min", "1 Bed", "2 Beds", "3 Beds", "4+ Beds"]
        beds_min = display_options(beds_min_options)
        beds_max_options = ["No Max", "Studio", "1 Bed", "2 Beds", "3 Beds"]
        beds_max = display_options(beds_max_options)
        return min_price, max_price, beds_min, beds_max

    @classmethod
    def get_filters_spanish(cls):
        """Añade filtros complementarios para precisar tu búsqueda."""
        min_precio = input("Minimo precio desde: ")
        max_precio = input("Maximo precio hasta: ")
        hab_min_opciones = ["Sin Mínimo", "1 habitación", "2 habitaciones", "3 habitaciones", "4+ habitaciones"]
        hab_min = display_options(hab_min_opciones)
        hab_max_opciones = ["Sin Máximo", "Estudio", "1 habitación", "2 habitaciones", "3 habitaciones"]
        hab_max = display_options(hab_max_opciones)
        return min_precio, max_precio, hab_min, hab_max

    def choose_lang_search(self) -> str:
        """Access the main page and returns the page that allows to
        change the filters for your researches."""
        driver = webdriver.Chrome(executable_path=self.chromedriver_path)
        driver.get(url=self.URL)
        try:
            if self.lang == "spanish":
                driver.find_element(By.ID, 'primaryButton').click()
            else:
                driver.find_element(By.ID, "secondaryButton").click()
        except AttributeError:
            driver.find_element(By.ID, "secondaryButton").click()
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, ".inputWrapper a").click()
        sleep(5)
        return driver.current_url

    def search_filters(self):
        """Add the parameters to precise your results.
        Returns a link with all the filters added."""
        sleep(5)
        self.driver.get(self.choose_lang_search())

        search_location = self.driver.find_element(By.ID, 'searchBarLookup')
        search_location.send_keys(self.location)
        search_location.send_keys(Keys.ENTER)
        sleep(5)

        rent_range = self.driver.find_element(By.ID, 'rentRangeLink')
        rent_range.click()
        sleep(5)
        min_price = rent_range.find_element(By.XPATH, '//*[@id="min-input"]')
        min_price.send_keys(self.min_price)
        max_price = rent_range.find_element(By.XPATH, '//*[@id="max-input"]')
        max_price.send_keys(self.max_price)
        max_price.send_keys(Keys.ENTER)
        sleep(5)

        num_beds = self.driver.find_element(By.CLASS_NAME, 'bedselector')
        num_beds.click()
        min_bedroom_options = self.driver.find_elements(By.CSS_SELECTOR, '.minBedOptions li')
        for num_bedroom in min_bedroom_options:
            if num_bedroom.text == self.min:
                num_bedroom.click()
        sleep(5)
        max_bedroom_option = self.driver.find_elements(By.CSS_SELECTOR, '.maxBedOptions li')
        for more_bedroom in max_bedroom_option:
            if more_bedroom.text == self.max:
                more_bedroom.click()
        sleep(5)
        return self.driver.current_url

    def get_results(self) -> list:
        """Return a list of dictionaries with all the values."""
        self.driver.get(url=self.search_filters())
        results_dict = []
        result_container = [result for result in self.driver.find_elements(By.CLASS_NAME, "property-information")]
        labels = [result.text.split("\n") for result in self.driver.find_elements(By.CLASS_NAME, "property-information")]
        urls = [url.find_element(By.CLASS_NAME, 'property-link').get_attribute("href") for url in result_container]
        locations = [location[1] for location in labels]
        prices = [price.text for price in self.driver.find_elements(By.CLASS_NAME, 'property-pricing')]
        for i in range(len(urls)):
            all_results = {"Price": prices[i], "URL": urls[i], "Location": locations[i]}
            results_dict.append(all_results)
        return results_dict


def put_to_google_form(chromedriver_path, address, link, price):
    """Add data to Renting Research Google Form."""
    google_form = "https://docs.google.com/forms/d/1aNRi2_vYmg5-NeSlw9E7HLULm39iMPpNFPDxnvIDtuQ/viewform?pli=1&pli=1&" \
                  "edit_requested=true"
    driver = webdriver.Chrome(executable_path=chromedriver_path)
    driver.get(url=google_form)
    sleep(5)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/'
                                                  'div[1]/div/div[1]/input')
    address_input.send_keys(address)
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/'
                                                'div/div[1]/input')
    price_input.send_keys(price)
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/'
                                               'div/div[1]/input')
    link_input.send_keys(link)
    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div').click()
    sleep(5)
    driver.quit()
