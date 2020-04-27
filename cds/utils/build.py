import json
import requests

API_URL = 'https://api.jatoflex.com/api/en-ca'

def process(make, province):
    ''' Process Build Data '''
    response = send_request(f'/makes/{make.lower()}/models/')
    data = []

    for year in ['2019', '2020']:
        for result in response['results']:
            for model in result['modelYears']:

                # Skip Non models
                if model['modelYear'] != year:
                    continue

                # Get Version Information
                url = model['links'][0]['href'].replace('https://api.jatoflex.com/api/en-ca', '')
                trimlines = send_request(url + 'versions')

                # Trim Level Data
                for trim in trimlines['results']:
                    vehicle_id = str(trim['vehicleId'])
                    feature_list = send_request(f'/features/{vehicle_id}?pageSize=400')
                    types = ['Engine', 'Horsepower', 'Fuel type', 'Displacement (cc)', 'Torque (ft lbs)']
                    features = []

                    # Additional Feature Data
                    feature_data = {
                        'Fuel type' : '',
                        'Engine' : '',
                        'Horsepower' : '',
                        'Torque (ft lbs)' : '',
                        'Displacement (cc)' : '',
                    }

                    # Retrieve Features
                    if 'results' in feature_list:
                        for feature in feature_list['results']:
                            if not feature['content']:
                                continue

                            if not 'Not Available' in feature['content']:
                                features.append({
                                    feature['feature'] : feature['content']
                                })

                                for type in types:
                                    if feature['feature'] == type:
                                        feature_data[type] = feature['content']

                    data.append({
                        'year'            : trim['modelYear'],
                        'make'            : trim['makeName'],
                        'model'           : trim['modelName'],
                        'trim'            : trim['trimName'],
                        'trim_id'         : trim['vehicleId'],
                        'body_type'       : f"{trim['drivenWheels']} {trim['trimName']} {trim['bodyStyleName']}",
                        'model_code'      : trim['manufacturerCode'],
                        'msrp'            : trim['msrp'],
                        'invoice'         : trim['invoice'],
                        'freight'         : trim['delivery'],
                        'type'            : trim['bodyStyleName'],
                        'doors'           : trim['numberOfDoors'],
                        'engine'          : feature_data['Engine'],
                        'horsepower'      : feature_data['Horsepower'],
                        'torque'          : feature_data['Torque (ft lbs)'],
                        'displacement'    : feature_data['Displacement (cc)'],
                        'fuel'            : feature_data['Fuel type'],
                        'photo'           : ('https://sslphotos.jato.com/PHOTO300' + str(trim['photoPath']) if trim['photoPath'] else ''),
                        'transmission'    : trim['transmissionType'],
                        'drivetrain'      : trim['drivenWheels'],
                        'efficiency_hwy'  : trim['fuelEconHwy'],
                        'efficiency_city' : trim['fuelEconCity'],
                        'features'        : features
                    })

    return data

def get_auth_token():
    ''' Retrieve JATO Authentication Token '''
    response = requests.post('https://auth.jatoflex.com/oauth/token', data={
        'username' : 'ca.coredealer',
        'password' : 'play7time',
        'grant_type' : 'password',
    })

    data = json.loads(response.content)

    if 'access_token' in data:
        return data['access_token']

    return ''

def send_request(uri, token=''):
    ''' Send Request '''
    if token == '':
        token = get_auth_token()

    request = requests.get(API_URL + uri, headers={
        'Subscription-Key': '3b1946486f314fecb6ad55cd626a0c79',
        'Authorization': 'Bearer ' + token,
    })

    return json.loads(request.text)
