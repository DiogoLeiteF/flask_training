import io
from time import time
from flask import Blueprint, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
from .models import User, Product, Sale
from flask_login import current_user


graph = Blueprint('graph', __name__)


@graph.route('/admin1.png')
def plot_admin_png():
    fig = create_figure_admin()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure_admin():
    users = User.query.all()
    products = Product.query.all()
    sales = Sale.query.all()
    time = [x.date_created.date() for x in users]
    quant = [x.sold for x in products]
    name = [x.name for x in products]
    quat = [x.date_created.date() for x in sales]
    date = [x.date_created.date() for x in sales]
    value = [x.profit for x in sales]

# users over time
    fig = plt.figure(figsize=(10, 20))
    axis = fig.add_subplot(4, 1, 1)
    axis.set_title('User Registration Over Time')
    plt.xticks(rotation=45)
    axis.hist(time, color='grey')

# products sold
    ax = fig.add_subplot(4, 1, 2)
    ax.set_title('Products Sold')
    plt.xticks(rotation=45)
    ax.bar(name, quant, color='grey')

# sales over time
    ax = fig.add_subplot(4, 1, 3)
    ax.set_title('Sales Over Time')
    plt.xticks(rotation=45)
    ax.hist(quat, color='grey')


# imcome over time~

    ax = fig.add_subplot(4, 1, 4)
    ax.set_title('Profit')
    plt.xticks(rotation=45)
    ax.bar(date, value, color='grey')

    plt.tight_layout()
    return fig


@graph.route('/user.png')
def plot_user_png():
    fig = create_figure_user()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure_user():
    sales = Sale.query.filter_by(user_id=current_user.id).all()
    date = [sale.date_created.date() for sale in sales]
    value = [sale.total_value for sale in sales]

# value over time
    fig1 = plt.figure(figsize=(10, 7))
    axis = fig1.add_subplot(1, 1, 1)
    plt.title('Value Spent')
    plt.xticks(rotation=45)
    axis.bar(date, value, color='grey')
    plt.tight_layout()
    return fig1


@graph.route('/supplier.png')
def plot_supplier_png():
    fig = create_figure_supplier()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure_supplier():
    products = Product.query.filter_by(supplier=current_user.first_name).all()
    sales = Sale.query.all()
    names = [x.name for x in products]
    quant = [x.sold for x in products]
    time_ = []
    value = 0
    value_list = []
    for sale in sales:
        for prod in sale.prod_list:
            for product in products:
                if prod.product_id == product.prod_id:
                    time_.append(sale.date_created.date())
                    value += product.supplier_price
                    value_list.append(value)

# Sold quantities
    fig = plt.figure(figsize=(10, 15))

    axis = fig.add_subplot(3, 1, 1)
    plt.title('Products Sold')
    axis.bar(names, quant, color='grey')


# Sales over time
    axis = fig.add_subplot(3, 1, 2)
    plt.title('Sales Over Time')
    plt.xticks(rotation=45)
    axis.hist(time_, color='grey')


# income over time
    axis = fig.add_subplot(3, 1, 3)
    plt.title('Cumulative Income')
    plt.xticks(rotation=45)
    axis.plot(time_, value_list, color='grey')

    plt.tight_layout()
    return fig
