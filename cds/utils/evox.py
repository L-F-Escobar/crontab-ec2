import json
import requests

API_URL = 'http://api.evoximages.com/api/v1'

def send_request(uri, **kwargs):
    ''' Send Request '''
    request = requests.get(
        API_URL + uri, headers={
        'x-api-key' : '7VUPJ7sSeHGqMpTxfzQ95nqetVd3xLdG'
    })

    return json.loads(request.text)

def get_vehicle(year, make, model, trim):
    ''' Get Vehicle Photos & Colours '''
    response = send_request(f'/vehicles?year={year}&make={make}&model={model}&trim={trim}')

    if 'data' in response:
        if len(response['data']) > 0:
            response = send_request('/vehicles/' + str(response['data'][0]['vifnum']) + '/products/27/214')
            if 'urls' in response:
                for url in response['urls']:
                    if '_1280_' in url:
                        return url

    return ''
