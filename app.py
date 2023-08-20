import os
from flask import Flask, request, render_template, redirect, flash, session, jsonify, json, g, send_from_directory
from sqlalchemy import func, select, column, text
import requests
from flask_debugtoolbar import DebugToolbarExtension
#from flask_migrate import Migrate
from models import db, connect_db, Message, Follows, Likes, Favorites, Effect_Tag, ProductTag, Product, Category, Plant_facility, Strain, Seedling, User, Sector, Account, Customer, Invoice, Bill, Vendor, Sale, Basket, Double_Entry, Journal_Entry, TransactionCR, TransactionDB, Direct_Message, ProductRating
from forms import ProductForm, CategoryForm, RegisterForm, LoginForm, SearchForm
import main
from formulas import make_shop, get_APIdata_all, get_APIdata, get_sectors, generate_reviews, generate_likes, random_generator, delete_favorites, generate_favorites, balance_sheet_data_placeholder, get_sales_by_sector, get_currUser_orders, generate_daily_bill_metrics, generate_daily_sale_metrics, generate_daily_metrics, get_random_date, get_random_datetime, get_past_datetime, get_quote, set_date, parse_date, limit_month_revenue, parse_sales_numbers, parse_date_bills, get_product_sale_data, get_timedelta, get_news, get_past_date, random_products
from main import generate_index_html, APPLICATION_ID, LOCATION_ID, ACCESS_TOKEN, client, location, ACCOUNT_CURRENCY, ACCOUNT_COUNTRY, CONFIG_TYPE, PAYMENT_FORM_URL, Payment
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, validators, ValidationError, SelectField 
from flask_bcrypt import Bcrypt
from csv import DictReader
import csv
import datetime
import configparser
import logging
import uuid
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from square.client import Client
from pydantic import BaseModel
from faker import Faker
from keys import DATABASEURI_ZENTRY, SECRET_KEY_ZENTRY, DATABASEURI_LOCAL, BASE_URL 
from api_views import api
from constants import randprods12, categories, subtypes
import random
bcrypt = Bcrypt()
fake = Faker()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASEURI_ZENTRY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY_ZENTRY

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

#migrate = Migrate(app, db)

app.register_blueprint(api, url_prefix="/")

PAYMENT_FORM_URL = (
    "https://web.squarecdn.com/v1/square.js"
    if CONFIG_TYPE == "PRODUCTION"
    else "https://sandbox.web.squarecdn.com/v1/square.js"
)


@app.before_request
def add_user_to_g():

    if "cart" in session:
        session["cart"] = session["cart"]
    else:
        session["cart"] = []


#backend routes zentry


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    
    return render_template('/front-end/404.html'), 404


#@app.route('/favicon.ico') 
#def favicon(): 
#    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=["GET", "POST"])
def redirect_list_users():
    '''Zentry Backend Dashboard Home'''
    currUser = 'friend'
    customers = Customer.query.all()
    customers.insert(0, 'fix')

    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
        flash(f"Welcome back, {currUser[0].username}!", "alert alert-success alert-dismissible border border-success fade show col-3")
    else:
        return redirect('/login')
        flash(f"Welcome back, {currUser}!", "alert alert-success alert-dismissible border border-success fade show col-3")

    #now = datetime.datetime.now()

    #data generation for revenue/projection/expenses line graph1

    #TransactionCR.query.filter(TransactionCR.account_number==300, TransactionCR.date <= '3-3-2023').all()
    today = datetime.datetime(2023, 4, 30, 18, 00).strftime('%m-%d-%y')
    this_month = datetime.datetime(2023, 3, 31, 18, 00).strftime('%m-%d-%y')
    last_month=datetime.datetime(2023, 2, 28, 18, 00).strftime('%m-%d-%y')
    two_months_ago=datetime.datetime(2023, 1, 30, 18, 00).strftime('%m-%d-%y')
    three_months_ago=datetime.datetime(2022, 12, 31, 18, 00).strftime('%m-%d-%y')
    four_months_ago=datetime.datetime(2022, 11, 30, 18, 00).strftime('%m-%d-%y')
    five_months_ago=datetime.datetime(2022, 10, 31, 18, 00).strftime('%m-%d-%y')

    query = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300) AND (date <= :today) AND (date > :this_month)")
    res1 = db.session.execute(query, {"this_month": this_month, "today": today}).fetchall()
    query1 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300) AND (date <= :this_month) AND (date > :last_month)")
    res2 = db.session.execute(query1, {"this_month": this_month, "last_month": last_month}).fetchall()
    query2 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300)  AND (date <= :last_month) AND (date > :two_months_ago)")
    res3 = db.session.execute(query2, {"last_month": last_month, "two_months_ago": two_months_ago }).fetchall()
    query3 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300)  AND (date <= :two_months_ago) AND (date > :three_months_ago)")
    res4 = db.session.execute(query3, {"two_months_ago": two_months_ago, "three_months_ago": three_months_ago}).fetchall()
    query4 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300)  AND (date <= :three_months_ago) AND (date > :four_months_ago)")
    res5 = db.session.execute(query4, {"three_months_ago": three_months_ago, "four_months_ago": four_months_ago}).fetchall()
    query5 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300)  AND (date <= :four_months_ago) AND (date > :five_months_ago)")
    res6 = db.session.execute(query5, {"four_months_ago": four_months_ago, "five_months_ago": five_months_ago}).fetchall()
    real_revenue=[]
    real_revenue.append(res1)
    real_revenue.append(res2)
    real_revenue.append(res3)
    real_revenue.append(res4)
    real_revenue.append(res5)
    real_revenue.append(res6)


    #revenue_data = set_date(datetime.datetime.now())
    #parsed_dates = parse_date(revenue_data)
    #sales_numbers = parse_sales_numbers(revenue_data)
    #revenue = limit_month_revenue(parsed_dates)
    #expenses = parse_date_bills(revenue_data)
    expenses = [52004,96385,69255,72559,45077, 76888, 64744]
    projection = []
    projection_calculator = [.88, .90, .72, .69, .84, .92, .82]
    for i in range(len(real_revenue)):
        projection.append(real_revenue[i][0][0]*projection_calculator[i])


    #data generation for sales by product graph

    popular_products = get_product_sale_data()
    
        
    #data generation for recent sales - enter number of days in the past you want data to be generated for.
    ourDelta = datetime.datetime(2023, 5, 8, 18, 00) - datetime.datetime.now()
    recent_sales = get_timedelta(ourDelta.days*-1)
    

    #get trending news from newsapi

    news = get_news()

    x_axis = []

    x_axis.append(today)
    x_axis.append(this_month)
    
    x_axis.append(last_month)
    
    x_axis.append(two_months_ago)
    
    x_axis.append(three_months_ago)
    x_axis.append(four_months_ago)

    


    #import pdb
    #pdb.set_trace()                       
                
    return render_template('add_product.html', 
                           currUser=currUser, 
                           
                           x_axis=x_axis,
                            
                           
                           real_revenue=real_revenue,
                           expenses=expenses, 
                           projection=projection,
                           popular_products=popular_products,
                           recent_sales=recent_sales,
                           customers=customers,
                           news=news)







@app.route('/orders', methods=["GET", "POST"])
def ssffssf():
    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/login')
    form = ProductForm()
    products = Product.query.all()
    products.insert(0, 'FIXINDEX')

    customers = Customer.query.all()
    customers.insert(0, 'FIXINDEX')

    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()

    orders = Invoice.query.all()
    orders.insert(0, 'FIXINDEX')

    baskets = Basket.query.all()
    baskets.insert(0, 'FIXINDEX')

    #use get_past_date to pick a date in the past to generate all sales for. if generate all time it could take around 20 seconds to load. not good for user experience.
    # change get_past_date parameter to number of days you wish to generate sales data for.

    past_date = get_past_date(100)
    sales = Basket.query.filter(Basket.submitted_at > past_date).all()
    

    

    return render_template("order_page.html", orders=orders, sales=sales, products=products, baskets=baskets, customers=customers, currUser=currUser)

@app.route('/orders1', methods=["GET", "POST"])
def ssff1ssf():
    form = ProductForm()
    products = Product.query.all()
    products.insert(0, 'FIXINDEX')

    customers = Customer.query.all()
    customers.insert(0, 'FIXINDEX')

    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()

    orders = Invoice.query.all()
    orders.insert(0, 'FIXINDEX')

    sales = Sale.query.all()
    
    baskets = Basket.query.all()
    baskets.insert(0, 'FIXINDEX')

    return render_template("/back-end/order-list.html", orders=orders, sales=sales, products=products, baskets=baskets, customers=customers)

@app.route('/payments-screen', methods=["GET", "POST"])
def dsdds():
    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/login')
    form = ProductForm()
    products = Product.query.all()
    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()
    

    resp = main.generate_index_html()
    print(resp.body)

    idempotency_key = str(uuid.uuid4())
    session['idempotency_key'] = idempotency_key
    #import pdb
    #pdb.set_trace()

    return render_template('payments-screen.html', currUser=currUser, resp=resp, idempotency_key=idempotency_key, APPLICATION_ID=APPLICATION_ID, LOCATION_ID=LOCATION_ID, ACCOUNT_COUNTRY=ACCOUNT_COUNTRY, ACCOUNT_CURRENCY=ACCOUNT_CURRENCY,
                           location=location, client=client, PAYMENT_FORM_URL=PAYMENT_FORM_URL)


#class Payment(BaseModel):
#    token: str
#    idempotencyKey: str

@app.route('/process-payment', methods=["GET", "POST"])
def process_payment():
    logging.info("Creating payment")
    # Charge the customer's card
    id = session["user_id"]
    currUser = User.query.get(id)
    result = client.payments.create_payment(
    body = {
    "source_id": "cnon:card-nonce-ok",
    "idempotency_key": session['idempotency_key'],
    "amount_money": {
        "amount": int(session['total']),
        "currency": "USD"
    },
    "app_fee_money": {
        "amount": 2,
        "currency": "USD"
    },
    "autocomplete": True,
    "location_id": "LH047DMF8Z711",
    "reference_id": "888",
    "accept_partial_authorization": False,
    "buyer_email_address": currUser.email,
    "billing_address": {},
    "shipping_address": {},
    "note": "test payment 888",
    "statement_description_identifier": "BUDLY INVOICE#"
    }
    )

    if result.is_success():
      print(result.body)
      return result.body
    elif result.is_error():
      print(result.errors)
      
      return (jsonify(result, 201))



    

@app.route('/forms-layouts', methods=["GET", "POST"])
def ss():
    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/register')
    form = ProductForm()
    form_categories = CategoryForm()
    products = Product.query.all()
    categories = Category.query.all()
    sectors = Sector.query.all()

  


    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()

    categories = [(cat.id, cat.name) for cat in categories]
    form.category_id.choices = categories

    seedlings = [(seed.id) for seed in seedlings]
    form.seedling_id.choices = seedlings

    strains = [(strain.id, strain.name) for strain in strains]
    form.strain_id.choices = strains

    sectors = [(sector.id, sector.name) for sector in sectors]
    form.sector_id.choices = sectors

    plant_facilities = [(pf.id, pf.name) for pf in plant_facilities]
    form.plant_facility_id.choices = plant_facilities

    if form.validate_on_submit():
        name = form.name.data
        category_id = form.category_id.data
        seedling_id = form.seedling_id.data       
        strain_id = form.strain_id.data
        sector_id = form.sector_id.data
        plant_facility_id = form.plant_facility_id.data

        new_product = Product(name=name, strain_id=strain_id, sector_id=sector_id, plant_facility_id=plant_facility_id, seedling_id=seedling_id, category_id=category_id  )
        
        db.session.add(new_product)
        
        db.session.commit()

        new_product_category = ProductCategory(product_id=new_product.id, category_id=new_product.category_id)
        db.session.add(new_product_category)

        db.session.commit()

        flash("Added product to Budly database!", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
        return redirect('/')

    if form_categories.validate_on_submit():
        name = form_categories.name.data
        

        new_Category = Category(name=name )
        db.session.add(new_Category)
        db.session.commit()
        flash("Added category to Budly database!", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
        return redirect('/')
    
    return render_template('forms-layouts.html', currUser=currUser, products=products, categories=categories, sectors=sectors, seedlings=seedlings, strains=strains, plant_facilities=plant_facilities,  form=form, form_categories=form_categories)


@app.route('/tables-general', methods=["GET", "POST"])
def sdd():
    
    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/register')
    
    products = Product.query.all()
    
    strains = Strain.query.all()
    categories = Category.query.all()
   
    name_check = request.form.get('name')

 
    
    
    
    return render_template('tables-general.html', currUser=currUser, products=products, name_check=name_check, strains=strains, categories=categories)



@app.route('/tables-users', methods=["GET", "POST"])
def sddd():
    
    
    users = User.query.all()
    
    name_check = request.form.get('name')
    
    return render_template('tables-users.html', users=users, name_check=name_check)




@app.route('/users-profile', methods=["GET", "POST"])
def sddssd():
    
    users = User.query.all()
    
    name_check = request.form.get('name')

    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/register')
    
    users = User.query.all()
    
    name_check = request.form.get('name')

    #import pdb
    #pdb.set_trace()
    
    return render_template('users-profile.html', users=users, name_check=name_check, currUser=currUser)

#@app.route('/pages-login', methods=["GET", "POST"])
#def sdxd():
#    form = LoginForm()
#    products = Product.query.all()
#    name_check = request.form.get('name')
    

        
    
#    if "username" in session:
#        return redirect(f"/users/{session['username']}")

#    if form.validate_on_submit():
#        username = form.username.data
#        pwd = form.password.data
        
#        user = User.authenticate(username, pwd)
#        if user:
#            session["user_id"] = user.id
#            id = user.id
#            session["username"] = user.username
#            userdata = User.query.filter_by(id=id).all()
#            username = userdata[0].username
#            flash(f"You have successfully logged in, {username}!", "success col-3 alert alert-dismissible fade show")   
#            return redirect(f"/")
#        else:
#            flash(f"Invalid credentials!", "error")
#            return redirect("/pages-login")

#    return render_template('pages-login.html', products=products, name_check=name_check, form=form)

@app.route('/logout', methods=["POST"])
def logout():
    session.pop("user_id")
    if "username" in session:
        session.pop("username")
    flash(f"You have successfully logged out.", "success col-3 alert alert-dismissible fade show")   
    return redirect("/")


@app.route('/shop/logout', methods=["POST"])
def front_end_logout():
    session.pop("user_id")
    if "username" in session:
        session.pop("username")
    flash(f"You have successfully logged out.", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")   
    return redirect("/shop")

@app.route('/add_to_cart/<int:id>', methods=["POST"])
def add_to_cart(id):
    #session.pop("user_id")
    
    """add like"""
    if "username" not in session:
        flash("Log in to add product to cart!", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
        return redirect("/shop")

    item = Product.query.filter_by(id=id)
    

    if request.method == 'POST':
        
        quantity = int(request.form.get('quantity'))
        
        session["cart"].append((id,quantity))
        flash(f"Added {quantity} {item[0].name} to cart!", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
        
        return redirect("/products/cart")


@app.route('/update_cart/<int:id>', methods=["POST", "PATCH"])
def update_cart(id):
    session["cart"] = session["cart"]
    response = request.json["quant"]
    print(request.json)
    session["cart_update"] = []
    if not session["cart_update"]:
        
        session["cart_update"] = []
        response = tuple(map(int, response.split(', ')))
        session["cart_update"].append(response)

    else:
        response = tuple(map(int, response.split(', ')))
        session["cart_update"].append(response)

    #for item in session["cart"]:
    #    for item_new in session["cart_update"]:
    #        if item[0] == item_new[0]:
    #            idx = session["cart"].index(item[0])
    #            session["cart"][idx] = item_new

    for item in session["cart"]:
        if id == item[0]:
            idx = session["cart"].index(item)
            session["cart"][idx] = response
    session["cart_update"] = []
    flash("Cart Updated", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
 
    return (jsonify(session["cart_update"]), 201)


@app.route('/update_cart/<int:id>', methods=["DELETE"])
def remove_item_from_cart(id):

    for item in session["cart"]:
        if item[0] == id:
            idx = session["cart"].index(item)
            session["cart"].pop(idx)
            
    return jsonify((session["cart"]), 202)


@app.route('/products/cart', methods=["GET"])
def show_cart_items():
    carty = []
    cart = session["cart"]
    total=0
    for prod in cart:
        obj = Product.query.filter_by(id=prod[0])
        carty.append((obj[0], prod[1]))
        total = total + (obj[0].price*prod[1])
    
    return render_template('/front-end/cart_real.html', carty=carty, total=total)


@app.route('/checkout', methods=["GET"])
def add_items_to_checkout():
    carty = []
    test="test"
    cart = session["cart"]
    for prod in cart:
        obj = Product.query.filter_by(id=prod[0])
        carty.append((obj[0], prod[1]))
    resp = main.generate_index_html()
    print(resp.body)

    idempotency_key = str(uuid.uuid4())
    session['idempotency_key'] = idempotency_key
    return render_template('/front-end/checkout_real.html', carty=carty, resp=resp, idempotency_key=idempotency_key, APPLICATION_ID=APPLICATION_ID, LOCATION_ID=LOCATION_ID, ACCOUNT_COUNTRY=ACCOUNT_COUNTRY, ACCOUNT_CURRENCY=ACCOUNT_CURRENCY,
                           location=location, client=client, PAYMENT_FORM_URL=PAYMENT_FORM_URL)


@app.route('/order-success', methods=["GET"])
def order_success():
    return render_template('/front-end/order-success_real.html')


@app.route('/clearcart', methods=["GET"])
def notsureifillusethisroute():
    session["cart"] = []
    session["cart_update"] = []
    flash("cart cleared", "alert alert-success alert-dismissible border border-success fade show col-xl-4 mb-3 text-center")
    return redirect("/shop")


@app.route("/pages-register", methods=["GET", "POST"])
def register():
    '''register user: produce form and handle form submission'''

    form = RegisterForm()

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data

        if form.image_url.data:
            image_url = form.image_url.data
            user = User.signup( name, email, pwd, image_url)
            db.session.add(user)
            db.session.commit()
        else:
            image_url = 'https://randomuser.me/api/portraits/women/82.jpg'
            user = User.signup(name, email, pwd, image_url)
            
            db.session.add(user)
            db.session.commit()
        
        session["user_id"] = user.id
        session["username"] = user.username
        
        #on successful login, redirect to auth user pages
        flash(f"You have successfully registered!", "success col-3 alert alert-dismissible fade show")
        return redirect("/")

    else:
        return render_template("pages-register.html", form=form)



@app.route("/register", methods=["GET", "POST"])
def registerme():
    '''register user: produce form and handle form submission'''

    form = RegisterForm()

    if "username" in session:
        return redirect("/")

   
    #when form is submitted, create new User instance
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        #first_name = form.first_name.data
        #last_name = form.last_name.data
        email = form.email.data
        if form.image_url.data:
            image_url = form.image_url.data
            user = User.signup(username, email, pwd, image_url)
        user = User.signup(username, email, pwd, image_url="/static/images/default-pic.png")
        db.session.add(user)
        db.session.commit()
        
        session["user_id"] = user.id
        session["username"] = user.username

        #generate welcome message for new user inbox

        #welcome_msg = Direct_Message(text=f"Welcome to Zentry, {username}! With our streamlined customer relationship manager, getting business done has never been simpler. Visit zentry.onrender.com/shop to see your ecommerce page!", sender_id=1, recipient_id=session["user_id"])
        #db.session.add(welcome_msg)
        #db.session.commit()


        #on successful login, redirect to auth user pages
        flash(f"You have successfully registered!", "success col-3 alert alert-dismissible fade show")
        return redirect("/")

    else:
        return render_template("REG.HTML", form=form)



    ##########################################################
    #####              ACCOUNTING CENTER                 #####
    ##########################################################

@app.route('/invoice/<int:id>', methods=["GET", "POST"])
def sdddDDDDDDDDDDdd(id):
    
    form = ProductForm()
    products = Product.query.all()
    products.insert(0, 'FIXINDEX')

    customers = Customer.query.all()
    customers.insert(0, 'FIXINDEX')

    users = User.query.all()
    users.insert(0, 'FIXINDEX')

    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()

    orders = Invoice.query.all()
    orders.insert(0, 'FIXINDEX')

    sales = Sale.query.all()
    
    baskets = Basket.query.all()
    baskets.insert(0, 'FIXINDEX')
    
    invoice = Invoice.query.filter_by(id=id)

    test=fake.address()
     
    

    totalprice = 0
    counter = 0
    discount = 0
    for product in baskets[invoice[0].id].products:
        
        if totalprice < baskets[invoice[0].id].amount:
            totalprice = totalprice + product.price
            counter = counter+1
        elif totalprice == baskets[invoice[0].id].amount:
            totalprice = totalprice
        elif totalprice > baskets[invoice[0].id].amount:
            
            discount = totalprice - baskets[invoice[0].id].amount
            
            totalprice = totalprice - discount
 
    #import pdb
    #pdb.set_trace()
    
    
    return render_template('/invoice/invoice-1.html', discount=discount, counter=counter, totalprice=totalprice, test=test, users=users, products=products,  strains=strains, categories=categories, invoice=invoice, baskets=baskets, customers=customers)


@app.route('/order-detail/<int:id>', methods=["GET", "POST"])
def sdddDDDDddssDDDDDDdd(id):
    
    if "username" in session:
        user_id = session["user_id"]
        currUser = User.query.filter_by(id=id)
    else:
        return redirect('/login')

    form = ProductForm()
    products = Product.query.all()
    products.insert(0, 'FIXINDEX')

    customers = Customer.query.all()
    customers.insert(0, 'FIXINDEX')

    users = User.query.all()
    users.insert(0, 'FIXINDEX')

    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()

    orders = Invoice.query.all()
    orders.insert(0, 'FIXINDEX')

    sales = Sale.query.all()
    
    baskets = Basket.query.all()
    baskets.insert(0, 'FIXINDEX')
    
    invoice = Invoice.query.filter_by(id=id)

    test=fake.address()
     
    consult_tax = round((invoice[0].amount*0.04), 2)
    consult_subtotal = round((invoice[0].amount*0.96), 2)
    tax = 0
    pretax_total = 0
    totalprice = 0
    counter = 0
    discount = 0
    for product in baskets[invoice[0].id].products:
        

        if totalprice < baskets[invoice[0].id].amount:
            totalprice = totalprice + product.price
            counter = counter+1
        elif totalprice == baskets[invoice[0].id].amount:
            totalprice = totalprice
        elif totalprice > baskets[invoice[0].id].amount:
            
            discount = totalprice - baskets[invoice[0].id].amount
            
            

            totalprice = totalprice - discount

            pretax_total = round((totalprice*0.96), 2)
            tax = totalprice*0.04
 
    #import pdb
    #pdb.set_trace()
    
    
    return render_template('/back-end/order-detail.html', currUser=currUser, consult_tax=consult_tax, consult_subtotal=consult_subtotal, tax=tax, discount=discount, pretax_total=pretax_total, counter=counter, totalprice=totalprice, test=test, users=users, products=products,  strains=strains, categories=categories, invoice=invoice, baskets=baskets, customers=customers)


@app.route('/login', methods=["GET", "POST"])
def ssssdddes():
    
    products = Product.query.all()
    categories = Category.query.all()
    seedlings = Seedling.query.all()
    strains = Strain.query.all()
    plant_facilities = Plant_facility.query.all()
    form = LoginForm()
    products = Product.query.all()
    name_check = request.form.get('name')
    

        
    
    if "username" in session:
        return redirect(f"/users-profile")

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        
        user = User.authenticate(username, pwd)
        if user:
            session["user_id"] = user.id
            id = user.id
            session["username"] = user.username
            userdata = User.query.filter_by(id=id).all()
            username = userdata[0].username
            flash(f"You have successfully logged in, {username}!", "success col-3 alert alert-dismissible fade show")   
            return redirect(f"/")
        else:
            flash(f"Invalid credentials!", "error")
            return redirect("/pages-login")

    return render_template('LOG.HTML',  products=products, name_check=name_check, form=form)


@app.route('/products', methods=["GET", "POST"])
def show_products():
    if "username" in session:
        user_id = session["user_id"]
        currUser = User.query.filter_by(id=user_id)
    else:
        currUser = []
    products = Product.query.all()
    sectors = Sector.query.all()
    strains = Strain.query.all()
    facilities = Plant_facility.query.all()
    
    trending_products = random_products(7)
    similar_products = random_products(12)
    category=''
    #import pdb
    #pdb.set_trace()
    
    return render_template('front-end/category_real.html', 
                           products=products, 
                           category=category, 
                           currUser=currUser, 
                           categories=sectors,
                           strains=strains,
                           
                           trending_products=trending_products,
                           similar_products=similar_products,
                           facilities=facilities)

@app.route('/products/<int:id>', methods=["GET", "POST"])
def show_product_detail(id):
    '''Here we render each product in RESTFUL fashion. Photo, description, pricing, product origin details'''

    #product = get_APIdata(id=id, model='products')
    product = Product.query.filter(Product.id==id).all()
    reviews = []
    #reviews = product[0].messages
    users = []
    #for review in reviews:
    #    user=User.query.filter_by(id=review.user_id)
    #    users.append(user[0])
    

    strains = Strain.query.all()    
    facilities = Plant_facility.query.all()    
    trending_products = random_products(7)
    similar_products = random_products(12)
    print(product)
    
    
    

    return render_template('/front-end/product.html', 
                           product=product, 
                           reviews=reviews,
                           users=users,
                                                      
                           strains=strains,                            
                           trending_products=trending_products,
                           similar_products=similar_products,
                           facilities=facilities)


@app.route('/category/<int:id>', methods=["GET", "POST"])
def show_category_detail(id):
    '''Here we render each category and their respective products in RESTFUL fashion. Photo, description, pricing, product origin details'''
    if "username" in session:
        user_id = session["user_id"]
        currUser = User.query.filter_by(id=user_id)
    else:
        currUser = []
    category = Sector.query.get_or_404(id)
    #cat_prods = get_APIdata_all(f'products/sectors/{id}')
    cat_prods = Product.query.filter(Product.sector_id==id).all()
    
    strains = Strain.query.all()
    facilities = Plant_facility.query.all()
    
    trending_products = random_products(7)
    similar_products = random_products(12)
    
    #import pdb
    #pdb.set_trace()
    
    return render_template('front-end/category_real.html', 
                           category=category, 
                           currUser=currUser, 
                           id=id,
                           strains=strains,
                           cat_prods=cat_prods, 
                           trending_products=trending_products,
                           similar_products=similar_products,
                           facilities=facilities)


@app.route('/shop', methods=["GET", "POST"])
def show_main_shop_page():
    '''Here we render each product in RESTFUL fashion. Photo, description, pricing, product origin details'''

    strains = Strain.query.all()
    facilities = Plant_facility.query.all()
    shop=make_shop()

    return render_template('/front-end/shop_real.html', 
                           strains=strains,
                           trending_products=shop[0],
                           facilities=facilities,
                           sales_prods = shop[2],
                           va_prods=shop[1])


@app.route('/social/home')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """
    now = datetime.date.today()
    quote = get_quote()
    trending_products = random_products(4)


    if "username" in session:
        id = session["user_id"]
        currUser = User.query.filter_by(id=id)

    else:
        currUser = None

    if currUser:
        user = currUser[0]
        followed_users = user.following
        followed_users_id = []
        for user in followed_users:
            followed_users_id.append(user.id)
        
        messages = (Message
                    .query
                    .filter(Message.user_id.in_(followed_users_id))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())
        recent_messages = (Message
                        .query
                        .order_by(Message.timestamp.desc())
                        .limit(3)
                        .all())
        #raise
        
        
        return render_template('/front-end/blog-detail.html', messages=messages, recent_messages=recent_messages, currUser=currUser, now=now, quote=quote, trending_products=trending_products)

    else:
        recent_messages = (Message
                .query
                .order_by(Message.timestamp.desc())
                .limit(3)
                .all())
        messages = (Message
                .query
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
        return render_template('/front-end/blog-detail.html', messages=messages, recent_messages=recent_messages, currUser=currUser, now=now, quote=quote, trending_products=trending_products)



@app.route('/social/dashboard')
def show_chatter_feed():
    '''user dashboard home - show general feed and account data'''
    #import pdb
    #pdb.set_trace()
    if "username" in session:
        id = session["user_id"]
        currUser = User.query.get(id)
        g.user = currUser

    else:
        currUser = None
        flash(f"Log in to view your dashboard!", "alert alert-success alert-dismissible border border-success fade show col-3 mb-3 mt-3 text-center")
        return redirect('/social/home')
    
    if g.user:
        similar_products = random_products(12)
        wishlist = g.user.favorites
        liked_messages = g.user.likes
    
        
        followed_users = g.user.following
        followed_users_id = []
        for user in followed_users:
            followed_users_id.append(user.id)
        
        messages = (Message
                    .query
                    .filter(Message.user_id.in_(followed_users_id))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())
        recent_messages = (Message
                        .query
                        .order_by(Message.timestamp.desc())
                        .limit(3)
                        .all())
        
    orders = get_currUser_orders(g.user.id)
    if not orders:
        
        orders = get_currUser_orders(23)
    #generate_daily_metrics(100)
    #generate_daily_bill_metrics(2)
    #generate_daily_sale_metrics(3)
    

    

    return render_template('/front-end/my_dashboard.html', wishlist=wishlist, orders=orders, similar_products=similar_products, messages=messages, recent_messages=recent_messages, user=user, liked_messages=liked_messages)



#pass stuff to navbar search
@app.context_processor
def base():

    """If we're logged in, add current user to Flask global."""
   
    if "username" in session:
        #Here we address an edge case where if the User has been deleted, but the User data persists in the session, user will not be able to access the site and no pages will load.
        if User.query.filter(User.id==session['user_id']).all() == []:
            session.pop("username")
            session.pop("user_id")
            return redirect('/shop')
        #Here we return to our auth process
        id = session["user_id"]
        g.user = User.query.get(id)
        #if g.user.dms_received:
        #    g.user_dms = g.user.dms_received
        #    g.received_msgs_info = []
        #    for msg in g.user_dms:
        #        sender = User.query.get(msg.sender_id)
        #        g.received_msgs_info.append((sender.username, sender.image_url))


    else:
        g.user = None    

    search_form = SearchForm()
    now = datetime.date.today()
    quote = get_quote()
    category_svgs=['general_assets/images/svg/plant.svg',
                   'general_assets/images/svg/vape.svg',
                   'general_assets/images/svg/cloud.svg',
                   'general_assets/images/svg/radish.svg',
                   'general_assets/images/svg/umbrella.svg',
                   'general_assets/images/svg/headphone.svg',
                   'general_assets/images/svg/box.svg',
                   'general_assets/images/svg/tag.svg'
                   
                   ]
    similar_products = random_products(12)
    
    
    #sectors=categories
    sectors=Sector.query.all()
    subtypes=Category.query.all()
    #similar_products=randprods12
    similar_products=Product.query.filter(Product.id<13).all()

    deal_prods = []
    for i in range(4):
        deal_prods.append(similar_products[i])
    base = 50
    #cant query in the context processor to api. cmon. you knew that.........
    #for i in range(4):
    #    base = base+10
    #    deal_prods.append(get_APIdata(base, 'products'))
    cart = session["cart"]
    carty = []    
    total=0
    quantity=0
    for prod in cart:
        obj = Product.query.filter_by(id=prod[0])
        carty.append((obj[0], prod[1]))
        total = total + (obj[0].price*prod[1])
        quantity = quantity + prod[1]

    session['total'] = total
 

    #sectors = get_sectors()
    
    
    

    return dict(category_svgs=category_svgs, subtypes=subtypes, search_form=search_form, now=now, quote=quote, cart=carty, total=total, quantity=quantity, categories=sectors, similar_products=similar_products, deal_prods=deal_prods)



#search function

@app.route('/search', methods=['POST'])
def search():
    search_form=SearchForm()
    quote = get_quote()
    trending_products = random_products(4)
    recent_messages = (Message
                        .query
                        .order_by(Message.timestamp.desc())
                        .limit(3)
                        .all())
    if search_form.validate_on_submit():
        #get data from submitted form
        query = search_form.query.data
        #query the database
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).order_by(Product.name).all()
        products_description = Product.query.filter(Product.description.ilike(f'%{query}%')).order_by(Product.description).all()
        users = User.query.filter(User.username.ilike(f'%{query}%')).order_by(User.username).all()
        comments = Message.query.filter(Message.text.ilike(f'%{query}%')).order_by(Message.text).all()
        #products = products
        return render_template("/front-end/search_real.html", products_description=products_description, recent_messages=recent_messages, trending_products=trending_products, search_form=search_form, query = query, products=products, users=users, comments=comments, quote=quote)
    
@app.route('/nav', methods=["GET"])
def showNav():

    product = []
    try:
        resp = requests.get(
            "http://localhost:5000/api/products/1",
            #params={"term": "billy bragg", "limit": 3}
            
       )

        resp = resp.json()
        data = resp['0']
        #import pdb
        #pdb.set_trace()
        product.append(data)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        
        return render_template("nav.html", product=product)
    
    return render_template("nav.html", product=product)


#backend financial routes



@app.route('/finance', methods=['GET'])
def showFinancialData():
    return render_template("finance.html")

@app.route('/financelight', methods=['GET'])
def showLightFinancialData():
    return render_template("lightdemo.html")

@app.route('/accounting', methods=['GET'])
def showCharts():
    #import pdb
    #pdb.set_trace()
    #use CATEOGRIES UNIVERSAL VARIABLE
    sector_sales = get_sales_by_sector()

    #data generation for sales by product graph
    popular_products = get_product_sale_data()

    ## rev vs expenses table. modify later for less error prone date generation.

    revenue_data = set_date(datetime.datetime.now())
    parsed_dates = parse_date(revenue_data)
    sales_numbers = parse_sales_numbers(revenue_data)
    revenue = limit_month_revenue(parsed_dates)
    expenses = parse_date_bills(revenue_data)
    projection = []
    projection_calculator = [.88, .90, .72, .69, .84, .92, .82]
    for i in range(7):
        projection.append(revenue[i]*projection_calculator[i])

    x_axis = []
    x_axis.append(get_past_date(30))
    x_axis.append(get_past_date(60))
    x_axis.append(get_past_date(90))
    x_axis.append(get_past_date(120))
    x_axis.append(get_past_date(150))
    x_axis.append(get_past_date(180))
    x_axis.append(get_past_date(210))



    '''given list of dates, calculate monthly sales by sector. list of lists.'''
    monthly_sector_sales_data = [0,0,0,0,0]
    monthly_sector_sales_data2 = [0,0,0,0,0]
    monthly_sector_sales_data3 = [0,0,0,0,0]
    monthly_sector_sales_data4 = [0,0,0,0,0]
    monthly_sector_sales_data5 = [0,0,0,0,0]
    monthly_sector_sales_data6 = [0,0,0,0,0]
    monthly_sector_sales_data7 = [0,0,0,0,0]
    
    monthly_data = Basket.query.filter(Basket.submitted_at > x_axis[0]).all()
    for basket in monthly_data:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data[0] = monthly_sector_sales_data[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data[1] = monthly_sector_sales_data[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data[2] = monthly_sector_sales_data[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data[3] = monthly_sector_sales_data[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data[4] = monthly_sector_sales_data[4]+1

    monthly_data2 = Basket.query.filter(Basket.submitted_at > x_axis[1], Basket.submitted_at < x_axis[0]).all()
    for basket in monthly_data2:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data2[0] = monthly_sector_sales_data2[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data2[1] = monthly_sector_sales_data2[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data2[2] = monthly_sector_sales_data2[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data2[3] = monthly_sector_sales_data2[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data2[4] = monthly_sector_sales_data2[4]+1
    monthly_data3 = Basket.query.filter(Basket.submitted_at > x_axis[2], Basket.submitted_at < x_axis[1]).all()
    for basket in monthly_data3:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data3[0] = monthly_sector_sales_data3[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data3[1] = monthly_sector_sales_data3[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data3[2] = monthly_sector_sales_data3[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data3[3] = monthly_sector_sales_data3[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data3[4] = monthly_sector_sales_data3[4]+1
    monthly_data4 = Basket.query.filter(Basket.submitted_at > x_axis[3], Basket.submitted_at < x_axis[2]).all()
    for basket in monthly_data4:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data4[0] = monthly_sector_sales_data4[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data4[1] = monthly_sector_sales_data4[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data4[2] = monthly_sector_sales_data4[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data4[3] = monthly_sector_sales_data4[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data4[4] = monthly_sector_sales_data4[4]+1
    monthly_data5 = Basket.query.filter(Basket.submitted_at > x_axis[4], Basket.submitted_at < x_axis[3]).all()
    for basket in monthly_data5:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data5[0] = monthly_sector_sales_data5[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data5[1] = monthly_sector_sales_data5[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data5[2] = monthly_sector_sales_data5[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data5[3] = monthly_sector_sales_data5[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data5[4] = monthly_sector_sales_data5[4]+1
    monthly_data6 = Basket.query.filter(Basket.submitted_at > x_axis[5], Basket.submitted_at < x_axis[4]).all()
    for basket in monthly_data6:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data6[0] = monthly_sector_sales_data6[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data6[1] = monthly_sector_sales_data6[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data6[2] = monthly_sector_sales_data6[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data6[3] = monthly_sector_sales_data6[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data6[4] = monthly_sector_sales_data6[4]+1

    monthly_data7 = Basket.query.filter(Basket.submitted_at > x_axis[6], Basket.submitted_at < x_axis[5]).all()
    for basket in monthly_data7:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data7[0] = monthly_sector_sales_data7[0]+1
            elif prod.sector_id == 2:
                monthly_sector_sales_data7[1] = monthly_sector_sales_data7[1]+1
            elif prod.sector_id == 3:
                monthly_sector_sales_data7[2] = monthly_sector_sales_data7[2]+1
            elif prod.sector_id == 4:
                monthly_sector_sales_data7[3] = monthly_sector_sales_data7[3]+1
            elif prod.sector_id == 5:
                monthly_sector_sales_data7[4] = monthly_sector_sales_data7[4]+1
    
    

    '''given num_days, calculate date that many days in the past from today using datetime.datetime.now()'''
    num_days = 55
    month_sales_by_sector = [0,0,0,0,0]
    now = datetime.datetime.now()
    past_date = now - datetime.timedelta(days=num_days)
    recent_sales = []
    recent_sales_data = Basket.query.filter(Basket.submitted_at > past_date).all()
    for basket in recent_sales_data:

        recent_sales.append(basket)

        for prod in basket.products:

            if prod.sector_id == 1:
                month_sales_by_sector[0] = month_sales_by_sector[0]+1
            elif prod.sector_id == 2:
                month_sales_by_sector[1] = month_sales_by_sector[1]+1
            elif prod.sector_id == 3:
                month_sales_by_sector[2] = month_sales_by_sector[2]+1
            elif prod.sector_id == 4:
                month_sales_by_sector[3] = month_sales_by_sector[3]+1
            elif prod.sector_id == 5:
                month_sales_by_sector[4] = month_sales_by_sector[4]+1

        
    #import pdb
    #pdb.set_trace()
    return render_template("accounting_charts.html", 
                           sector_sales=sector_sales, 
                           popular_products=popular_products,
                           sales_numbers = sales_numbers,
                           x_axis=x_axis,
                           revenue_data=revenue_data, 
                           parsed_revenue=parsed_dates, 
                           revenue=revenue, expenses=expenses, 
                           projection=projection,
                           month_sales_by_sector=month_sales_by_sector,
                           num_days=num_days,
                           monthly_sector_sales_data=monthly_sector_sales_data,
                           monthly_sector_sales_data2=monthly_sector_sales_data2,
                           monthly_sector_sales_data3=monthly_sector_sales_data3,
                           monthly_sector_sales_data4=monthly_sector_sales_data4,
                           monthly_sector_sales_data5=monthly_sector_sales_data5,
                           monthly_sector_sales_data6=monthly_sector_sales_data6,
                           monthly_sector_sales_data7=monthly_sector_sales_data7)

@app.route('/invoice', methods=['GET'])
def showAccountingCharts():
    invoices = Invoice.query.all()
    customers = Customer.query.all()
    return render_template("all_invoices.html", invoices=invoices, customers=customers)

@app.route('/users', methods=['GET'])
def showAllUsers():
    users = User.query.all()
    trending_products = random_products(4)
    recent_messages = (Message
                    .query
                    .order_by(Message.timestamp.desc())
                    .limit(3)
                    .all())
    return render_template("/front-end/users.html", users=users, trending_products=trending_products, recent_messages=recent_messages)

@app.route('/financial_reporting', methods=["GET"])
def show_financial_reports():
    fin_data = balance_sheet_data_placeholder()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render_template("financial-reports.html", fin_data=fin_data, months=months)


@app.route('/revenue', methods=["GET"])
def show_revenue_charts():

    ## rev vs expenses table. modify later for less error prone date generation. SWEETIE MOVE THIS TO FORMULAS NO ONE WANTS TO SEE THIS
    import pdb
    pdb.set_trace()




    revenue_data = set_date(datetime.datetime.now())
    parsed_dates = parse_date(revenue_data)
    sales_numbers = parse_sales_numbers(revenue_data)
    revenue = limit_month_revenue(parsed_dates)
    expenses = parse_date_bills(revenue_data)
    projection = []
    projection_calculator = [.88, .90, .72, .69, .84, .92, .82]
    for i in range(7):
        projection.append(revenue[i]*projection_calculator[i])

    x_axis = []
    x_axis.append(get_past_date(30))
    x_axis.append(get_past_date(60))
    x_axis.append(get_past_date(90))
    x_axis.append(get_past_date(120))
    x_axis.append(get_past_date(150))
    x_axis.append(get_past_date(180))
    x_axis.append(get_past_date(210))

    '''given num_days, calculate date that many days in the past from today using datetime.datetime.now()'''
    num_days = 55
    month_sales_by_sector = [0,0,0,0,0]
    now = datetime.datetime.now()
    past_date = now - datetime.timedelta(days=num_days)
    recent_sales = []
    recent_sales_data = Basket.query.filter(Basket.submitted_at > past_date).all()
    for basket in recent_sales_data:

        recent_sales.append(basket)

        for prod in basket.products:

            if prod.sector_id == 1:
                month_sales_by_sector[0] = month_sales_by_sector[0]+prod.price
            elif prod.sector_id == 2:
                month_sales_by_sector[1] = month_sales_by_sector[1]+prod.price
            elif prod.sector_id == 3:
                month_sales_by_sector[2] = month_sales_by_sector[2]+prod.price
            elif prod.sector_id == 4:
                month_sales_by_sector[3] = month_sales_by_sector[3]+prod.price
            elif prod.sector_id == 5:
                month_sales_by_sector[4] = month_sales_by_sector[4]+prod.price

    
    '''given list of dates, calculate monthly sales by sector. list of lists.'''
    monthly_sector_sales_data = [0,0,0,0,0]
    monthly_sector_sales_data2 = [0,0,0,0,0]
    monthly_sector_sales_data3 = [0,0,0,0,0]
    monthly_sector_sales_data4 = [0,0,0,0,0]
    monthly_sector_sales_data5 = [0,0,0,0,0]
    monthly_sector_sales_data6 = [0,0,0,0,0]
    monthly_sector_sales_data7 = [0,0,0,0,0]
    
    monthly_data = Basket.query.filter(Basket.submitted_at > x_axis[0]).all()
    for basket in monthly_data:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data[0] = monthly_sector_sales_data[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data[1] = monthly_sector_sales_data[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data[2] = monthly_sector_sales_data[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data[3] = monthly_sector_sales_data[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data[4] = monthly_sector_sales_data[4]+prod.price

    monthly_data2 = Basket.query.filter(Basket.submitted_at > x_axis[1], Basket.submitted_at < x_axis[0]).all()
    for basket in monthly_data2:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data2[0] = monthly_sector_sales_data2[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data2[1] = monthly_sector_sales_data2[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data2[2] = monthly_sector_sales_data2[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data2[3] = monthly_sector_sales_data2[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data2[4] = monthly_sector_sales_data2[4]+prod.price
    monthly_data3 = Basket.query.filter(Basket.submitted_at > x_axis[2], Basket.submitted_at < x_axis[1]).all()
    for basket in monthly_data3:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data3[0] = monthly_sector_sales_data3[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data3[1] = monthly_sector_sales_data3[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data3[2] = monthly_sector_sales_data3[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data3[3] = monthly_sector_sales_data3[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data3[4] = monthly_sector_sales_data3[4]+prod.price
    monthly_data4 = Basket.query.filter(Basket.submitted_at > x_axis[3], Basket.submitted_at < x_axis[2]).all()
    for basket in monthly_data4:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data4[0] = monthly_sector_sales_data4[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data4[1] = monthly_sector_sales_data4[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data4[2] = monthly_sector_sales_data4[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data4[3] = monthly_sector_sales_data4[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data4[4] = monthly_sector_sales_data4[4]+prod.price
    monthly_data5 = Basket.query.filter(Basket.submitted_at > x_axis[4], Basket.submitted_at < x_axis[3]).all()
    for basket in monthly_data5:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data5[0] = monthly_sector_sales_data5[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data5[1] = monthly_sector_sales_data5[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data5[2] = monthly_sector_sales_data5[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data5[3] = monthly_sector_sales_data5[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data5[4] = monthly_sector_sales_data5[4]+prod.price
    monthly_data6 = Basket.query.filter(Basket.submitted_at > x_axis[5], Basket.submitted_at < x_axis[4]).all()
    for basket in monthly_data6:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data6[0] = monthly_sector_sales_data6[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data6[1] = monthly_sector_sales_data6[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data6[2] = monthly_sector_sales_data6[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data6[3] = monthly_sector_sales_data6[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data6[4] = monthly_sector_sales_data6[4]+prod.price

    monthly_data7 = Basket.query.filter(Basket.submitted_at > x_axis[6], Basket.submitted_at < x_axis[5]).all()
    for basket in monthly_data7:

        for prod in basket.products:

            if prod.sector_id == 1:
                monthly_sector_sales_data7[0] = monthly_sector_sales_data7[0]+prod.price
            elif prod.sector_id == 2:
                monthly_sector_sales_data7[1] = monthly_sector_sales_data7[1]+prod.price
            elif prod.sector_id == 3:
                monthly_sector_sales_data7[2] = monthly_sector_sales_data7[2]+prod.price
            elif prod.sector_id == 4:
                monthly_sector_sales_data7[3] = monthly_sector_sales_data7[3]+prod.price
            elif prod.sector_id == 5:
                monthly_sector_sales_data7[4] = monthly_sector_sales_data7[4]+prod.price

    #data generation for sales by product graph
    popular_products = get_product_sale_data()

    sector_sales = get_sales_by_sector()

    return render_template("revenue.html", 
                            
                           month_sales_by_sector=month_sales_by_sector,
                           sales_numbers = sales_numbers,
                           sector_sales = sector_sales,
                           x_axis=x_axis,
                           revenue_data=revenue_data, 
                           parsed_revenue=parsed_dates, 
                           revenue=revenue, expenses=expenses, 
                           projection=projection,
                           num_days=num_days,
                           popular_products=popular_products,
                           monthly_sector_sales_data=monthly_sector_sales_data,
                           monthly_sector_sales_data2=monthly_sector_sales_data2,
                           monthly_sector_sales_data3=monthly_sector_sales_data3,
                           monthly_sector_sales_data4=monthly_sector_sales_data4,
                           monthly_sector_sales_data5=monthly_sector_sales_data5,
                           monthly_sector_sales_data6=monthly_sector_sales_data6,
                           monthly_sector_sales_data7=monthly_sector_sales_data7
                           )


@app.route('/about', methods=['GET'])
def show_about_page():
    
    return render_template("/front-end/about-us.html")


##############################################################################
# General user routes: UPDATE ME TO MAKE THIS WORK THIS WEEK THATS MY GOAL OK MAKE IT HAPPEN SIS

#@app.route('/users')
#def list_users():
#    """Page with listing of users.

#    Can take a 'q' param in querystring to search by that username.
#    """

#    search = request.args.get('q')

#    if not search:
#        users = User.query.all()
#    else:
#        users = User.query.filter(User.username.like(f"%{search}%")).all()

#    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)
    num_of_likes = len(user.likes)
    wishlist = user.favorites
    # snagging messages in order from the database;
    # user.messages won't be in order by default
    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
    
    return render_template('front-end/user_info.html', user=user, messages=messages, num_of_likes=num_of_likes, wishlist=wishlist)


@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    following = user.following
    
    return render_template('front-end/user_following.html', user=user, following=following)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    followers = user.followers
    return render_template('front-end/user_followers.html', user=user, followers=followers)


@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get_or_404(follow_id)
    user = User.query.get_or_404(session["user_id"])
    user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    followed_user = User.query.get(follow_id)
    user = User.query.get_or_404(session["user_id"])
    user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{user.id}/following")


@app.route('/users/profile', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""
    
    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
        
    user=g.user
    id = user.id
    form = UpdateUserForm(obj=user)
    

    if form.validate_on_submit():

        loggeduser = User.authenticate(form.username.data,
                                 form.password.data)

        if loggeduser:
            email = form.email.data
            username = form.username.data       
            bio = form.bio.data
            image_url = form.image_url.data
            header_image_url = form.header_image_url.data

            user.email=email
            user.username=username
            user.bio=bio
            user.image_url=image_url
            user.header_image_url=header_image_url

            db.session.add(user)
            db.session.commit()
            flash("Updated profile successfully", 'success')
            return redirect(f'/users/{id}')

        flash("Invalid credentials.", 'danger')

        
    # IMPLEMENT THIS
    return render_template('users/edit.html', form=form, user=user)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

@app.route('/users/add_like/<int:id>', methods=["POST"])
def add_like(id):
    """add like"""
    if not session["user_id"]:
        flash("Log in to like a message!.", "danger")
        return redirect("/")
    
    currUser = User.query.get_or_404(session["user_id"])
    msg = Message.query.filter_by(id=id)
    if request.method == 'POST':
        if Likes.query.filter_by(user_id=currUser.id, message_id=msg[0].id).first():
            unlike = Likes.query.filter_by(user_id=currUser.id, message_id=msg[0].id)
            db.session.delete(unlike[0])
            db.session.commit()
            flash("Removed from liked!", "alert alert-success alert-dismissible border border-success fade show col-3")
            return redirect(f"/users/{currUser.id}/liked")

        user_id=currUser.id
        message_id=msg[0].id
        new_like = Likes(user_id=user_id, message_id=message_id)
        db.session.add(new_like)
        db.session.commit()
        flash("Added to liked messages!", "alert alert-success alert-dismissible border border-success fade show col-3")
        
        return redirect(f"/users/{user_id}/liked")


@app.route('/users/<int:id>/liked')
def show_likes(id):
    """add like"""
    if not session["user_id"]:
        flash("Log in to liked messages!.", "danger")
        return redirect("/sfef")
    user = User.query.get_or_404(id)
    liked_messages = user.likes

    return render_template("front-end/user_likes.html", user=user, liked_messages=liked_messages)
##############################################################################
# Messages routes:

@app.route('/messages/new', methods=["GET", "POST"])
def messages_add():
    """Add a message:

    Show form if GET. If valid, update message and redirect to user page.
    """

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(text=form.text.data)
        g.user.messages.append(msg)
        db.session.commit()

        return redirect(f"/users/{g.user.id}")

    return render_template('messages/new.html', form=form)


@app.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id):
    """Show a message."""

    msg = Message.query.get(message_id)
    return render_template('messages/show.html', message=msg)


@app.route('/messages/<int:message_id>/delete', methods=["POST"])
def messages_destroy(message_id):
    """Delete a message."""

    if not session["user_id"]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    msg = Message.query.get(message_id)
    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


##############################################################################

@app.route('/blank', methods=["GET"])
def testingthis():
    
    
    return render_template('blank.html')


@app.route('/shop/login', methods=["GET", "POST"])
def front_end_login():
    '''login user: produce form and handle form submission'''
    form = LoginForm()
    if "username" in session:
        return redirect("/shop")

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        
        user = User.authenticate(username, pwd)
        if user:
            session["user_id"] = user.id
            id = user.id
            session["username"] = user.username
            userdata = User.query.filter_by(id=id).all()
            username = userdata[0].username
            flash(f"You have successfully logged in, {username}!", "success col-3 alert alert-dismissible fade show")   
            return redirect(f"/shop")
        else:
            flash(f"Invalid credentials!", "error")
            return redirect("/front-end/login")
    
    return render_template('/front-end/login.html', form=form)

@app.route('/shop/register', methods=["GET", "POST"])
def front_end_register_user():
    '''register user: produce form and handle form submission'''

    form = RegisterForm()

    if "username" in session:
        return redirect("/shop")

   

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        #first_name = form.first_name.data
        #last_name = form.last_name.data
        email = form.email.data
        image_url = form.image_url.data
        user = User.signup(username, email, pwd, image_url)
        db.session.add(user)
        db.session.commit()
        
        session["user_id"] = user.id
        session["username"] = user.username
        
        #on successful login, redirect to auth user pages
        flash(f"You have successfully registered!", "success col-3 alert alert-dismissible fade show")
        return redirect("/shop")

    else:
        return render_template("/front-end/register.html", form=form)


