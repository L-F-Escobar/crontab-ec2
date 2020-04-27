import json
import requests

API_URL = 'http://partnerhub.pbsdealers.com/json/reply/'

def send_request(uri, **kwargs):
    ''' Send Request '''
    request = requests.post(
        API_URL + uri, data=kwargs['data'], auth=('CoreDealerService', 'FT497WZ46')
    )

    return json.loads(request.text, strict=False)

def get_customers(id, start_date=''):
    ''' Retieve a list of customers '''
    data = []

    response = send_request('ContactGet', data={
        'SerialNumber' : id,
        'IncludeInactive' : False,
        'ModifiedSince' : start_date
    })

    for customer in response['Contacts']:
        name = get_field(customer, 'FirstName').lower().title() + ' ' + get_field(customer, 'LastName').lower().title()

        if get_field(customer, 'IsBusiness'):
            name = get_field(customer, 'NameCompany')
            if name == '':
                name = get_field(customer, 'LastName').title()

        data.append({
            'type'        : ('B' if get_field(customer, 'IsBusiness') else 'I'),
            'number'      : get_field(customer, 'ContactId'),
            'first_name'  : get_field(customer, 'FirstName').title(),
            'middle_name' : get_field(customer, 'MiddleName').title(),
            'last_name'   : get_field(customer, 'LastName').title(),
            'full_name'   : name,
            'address'     : get_field(customer, 'Address').title(),
            'city'        : get_field(customer, 'City').title(),
            'province'    : get_field(customer, 'State').title(),
            'country'     : 'Canada',
            'postal_code' : get_field(customer, 'ZipCode'),
            'home'        : get_field(customer, 'HomePhone'),
            'cell'        : get_field(customer, 'CellPhone'),
            'email'       : get_field(customer, 'EmailAddress'),
            'work'        : get_field(customer, 'BusinessPhone'),
            'can_email'   : 1,
            'can_call'    : 1,
            'can_mail'    : 1,
        })

    return data

def get_deals(id, start_date=''):
    ''' Retieve a list of customers '''
    data = {}
    vin_list = []

    response = send_request('DealGet', data={
        'SerialNumber' : id,
        'SystemDeliverySince' : start_date
    })

    for sale in response['Deals']:
        if len(sale['Vehicles']) <= 0:
            continue

        vin_list.append(get_field(sale['Vehicles'][0], 'VehicleRef'))

        if not get_field(sale, 'BuyerRef') in data:
            data[get_field(sale, 'BuyerRef')] = []

        deal = {
            'customer_number'      : get_field(sale, 'BuyerRef'),
            'deal_number'          : get_field(sale, 'DealKey'),
            'vehicle_ref'          : get_field(sale['Vehicles'][0], 'VehicleRef'),
            'vin'                  : '',
            'stock'                : '',
            'stock_type'           : ('new' if 'IsNewVehicle' in sale['Vehicles'][0] and sale['Vehicles'][0]['IsNewVehicle'] else 'used'),
            'cost'                 : 0,
            'invoice'              : 0,
            'price'                : get_field(sale, 'Price'),
            'holdback'             : 0,
            'msrp'                 : 0,
            'kilometres'           : get_field(sale, 'SaleOdometer'),
            'package_code'         : '',
            'model_code'           : '',
            'int_color'            : '',
            'ext_color'            : '',
            'transmission'         : '',
            'stocked_at'           : None,
            'type'                 : get_field(sale, 'DealType').lower(),
            'sold_at'              : get_field(sale, 'ContractDate')[0:10] + ' 00:00:00',
            'bank_number'          : '',
            'bank_name'            : '',
            'bank_address'         : '',
            'price'                : get_field(sale, 'Price'),
            'cost'                 : 0,
            'journal_amount'       : 0,
            'journal_cost'         : 0,
            'adjustments'          : 0,
            'adjusted_cost'        : 0,
            'trade_value'          : 0,
            'trade_gross'          : 0,
            'incentives'           : 0,
            'frequency'            : 0,
            'rate'                 : get_field(sale, 'APR'),
            'term'                 : 0,
            'payment'              : 0,
            'amount'               : 0,
            'downpayment'          : 0,
            'residual_rate'        : 0,
            'residual_amount'      : 0,
            'mileage_allowed'      : 0,
            'mileage_rate'         : 0,
            'capital_cost'         : 0,
            'trade_ref'            : '',
            'trade_stock'          : '',
            'trade_vin'            : '',
            'trade_year'           : '',
            'trade_model'          : '',
            'trade_make'           : '',
            'trade_model'          : '',
            'trade_model_code'     : '',
            'trade_transmission'   : '',
            'trade_package'        : '',
            'trade_color'          : '',
            'trade_mileage'        : 0,
            'cobuyer_suffix'       : '',
            'cobuyer_first_name'   : '',
            'cobuyer_last_name'    : '',
            'cobuyer_full_name'    : '',
            'cobuyer_phone'        : '',
            'cobuyer_work'         : '',
            'cobuyer_cell'         : '',
            'cobuyer_email'        : '',
            'cobuyer_address'      : '',
            'cobuyer_city'         : '',
            'cobuyer_province'     : '',
            'cobuyer_country'      : '',
            'cobuyer_postal_code'  : '',
            'salesperson_name'     : '',
            'salesperson_number'   : '',
            'warranty_name'        : '',
            'warranty_term'        : 0,
            'warranty_mileage'     : 0,
            'warranty_cost'        : 0,
            'warranty_sale'        : 0,
        }

        # Financial Information
        if get_field(sale, 'DealType').lower() != 'cash':
            deal['term'] = get_field(sale, 'PaymentTerm')
            deal['frequency'] = 'm'

            if get_field(sale, 'PaymentsPerYear') == 26:
                deal['term'] = int((get_field(sale, 'PaymentTerm') / 26) * 12)
                deal['frequency'] = 'b'

            if get_field(sale, 'DealType').lower() == 'finance':
                if 'BalanceToFinance' in sale['FinanceInfo']:
                    deal['amount'] = sale['FinanceInfo']['BalanceToFinance']
                if 'Payment' in sale['FinanceInfo']:
                    deal['payment'] = sale['FinanceInfo']['Payment']

                # Bank Information
                if 'Code' in sale['FinanceInfo']['BankInfo']:
                    deal['bank_number'] = sale['FinanceInfo']['BankInfo']['Code']
                if 'Name' in sale['FinanceInfo']['BankInfo']:
                    deal['bank_name'] = sale['FinanceInfo']['BankInfo']['Name']
            else:
                if 'Payment' in sale['LeaseInfo']:
                    deal['payment'] = sale['LeaseInfo']['Payment']
                if 'ResidualPercent' in sale['LeaseInfo']:
                    deal['residual_rate'] = sale['LeaseInfo']['ResidualPercent']
                if 'ResidualAmount' in sale['LeaseInfo']:
                    deal['residual_amount'] = sale['LeaseInfo']['ResidualAmount']
                if 'MileageAllowed' in sale['LeaseInfo']:
                    deal['mileage_allowed'] = sale['LeaseInfo']['MileageAllowed']
                if 'MileageRate' in sale['LeaseInfo']:
                    deal['mileage_rate'] = sale['LeaseInfo']['MileageRate']
                if 'CapCost' in sale['LeaseInfo']:
                    deal['capital_cost'] = sale['LeaseInfo']['CapCost']
        else:
            if 'DueOnDelivery' in sale['CashInfo']:
                deal['amount'] = sale['CashInfo']['DueOnDelivery']
                if deal['amount'] < sale['CashInfo']['MSRP']:
                    deal['amount'] = sale['CashInfo']['MSRP']

        # Trade Information
        if 'Trades' in sale and len(sale['Trades']) > 0:
            if 'VehicleRef' in sale['Trades'][0]:
                deal['trade_ref'] = sale['Trades'][0]['VehicleRef']
                deal['trade_mileage'] = sale['Trades'][0]['Odometer']

        # Co-Buyer Information
        if len(sale['CoBuyerRefs']) > 0:
            customer = send_request('ContactGet', data={
                'SerialNumber' : id,
                'ContactId' : sale['CoBuyerRefs'][0]
            })

            customer = customer['Contacts'][0]

            deal['cobuyer_first_name'] = get_field(customer, 'FirstName').title()
            deal['cobuyer_last_name'] = get_field(customer, 'LastName').title()
            deal['cobuyer_full_name'] = deal['cobuyer_first_name'] + ' ' + deal['cobuyer_last_name']
            deal['cobuyer_phone'] = get_field(customer, 'HomePhone')
            deal['cobuyer_work'] = get_field(customer, 'BusinessPhone')
            deal['cobuyer_email'] = get_field(customer, 'EmailAddress')
            deal['cobuyer_cell'] = get_field(customer, 'CellPhone')
            deal['cobuyer_address'] = get_field(customer, 'Address').title()
            deal['cobuyer_city'] = get_field(customer, 'City').title()
            deal['cobuyer_province'] = get_field(customer, 'State').title()
            deal['cobuyer_country'] = 'Canada'
            deal['cobuyer_postal_code'] = get_field(customer, 'ZipCode')

        # Warranty
        if len(sale['Warranties']) > 0:
            if sale['Warranties'][0]['CompanyName'] != '':
                deal['warranty_name'] = sale['Warranties'][0]['CompanyName']
                deal['warranty_term'] = sale['Warranties'][0]['Term']
                deal['warranty_mileage'] = sale['Warranties'][0]['Mileage']
                deal['warranty_cost'] = sale['Warranties'][0]['Cost']
                deal['warranty_sale'] = sale['Warranties'][0]['Price']

        # Staff
        if len(sale['UserRoles']) > 0:
            for employee in sale['UserRoles']:
                if employee['Role'] == 'SalesRep' and 'Name' in employee:
                    deal['salesperson_number'] = sale['UserRoles'][0]['EmployeeRef']
                    deal['salesperson_name'] = sale['UserRoles'][0]['Name'].lower().title()

        data[get_field(sale, 'BuyerRef')].append(deal)

    vehicles = send_request('VehicleGet', data={
        'SerialNumber' : id,
        'IncludeInactive' : True
    })

    if 'Vehicles' in vehicles:
        for vehicle in vehicles['Vehicles']:
            for owner, deal_list in data.items():
                for app in deal_list:
                    if app['vehicle_ref'] == vehicle['VehicleId']:
                        app['vin'] = vehicle['VIN']
                        app['stock'] = vehicle['StockNumber']
                        app['cost'] = vehicle['BaseMSR']
                        app['invoice'] = vehicle['Retail']
                        app['price'] = (vehicle['Order']['Price'] if 'Order' in vehicle else 0)
                        app['msrp'] = vehicle['Retail']
                        app['holdback'] = 0
                        app['kilometres'] = vehicle['Odometer']
                        app['package_code'] = ''
                        app['model_code'] = vehicle['ModelNumber']
                        app['int_color'] = (vehicle['InteriorColor']['Description'].replace('/', '') if 'InteriorColor' in vehicle and 'Description' in vehicle['InteriorColor'] else '')
                        app['ext_color'] = (vehicle['ExteriorColor']['Description'].replace('/', '') if 'ExteriorColor' in vehicle and 'Description' in vehicle['ExteriorColor'] else '')
                        app['transmission'] = vehicle['Transmission']
                        app['stocked_at'] = None

                    if app['trade_ref'] == vehicle['VehicleId']:
                        app['trade_vin'] = vehicle['VIN']
                        app['trade_model_code'] = vehicle['ModelNumber']
                        app['trade_package'] = ''
                        app['trade_transmission'] = vehicle['Transmission']
                        app['trade_color'] = (vehicle['ExteriorColor']['Description'].replace('/', '') if 'ExteriorColor' in vehicle and 'Description' in vehicle['ExteriorColor'] else '')

    return data

def get_service(id, start_date=''):
    ''' Retieve a Service List '''
    data = {}
    vin_list = []

    response = send_request('RepairOrderGet', data={
        'SerialNumber' : id,
        'OpenDateSince' : start_date,
    })

    if 'RepairOrders' in response:
        for repair in response['RepairOrders']:
            vin_list.append(get_field(repair, 'VehicleRef'))

            if not get_field(repair, 'ContactRef') in data:
                data[get_field(repair, 'ContactRef')] = []

            parts = 0
            labour = 0
            description = ''

            if len(repair['Requests']) > 0 and 'CustomerSummary' in repair:
                parts = repair['CustomerSummary']['Parts']
                labour = repair['CustomerSummary']['Labour']

                if 'RequestDescription' in repair['Requests'][0]:
                    description = repair['Requests'][0]['RequestDescription']

                data[get_field(repair, 'ContactRef')].append({
                    'vin_ref'         : get_field(repair, 'VehicleRef'),
                    'customer_number' : get_field(repair, 'ContactRef'),
                    'ro'              : get_field(repair, 'RepairOrderNumber'),
                    'mileage'         : get_field(repair, 'MileageIn'),
                    'completed_at'    : get_field(repair, 'DateOpened')[0:16].replace('T', ' ') + ":00",
                    'opened_at'       : get_field(repair, 'DateOpened')[0:16].replace('T', ' ') + ":00",
                    'description'     : description,
                    'total'           : parts + labour,
                    'total_labour'    : labour,
                    'total_warranty'  : 0,
                    'total_parts'     : parts,
                    'vin'             : '',
                    'stock'           : '',
                    'stock_type'      : '',
                    'cost'            : 0,
                    'invoice'         : 0,
                    'price'           : 0,
                    'holdback'        : 0,
                    'msrp'            : 0,
                    'kilometres'      : '',
                    'package_code'    : '',
                    'model_code'      : '',
                    'int_color'       : '',
                    'ext_color'       : '',
                    'transmission'    : '',
                    'stocked_at'      : None
                })

    vehicles = send_request('VehicleGet', data={
        'SerialNumber' : id,
        'IncludeInactive' : True
    })

    if 'Vehicles' in vehicles:
        for vehicle in vehicles['Vehicles']:
            if vehicle['OwnerRef'] in data:
                for app in data[vehicle['OwnerRef']]:
                    if app['vin_ref'] == vehicle['VehicleId']:
                        app['vin'] = vehicle['VIN']
                        app['stock'] = vehicle['StockNumber']
                        app['stock_type'] = 'used'
                        app['cost'] = vehicle['BaseMSR']
                        app['invoice'] = vehicle['Retail']
                        app['price'] = (vehicle['Order']['Price'] if 'Order' in vehicle else 0)
                        app['msrp'] = vehicle['Retail']
                        app['holdback'] = 0
                        app['kilometres'] = vehicle['Odometer']
                        app['package_code'] = ''
                        app['model_code'] = vehicle['ModelNumber']
                        app['int_color'] = (vehicle['InteriorColor']['Description'].replace('/', '') if 'InteriorColor' in vehicle and 'Description' in vehicle['InteriorColor'] else '')
                        app['ext_color'] = (vehicle['ExteriorColor']['Description'].replace('/', '') if 'ExteriorColor' in vehicle and 'Description' in vehicle['ExteriorColor'] else '')
                        app['transmission'] = vehicle['Transmission']
                        app['stocked_at'] = None

    return data

def get_service_appointments(id, start_date=''):
    ''' Retieve a Service Appointents '''
    data = {}
    vin_list = []

    response = send_request('AppointmentGet', data={
        'SerialNumber' : id,
        'AppointmentSince' : start_date
    })

    for appointment in response['Appointments']:
        vin_list.append(get_field(appointment, 'VehicleRef'))

        if not get_field(appointment, 'ContactRef') in data:
            data[get_field(appointment, 'ContactRef')] = []

        data[get_field(appointment, 'ContactRef')].append({
            'vin_ref'             : get_field(appointment, 'VehicleRef'),
            'customer_number'     : get_field(appointment, 'ContactRef'),
            'number'              : get_field(appointment, 'AppointmentNumber'),
            'appointment_created' : get_field(appointment, 'LastUpdate').replace('T', ' ')[0:19],
            'appointment_at'      : get_field(appointment, 'AppointmentTime').replace('T', ' ')[0:19],
            'promised_date'       : get_field(appointment, 'AppointmentTime').replace('T', ' ')[0:19],
            'vin'                 : '',
            'stock'               : '',
            'stock_type'          : '',
            'cost'                : 0,
            'invoice'             : 0,
            'price'               : 0,
            'holdback'            : 0,
            'msrp'                : 0,
            'kilometres'          : '',
            'package_code'        : '',
            'model_code'          : '',
            'int_color'           : '',
            'ext_color'           : '',
            'transmission'        : '',
            'stocked_at'          : None
        })

    vehicles = send_request('VehicleGet', data={
        'SerialNumber' : id,
        'IncludeInactive' : True
    })

    if 'Vehicles' in vehicles:
        for vehicle in vehicles['Vehicles']:
            if vehicle['OwnerRef'] in data:
                for app in data[vehicle['OwnerRef']]:
                    if app['vin_ref'] == vehicle['VehicleId']:
                        app['vin'] = vehicle['VIN']
                        app['stock'] = vehicle['StockNumber']
                        app['stock_type'] = 'used'
                        app['cost'] = vehicle['BaseMSR']
                        app['invoice'] = vehicle['Retail']
                        app['price'] = (vehicle['Order']['Price'] if 'Order' in vehicle else 0)
                        app['msrp'] = vehicle['Retail']
                        app['holdback'] = 0
                        app['kilometres'] = vehicle['Odometer']
                        app['package_code'] = ''
                        app['model_code'] = vehicle['ModelNumber']
                        app['int_color'] = (vehicle['InteriorColor']['Description'].replace('/', '') if 'InteriorColor' in vehicle and 'Description' in vehicle['InteriorColor'] else '')
                        app['ext_color'] = (vehicle['ExteriorColor']['Description'].replace('/', '') if 'ExteriorColor' in vehicle and 'Description' in vehicle['ExteriorColor'] else '')
                        app['transmission'] = vehicle['Transmission']
                        app['stocked_at'] = None
    return data

def get_inventory(id, start_date=''):
    ''' Retrieve a Inventory '''
    data = []

    response = send_request('VehicleGet', data={
        'SerialNumber' : id,
        'StatusList' : ['new', 'used']
    })

    for vehicle in response['Vehicles']:
        type = ''
        if get_field(vehicle, 'Status').lower() in ['new', 'used']:
            type = get_field(vehicle, 'Status').lower()
            data.append({
                'vin'          : get_field(vehicle, 'VIN'),
                'stock'        : get_field(vehicle, 'StockNumber'),
                'stock_type'   : type,
                'cost'         : get_field(vehicle, 'BaseMSR'),
                'invoice'      : get_field(vehicle, 'Retail'),
                'msrp'         : get_field(vehicle, 'Retail'),
                'price'        : (vehicle['Order']['Price'] if 'Order' in vehicle else 0),
                'holdback'     : 0,
                'kilometres'   : get_field(vehicle, 'Odometer'),
                'package_code' : get_field(vehicle, ''),
                'model_code'   : get_field(vehicle, 'ModelNumber'),
                'int_color'    : (vehicle['InteriorColor']['Description'].replace('/', '') if 'InteriorColor' in vehicle and 'Description' in vehicle['InteriorColor'] else ''),
                'ext_color'    : (vehicle['ExteriorColor']['Description'].replace('/', '') if 'ExteriorColor' in vehicle and 'Description' in vehicle['ExteriorColor'] else ''),
                'transmission' : get_field(vehicle, 'Transmission'),
                'stocked_at'   : get_field(vehicle, 'DateReceived').replace('T', ' ')[0:19] if get_field(vehicle, 'DateReceived') != '' else None
            })

    return data

def get_field(data, field):
    ''' Retrieve values from field '''
    try:
        return data[field]
    except:
        return ''
