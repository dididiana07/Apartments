import os
from apartment import Apartments, put_to_google_form

def main():
    chromedriver_path = os.environ["CHROMEDRIVER_PATH"]
    apartment_obj = Apartments(chromedriver_path=chromedriver_path,
                               usa_city="San Francisco",
                               lang="Spanish")

    results = apartment_obj.get_results()
    for result in results:
        put_to_google_form(chromedriver_path=chromedriver_path,
                           link=result["URL"],
                           address=result["Location"],
                           price=result["Price"])


if __name__ == "__main__":
    main()
