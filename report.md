# Assignment 1: Web services

This report will give you an overview about the design and the implementation of a RESTful API in Python. The aim is to get some information about countries in the world and their temperatures.  
This project has been developed giving the user a simple interface to access geographical and meteorological data, using HTTP requests.
The project is divided in two files: `api.py`, which is the actual API, and `script.py`, which is the application showed to the user that consumes the API.  

## `api.py`

This API was made to be resource oriented, with the endpoints representing the actions that can be executed on the resources. They are meant to be self-explanatory and use words reminding the data that will be returned as result of the requests.  
The API follows the RESTful principles using HTTP methods on the operations (e.g. GET to retrieve resources) to get the informations requested.  
Requests to third-party services are made asynchronously to not risk to block the server.  
To handle faulty requests, the API gives back error messages followed by an HTTP state code (400 or 500 based on the type of error).  

## `script.py`

In this file there is the actual application used by the user to make operations consuming the API made before.
The user will see an intuitive menu with 9 options, one for each operation (except for the last one which is made to exit the program).  
First, the answer to the query of which country in South America is currently the warmest will be displayed, then it will be automatically added to favourites list and the graph containing the temperature forecast for the following four days will appear. Doing this operations normally would have taken a lot of time, so the module `concurrent.futures` was introduced to execute the checking tasks on each element of the JSON Object at the same time, making it faster for the server to elaborate all data.  
To display the line graph of the temperature forecats for the following _n_ days, `Tkinter` library was used to create an empty window where the graph image (loaded from the link provided by [quickchart.io](https://quickchart.io/) using `PIL` module) is shown.  

## Personal considerations

Personally, I think working on this project has been very challenging. This helped me knowing better and deepen what I learned during theory class. Moreover this was my first time using Python to make a program so I could also improve my Python skills discovering new features about this programming language.  
Working on the project took me about 43 hours totally, because I encountered some problems trying to make the program a bit faster and also because I didn't know anything about `Flask`, so I had to read something about it before starting to code.
