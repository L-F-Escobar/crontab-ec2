import json
import requests

API_URL = 'http://api.unhaggle.com/api/incentives/fetch'

def send_request(uri):
    ''' Get Incentives '''
    request = requests.get(API_URL + uri, headers={
        'Api-Key' : 'core-dealer-services:IcTvYuxyzxfNpxHuAMWYT7o4ngE'
    })

    return json.loads(request.text)

def get_residuals(trim, postal):
    ''' Retrieve Residual Values '''
    response = send_request(f'/residual/{trim}/by_postal_code/{postal}/?special=1')
    data = {}

    if 'lease_km_allowance_residual' in response and '20000.00' in response['lease_km_allowance_residual']:
        for term, residual in response['lease_km_allowance_residual']['20000.00'].items():
                data[term] = (0 if 'N/A' in residual else residual)

    return data

def retrieve(trim, postal):
    ''' Retrieve incentive for trim_id '''
    response = send_request(f'/{trim}/by_postal_code/{postal}/?special=1')
    residuals = get_residuals(trim, postal)
    data = []

    if 'methods' in response[0]:
        for type, incentive in response[0]['methods'].items():
            if type != 'cash':
                for term, rate in incentive['terms'].items():
                    if rate != 'N/A':
                        residual = 0

                        if type == 'lease':
                            residual = (residuals[term] if term in residuals else 0)

                        data.append({
                            'year'      : response[0]['year'],
                            'make'      : response[0]['make'],
                            'model'     : response[0]['model'],
                            'trim'      : response[0]['trim'],
                            'type'      : type,
                            'program'   : incentive['rebate_name'],
                            'incentive' : 'rate',
                            'term'      : term,
                            'rate'      : rate,
                            'residual'  : residual,
                            'factor'    : (float(rate) / 2400 if type == 'lease' else 0),
                            'cash'      : incentive['rebate_pre_tax'],
                            'start_at'  : response[0]['start_date'],
                            'end_at'    : response[0]['end_date']
                        })

    if 'special' in response[0]:
        for incentive in response[0]['special']:
            if 'standard' not in incentive['id'].lower():
                continue

            for term, rate in incentive['terms'].items():
                if rate != 'N/A':
                    residual = 0

                    if 'lease' in incentive['id'].lower() :
                        residual = (residuals[term] if term in residuals else 0)

                    data.append({
                        'year'      : response[0]['year'],
                        'make'      : response[0]['make'],
                        'model'     : response[0]['model'],
                        'trim'      : response[0]['trim'],
                        'type'      : ('finance' if 'finance' in incentive['id'].lower() else 'lease'),
                        'program'   : incentive['rebate_name'],
                        'incentive' : 'rate',
                        'term'      : term,
                        'rate'      : rate,
                        'residual'  : residual,
                        'factor'    : (float(rate) / 2400 if 'lease' in incentive['id'].lower() else 0),
                        'cash'      : incentive['rebate_pre_tax'],
                        'start_at'  : response[0]['start_date'],
                        'end_at'    : response[0]['end_date']
                    })

                    if int(incentive['rebate_pre_tax']) > 0:
                        data.append({
                            'year'      : response[0]['year'],
                            'make'      : response[0]['make'],
                            'model'     : response[0]['model'],
                            'trim'      : response[0]['trim'],
                            'type'      : ('finance' if 'finance' in incentive['id'].lower() else 'lease'),
                            'program'   : incentive['rebate_name'],
                            'incentive' : 'cash',
                            'term'      : term,
                            'rate'      : rate,
                            'residual'  : residual,
                            'factor'    : (float(rate) / 2400 if 'lease' in incentive['id'].lower() else 0),
                            'cash'      : incentive['rebate_pre_tax'],
                            'start_at'  : response[0]['start_date'],
                            'end_at'    : response[0]['end_date']
                        })
    return data
