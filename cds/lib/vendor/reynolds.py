import csv
import datetime

def get_customers(id, start_date=''):
    ''' Get Customers '''
    input_file = csv.DictReader(open('/Applications/MAMP/htdocs/cds-cli/cds/files/sales.csv'))
    data = []

    for customer in input_file:
        name = get_field(customer, 'B-FMI').lower().title() + ' ' + get_field(customer, 'B-LST-NME').lower().title()

        data.append({
            'type'        : 'I',
            'number'      : get_field(customer, 'CUST-NO'),
            'first_name'  : get_field(customer, 'B-FMI').title(),
            'middle_name' : get_field(customer, 'MIDDLE-NAME-DV').title(),
            'last_name'   : get_field(customer, 'B-LST-NME').title(),
            'full_name'   : name,
            'address'     : get_field(customer, 'B-ADD').title(),
            'city'        : get_field(customer, 'B-CITY').title(),
            'province'    : get_field(customer, 'B-ST').upper(),
            'country'     : get_field(customer, 'B-COUNTY').title(),
            'postal_code' : get_field(customer, 'B-ZIP').title(),
            'home'        : get_field(customer, 'B-H-PHONE'),
            'cell'        : get_field(customer, 'PH-CELL-FMT-DV'),
            'email'       : get_field(customer, 'EMAIL-ADDRESS-DV'),
            'work'        : get_field(customer, 'B-W-PHONE'),
            'can_email'   : 1,
            'can_call'    : 1,
            'can_mail'    : 1,
        })

    return data

def get_deals(id, start_date=''):
    ''' Retieve a list of Deals '''
    input_file = csv.DictReader(open('/Applications/MAMP/htdocs/cds-cli/cds/files/sales.csv'))
    data = {}

    for sale in input_file:
        type = 'finance'

        if get_field(sale, 'TERM') == '1':
            type = 'cash'
        else:
            if get_field(sale, 'AMT-FIN') == '0':
                type = 'lease'

        if not get_field(sale, 'CUST-NO') in data:
            data[get_field(sale, 'CUST-NO')] = []

        deal = {
            'customer_number'      : get_field(sale, 'CUST-NO'),
            'deal_number'          : get_field(sale, 'DEAL-NO'),
            'vehicle_ref'          : get_field(sale, 'ID-NO'),
            'vin'                  : get_field(sale, 'ID-NO'),
            'stock'                : get_field(sale, 'STK-NO'),
            'stock_type'           : ('new' if get_field(sale, 'NUO').upper() == 'N' else 'used'),
            'cost'                 : 0,
            'invoice'              : 0,
            'price'                : get_field(sale, 'PRICE') if get_field(sale, 'PRICE') else 0,
            'holdback'             : 0,
            'msrp'                 : 0,
            'kilometres'           : get_field(sale, 'SaleOdometer'),
            'package_code'         : get_field(sale, ''),
            'model_code'           : get_field(sale, 'MDL-NO'),
            'int_color'            : get_field(sale, 'INT-COLOR'),
            'ext_color'            : get_field(sale, 'CLR'),
            'transmission'         : get_field(sale, 'ODOM'),
            'stocked_at'           : None,
            'type'                 : type,
            'sold_at'              : datetime.datetime.strptime(get_field(sale, 'DEAL-DATE'), '%m/%d/%y').strftime('%Y-%m-%d')  + ' 00:00:00',
            'bank_number'          : get_field(sale, 'BANK-ID'),
            'bank_name'            : get_field(sale, 'BANK-NAME'),
            'bank_address'         : get_field(sale, 'BANK-ADD'),
            'cost'                 : 0,
            'journal_amount'       : 0,
            'journal_cost'         : 0,
            'adjustments'          : 0,
            'adjusted_cost'        : 0,
            'trade_value'          : get_field(sale, 'TRADE1') if get_field(sale, 'TRADE1') else 0,
            'trade_gross'          : 0,
            'incentives'           : 0,
            'frequency'            : 0,
            'rate'                 : 0,
            'term'                 : get_field(sale, 'TERM') if get_field(sale, 'TERM') else 0,
            'payment'              : get_field(sale, 'PAYMENT') if get_field(sale, 'PAYMENT') else 0,
            'amount'               : get_field(sale, 'AMT-FIN') if get_field(sale, 'AMT-FIN') else 0,
            'downpayment'          : get_field(sale, 'CASH-DOWN') if get_field(sale, 'CASH-DOWN') else 0,
            'residual_rate'        : 0,
            'residual_amount'      : 0,
            'mileage_allowed'      : 0,
            'mileage_rate'         : 0,
            'capital_cost'         : 0,
            'trade_ref'            : get_field(sale, 'TR1-ID'),
            'trade_stock'          : '',
            'trade_vin'            : get_field(sale, 'TR1-ID'),
            'trade_year'           : get_field(sale, 'TR1-YEAR'),
            'trade_make'           : get_field(sale, 'TR1-MAKE'),
            'trade_model'          : get_field(sale, 'TR1-MODEL'),
            'trade_model_code'     : '',
            'trade_transmission'   : '',
            'trade_package'        : '',
            'trade_color'          : '',
            'trade_mileage'        : get_field(sale, 'T-ODOM1'),
            'cobuyer_suffix'       : get_field(sale, 'C-SUFFIX'),
            'cobuyer_first_name'   : get_field(sale, 'C-FMI'),
            'cobuyer_last_name'    : get_field(sale, 'C-LST-NME'),
            'cobuyer_full_name'    : get_field(sale, 'C-NAME'),
            'cobuyer_phone'        : get_field(sale, 'C-H-PHONE'),
            'cobuyer_work'         : get_field(sale, 'C-W-PHONE'),
            'cobuyer_cell'         : get_field(sale, 'CB-CELL'),
            'cobuyer_email'        : get_field(sale, 'CB-EMAIL'),
            'cobuyer_address'      : get_field(sale, 'C-ADD'),
            'cobuyer_city'         : get_field(sale, 'C-CITY'),
            'cobuyer_province'     : get_field(sale, 'C-ST'),
            'cobuyer_country'      : get_field(sale, 'C-COUNTY'),
            'cobuyer_postal_code'  : get_field(sale, 'C-ZIP'),
            'salesperson_name'     : '',
            'salesperson_number'   : '',
            'warranty_name'        : '',
            'warranty_term'        : 0,
            'warranty_mileage'     : 0,
            'warranty_cost'        : 0,
            'warranty_sale'        : 0,
        }


        data[get_field(sale, 'CUST-NO')].append(deal)

    return data

def get_field(data, field):
    ''' Retrieve values from field '''
    try:
        return data[field]
    except:
        return ''
