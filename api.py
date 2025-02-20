from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import requests
import argparse

app = Flask(__name__)
api = Api(app)

API_KEY_OpenWeatherMap = "cb8666fc8be7b92438aca9fcfc5c160c"     # ← INSERT KEY HERE

continents_list = ["Asia", "Africa", "North America", "South America", "Europe"]
fav_list = []

def getCapitalCoordinates(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        capital_info = data[0].get('capitalInfo')
        if capital_info:
            lat =  capital_info.get('latlng', [])[0]
            lng =  capital_info.get('latlng', [])[1]
            return lat, lng
    return None

def generateUrl(temperatures):
    temperatures_str =','.join(map(str, temperatures))
    labels_str = '1,2,3,4,5'
    url = f"https://quickchart.io/chart?c={{type:'line',data:{{labels:[{labels_str}],datasets:[{{label:'Temperature',data:[{temperatures_str}]}}]}}}}"
    return url

class GetCountries(Resource):
    def get(self):
        url = f"https://restcountries.com/v3.1/all"
        response= requests.get(url)
        if response.status_code == 200:
            data = response.json()
            countries_in_continent = [country.get('name').get('common') for country in data]
            return countries_in_continent
            # return jsonify(countries_in_continent)
        else:
            return "Failed to fetch countries", 500
            # return jsonify({"error" : "Failed to fetch countries"}), 500

class GetCountriesByContinent(Resource):
    def get(self, continent):
        continent = continent.title()
        countries_in_continent = []
        if continent not in continents_list:
            return "Invalid continent, choose one from this list: Asia, Africa, North America, South America, Europe"
        url = f"https://restcountries.com/v3.1/all"
        response= requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if continent == "Asia" or continent == "Africa" or continent == "Europe":
                countries_in_continent = [country.get('name').get('common')
                                          for country in data if continent == country.get('region')]
            if continent == "North America" or continent == "South America":
                countries_in_continent = [country.get('name').get('common')
                                          for country in data if continent == country.get('subregion')]
            return countries_in_continent
            # return jsonify(countries_in_continent)
        else:
            return "Failed to fetch countries", 500
            # return jsonify({"error" : "Failed to fetch countries"}), 500

class GetCountryInfo(Resource):
    def get(self, country):
        url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            country_info = [{'capital' : country.get('capital'), 
                             'latlng' : country.get('capitalInfo').get('latlng'),
                             'population' : country.get('population'),
                             'area' : country.get('area')} 
                             for country in data]
            return country_info
            # return jsonify(country_info)
        else:
            return "Country not found", 404
            # return jsonify({"error" : "Country not found"}), 404

class GetCountryTemp(Resource):
    def get(self, country):
        API_KEY_OpenWeatherMap = "cb8666fc8be7b92438aca9fcfc5c160c"
        coordinates = getCapitalCoordinates(country)
        if coordinates is not None:
            lat, lon = coordinates
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY_OpenWeatherMap}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                temperature = data.get('main').get('temp')
                return float(temperature)
                # return jsonify({'temperature' : temperature})
            else:
                return "Failed to fetch weather data", 500
                # return jsonify({"error" : "Failed to fetch weather data"}), 500
        else:
            return "Failed to fetch coordinates", 500
            # Gestisci il caso in cui le coordinate non siano disponibili

class GetFavList(Resource):
    def get(self):
        return fav_list
        # return jsonify(fav_list)

class ClearFavList(Resource):
    def get(self):
        fav_list.clear()
        return "Favourites list empty"
        # return jsonify({"message" : "Favourites list empty"})

class AddFavList(Resource):
    def get(self, country):
        url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            country_name = data[0].get('name').get('common')
            if country_name not in fav_list:
                fav_list.append(country_name)
                return fav_list
                # return jsonify({"favourites": fav_list})
            else:
                return "Country already in favourites list"
                # return jsonify({"error" : "Country already in favourites list"})
        else:
            return "Failed to fetch country", 500
            # return jsonify({"error" : "Failed to fetch country"}), 500

class RemoveFavList(Resource):
    def get(self, country):
        url = f"https://restcountries.com/v3.1/name/{country}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            country_name = data[0].get('name').get('common')
            if country_name in fav_list:
                fav_list.remove(country_name)
                return fav_list
                # return jsonify({"favourites": fav_list})
            else:
                return "Country not in favourites list"
                # return jsonify({"error" : "Country not in favourites list"})
        else:
            return "Failed to fetch country", 500
            # return jsonify({"error" : "Failed to fetch country"}), 500

class GenerateTempChart(Resource):
    def get(self, country, days):
        API_KEY_OpenWeatherMap = "cb8666fc8be7b92438aca9fcfc5c160c"
        lat, lon = getCapitalCoordinates(country)
        if days < 1:
            return "Inavlid days number"
            # return jsonify({'message' : 'Inavlid days number'})
        if days > 5:
            return "Days number too big"
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={days}&appid={API_KEY_OpenWeatherMap}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperatures = []
            for item in data['list']:
                temperature = item['main']['temp']
                temperatures.append(temperature)
            chart_url = generateUrl(temperatures)
            return chart_url
            # return jsonify({'chart_url' : chart_url})
        else:
            return "Failed to fetch weather data", 500
            # return jsonify({'error' : 'Failed to fetch weather data'}), 500

class ApiInfo(Resource):
    def get(self):
        info = {
            'API Name': 'Countries and Temperatures API',
            'Description': 'API to get informations about countries and temperatures',
            'Endpoints': {
                '/countries': 'Returns the list of all countries in the world',
                '/countries/<string:continent>': 'Returns the list of all countries in a continent',
                '/country/<string:country>': 'Returns some information about a country',
                '/favourites': 'Returns the list of your favourite countries',
                '/favourites/empty': 'Empty the list of your favourite countries',
                '/favourites/add/<string:country>': 'Add a new country to the favourites list',
                '/favourites/remove/<string:country>': 'Remove a country from the favourites list',
                '/temperature/<string:country>': 'Return the current temperature of a country',
                '/temperature/<string:country>/<int:days>': 'Return the link of the chart of the temperatures of a country',
                '/api-info': 'Returns the guide of this API'
            }
        }
        return info

api.add_resource(GetCountries, '/countries')
api.add_resource(GetCountriesByContinent, '/countries/<string:continent>')
api.add_resource(GetCountryInfo, '/country/<string:country>')
api.add_resource(GetCountryTemp, '/temperature/<string:country>')
api.add_resource(GetFavList, '/favourites')
api.add_resource(ClearFavList, '/favourites/empty')
api.add_resource(AddFavList, '/favourites/add/<string:country>')
api.add_resource(RemoveFavList, '/favourites/remove/<string:country>')
api.add_resource(GenerateTempChart, '/temperature/<string:country>/<int:days>')
api.add_resource(ApiInfo, '/api-info')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key")
    args = parser.parse_args()
    API_KEY_OpenWeatherMap = args.key
    app.run(debug=True)