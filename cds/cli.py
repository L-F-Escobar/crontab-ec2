import sys
import click
import datetime
import traceback
from cds.db.database import *
from cds.models.incentives import *
from cds.models.vehicles import *
from cds.models.dealers import *
from cds.models.service import *
from cds.models.customers import *
from cds.models.build import *
from cds.models.deals import *
from cds.models.vendor import *
from cds.models.appointments import *
from cds.models.opportunities import *
from cds.models.alerts import *
from cds.models.users import *
from cds.models.prospects import *
from cds.models.conversations import *
from cds.models.notes import *
from cds.models.leads import *
from cds.utils import vin
from cds.utils import gmail
from cds.utils import valuation
from cds.utils import incentives
from cds.utils import build
from cds.utils import evox
from cds.lib.vendor import pbs
from cds.lib.vendor import reynolds

from datetime import date, timedelta
from sqlalchemy.orm import sessionmaker
from dateutil.relativedelta import relativedelta

engine = database.main()

Session = sessionmaker(bind=engine)
session = Session()

@click.command()
@click.option('--key', default=None, help='Dealer Key')
def cli(key):
    store = session.query(Dealer).filter(Dealer.key == key).first()

    if store:
        click.echo('\r\n')
        click.echo(click.style(' {:80s} '.format(key + ' | ' + store.name), bg='yellow', fg='black'))

        process(store)

    session.close()

def get_gmail_service():
    ''' Will refresh token automatically if expired. '''
    return gmail.get_service()

def process(store):
    # # Process Build Data
    #update_build(store.brand, store.province, store.postal_code)

    # Process DMS Data
    #update_dms_data(store, '2011-01-01 00:00:00', True)

    # Update Opportunity
    update_opportunities(store)

    return ""

def update_customer(data):
    ''' Create / Update Customer '''
    try:
        customer = session.query(Customer).filter(
            Customer.number == data['number']
        ).first()

        if not customer:
            customer = Customer()
            customer.number = data['number']
            customer.type = data['type']
            customer.full_name = data['full_name']
            customer.first_name = data['first_name']
            customer.middle_name = data['middle_name']
            customer.last_name = data['last_name']
            customer.address = data['address']
            customer.city = data['city']
            customer.province = data['province']
            customer.country = data['country']
            customer.postal_code = data['postal_code']
            customer.distance = 0
            customer.updated_at = datetime.datetime.now()
            customer.created_at = datetime.datetime.now()

            session.add(customer)
            session.flush()
            session.refresh(customer)

        contact = session.query(CustomerContact).filter(
            CustomerContact.customer_id == customer.id
        ).first()

        if not contact:
            contact = CustomerContact()
            contact.customer_id = customer.id
            contact.created_at = datetime.datetime.now()

        contact.home = data['home']
        contact.cell = data['cell']
        contact.work = data['work']
        contact.email = data['email']
        contact.can_mail = data['can_mail']
        contact.can_email = data['can_email']
        contact.can_call = data['can_call']
        contact.updated_at = datetime.datetime.now()

        session.add(contact)

        return {
            'id'     : customer.id,
            'number' : customer.number
        }
    except Exception as e:
        print(traceback.format_exc())

def update_deal(customer_id, data):
    ''' Create / Update Deal '''
    try:
        deal = session.query(Deal).filter(
            Deal.number == data['deal_number']
        ).first()

        if not deal:
            vehicle = update_vehicle({
                'vin'             : data['vin'],
                'stock'           : data['stock'],
                'stock_type'      : data['stock_type'],
                'cost'            : data['cost'],
                'invoice'         : data['invoice'],
                'price'           : data['price'],
                'msrp'            : data['msrp'],
                'holdback'        : data['holdback'],
                'kilometres'      : data['kilometres'],
                'package_code'    : data['package_code'],
                'model_code'      : data['model_code'],
                'int_color'       : data['int_color'],
                'ext_color'       : data['ext_color'],
                'transmission'    : data['transmission'],
                'stocked_at'      : data['stocked_at'],
                'deleted_at'      : datetime.datetime.now()
            })

            deal = Deal()
            deal.number = data['deal_number']
            deal.vehicle_id = vehicle.id
            deal.customer_id = customer_id
            deal.type = data['type']
            deal.mileage = data['kilometres']
            deal.price = data['price']
            deal.cost = data['cost']
            deal.journal_amount = data['journal_amount']
            deal.journal_cost = data['journal_cost']
            deal.adjustments = data['adjustments']
            deal.adjusted_cost = data['adjusted_cost']
            deal.trade_value = data['trade_value']
            deal.trade_gross = data['trade_gross']
            deal.incentives = data['incentives']
            deal.sold_at = data['sold_at']
            deal.created_at = datetime.datetime.now()
            deal.updated_at = datetime.datetime.now()

            session.add(deal)
            session.flush()
            session.refresh(deal)

            # Financing Details
            financing = DealFinancing()
            financing.deal_id = deal.id
            financing.type = data['type']
            financing.bank_name = data['bank_name']
            financing.bank_number = data['bank_number']
            financing.bank_address = data['bank_address']
            financing.term = data['term']
            financing.rate = data['rate']
            financing.frequency = data['frequency']
            financing.payment = data['payment']
            financing.amount = data['amount']
            financing.downpayment = data['downpayment']
            financing.capital_cost = data['capital_cost']
            financing.residual_rate = data['residual_rate']
            financing.residual_amount = data['residual_amount']
            financing.mileage_allowed = data['mileage_allowed']
            financing.mileage_rate = data['mileage_rate']
            financing.created_at = datetime.datetime.now()
            financing.updated_at = datetime.datetime.now()

            session.add(financing)

            # Customer Ownership
            ownership = CustomerVehicle()
            ownership.vehicle_id = vehicle.id
            ownership.customer_id = customer_id
            ownership.created_at = datetime.datetime.now()
            ownership.updated_at = datetime.datetime.now()

            session.add(ownership)

            # Tradein Vehicle
            if data['trade_vin'] != '':
                trade_vehicle = update_vehicle({
                    'vin'             : data['trade_vin'],
                    'stock'           : data['trade_stock'],
                    'stock_type'      : 'used',
                    'cost'            : 0,
                    'invoice'         : 0,
                    'price'           : 0,
                    'msrp'            : 0,
                    'holdback'        : 0,
                    'kilometres'      : data['trade_mileage'],
                    'package_code'    : data['trade_package'],
                    'model_code'      : data['trade_model_code'],
                    'int_color'       : '',
                    'ext_color'       : data['trade_color'],
                    'transmission'    : data['trade_transmission'],
                    'stocked_at'      : data['sold_at'],
                    'deleted_at'      : datetime.datetime.now()
                })

                trade = DealTrade()
                trade.deal_id = deal.id
                trade.vehicle_id = trade_vehicle.id
                trade.vin = trade_vehicle.vin
                trade.year = trade_vehicle.year
                trade.make = trade_vehicle.make
                trade.model = trade_vehicle.model
                trade.trim = trade_vehicle.trim
                trade.mileage = data['trade_mileage']
                trade.created_at = datetime.datetime.now()
                trade.updated_at = datetime.datetime.now()

                session.add(trade)

                # Update Ownership Records
                ownership = session.query(CustomerVehicle).filter(
                    CustomerVehicle.vehicle_id == trade_vehicle.id
                ).filter(
                    CustomerVehicle.customer_id == customer_id
                ).filter(
                    CustomerVehicle.deleted_at == None
                ).first()

                if ownership:
                    ownership.deleted_at = data['sold_at']

            # Staff
            if data['salesperson_name'] != '':
                employee = DealEmployee()
                employee.deal_id = deal.id
                employee.type = 'salesperson'
                employee.number = data['salesperson_number']
                employee.name = data['salesperson_name']
                employee.created_at = datetime.datetime.now()
                employee.updated_at = datetime.datetime.now()

                session.add(employee)

            # Co-Buyer
            if data['cobuyer_full_name'] != '':
                cobuyer = DealCoBuyer()
                cobuyer.deal_id = deal.id
                cobuyer.first_name = data['cobuyer_first_name']
                cobuyer.last_name = data['cobuyer_last_name']
                cobuyer.full_name = data['cobuyer_full_name']
                cobuyer.address = data['cobuyer_address']
                cobuyer.city = data['cobuyer_city']
                cobuyer.province = data['cobuyer_province']
                cobuyer.country = data['cobuyer_country']
                cobuyer.postal_code = data['cobuyer_postal_code']
                cobuyer.home = data['cobuyer_phone']
                cobuyer.cell = data['cobuyer_cell']
                cobuyer.work = data['cobuyer_work']
                cobuyer.email = data['cobuyer_email']
                cobuyer.created_at = datetime.datetime.now()
                cobuyer.updated_at = datetime.datetime.now()

                session.add(cobuyer)

            # Warranty
            if data['warranty_name'] != '':
                warranty = DealWarranty()
                warranty.deal_id = deal.id
                warranty.name = data['warranty_name']
                warranty.term = data['warranty_term']
                warranty.mileage = data['warranty_mileage']
                warranty.sale = data['warranty_sale']
                warranty.cost = data['warranty_cost']
                warranty.created_at = datetime.datetime.now()
                warranty.updated_at = datetime.datetime.now()

                session.add(warranty)

    except Exception as e:
        print(traceback.format_exc())

def update_service(customer_id, data):
    ''' Create / Update Service Data '''
    try:
        vehicle = session.query(Vehicle).filter(
            Vehicle.vin == data['vin']
        ).first()

        if not vehicle:
            vehicle = update_vehicle({
                'vin'             : data['vin'],
                'stock'           : data['stock'],
                'stock_type'      : data['stock_type'],
                'cost'            : data['cost'],
                'invoice'         : data['invoice'],
                'price'           : data['price'],
                'msrp'            : data['msrp'],
                'holdback'        : data['holdback'],
                'kilometres'      : data['kilometres'],
                'package_code'    : data['package_code'],
                'model_code'      : data['model_code'],
                'int_color'       : data['int_color'],
                'ext_color'       : data['ext_color'],
                'transmission'    : data['transmission'],
                'stocked_at'      : data['stocked_at'],
                'deleted_at'      : datetime.datetime.now()
            })

        repair = session.query(Service.id).filter(
            Service.ro == data['ro']
        ).first()

        if not repair:
            repair = Service()
            repair.customer_id = customer_id
            repair.vehicle_id = vehicle.id
            repair.ro = data['ro']
            repair.description = data['description']
            repair.mileage = data['mileage']
            repair.total = data['total']
            repair.total_labour = data['total_labour']
            repair.total_parts = data['total_parts']
            repair.total_warranty = data['total_warranty']
            repair.opened_at = data['opened_at']
            repair.completed_at = data['completed_at']
            repair.created_at = datetime.datetime.now()
            repair.updated_at = datetime.datetime.now()

            session.add(repair)

            ownership = session.query(CustomerVehicle.id).filter(CustomerVehicle.vehicle_id == vehicle.id).first()

            if not ownership:
                ownership = CustomerVehicle()
                ownership.vehicle_id = vehicle.id
                ownership.customer_id = customer_id
                ownership.created_at = datetime.datetime.now()
                ownership.updated_at = datetime.datetime.now()

                session.add(ownership)

    except Exception as e:
        print(traceback.format_exc())

def update_service_appointment(customer_id, data):
    ''' Create / Update Service Appointent '''
    try:
        vehicle = session.query(Vehicle).filter(
            Vehicle.vin == data['vin']
        ).first()

        if not vehicle:
            vehicle = update_vehicle({
                'vin'             : data['vin'],
                'stock'           : data['stock'],
                'stock_type'      : data['stock_type'],
                'cost'            : data['cost'],
                'invoice'         : data['invoice'],
                'price'           : data['price'],
                'msrp'            : data['msrp'],
                'holdback'        : data['holdback'],
                'kilometres'      : data['kilometres'],
                'package_code'    : data['package_code'],
                'model_code'      : data['model_code'],
                'int_color'       : data['int_color'],
                'ext_color'       : data['ext_color'],
                'transmission'    : data['transmission'],
                'stocked_at'      : data['stocked_at'],
                'deleted_at'      : datetime.datetime.now()
            })

        appointment = session.query(ServiceAppointment).filter(
            ServiceAppointment.number == data['number']
        ).first()

        if vehicle and not appointment:
            appointment = ServiceAppointment()
            appointment.customer_id = customer_id
            appointment.vehicle_id = vehicle.id
            appointment.number = data['number']
            appointment.appointment_at = data['appointment_at']
            appointment.created_at = datetime.datetime.now()
            appointment.updated_at = datetime.datetime.now()

            session.add(appointment)

            ownership = session.query(CustomerVehicle.id).filter(CustomerVehicle.vehicle_id == vehicle.id).first()

            if not ownership:
                ownership = CustomerVehicle()
                ownership.vehicle_id = vehicle.id
                ownership.customer_id = customer_id
                ownership.created_at = datetime.datetime.now()
                ownership.updated_at = datetime.datetime.now()

                session.add(ownership)
    except Exception as e:
        print(traceback.format_exc())

def update_vehicle(data):
    ''' Create / Update Vehicle Data '''
    try:
        vehicle = session.query(Vehicle).filter(
            Vehicle.vin == data['vin']
        ).first()

        if not vehicle or not vehicle.decoded_at:
            should_add = False
            data = vin.decode(data, data['token'] if 'token' in data else '')

            if 'token' in data:
                photo = evox.get_vehicle(data['year'], data['make'], data['model'], data['trim'])

            if not vehicle:
                vehicle = Vehicle()
                vehicle.deleted_at = data['deleted_at']
                vehicle.created_at = datetime.datetime.now()
                vehicle.updated_at = datetime.datetime.now()
                should_add = True

            vehicle.vin = data['vin']
            vehicle.stock = data['stock']
            vehicle.stock_type = data['stock_type']
            vehicle.year = data['year']
            vehicle.make = data['make']
            vehicle.model = data['model']
            vehicle.trim = data['trim']
            vehicle.trim_id = data['trim_id']
            vehicle.price = data['price']
            vehicle.cost = data['cost']
            vehicle.invoice = data['invoice']
            vehicle.msrp = data['msrp']
            vehicle.holdback = data['holdback']
            vehicle.model_code = data['model_code']
            vehicle.type = data['type']
            vehicle.body_type = data['body_type']
            vehicle.engine = data['engine']
            vehicle.horsepower = data['horsepower']
            vehicle.displacement = data['displacement']
            vehicle.drivetrain = data['drivetrain']
            vehicle.fuel = data['fuel']
            vehicle.doors = data['doors']
            vehicle.ext_color = data['ext_color']
            vehicle.int_color = data['int_color']
            vehicle.transmission = data['transmission']
            vehicle.kilometres = data['kilometres']
            vehicle.searchable = ''
            vehicle.efficiency_city = data['efficiency_city']
            vehicle.efficiency_hwy = data['efficiency_hwy']

            if 'token' in data:
                vehicle.photo = (photo if photo != '' else data['photo'])

            vehicle.stocked_at = data['stocked_at']

            if data['trim_id']:
                vehicle.decoded_at = datetime.datetime.now()

            if should_add:
                session.add(vehicle)
                session.flush()
                session.refresh(vehicle)

            if 'features' in data and len(data['features']) > 0:
                for item in data['features']:
                    for key, value in item.items():
                        feature = VehicleFeature()
                        feature.vehicle_id = vehicle.id
                        feature.option = key
                        feature.value = value
                        feature.created_at = datetime.datetime.now()
                        feature.updated_at = datetime.datetime.now()

                        session.add(feature)

        return vehicle
    except Exception as e:
        print(traceback.format_exc())

def update_vehicle_valuation(vehicle):
    ''' Update Vehicle Value '''
    try:
        date_limit = datetime.datetime.now() - datetime.timedelta(days=90)
        date_limit = date_limit.strftime('%Y-%m-%d')

        active = session.query(VehicleValue.created_at, VehicleValue.active).filter(VehicleValue.active == 1).filter(
            VehicleValue.vehicle_id == vehicle.id
        ).first()

        if not active or active and str(active.created_at) <= date_limit:
            data = valuation.determine(
                vehicle.vin,
                vehicle.model_code,
                vehicle.kilometres,
                'ON'
            )

            value = VehicleValue()
            value.vehicle_id = vehicle.id
            value.value = data['value']
            value.great = data['great']
            value.good = data['good']
            value.average = data['average']
            value.rough = data['rough']
            value.active = 1
            value.created_at = datetime.datetime.now()
            value.updated_at = datetime.datetime.now()

            if active:
                active.active = 0

            session.add(value)
    except Exception as e:
        print(traceback.format_exc())


def should_valuate(vehicle):
    ''' Check If Applicable For Update '''
    if not vehicle.deleted_at:
        return False

    service = session.query(Service.completed_at).filter(
        Service.vehicle_id == vehicle.id
    ).order_by(
        Service.completed_at.desc()
    ).first()

    if service:
        date_limit = datetime.datetime.now() - datetime.timedelta(days=820)
        date_limit = date_limit.strftime('%Y-%m-%d')

        if str(service.completed_at) < date_limit:
            return False

    return True

def update_dms_data(brand, start_date, onboard=False):
    ''' Update DMS Data '''
    # feeds = session.query(Feed).all()
    # data = {}
    #
    # types = {
    #     'inventory'    : 'get_inventory',
    #     'customers'    : 'get_customers',
    #     'service'      : 'get_service',
    #     'appointments' : 'get_service_appointments',
    #     'sales'        : 'get_deals'
    # }
    #
    # for feed in feeds:
    #     type = feed.type.name.lower()
    #     name = feed.vendor.name.lower()
    #
    #     if name == "reynolds":
    #         continue
    #
    #     if type in types:
    #         run_service = getattr(globals().get(name), types[type])
    #         data[type] = run_service('5104', ('' if onboard else start_date))
    #
    #         click.echo(
    #             click.style(
    #                 ' {:80s} '.format(type.title() + ': ' + str(len(data[type]))),
    #                 bg='bright_black',
    #                 fg='white'
    #             )
    #         )
    #
    # click.echo('\r')
    # count = 1
    #
    # if 'inventory' in data:
    #     for vehicle in data['inventory']:
    #         update_vehicle({
    #             'vin'             : vehicle['vin'],
    #             'stock'           : vehicle['stock'],
    #             'stock_type'      : vehicle['stock_type'],
    #             'cost'            : vehicle['cost'],
    #             'invoice'         : vehicle['invoice'],
    #             'price'           : vehicle['price'],
    #             'msrp'            : vehicle['msrp'],
    #             'holdback'        : vehicle['holdback'],
    #             'kilometres'      : vehicle['kilometres'],
    #             'package_code'    : vehicle['package_code'],
    #             'model_code'      : vehicle['model_code'],
    #             'int_color'       : vehicle['int_color'],
    #             'ext_color'       : vehicle['ext_color'],
    #             'transmission'    : vehicle['transmission'],
    #             'stocked_at'      : vehicle['stocked_at'],
    #             'deleted_at'      : None
    #         })
    #
    #         sys.stdout.write("\r" + ' {:15s} '.format(str(count) + '/' + str(len(data[type]))) + ' Inventory Units Processed')
    #         sys.stdout.flush()
    #         count = count + 1
    #
    # count = 1
    #
    # for customer in data['customers']:
    #     customer_id = update_customer(customer)
    #
    #     if customer_id != '':
    #         # Create / Update Deals
    #         if 'sales' in data:
    #             if customer_id['number'] in data['sales']:
    #                 for deal in data['sales'][customer_id['number']]:
    #                     update_deal(
    #                         customer_id['id'],
    #                         deal
    #                 )
    #
    #         # Create / Update Service
    #         if 'service' in data:
    #             if customer_id['number'] in data['service']:
    #                 for service in data['service'][customer_id['number']]:
    #                     update_service(
    #                         customer_id['id'],
    #                         service
    #                     )
    #
    #         # Create / Update Appointments
    #         if 'appointments' in data:
    #             if customer_id['number'] in data['appointments']:
    #                 for appointment in data['appointments'][customer_id['number']]:
    #                     update_service_appointment(
    #                         customer_id['id'],
    #                         appointment
    #                     )
    #
    #         sys.stdout.write("\r" + ' {:15s} '.format(str(count) + '/' + str(len(data['customers']))) + ' Customers Processed')
    #         sys.stdout.flush()
    #
    #         count = count + 1
    #
    # session.commit()

    # Decode & Value Vehicles
    vehicles = session.query(Vehicle).all()
    token = vin.get_auth_token()
    count = 1

    for vehicle in vehicles:
        if not vehicle.decoded_at:
            vehicle = update_vehicle({
                'vin'          : vehicle.vin,
                'stock'        : vehicle.stock,
                'stock_type'   : vehicle.stock_type,
                'cost'         : vehicle.cost,
                'invoice'      : vehicle.invoice,
                'price'        : vehicle.price,
                'msrp'         : vehicle.msrp,
                'holdback'     : vehicle.holdback,
                'kilometres'   : vehicle.kilometres,
                'package_code' : vehicle.package_code,
                'model_code'   : vehicle.model_code,
                'int_color'    : vehicle.int_color,
                'ext_color'    : vehicle.ext_color,
                'transmission' : vehicle.transmission,
                'stocked_at'   : vehicle.stocked_at,
                'deleted_at'   : vehicle.deleted_at,
                'token'        : token
            })

            session.commit()

        # Update Values
        # if should_valuate(vehicle):
        #     update_vehicle_valuation(vehicle)


        sys.stdout.write("\r" + ' {:15s} '.format(str(count) + '/' + str(len(vehicles))) + ' Vehicles Checked')
        sys.stdout.flush()

        count = count + 1

    return brand

def update_build(brand, province, postal_code):
    ''' Update Build Data '''
    update_incentives('401748', postal_code)

    update_build_vehicle(brand, province)

    return brand

def update_incentives(trim_id, postal_code):
    ''' Update Vehicle Incentives '''
    try:
        rates = incentives.retrieve(trim_id, postal_code)

        for trim in rates:
            incentive = Incentive()
            incentive.program = trim['program']
            incentive.type = trim['type']
            incentive.incentive = trim['incentive']
            incentive.year = trim['year']
            incentive.make = trim['make']
            incentive.model = trim['model']
            incentive.trim = trim['trim']
            incentive.trim_id = trim_id
            incentive.term = trim['term']
            incentive.rate = trim['rate']
            incentive.residual = trim['residual']
            incentive.factor = trim['factor']
            incentive.cash = trim['cash']
            incentive.active = 1
            incentive.start_at = trim['start_at']
            incentive.end_at = trim['end_at']
            incentive.created_at = datetime.datetime.now()
            incentive.updated_at = datetime.datetime.now()

            session.add(incentive)

        session.commit()
    except Exception as e:
        print(traceback.format_exc())

def update_build_vehicle(brand, province):
    ''' Update Build Data '''
    try:
        data = build.process(brand, province)

        for trim in data:
            vehicle = session.query(BuildVehicle).filter(
                BuildVehicle.trim_id == trim['trim_id']
            ).first()

            if not vehicle:
                vehicle = BuildVehicle()
                vehicle.year = trim['year']
                vehicle.make = trim['make']
                vehicle.model = trim['model']
                vehicle.trim = trim['trim']
                vehicle.trim_id = trim['trim_id']
                vehicle.body_type = trim['body_type']
                vehicle.model_code = trim['model_code']
                vehicle.msrp = trim['msrp']
                vehicle.invoice = trim['invoice']
                vehicle.freight = trim['freight']
                vehicle.type = trim['type']
                vehicle.doors = trim['doors']
                vehicle.engine = trim['engine']
                vehicle.horsepower = trim['horsepower']
                vehicle.displacement = trim['displacement']
                vehicle.torque = trim['torque']
                vehicle.fuel = trim['fuel']
                vehicle.transmission = trim['transmission']
                vehicle.drivetrain = trim['drivetrain']
                vehicle.efficiency_city = trim['efficiency_city']
                vehicle.efficiency_hwy = trim['efficiency_hwy']
                vehicle.created_at = datetime.datetime.now()
                vehicle.updated_at = datetime.datetime.now()

                session.add(vehicle)
                session.flush()
                session.refresh(vehicle)

            stock_photo = evox.get_vehicle(trim['year'], trim['make'], trim['model'], trim['trim'])

            if stock_photo != '':
                photo = session.query(BuildVehiclePhoto).filter(BuildVehiclePhoto.code == '01').filter(
                    BuildVehiclePhoto.build_vehicle_id == vehicle.id
                ).filter(
                    BuildVehiclePhoto.type == 'Default'
                ).first()

                if not photo:
                    photo = BuildVehiclePhoto()
                    photo.build_vehicle_id = vehicle.id
                    photo.type = 'Default'
                    photo.code = '01'
                    photo.url = stock_photo
                    photo.created_at = datetime.datetime.now()
                    photo.updated_at = datetime.datetime.now()

                    session.add(photo)

            for item in trim['features']:
                for key, value in item.items():
                    if '/ (KM)' in key.upper():
                        warranty = BuildVehicleWarranty()
                        warranty.build_vehicle_id = vehicle.id
                        warranty.type = key
                        warranty.value = value
                        warranty.created_at = datetime.datetime.now()
                        warranty.updated_at = datetime.datetime.now()

                        session.add(warranty)
                    else:
                        feature = BuildVehicleFeature()
                        feature.build_vehicle_id = vehicle.id
                        feature.option = key
                        feature.value = value
                        feature.created_at = datetime.datetime.now()
                        feature.updated_at = datetime.datetime.now()

                        session.add(feature)

            click.echo(f'{vehicle.year} {vehicle.make} {vehicle.model} {vehicle.trim}')

        session.commit()
    except Exception as e:
        print(traceback.format_exc())

def get_customer_benchmarks(customer_id, vehicle_id):
    ''' Retrieves Benchmark Data '''
    data = {
        'name' : '',
        'vehicle_name' : '',
        'stock_type' : '',
        'rating' : 0,
        'apr' : 0,
        'payments' : 0,
        'payments_new' : 0,
        'payments_made' : 0,
        'payments_left' : 0,
        'term' : 0,
        'trade' : 0,
        'equity' : 0,
        'matches' : 0,
        'distance' : 0,
        'service_last' : 0,
        'service_total' : 0,
        'warranty' : None,
        'warranty_months' : 0,
        'warranty_mileage' : 0,
        'appointment_at' : None,
        'serviced_at' : None,
    }

    # Deal Data
    deal = session.query(Deal).filter(
        Deal.customer_id == customer_id,
        Deal.vehicle_id == vehicle_id
    ).first()

    if deal:
        data['apr'] = deal.financing.rate
        data['term'] = deal.financing.term
        data['payments'] = deal.financing.payment
        data['payments_left'] = 12
        data['payments_made'] = 32

    # Replacement

    # Customer Data
    customer = session.query(Customer.full_name, Customer.distance).filter(
        Customer.id == customer_id
    ).first()

    if customer:
        data['name'] = customer.full_name
        data['distance'] = customer.distance

    # Appointent
    appointment = session.query(ServiceAppointment).filter(
        ServiceAppointment.vehicle_id == vehicle_id,
    ).order_by(
        ServiceAppointment.appointment_at.desc()
    ).first()

    if appointment:
        data['appointment_at'] = appointment.appointment_at

    # Service
    service_total = 0

    services = session.query(Service).filter(
        Service.vehicle_id == vehicle_id
    )

    for service in services:
        service_total = service_total + service.total

    data['service_total'] =  service_total
    service = services.order_by(Service.completed_at.desc()).first()

    if service:
        data['serviced_at'] = service.completed_at
        data['service_last'] = service.total

    # Vehicle Data
    vehicle = session.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if vehicle:
        data['vehicle_name'] = f'{vehicle.year} {vehicle.make} {vehicle.model}'
        data['stock_type'] = vehicle.stock_type

        data['matches'] = session.query(Vehicle).filter(
            Vehicle.year == '2020',
            Vehicle.make == vehicle.make,
            Vehicle.model == vehicle.model,
            Vehicle.deleted_at == None
        ).count()

    # Warranty
    date_min = date.today() + relativedelta(months=-60)
    date_max = date.today() + relativedelta(months=-50)

    deal = session.query(Deal).filter(
        Deal.type.in_(['finance', 'cash']),
        Deal.customer_id == customer_id,
        Deal.vehicle_id == vehicle_id,
        Deal.sold_at >= date_min,
        Deal.sold_at <= date_max
    ).first()

    if deal:
        mileage = int(deal.vehicle.kilometres) if deal.vehicle.kilometres else 0
        mileage = (100000 - mileage)
        months = relativedelta(date.today(), date_min).years * 12 + relativedelta(date.today(), date_min).months
        print
        data['warranty'] = 'Manufacturers Warranty'
        data['warranty_months'] = months
        data['warranty_mileage'] = mileage

    return data

def update_opportunities(store):
    ''' Update Opportunities '''
    # Equity Opportunities

    # Service Opportunity
    appointments = session.query(ServiceAppointment).filter(
        ServiceAppointment.appointment_at >= '2020-04-09'
    ).all()

    for appointment in appointments:
        opportunity = session.query(Opportunity).filter(
            Opportunity.opportunity_type_id == 2,
            Opportunity.customer_id == appointment.customer_id,
            Opportunity.vehicle_id == appointment.vehicle_id,
            Opportunity.deleted_at == None
        ).first()

        if not opportunity:
            data = get_customer_benchmarks(
                appointment.customer_id,
                appointment.vehicle_id
            )

            opportunity = Opportunity()
            opportunity.customer_id = appointment.customer_id
            opportunity.vehicle_id = appointment.vehicle_id
            opportunity.opportunity_type_id = 2
            opportunity.name = data['name']
            opportunity.vehicle_name = data['vehicle_name']
            opportunity.stock_type = data['stock_type']
            opportunity.rating = data['rating']
            opportunity.term = data['term']
            opportunity.apr = data['apr']
            opportunity.payments = data['payments']
            opportunity.payments_new = data['payments_new']
            opportunity.payments_made = data['payments_made']
            opportunity.payments_left = data['payments_left']
            opportunity.trade = data['trade']
            opportunity.equity = data['equity']
            opportunity.matches = data['matches']
            opportunity.distance = data['distance']
            opportunity.service_last = data['service_last']
            opportunity.service_total = data['service_total']
            opportunity.warranty = data['warranty']
            opportunity.warranty_months = data['warranty_months']
            opportunity.warranty_mileage = data['warranty_mileage']
            opportunity.appointment_at = appointment.appointment_at
            opportunity.serviced_at = data['serviced_at']
            opportunity.created_at = datetime.datetime.now()
            opportunity.updated_at = datetime.datetime.now()

            session.add(opportunity)

    opportunities = session.query(Opportunity).filter(
        Opportunity.opportunity_type_id == 2,
        Opportunity.appointment_at < '2020-04-09',
        Opportunity.deleted_at == None
    ).all()

    for opportunity in opportunities:
        opportunity.deleted_at = datetime.datetime.now()

    # Lease Opportunity
    deals = session.query(Deal).filter(
        Deal.type == 'lease'
    ).all()

    for deal in deals:
        opportunity = session.query(Opportunity).filter(
            Opportunity.opportunity_type_id == 3,
            Opportunity.customer_id == deal.customer_id,
            Opportunity.vehicle_id == deal.vehicle_id,
            Opportunity.deleted_at == None
        ).first()

        if not opportunity:
            data = get_customer_benchmarks(
                deal.customer_id,
                deal.vehicle_id
            )

            opportunity = Opportunity()
            opportunity.customer_id = deal.customer_id
            opportunity.vehicle_id = deal.vehicle_id
            opportunity.opportunity_type_id = 3
            opportunity.name = data['name']
            opportunity.vehicle_name = data['vehicle_name']
            opportunity.stock_type = data['stock_type']
            opportunity.rating = data['rating']
            opportunity.term = data['term']
            opportunity.apr = data['apr']
            opportunity.payments = data['payments']
            opportunity.payments_new = data['payments_new']
            opportunity.payments_made = data['payments_made']
            opportunity.payments_left = data['payments_left']
            opportunity.trade = data['trade']
            opportunity.equity = data['equity']
            opportunity.matches = data['matches']
            opportunity.distance = data['distance']
            opportunity.service_last = data['service_last']
            opportunity.service_total = data['service_total']
            opportunity.warranty = data['warranty']
            opportunity.warranty_months = data['warranty_months']
            opportunity.warranty_mileage = data['warranty_mileage']
            opportunity.appointment_at = data['appointment_at']
            opportunity.serviced_at = data['serviced_at']
            opportunity.created_at = datetime.datetime.now()
            opportunity.updated_at = datetime.datetime.now()

            session.add(opportunity)

    # Warranty Opportunity
    date_min = date.today() + relativedelta(months=-60)
    date_max = date.today() + relativedelta(months=-50)

    deals = session.query(Deal).filter(
        Deal.type.in_(['finance', 'cash']),
        Deal.sold_at >= date_min,
        Deal.sold_at <= date_max
    ).all()

    for deal in deals:
        opportunity = session.query(Opportunity).filter(
            Opportunity.opportunity_type_id == 4,
            Opportunity.customer_id == deal.customer_id,
            Opportunity.vehicle_id == deal.vehicle_id,
            Opportunity.deleted_at == None
        ).first()

        if not opportunity:
            mileage = int(deal.vehicle.kilometres) if deal.vehicle.kilometres else 0

            if int(mileage) > 100000 or deal.vehicle.make.upper() != store.brand.upper():
                continue

            if date_min.year < float(deal.vehicle.year):
                data = get_customer_benchmarks(
                    deal.customer_id,
                    deal.vehicle_id
                )

                opportunity = Opportunity()
                opportunity.customer_id = deal.customer_id
                opportunity.vehicle_id = deal.vehicle_id
                opportunity.opportunity_type_id = 4
                opportunity.name = data['name']
                opportunity.vehicle_name = data['vehicle_name']
                opportunity.stock_type = data['stock_type']
                opportunity.rating = data['rating']
                opportunity.term = data['term']
                opportunity.apr = data['apr']
                opportunity.payments = data['payments']
                opportunity.payments_new = data['payments_new']
                opportunity.payments_made = data['payments_made']
                opportunity.payments_left = data['payments_left']
                opportunity.trade = data['trade']
                opportunity.equity = data['equity']
                opportunity.matches = data['matches']
                opportunity.distance = data['distance']
                opportunity.service_last = data['service_last']
                opportunity.service_total = data['service_total']
                opportunity.warranty = data['warranty']
                opportunity.warranty_months = data['warranty_months']
                opportunity.warranty_mileage = data['warranty_mileage']
                opportunity.appointment_at = data['appointment_at']
                opportunity.serviced_at = data['serviced_at']
                opportunity.created_at = datetime.datetime.now()
                opportunity.updated_at = datetime.datetime.now()

                session.add(opportunity)

    # Cash Opportunity
    deals = session.query(Deal).filter(
        Deal.type == 'cash'
    ).all()

    for deal in deals:
        opportunity = session.query(Opportunity).filter(
            Opportunity.opportunity_type_id == 5,
            Opportunity.customer_id == deal.customer_id,
            Opportunity.vehicle_id == deal.vehicle_id,
            Opportunity.deleted_at == None
        ).first()

        if not opportunity:
            data = get_customer_benchmarks(
                deal.customer_id,
                deal.vehicle_id
            )

            opportunity = Opportunity()
            opportunity.customer_id = deal.customer_id
            opportunity.vehicle_id = deal.vehicle_id
            opportunity.opportunity_type_id = 5
            opportunity.name = data['name']
            opportunity.vehicle_name = data['vehicle_name']
            opportunity.stock_type = data['stock_type']
            opportunity.rating = data['rating']
            opportunity.term = data['term']
            opportunity.apr = data['apr']
            opportunity.payments = data['payments']
            opportunity.payments_new = data['payments_new']
            opportunity.payments_made = data['payments_made']
            opportunity.payments_left = data['payments_left']
            opportunity.trade = data['trade']
            opportunity.equity = data['equity']
            opportunity.matches = data['matches']
            opportunity.distance = data['distance']
            opportunity.service_last = data['service_last']
            opportunity.service_total = data['service_total']
            opportunity.warranty = data['warranty']
            opportunity.warranty_months = data['warranty_months']
            opportunity.warranty_mileage = data['warranty_mileage']
            opportunity.appointment_at = data['appointment_at']
            opportunity.serviced_at = data['serviced_at']
            opportunity.created_at = datetime.datetime.now()
            opportunity.updated_at = datetime.datetime.now()

            session.add(opportunity)

    # Conquest Opportunity

    # Subprime Opportunity
    deals = session.query(Deal).filter(
        Deal.type == 'finance',
    ).all()

    for deal in deals:
        if deal.financing.rate > 8:
            opportunity = session.query(Opportunity).filter(
                Opportunity.opportunity_type_id == 7,
                Opportunity.customer_id == deal.customer_id,
                Opportunity.vehicle_id == deal.vehicle_id,
                Opportunity.deleted_at == None
            ).first()

            if not opportunity:
                data = get_customer_benchmarks(
                    deal.customer_id,
                    deal.vehicle_id
                )

                opportunity = Opportunity()
                opportunity.customer_id = deal.customer_id
                opportunity.vehicle_id = deal.vehicle_id
                opportunity.opportunity_type_id = 7
                opportunity.name = data['name']
                opportunity.vehicle_name = data['vehicle_name']
                opportunity.stock_type = data['stock_type']
                opportunity.rating = data['rating']
                opportunity.term = data['term']
                opportunity.apr = data['apr']
                opportunity.payments = data['payments']
                opportunity.payments_new = data['payments_new']
                opportunity.payments_made = data['payments_made']
                opportunity.payments_left = data['payments_left']
                opportunity.trade = data['trade']
                opportunity.equity = data['equity']
                opportunity.matches = data['matches']
                opportunity.distance = data['distance']
                opportunity.service_last = data['service_last']
                opportunity.service_total = data['service_total']
                opportunity.appointment_at = data['appointment_at']
                opportunity.serviced_at = data['serviced_at']
                opportunity.created_at = datetime.datetime.now()
                opportunity.updated_at = datetime.datetime.now()

                session.add(opportunity)

    session.commit()
