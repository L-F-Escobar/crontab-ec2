import json
import requests

API_URL = 'https://service.canadianblackbook.com/UsedCarWS/CanUsedAPI/UsedVehicle/VIN/'

def determine(vin, model_code, mileage, province):
    ''' Determine Value '''
    data = {
        'value'   : 0,
        'great'   : 0,
        'good'    : 0,
        'average' : 0,
        'rough'   : 0
    }

    response = send_request(vin, model_code, mileage, province)

    if 'used_vehicles' not in response:
        return data

    if len(response['used_vehicles']['used_vehicle_list']) > 0:
        valuation = response['used_vehicles']['used_vehicle_list'][0]

        data['great'] = valuation['adjusted_whole_xclean']
        data['good'] = valuation['adjusted_whole_clean']
        data['average'] = valuation['adjusted_whole_avg']
        data['rough'] = valuation['adjusted_whole_rough']
        data['value'] = data['average']

        if data['good'] > 0 and data['rough'] > 0:
            data['value'] = (data['good'] + data['rough']) / 2

    return data

def send_request(vin, model_code, mileage, province='ON'):
    ''' Send VIN Request '''
    params = f'{vin}?kilometres={mileage}&modelnumber={model_code}&province={province}&country=C'

    request = requests.get(
        API_URL + params, auth=('CoreDlr-API', 'CGfBkDU4bAqH')
    )

    return json.loads(request.text)
