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

def get_tempreture_location(city):
	url = f'https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}'
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		return {
			"temperature": data['current']['temp_c'],
			"city": data['location']['region']
		}
	else:
		return {
	  		"temperature": "Unknown",
			"city": "Unknown"
		}


@app.get("/")
def home():
	return {
		"message": "Hey There👋. Welcome to Greet App."
	}

@app.get('/api/hello')
async def get_requester_info(
	request: Request,
	x_forwarded_for: str = Header(None),
	visitor_name: str = Query(None)
):
	ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.client.host	
	visitor_name =  get_name(visitor_name)
	data = get_tempreture_location(ip)
	return {
		"client_ip": ip,
		"city": data['city'],
		"greeting": f"Hello, {visitor_name}!, the temperature is {data['tempreture']} degrees Celcius in {data['city']}"
	}

