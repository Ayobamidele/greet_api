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

def get_location(ip):
	location_response = requests.get(f"https://ipapi.co/{ip}/json/")
	return location_response.json().get("city", "Unknown City")


def get_tempreture_in_celcius(city):
	url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}'
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		temperature = data['current']['temp_c']
		return temperature
	else:
		return "Unknown"



@app.get('/api/hello')
async def get_requester_info(
	request: Request,
	x_forwarded_for: str = Header(None),
	visitor_name: str = Query(None)
):
	ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.client.host	
	visitor_name =  get_name(visitor_name)
	city = get_location(ip)
	celcius = get_tempreture_in_celcius(city)
	return {
		"client_ip": ip,
		"city": city,
		"greeting": f"Hello, {visitor_name}!, the temperature is {celcius} degrees Celcius in {city}"
	}
