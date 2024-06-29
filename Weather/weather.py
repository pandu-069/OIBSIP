import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap
import ttkbootstrap.window

#Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "5731c0a66b712c17b67b85ef40bdf7d9"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    #Parse the response JSON to get the weather information
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temparature = weather['main']['temp'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    #Get the icon url and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temparature, description, city, country)

#Fuction to search for the city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if  result is None:
        return
    #If the city is found unpack the weather inforation
    icon_url, temperature, description, city, country = result
    location_label.configure(text=f"{city} , {country}")

    #Get the weather image from the URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    #Update the temparature and labels
    temperature_label.configure(text=f"Temparature : {temperature:.2f} C")
    description_label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

#Entry widget -> to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#Button widget -> to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle = "Warning")
search_button.pack(pady=10)

#Label widget -> to show the city / country name
location_label = tk.Label(root, font = "Helvetica, 25")
location_label.pack(pady=20)

#Label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

#Label widget -> to show the temparature
temperature_label = tk.Label(root, font = "Helvetica, 20")
temperature_label.pack()

#Label widget to show the weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()