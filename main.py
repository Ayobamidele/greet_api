from fastapi import FastAPI, Request, Header, Query
import requests
import os

app = FastAPI()
weather_api_key = os.environ.get("WEATHER_API_KEY")

def get_name(name):
	start_index = name.find('"')
	end_index = name.find('"', start_index + 1)

	if start_index == -1 or end_index == -1:
		start_index = name.find("'")
		end_index = name.find("'", start_index + 1)

	if start_index != -1 and end_index != -1:
		return name[start_index + 1:end_index]
	else:
		return name



def get_weather_api_url(city):
	url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}'
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		temperature = data['current']['temp_c']
		return temperature
	else:
		return None



@app.get('/api/hello')
async def get_requester_info(
	request: Request,
	x_forwarded_for: str = Header(None),
	visitor_name: str = Query(None, description="Name of the visitor")
):
	ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.client.host	
	visitor_name =  get_name(visitor_name)
	location_response = requests.get(f"https://ipapi.co/{ip}/json/")
	location_data = location_response.json()
	city = location_data.get("city", "Unknown City")
 
	weather_data = get_weather_api_url(city)
	
	print(weather_data)
	

	return {
		"client_ip": ip,
		"city": city,
		"greeting": f"Hello, {visitor_name}!, the temperature is 11 degrees Celcius in {city}"
	}


# # Use a weather API to get the temperature for the detected city
	# # Example: OpenWeatherMap API
	# api_key = "YOUR_OPENWEATHERMAP_API_KEY"
	# weather_response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
	# weather_data = weather_response.json()
	# temperature = weather_data.get("main", {}).get("temp", "Unknown")