from models import db, connect_db, Message, Likes, Favorites, Effect_Tag, ProductTag, Product, Category, Plant_facility, Strain, Seedling, User, Sector, Account, Customer, Invoice, Bill, Vendor, Sale, Basket, Double_Entry, Journal_Entry, TransactionCR, TransactionDB
from forms import ProductForm, CategoryForm, RegisterForm, LoginForm
import datetime
from sqlalchemy import func
from newsapi import NewsApiClient
from random import choice, randint, sample, uniform
import random
from random import uniform
import requests
from faker import Faker
from keys import BASE_URL

fake = Faker()


########################
## ZentryAPI Requests ##
########################

def random_products(num_products):
    '''ZentryAPI request to /api/products/random/<int:num_products>, provide num_products to specify number of results'''
    products = []
    try:
        resp = requests.get(f'{BASE_URL}/api/products/random/{num_products}',          
       )

        resp = resp.json()
        

    except requests.exceptions.RequestException as e:  # This is the correct syntax

        products.append(e)
        return products

    return resp

def get_sectors():
    '''ZentryAPI request to /api/sectors, returns list of sectors json format'''
    try:
        resp = requests.get(
            f"{BASE_URL}/api/sectors",
            #params={"term": "billy bragg", "limit": 3}
            
       )

        resp = resp.json()



    except requests.exceptions.RequestException as e:  # This is the correct syntax
        
        return e
    return resp

def get_APIdata(id, model):
    '''ZentryAPI request to specified endpoint, returns id generated data'''
    product = []
    try:
        resp = requests.get(
            f"{BASE_URL}/api/{model}/{id}",
            #params={"term": "billy bragg", "limit": 3}
            
       )

        resp = resp.json()
        data = resp['0']
        #import pdb
        #pdb.set_trace()
        product.append(data)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        product.append(e)
        return product
    
    return product


def get_APIdata_all(model):
    '''ZentryAPI request to specified endpoint, returns list of all model rows'''
    product = []
    try:
        resp = requests.get(
            f"{BASE_URL}/api/{model}",
            #params={"term": "billy bragg", "limit": 3}
            
       )

        resp = resp.json()
        db.session.commit()
        #import pdb
        #pdb.set_trace()
        product.append(resp)

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        product.append(e)
        return product
    
    return product

###########################
## External API Requests ##
###########################


def get_news():
    ''' use news api to get latest trending articles for dashboard home'''
    # Init
    newsapi = NewsApiClient(api_key='ef3400ea0a6a48cbbed5e1b0deb6ade9')
    now = datetime.datetime.now()
    weekago = now - datetime.timedelta(days=7)
    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(q='business',
                                          #sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

    # /v2/everything
    all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param=weekago,
                                      to=now,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()
    return top_headlines


def get_quote():
    ''' use quotable.io api to generate random quote with 50 char limit'''
    quote = ''

    #try:
    #    resp = requests.get(
    #        "https://api.quotable.io/quotes/random?maxLength=50",
    #        #params={"term": "billy bragg", "limit": 3}
    #   )

    #    resp = resp.json()
    #    if resp[0]["author"]:
    #        return resp
    #    else:
    #        return [{"_id":"f6PUk-AOBm","author":"H. G. Wells","content":"If you fell down yesterday, stand up today.","tags":["Motivational"],"authorSlug":"h-g-wells","length":43,"dateAdded":"2022-07-06","dateModified":"2023-04-14"}]
    #except requests.exceptions.RequestException as e:  # This is the correct syntax
    #    return [{"_id":"f6PUk-AOBm","author":"H. G. Wells","content":"If you fell down yesterday, stand up today.","tags":["Motivational"],"authorSlug":"h-g-wells","length":43,"dateAdded":"2022-07-06","dateModified":"2023-04-14"}]
  
    return [{"_id":"f6PUk-AOBm","author":"H. G. Wells","content":"If you fell down yesterday, stand up today.","tags":["Motivational"],"authorSlug":"h-g-wells","length":43,"dateAdded":"2022-07-06","dateModified":"2023-04-14"}]
  




########################
##  Datetime Helpers  ## ORGANIZE ME
########################


def get_random_datetime_year(year_gap=2):
    """Get a random datetime within the last few years."""

    now = datetime.datetime.now()
    then = now.replace(year=now.year - year_gap)
    random_timestamp = uniform(then.timestamp(), now.timestamp())

    return datetime.fromtimestamp(random_timestamp)

def set_date(current_date):
        '''take dateTime object and return 7 dates for the 7 months prior to given dateTime object'''   

        sales=Sale.query.all()
        baskets=Basket.query.all()
        #current_date = datetime.datetime.now()
        sales_data = ['']
        revenue_data = []
        date_helper = 30
        for i in range(7):
            date = get_past_date(date_helper)
            revenue_data.append(date)
            date_helper = date_helper+30
        print(revenue_data)


        return revenue_data
    

def parse_date(revenue_data):
    '''take given array of dates from set_date function and return 7 mtd revenue values for the 6 dateTime objects in the array.'''  

    revenue_parsed = []
    
    for date in revenue_data:
        sales_data_mtd = Basket.query.filter(Basket.submitted_at > date).all()
        revenue_mtd = 0
        
        for basket in sales_data_mtd:
            revenue_mtd = revenue_mtd + basket.amount
        revenue_parsed.append(revenue_mtd)
        
        
        
    return revenue_parsed

def limit_month_revenue(revenue_parsed):
    '''reorder parse_date return value to properly generate sales by month in line graph on reports dashboard'''
    revenue = []
    revenue.append(revenue_parsed[0])
    revenue.append(revenue_parsed[1]-revenue_parsed[0])
    revenue.append(revenue_parsed[2]-revenue_parsed[1])
    revenue.append(revenue_parsed[3]-revenue_parsed[2])
    revenue.append(revenue_parsed[4]-revenue_parsed[3])
    revenue.append(revenue_parsed[5]-revenue_parsed[4])
    revenue.append(revenue_parsed[6]-revenue_parsed[5])
    return revenue

def parse_date_bills(revenue_data):
    '''take given array of dates from set_date function and return 7 mtd bills # values for the 7 dateTime objects in the array.'''  
    expenses = []
    expenses_parsed = []
    
    for date in revenue_data:
        expense_data_mtd = Bill.query.filter(Bill.date_billed > date).all()
        expenses_mtd = 0
        
        for bill in expense_data_mtd:
            expenses_mtd = expenses_mtd + bill.amount
        expenses.append(expenses_mtd)
        
        
    expenses_parsed.append(expenses[0])    
    expenses_parsed.append(expenses[1]-expenses[0])    
    expenses_parsed.append(expenses[2]-expenses[1])    
    expenses_parsed.append(expenses[3]-expenses[2])    
    expenses_parsed.append(expenses[4]-expenses[3])
    expenses_parsed.append(expenses[5]-expenses[4])
    expenses_parsed.append(expenses[6]-expenses[5])
    
    return expenses_parsed




def parse_sales_numbers(revenue_data):
    '''take given array of dates from set_date function and return 7 mtd sales # values for the 7 dateTime objects in the array.'''  
    sales_numbers = []
    sales_numbers_parsed = []
    for date in revenue_data:
        sales_data_mtd = Basket.query.filter(Basket.submitted_at > date).all()
        revenue_mtd = 0
        sales_numbers.append(len(sales_data_mtd))
                               
    sales_numbers_parsed.append(sales_numbers[0])
    sales_numbers_parsed.append(sales_numbers[1]-sales_numbers[0])
    sales_numbers_parsed.append(sales_numbers[2]-sales_numbers[1])
    sales_numbers_parsed.append(sales_numbers[3]-sales_numbers[2])
    sales_numbers_parsed.append(sales_numbers[4]-sales_numbers[3])
    sales_numbers_parsed.append(sales_numbers[5]-sales_numbers[4])
    sales_numbers_parsed.append(sales_numbers[6]-sales_numbers[5])
    return sales_numbers_parsed





def get_product_sale_data():
    '''Use count to get number of sales per product in database.'''
    total_sales_by_product = db.session.query(func.count(Sale.product_id), Sale.product_id).group_by(Sale.product_id).all()
    popular_products_queryfinder = []
    popular_products = []
    for prod in total_sales_by_product:
        if prod[0] > 203:
            popular_products_queryfinder.append(prod)
    #print(popular_products_queryfinder)
    popular_products_queryfinder.sort(reverse=True)
    for prod in popular_products_queryfinder:
        popular_prod = Product.query.get(prod[1])
        popular_products.append(popular_prod)
    return popular_products

def get_timedelta(num_days):
    '''given num_days, calculate date that many days in the past from today using datetime.datetime.now()'''
    now = datetime.datetime.now()
    past_date = now - datetime.timedelta(days=num_days)
    recent_sales = []
    recent_sales_data = Basket.query.filter(Basket.submitted_at > past_date).all()
    for basket in recent_sales_data:
        recent_sales.append(basket)
    return recent_sales

def get_past_date(num_days):
    '''given num days get past datetime obj'''
    now = datetime.date.today()
    past_date = now - datetime.timedelta(days=num_days)
    return past_date

def get_past_datetime(num_days):
    '''given num days get past datetime obj'''
    now = datetime.datetime.now()
    past_date = now - datetime.timedelta(days=num_days)
    return past_date

################################
##  Sales Helpers ORGANIZE ME ##
################################


def random_generator(num_units, model):
    '''choose amount of random units to be added to a list'''

    models = model.query.all()
    rand_gen= []
    
    for x in range(num_units):
        unit = choice(models)
        rand_gen.append(unit)
    rand_gen = list(set(rand_gen))
    while len(rand_gen) < num_units:
        unit2=choice(models)
        rand_gen.append(unit2)
        rand_gen = list(set(rand_gen))
    
        
            
    return rand_gen


def get_random_date(within_num_days):
    """Get a random datetime within the last few years."""

    now = datetime.date.today()
    then = get_past_date(within_num_days)
    random_timestamp = uniform(then.timestamp(), now.timestamp())

    return datetime.datetime.fromtimestamp(random_timestamp)

def get_random_datetime(within_num_days):
    """Get a random date within the last few years."""

    now = datetime.datetime.now()
    then = get_past_datetime(within_num_days)
    random_timestamp = uniform(then.timestamp(), now.timestamp())

    return datetime.datetime.fromtimestamp(random_timestamp)

def get_currUser_orders(id):
    ''' return list of all baskets for customer_id'''
    
    
    orders = Basket.query.filter_by(customer_id=id).all()
    return orders


def get_sales_by_sector():
    '''returns a list in which each index value is the number of product sales for each sector, from sectors 1 - 7.'''

    sectors = Sector.query.all()
    count = 0
    sales_by_sector = []
    for sector in sectors:
        for prod in sector.products:
            count = count + len(prod.baskets)
        sales_by_sector.append(count)
        count = 0
    return sales_by_sector
    
def balance_sheet_data_placeholder():
    ''' acccount values - and placeholders in lieu of business data. soon to be dynamically generated'''
    financial_data = []
    cash=Account.query.get(2)
    cash_balance =0
    for entry in cash.transactions_db:
        cash_balance = cash_balance + (entry.amount*entry.direction)
    for entry in cash.transactions_cr:
        cash_balance = cash_balance + (entry.amount*entry.direction)

    
    inventory=56000
    securities=23000
    land=112252
    accounts_payable =12592
    deferred_revenue =969379
    term_debt=18009
    capital=890059
    retained_earnings=596893

    financial_data.append(cash_balance)
    financial_data.append(inventory)
    financial_data.append(securities)
    financial_data.append(land)
    financial_data.append(accounts_payable)
    financial_data.append(deferred_revenue)
    financial_data.append(term_debt)
    financial_data.append(capital)
    financial_data.append(retained_earnings)

    return financial_data



################################################################
## Database Modifiers --- Record Generation / Deletion [Mass] ##
################################################################


def generate_favorites():
    '''seed favorites data - user to product(s)'''
    products = Product.query.all()
    users = User.query.all()
    
    for user in users:
        fav_list = random_products(12)
        for fav in fav_list:
            new_fav = Favorites(user_id=user.id, product_id=fav.id)
            db.session.add(new_fav)
            db.session.commit()

def delete_favorites():
    ''' delete all user product favorites'''

    favs = Likes.query.all()
    for fav in favs:
        db.session.delete(fav)
        db.session.commit()

def generate_likes():
    '''seed likes data - user to message(s)'''
    messages = Message.query.all()
    users = User.query.all()
    
    for user in users:
        message_list = random_generator(50, Message)
        for msg in message_list:
            new_like = Likes(user_id=user.id, message_id=msg.id)
            db.session.add(new_like)
            db.session.commit()


def generate_reviews(NUM_REVIEWS_PER_USER):
    '''seed reviews data - user to message(s)'''
    
    users = User.query.all()
    MAX_WARBLER_LENGTH=140
    for user in users:

        review_list = random_products(NUM_REVIEWS_PER_USER)

        for prod in review_list:
            
            new_review = Message(text=fake.paragraph()[:MAX_WARBLER_LENGTH],
                          timestamp=get_random_datetime(2),
                          user_id=user.id,
                          product_id=prod.id)
            db.session.add(new_review)
            db.session.commit()
            
def generate_daily_metrics(num_records):
    
    #NUM_USERS = len(User.query.all())-1
    NUM_USERS = 300

    for i in range(num_records):

        date = get_random_datetime(1)
        msg = Message(
            text=fake.paragraph()[:140],
            timestamp=date,
            user_id=randint(1, NUM_USERS)
        )
        db.session.add(msg)
        db.session.commit()

        totalmsgs = len(Message.query.all())
    return totalmsgs


def generate_daily_sale_metrics(num_records, within_num_days):
    
    NUM_USERS = len(User.query.all())-1
    NUM_CUSTOMERS = len(Customer.query.all())-1
    users = []
    customers = []
    baskets = []
    invoices = []
    initial_lengths = [len(Basket.query.all()), len(Invoice.query.all()), len(Journal_Entry.query.all()), len(Sale.query.all())]
    for i in range(1, NUM_USERS):
        users.append(i)
    for i in range(1, NUM_CUSTOMERS):
        customers.append(i)

    for i in range(num_records):

        date = get_random_datetime(within_num_days)

        #gen basket for num_records
        
        
        basket = Basket(customer_id = choice(customers), submitted_at=date, amount=random.sample(range(50, 1000), 1)[0])
        baskets.append(basket)
        db.session.add(basket)
        db.session.commit()
        #gen invoice for num_records


        #new invoices

        
    for basket in baskets:
        customer = Customer.query.filter_by(user_id=basket.customer_id)
        invoice = Invoice(id=basket.id, customer_id=basket.customer_id, date_billed=basket.submitted_at, payment_info=customer[0].payment_info, amount=basket.amount  )
        invoices.append(invoice)
        db.session.add(invoice)
        db.session.commit()


        
        products = Product.query.all()
        for invoice in invoices:
            rand_products = random.sample(products, 90)
            amount = invoice.amount
            i=0
            while amount > 0:

            
           
                amount=amount-rand_products[i].price
                if amount < 0: 
                    discount = amount
                    amount=amount+rand_products[i].price
                
                    newDiscountedSale=Sale(product_id=rand_products[i].id, basket_id=invoice.id, customer_id=invoice.customer_id, discount=discount)
                    db.session.add(newDiscountedSale)
                    db.session.flush()
                    db.session.commit()
                    amount = 0
                    i=i+1
                elif amount > 0:
                    newSale=Sale(product_id=rand_products[i].id, basket_id=invoice.id, customer_id=invoice.customer_id)
                    db.session.add(newSale)
                    db.session.flush()
                    db.session.commit()
                    i=i+1
        
            debit_to_cash = TransactionDB(date=invoice.date_billed, amount=invoice.amount, account_number=110, direction=1)
            credit_to_revenue = TransactionCR(date=invoice.date_billed, amount=invoice.amount, account_number=300, direction=-1)

            db.session.add(debit_to_cash)
            db.session.add(credit_to_revenue)
            db.session.commit()



            debit_to_COGS = TransactionDB(date=invoice.date_billed, amount=invoice.amount, account_number=410, direction=1)
            credit_to_assets = TransactionCR(date=invoice.date_billed, amount=invoice.amount, account_number=100, direction=-1)

            db.session.add(debit_to_COGS)
            db.session.add(credit_to_assets)
            db.session.commit()



            journal1= Journal_Entry(description="Auto-generated JE for Budly invoice")

            db.session.add(journal1)
            db.session.commit()

            dbl_entry1 = Double_Entry(db_id=debit_to_cash.id, cr_id=credit_to_revenue.id, jr_id=journal1.id)
            dbl_entry2 = Double_Entry(db_id=debit_to_COGS.id, cr_id=credit_to_assets.id, jr_id=journal1.id)

            db.session.add(dbl_entry1)
            db.session.add(dbl_entry2)
            db.session.commit() 
        


        
        new_totals = {"Baskets": (len(Basket.query.all()), initial_lengths[0] ),
                      "Invoices": (len(Invoice.query.all()), initial_lengths[1] ),
                      "Journal Entries": (len(Journal_Entry.query.all()), initial_lengths[2] ),
                      "Sales": (len(Sale.query.all()), initial_lengths[3] ),
                      }
    return new_totals


def generate_daily_bill_metrics(num_records):

    date = get_random_datetime(1)
    initial_length = len(Bill.query.all())
    for i in range(num_records):
        bill = Bill(vendor_id=choice(range(1,21)), date_billed=date, amount=random.sample(range(50, 1000), 1)[0])
        db.session.add(bill)
        db.session.commit()

    new_total = {"Bills": (len(Bill.query.all()), initial_length ),
                 }
    return new_total      