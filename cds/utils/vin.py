import json
import requests

API_URL = 'https://api.jatoflex.com/api/en-ca'

def decode(data, token=''):
    vehicle = {
        'vin'             : data['vin'],
        'stock'           : data['stock'],
        'stock_type'      : data['stock_type'],
        'status'          : '',
        'year'            : '',
        'make'            : '',
        'model'           : '',
        'trim'            : '',
        'trim_id'         : '',
        'price'           : data['price'],
        'cost'            : data['cost'],
        'invoice'         : data['invoice'],
        'msrp'            : data['msrp'],
        'holdback'        : data['holdback'],
        'model_code'      : data['model_code'],
        'type'            : '',
        'body_type'       : '',
        'engine'          : '',
        'horsepower'      : '',
        'displacement'    : '',
        'drivetrain'      : '',
        'fuel'            : '',
        'doors'           : '',
        'ext_color'       : data['ext_color'],
        'int_color'       : data['int_color'],
        'transmission'    : '',
        'kilometres'      : data['kilometres'],
        'efficiency_city' : '',
        'efficiency_hwy'  : '',
        'photo'           : '',
        'stocked_at'      : data['stocked_at'],
        'deleted_at'      : data['deleted_at']
    }

    if token == '' or data['vin'] == '':
        return vehicle

    vehicle['token'] = token
    response = send_request('/vin/decode/' + data['vin'], token)

    if len(response['versions']) > 0 :
        decoded = response
        response = send_request('/vehicle/' + str(decoded['versions'][0]['vehicle_ID']), token)

        vehicle['year'] = response['modelYear']
        vehicle['make'] = response['makeName']
        vehicle['model'] = response['modelName']
        vehicle['trim'] = response['trimName']
        vehicle['trim_id'] = decoded['versions'][0]['vehicle_ID']
        vehicle['type'] = response['bodyStyleName']
        vehicle['body_type'] = decoded['bodyStyle']
        vehicle['drivetrain'] = response['drivenWheels']
        vehicle['doors'] = response['numberOfDoors']
        vehicle['fuel'] = decoded['fuelType']
        vehicle['engine'] = decoded['engine']
        vehicle['transmission'] = response['transmissionType']
        vehicle['efficiency_city'] = response['fuelEconCity']
        vehicle['efficiency_hwy'] = response['fuelEconHwy']

        if 'photoPath' in response and response['photoPath']:
            vehicle['photo'] = 'https://sslphotos.jato.com/PHOTO300' + response['photoPath']

        # Get Features
        response = send_request('/features/' + str(decoded['versions'][0]['vehicle_ID']) + '?pageSize=1000', token)
        features = []

        if 'results' in response:
            for result in response['results']:
                if result['content'] == 'Standard':
                    features.append({
                        result['feature'] : result['content']
                    })

                if result['feature'] == "Horsepower":
                    vehicle['horsepower'] = (result['content'] if ',' not in result['content'] else result['content'].split(',')[0])

                if result['feature'] == "Displacement (cc)":
                    vehicle['displacement'] = (result['content'] if ',' not in result['content'] else result['content'].split(',')[0])

                if result['feature'] == "Engine":
                    vehicle['engine'] = result['content'].replace('In-line4', '').replace('In-line6', '')

        vehicle['features'] = features

    return vehicle

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

def get_vehicle_photo(trim_id):
    ''' Retrieve Vehicle Stock Photo '''
    response = send_request('/images/JATO?competitors=' + str(trim_id))
    print(response)

def send_request(uri, token=''):
    ''' Send VIN Request '''
    if token == '':
        token = get_auth_token()

    request = requests.get(API_URL + uri, headers={
        'Subscription-Key': '3b1946486f314fecb6ad55cd626a0c79',
        'Authorization': 'Bearer ' + token,
    })

    return json.loads(request.text)
