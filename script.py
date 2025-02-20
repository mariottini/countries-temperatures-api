import io
import json
import requests
import tkinter as tk
from PIL import Image, ImageTk
import concurrent.futures

API_URL= "http://localhost:5000"

def mainMenu():
    print("What wuold you like to do?\n" +
          "[1] Get the list of all countries in the world\n" +
          "[2] Get the list of all countries in a continent\n" +
          "[3] Get some information about a country\n" +
          "[4] Get the list of your favourite countries\n" +
          "[5] Edit your favourites list\n" +
          "[6] Get the current temperature of a country\n" +
          "[7] Get a chart of the temperatures of a country (up to 5 days)\n" +
          "[8] Api info\n" +
          "[0] Close"
          )
    
def editFavListMenu():
    print("What wuold you like to do?\n" +
          "[1] Add a new country to favourites\n" +
          "[2] Remove a country from favourites\n" +
          "[3] Clear your favourites list\n"
          )


# api.add_resource(GetCountries, '/countries')
def getCountries():
    response = requests.get(f"{API_URL}/countries")
    if response.status_code == 200:
        # countries = response.json()
        countries = json.dumps(response.json(), indent=4)
        return countries
    else:
        print(f"Failed to fetch countries: {response.text}")
        return None


# api.add_resource(GetCountriesByContinent, '/countries/<string:continent>')
def getCountriesByContinent(continent):
    response = requests.get(f"{API_URL}/countries/{continent}")
    if response.status_code == 200:
        countries = response.json()
        # countries = json.dumps(response.json(), indent=4)
        return countries
    else:
        print(f"Failed to fetch countries: {response.text}")
        return None
    
# api.add_resource(GetCountryInfo, '/country/<string:country>')
def getCountryInfo(country):
    response = requests.get(f"{API_URL}/country/{country}")
    if response.status_code == 200:
        # info = response.json()
        info = json.dumps(response.json(), indent=4)
        return info
    else:
        print(f"Failed to fetch informations: {response.text}")

# api.add_resource(GetFavList, '/favourites')
def getFavList():
    response = requests.get(f"{API_URL}/favourites")
    if response.status_code == 200:
        favList = response.json()
        # favList = json.dumps(response.json(), indent=4)
        return favList
    else:
        print(f"Failed to fetch list: {response.text}")

# api.add_resource(ClearFavList, '/favourites/empty')
def clearFavList():
    response = requests.get(f"{API_URL}/favourites/empty")
    if response.status_code == 200:
        message = response.json()
        return message
    else:
        print(f"Failed to fetch list: {response.text}")

# api.add_resource(AddFavList, '/favourites/add/<string:country>')
def addFavList(country):
    response = requests.get(f"{API_URL}/favourites/add/{country}")
    if response.status_code == 200:
        favList = response.json()
        # favList = json.dumps(response.json(), indent=4)
        return favList
    else:
        print(f"Failed to fetch list: {response.text}")

# api.add_resource(RemoveFavList, '/favourites/remove/<string:country>')
def removeFavList(country):
    response = requests.get(f"{API_URL}/favourites/remove/{country}")
    if response.status_code == 200:
        favList = response.json()
        # favList = json.dumps(response.json(), indent=4)
        return favList
    else:
        print(f"Failed to fetch list: {response.text}")

# api.add_resource(GetCountryTemp, '/temperature/<string:country>')
def getCountryTemp(country):
    response = requests.get(f"{API_URL}/temperature/{country}")
    if response.status_code == 200:
        temp = response.json()
        return temp
    else:
        print(f"Failed to fetch temperature: {response.text}")

# api.add_resource(GenerateTempChart, '/temperature/<string:country>/<int:days>')
def generateTempChart(country, days):
    response = requests.get(f"{API_URL}/temperature/{country}/{days}")
    if response.status_code == 200:
        chart = response.json()
        # return chart
        print(f"Open the chart to see the results!")
        root = tk.Tk()
        root.title(f"Temperatures in {country} for the next {days} days")
        root.geometry("1100x660")
        response = requests.get(chart)
        image = Image.open(io.BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo)
        label.image = photo
        label.place(x=50, y=30)
        root.mainloop()
    else:
        print(f"Failed to generate chart: {response.text}")

def apiInfo():
    response = requests.get(f"{API_URL}/api-info")
    if response.status_code == 200:
        # info = response.json()
        info = json.dumps(response.json(), indent=4)
        return info
    else:
        print(f"Failed to fetch info: {response.text}")

# def getMaxTemperaturesByRegion(countries):                    # TOO SLOW: 50secs using South America
#     maxTemp = float('-inf')
#     warmestCountry = None
#     for country in countries:
#         temperature = getCountryTemp(country)
#         if temperature is not None and temperature > maxTemp:
#             maxTemp = temperature
#             warmestCountry = country
#     return warmestCountry

def getMaxTemperaturesByRegion(countries):                      # FASTER: 15secs using South America
    maxTemp = float('-inf')
    warmestCountry = None

    def check_temperature(country):
        temperature = getCountryTemp(country)
        return country, temperature

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(check_temperature, countries)

        for country, temperature in results:
            if temperature is not None and temperature > maxTemp:
                maxTemp = temperature
                warmestCountry = country

    return warmestCountry

def main():
    print("Loading data...")

    continent = "South America"
    countries = getCountriesByContinent(continent)
    warmestCountry = getMaxTemperaturesByRegion(countries)
    temp = getCountryTemp(warmestCountry)
    days = 4 #(days = x to display today and the next x days)

    print(f"The warmest country in {continent} is {warmestCountry} with {temp}°C")
    addFavList(warmestCountry)
    print(f"{warmestCountry} added to Favourites List!")
    print(f"Favourite List: {getFavList()}")
    print(f"Temperature in {warmestCountry} for the next {days+1} days:")
    print(generateTempChart(warmestCountry, days+1))

    mainMenu()
    selectionMain = int(input())

    if selectionMain == 1:
        countries = getCountries()
        if countries:
            print(f"Countries:", countries)

    if selectionMain == 2:
        print("What continent?")
        continent = input()
        countries = getCountriesByContinent(continent)
        if countries:
            print(f"Countries in {continent.capitalize()}:", countries)

    if selectionMain == 3:
        print("What country?")
        country = input()
        info = getCountryInfo(country)
        if info:
            print(f"Some informations about {country.capitalize()}:", info)

    if selectionMain == 4:
        favList = getFavList()
        if favList:
            print(f"Favourites:", favList)
        else:
            print("Your favourites list is empty!")

    if selectionMain == 5:
        editFavListMenu()
        selectionEditFavList = int(input())
        if selectionEditFavList == 1:
            print("What country?")
            country = input()
            favList = addFavList(country)
            if favList:
                print(f"Favourites:", favList)
            else:
                print("Your favourites list is empty!")
        if selectionEditFavList == 2:
            print("What country?")
            country = input()
            favList = removeFavList(country)
            if favList:
                print(f"Favourites:", favList)
            else:
                print("Your favourites list is empty!")
        if selectionEditFavList == 3:
            favList = clearFavList()
            if favList:
                print(f"Favourites:", favList)
            else:
                print("Your favourites list is empty!")

    if selectionMain == 6:
        print("What country?")
        country = input()
        temp = getCountryTemp(country)
        if temp:
            print(f"Current temperature in {country.capitalize()} is:", temp)

    if selectionMain == 7:
        print("What country?")
        country = input()
        print("How many days?")
        days = input()
        generateTempChart(country, days)

    if selectionMain == 8:
        info = apiInfo()
        if info :
            print(info)

    if selectionMain == 0:
        print(f"See you next! :)")

    input("Press any key to exit...")

if __name__ == "__main__":
    main()
    