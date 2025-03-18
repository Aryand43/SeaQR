import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

# OpenWeather API Key (DO NOT SHARE PUBLICLY)
OPENWEATHER_API_KEY = "c88cf6d1279911c21f6025eda7f051bf"

CITY = "Singapore"
LAT, LON = 1.3521, 103.8198

# OpenSky Flight API
FLIGHT_API_URL = "https://opensky-network.org/api/states/all"

def dashboard(request):
    return render(request, "dashboard/index.html")

def weather_data(request):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    
    print("Weather API Response:", response)  # Debugging output
    
    if "main" not in response:
        return JsonResponse({"error": "Invalid API response", "details": response}, status=500)

    return JsonResponse({
        "temperature": f"{response['main']['temp']}°C",
        "feels_like": f"{response['main']['feels_like']}°C",
        "humidity": f"{response['main']['humidity']}%",
        "pressure": f"{response['main']['pressure']} hPa",
        "weather": response['weather'][0]['description'].capitalize(),
        "wind_speed": f"{response['wind']['speed']} m/s"
    })

def flight_data(request):
    response = requests.get(FLIGHT_API_URL).json()

    if "states" not in response:
        return JsonResponse({"error": "Invalid flight API response", "details": response}, status=500)

    flights = []
    for flight in response["states"]:
        if flight[5] and flight[6]:  # Only keep flights with coordinates
            flights.append({
                "callsign": flight[1].strip(),
                "lat": flight[6],
                "lon": flight[5],
                "alt": flight[7]  # Altitude in meters
            })
    return JsonResponse(flights, safe=False)
# Function to generate video feed
def generate_video():
    cap = cv2.VideoCapture(0)  # Change '0' to a file path if using a saved video
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# Function to send video feed response

def video_feed(request):
    return StreamingHttpResponse(generate_video(), content_type='multipart/x-mixed-replace; boundary=frame')