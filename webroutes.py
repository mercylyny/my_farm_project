from flask import Blueprint, render_template, request, redirect, url_for
from models import Customer, Input, Output, Message, Dashboard

web = Blueprint('web', __name__)


@web.route('/')
def dashboard():
    stats = Dashboard.get_stats()
    return render_template('dashboard.html', **stats)


@web.route('/customers')
def customers():
    customer = Customer.get_all()
    return render_template('customers.html', customers=customers)


@web.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']

    Customer.create(name, phone, email, address)
    return redirect(url_for('web.customers'))


@web.route('/inputs')
def inputs():
    inputs = Input.get_all()
    return render_template('inputs.html', inputs=inputs)


@web.route('/add_input', methods=['POST'])
def add_input():
    item_name = request.form['item_name']
    category = request.form['category']
    quantity = float(request.form['quantity'])
    unit = request.form['unit']
    cost_per_unit = float(request.form['cost_per_unit'])
    supplier = request.form['supplier']

    Input.create(item_name, category, quantity, unit, cost_per_unit, supplier)
    return redirect(url_for('web.inputs'))


@web.route('/outputs')
def outputs():
    outputs = Output.get_all()
    customers = Customer.get_all()
    return render_template('outputs.html', outputs=outputs, customers=customers)


@web.route('/add_output', methods=['POST'])
def add_output():
    product_name = request.form['product_name']
    quantity = float(request.form['quantity'])
    unit = request.form['unit']
    price_per_unit = float(request.form['price_per_unit'])
    customer_id = request.form['customer_id'] if request.form['customer_id'] else None
    transport_cost = float(request.form['transport_cost']) if request.form['transport_cost'] else 0

    Output.create(product_name, quantity, unit, price_per_unit, customer_id, transport_cost)
    return redirect(url_for('web.outputs'))


@web.route('/messages')
def messages():
    messages = Message.get_all()
    customers = Customer.get_all()
    return render_template('messages.html', messages=messages, customers=customers)


@web.route('/send_message', methods=['POST'])
def send_message():
    customer_id = int(request.form['customer_id'])
    message = request.form['message']
    message_type = request.form['message_type']

    Message.create(customer_id, message, message_type)
    return redirect(url_for('web.messages'))


@web.route('/update_delivery_status', methods=['POST'])
def update_delivery_status():
    output_id = request.form['output_id']
    status = request.form['status']

    Output.update_delivery_status(output_id, status)
    return redirect(url_for('web.outputs'))