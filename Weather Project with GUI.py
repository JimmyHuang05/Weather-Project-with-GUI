import requests
import json
import tkinter as tk
from tkinter import messagebox

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

class CurrentWeatherAPI(WeatherAPI):
    def get_current_weather(self, location):
        url = f"{self.base_url}/{location}?unitGroup=metric&key={self.api_key}&contentType=json"
        response = requests.get(url)
        data = json.loads(response.text)
        current_conditions = data["currentConditions"]
        current_weather_info = {
            "datetime": current_conditions.get("datetime", ""),
            "temp": current_conditions.get("temp", ""),
            "humidity": current_conditions.get("humidity", ""),
            "windspeed": current_conditions.get("windspeed", ""),
            "description": current_conditions.get("conditions", "")
        }
        return current_weather_info

class FiveDayForecastAPI(WeatherAPI):
    def get_5_day_forecast(self, location):
        url = f"{self.base_url}/{location}/next5days?unitGroup=metric&key={self.api_key}&contentType=json"
        response = requests.get(url)
        data = json.loads(response.text)
        days = data["days"][:5]
        forecast_info = []
        for day in days:
            day_info = {
                "datetime": day.get("datetime", ""),
                "temp": day.get("temp", ""),
                "humidity": day.get("humidity", ""),
                "windspeed": day.get("windspeed", ""),
                "description": day.get("conditions", "")
            }
            forecast_info.append(day_info)
        return forecast_info

class WeatherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast Application")
        self.api_key = "GQJZJ3WWGNQUDNCJGZX6S5ZP8"

        self.location_var = tk.StringVar()
        self.result_text = tk.Text(self.root, height=10, width=50)

        self.location_label = tk.Label(self.root, text="Enter a city or location")
        self.location_label.pack(pady=10)

        self.location_entry = tk.Entry(self.root, textvariable=self.location_var)
        self.location_entry.pack(pady=10)

        self.current_weather_button = tk.Button(self.root, text="Get Current Weather",command=self.query_current_weather)
        self.current_weather_button.pack(pady=10)

        self.forecast_button = tk.Button(self.root, text="Get 5-Day Forecast", command=self.query_5_day_forecast)
        self.forecast_button.pack(pady=10)

        self.result_text.pack(pady=10)

    def query_current_weather(self):
        location = self.location_var.get()
        current_weather_api = CurrentWeatherAPI(self.api_key)
        try:
            current_weather = current_weather_api.get_current_weather(location)
            self.display_weather(location, current_weather)
        except:
            messagebox.showerror("Error", "Please try again!")

    def query_5_day_forecast(self):
        location = self.location_var.get()
        five_day_forecast_api = FiveDayForecastAPI(self.api_key)
        try:
            forecast = five_day_forecast_api.get_5_day_forecast(location)
            self.display_weather(location, forecast)
        except:
            messagebox.showerror("Error", "Please try again!")

    def display_weather(self, location, weather_info):
        self.result_text.delete(1.0, tk.END)
        if isinstance(weather_info, list):
            self.result_text.insert(tk.END, f"5-Days Forecast for {location}\n")
            for i, day_info in enumerate(weather_info, start=1):
                self.result_text.insert(tk.END, f"Day {i}: {day_info['temp']}C, {day_info['description']}\n")
        else:
            self.result_text.insert(tk.END, f"Current weather in {location}\n")
            self.result_text.insert(tk.END, f"Time：{weather_info['datetime']}\n")
            self.result_text.insert(tk.END, f"Temperature: {weather_info['temp']}°C\n")
            self.result_text.insert(tk.END, f"Description: {weather_info['description']}\n")
            self.result_text.insert(tk.END, f"Humidity: {weather_info['humidity']}%\n")
            self.result_text.insert(tk.END, f"Wind Speed: {weather_info['windspeed']}km/h\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherUI(root)
    root.mainloop()
