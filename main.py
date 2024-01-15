import requests


class BusParser:

	def __init__(self):
		self.cookies = {
		    'ASP.NET_SessionId': 'oclmsz4t3r1o5h1i3hvtwmxa',
		    '__RequestVerificationToken_L2xvb2tvdXRfeWFyZA2': 'DrNenWqq6Gmijfg3VvzI3RMVmhyLcl2hbqyYrTl9e2YeK0eZghc5ufeknk0iXbKtg2IrAsAWFTHUBf86Kta3BMdRDr40hHZufgNkSVV4DTE1',
		    '_ga': 'GA1.1.950650976.1700487850',
		    '_ga_CZQSPX20W4': 'GS1.1.1701013858.2.1.1701014567.0.0.0',
		}
		self.headers = {
		    'Accept': 'application/json, text/plain, */*',
		    'Accept-Language': 'ru',
		    'Connection': 'keep-alive',
		    'Content-Type': 'application/x-www-form-urlencoded',
		    # 'Cookie': 'ASP.NET_SessionId=oclmsz4t3r1o5h1i3hvtwmxa; __RequestVerificationToken_L2xvb2tvdXRfeWFyZA2=DrNenWqq6Gmijfg3VvzI3RMVmhyLcl2hbqyYrTl9e2YeK0eZghc5ufeknk0iXbKtg2IrAsAWFTHUBf86Kta3BMdRDr40hHZufgNkSVV4DTE1; _ga=GA1.1.950650976.1700487850; _ga_CZQSPX20W4=GS1.1.1701013858.2.1.1701014567.0.0.0',
		    'Origin': 'https://www.minsktrans.by',
		    'Referer': 'https://www.minsktrans.by/lookout_yard/Home/Index/minsk',
		    'Sec-Fetch-Dest': 'empty',
		    'Sec-Fetch-Mode': 'cors',
		    'Sec-Fetch-Site': 'same-origin',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
		    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
		    'sec-ch-ua-mobile': '?0',
		    'sec-ch-ua-platform': '"Windows"',
		}

	def route_list(self):
		data = {
			'p':'minsk',
			'tt':'bus',
			'__RequestVerificationToken':'21SCGAuckxj5t_h7WUb-teynN9DNHD9ETFpFahbd8P7oKeEIVgLI8yHE3eQItubIdTOotjKvhWg2JaRNLNkeVuXO7Ms8t732MulY8qo_avs1',
		}

		response = requests.post('https://www.minsktrans.by/lookout_yard/Data/RouteList', cookies=self.cookies,
		                        headers=self.headers, data=data).json()

		routes = [route['Number'] for route in response['Routes']]

		return tuple(routes)


	def routes_and_stopes(self, bus_route):
		data = {
			'p':'minsk',
			'tt':'bus',
			'r': bus_route,
			'__RequestVerificationToken':'Vq5bY__Kz-cNY5gGFK6nH1HrxinKivqgwzCJC84PbYcNp-Qr9Hs4S7aX7RYjIyII33V_j7_Eb4ZD02PxQuHfiKi9hGg23HUGCujU2w9Z8P01',
		}

		response = requests.post('https://www.minsktrans.by/lookout_yard/Data/Route', cookies=self.cookies, headers=self.headers,
		                         data=data).json()

		route_a = response['Trips']['NameA']
		route_b = response['Trips']['NameB']

		names_stops_a = response['Trips']['StopNamesA']
		names_stops_b = response['Trips']['StopNamesB']

		id_stopsA = response['Trips']['StopsA']
		id_stopsB = response['Trips']['StopsB']

		id_name_route_a = ''
		for stop_id, stop_name in zip(id_stopsA, names_stops_a):
			id_name_route_a = id_name_route_a + f"{stop_id['Id']}. {stop_name}\n"
		id_name_route_b = ''
		for stop_id, stop_name in zip(id_stopsB, names_stops_b):
			id_name_route_b = id_name_route_b + f"{stop_id['Id']}. {stop_name}\n"

		text = f'''Направление маршрута: {route_a} 
	Индекс маршрута: 0
		
	Остановки: 
	{id_name_route_a}
	
	
	Направление маршрута: {route_b} 
	Индекс маршрута: 1
	
	Остановки:
	{id_name_route_b}
		'''
		print(f"\n{text}")

		return [[id_stopsA['Id'] for id_stopsA in id_stopsA], [id_stopsB['Id'] for id_stopsB in id_stopsB]]


	def schedule_for_stop(self, bus_route, stop, direction):
		data = {
			'p':'minsk',
			'tt':'bus',
			'r': bus_route,
			's': stop,
			'd': direction,
			'__RequestVerificationToken':'oSuEC7bISPi0b3LmD2Z7fKZ1FI2ZGXl3cMwpV18n4avmS146x-nc5nvuVPqYk760HqJHg_Y50SZ16v92SFm2vy0lgWk6n3SzvGIp2rMk0Yg1',
		}

		response = requests.post('https://www.minsktrans.by/lookout_yard/Data/Schedule', cookies=self.cookies, headers=self.headers,
		                         data=data).json()
		print(response)
		try:
			schedule_by_hours = response['Schedule']['HourLines']

		except:
			schedule_by_hours = response['DaysOfWeek'][0]['HourLines']

		hours_minutes = ''
		for schedule in schedule_by_hours:
			hours_minutes = hours_minutes + f"Час: {schedule['Hour']} Минуты: {schedule['Minutes']}\n"

		print(f"\n{hours_minutes}")


def main():
	parser = BusParser()
	routes = parser.route_list()
	bus_route = input('Введите номер автобуса: ')
	if bus_route not in routes:
		print('Такого автобуса нет')
		exit()

	else:
		stops_ids = parser.routes_and_stopes(bus_route=bus_route)
		direction = int(input('Введите направление: '))
		if direction != 0 and direction != 1:
			print('Направление может быть только 0 или 1')
			exit()

		else:
			stop_ids_direction = stops_ids[direction]
			stop = int(input('Введите номер остановки: '))
			if stop not in stop_ids_direction:
				print('Такой остановки нет')
				exit()
			else:
				parser.schedule_for_stop(bus_route=bus_route, stop=stop, direction=direction)

if __name__ == '__main__':
	main()