from fastapi import FastAPI, Request, Header, Query
import requests

app = FastAPI()

@app.get('/api/hello')
async def get_requester_info(
	request: Request,
	x_forwarded_for: str = Header(None),
	visitor_name: str = Query(None, description="Name of the visitor")
):
	# Get the client's IP address
	ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.client.host
	client_host = request.client.host
	print(client_host)
	# Use an IP-to-location service to get the city (you can replace this with your preferred service)
	# Example: https://ipapi.co/json/
	location_response = requests.get(f"https://ipapi.co/{ip}/json/")
	location_data = location_response.json()
	city = location_data.get("city", "Unknown City")

	# # Use a weather API to get the temperature for the detected city
	# # Example: OpenWeatherMap API
	# api_key = "YOUR_OPENWEATHERMAP_API_KEY"
	# weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
	# weather_data = weather_response.json()
	# temperature = weather_data.get("main", {}).get("temp", "Unknown")

	return {
		"ip": ip,
		"city": city,
		# "temperature": f"{temperature}°C",
		"visitor_name": visitor_name
	}
