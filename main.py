import requests
import flet as ft
from datetime import datetime

# Replace with your Unsplash and OpenWeatherMap API keys
UNSPLASH_ACCESS_KEY = "YBR7CJR88rFKic51F7zhGvR7BuleIsTGU6hfbjIZvkQ"
WEATHER_API_KEY = "965f1aaed4f5b4a6ee34c89d59fed4f2"

# Fetch wallpaper from Unsplash
def fetch_wallpaper():
    url = "https://api.unsplash.com/photos/random"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {"query": "nature", "orientation": "portrait"}  # Can be customized
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data["urls"]["regular"]

# Fetch weather and location data from OpenWeatherMap
def fetch_weather(city="New York"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather = data['weather'][0]['description'].title()
    temperature = data['main']['temp']
    location = f"{data['name']}, {data['sys']['country']}"
    return weather, temperature, location

# Determine color based on temperature
def temperature_color(temp):
    if temp > 30:
        return ft.colors.RED
    elif temp > 15:
        return ft.colors.ORANGE
    elif temp > 0:
        return ft.colors.BLUE
    else:
        return ft.colors.DARK_BLUE

# Main app
def main(page: ft.Page):
    # Control Page size
    page.window.width = 360
    page.window.top = 5
    page.window.left = 960

    # Fetch wallpaper URL
    wallpaper_url = fetch_wallpaper()

    # Fetch weather data (default: New York)
    weather, temperature, location = fetch_weather()

    # Get current date and time
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    current_time = now.strftime("%H:%M:%S")

    # Determine colors
    temp_color = temperature_color(temperature)
    text_color = ft.colors.WHITE  # Color of text inside the black box

    # Create wallpaper image background
    wallpaper = ft.Image(
        src=wallpaper_url,
        fit=ft.ImageFit.COVER,
        width=page.window_width,
        height=page.window_height,
    )

    # Create the overlay layout with a blackish box containing weather, date, time, and location data
    overlay_content = ft.Container(
        content=ft.Stack(
            [
                wallpaper,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(f"Weather: {weather}, {temperature}°C", color=text_color, size=24),
                            ft.Text(f"Location: {location}", color=text_color, size=24),
                            ft.Text(f"Date: {current_date}", color=text_color, size=22),
                            ft.Text(f"Time: {current_time}", color=text_color, size=22),
                        ],
                        alignment="center",
                        spacing=10,
                    ),
                    bgcolor=ft.colors.with_opacity(ft.colors.BLACK, 0.7),
                    padding=20,
                    alignment=ft.alignment.bottom_center,
                    width=page.window_width,
                    height=page.window_height,
                    # bgcolor=ft.colors.with_opacity(ft.colors.BLACK, 0.7),  # Blackish background box with some transparency
                ),
            ],
        ),
    )

    # Add overlay content to page and update
    page.add(overlay_content)
    page.update()

ft.app(target=main)
