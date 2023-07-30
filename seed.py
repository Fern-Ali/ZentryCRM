from models import User, db, Message, Follows, Likes, Favorites, Effect_Tag, ProductTag, Product, Category, Plant_facility, Strain, Seedling, Sector, Account, Customer, Invoice, Bill, Vendor, Sale, Basket, Double_Entry, Journal_Entry, TransactionCR, TransactionDB
from random import choice, randint, sample
from app import app
import datetime
from csv import DictReader

import random
import math


# Create all tables
db.drop_all()
db.create_all()

with open('generator/chart_of_accounts.csv') as chart_of_accounts:
    db.session.bulk_insert_mappings(Account, DictReader(chart_of_accounts))
    db.session.commit()


# If table isn't empty, empty it

User.query.delete()
with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))
    db.session.commit()

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

with open('generator/customers.csv') as customers:
    db.session.bulk_insert_mappings(Customer, DictReader(customers))
    db.session.commit()

with open('generator/products.csv') as products:
    db.session.bulk_insert_mappings(Product, DictReader(products))
    db.session.commit()
#new baskets
customers = Customer.query.all()
with open('generator/baskets.csv') as baskets:
    db.session.bulk_insert_mappings(Basket, DictReader(baskets))
    db.session.commit()


with open('generator/vendors.csv') as vendors:
    db.session.bulk_insert_mappings(Vendor, DictReader(vendors))
    db.session.commit()

with open('generator/bills.csv') as bills:
    db.session.bulk_insert_mappings(Bill, DictReader(bills))
    db.session.commit()


# Add Base Categories

cat1 = Category(name="Indica")
cat2 = Category(name="Sativa")
cat3 = Category(name="Hybrid")
cat4 = Category(name="THC")
cat5 = Category(name="CBD")
cat6 = Category(name="Apparel/Merch")

# Add Base Sectors

sector1 = Sector(name="Smokeables")
sector2 = Sector(name="Vapes")
sector3 = Sector(name="Concentrates")
sector4 = Sector(name="Edibles")
sector5 = Sector(name="Apparel")
sector6 = Sector(name="Merchandise")
sector7 = Sector(name="Hardware")



# Add Base Dummy Plant_facilities

facility1 = Plant_facility(name="North Chester Facility", location="123 Wood Lane, North Chester CA 22332")
facility2 = Plant_facility(name="West Chester Facility", location="456 Wood Lane, West Chester CA 22333")
facility3 = Plant_facility(name="East Chester Facility", location="789 Wood Lane, East Chester CA 22334")
facility4 = Plant_facility(name="South Chester Facility", location="222 Wood Lane, South Chester CA 22584")

db.session.add(cat1)
db.session.add(cat2)
db.session.add(cat3)
db.session.add(cat4)
db.session.add(cat5)
db.session.add(cat6)

db.session.add(sector1)
db.session.add(sector2)
db.session.add(sector3)
db.session.add(sector4)
db.session.add(sector5)
db.session.add(sector6)
db.session.add(sector7)



db.session.add(facility1)
db.session.add(facility2)
db.session.add(facility3)
db.session.add(facility4)

db.session.commit()


with open('generator/strains1.csv') as strains1:
    db.session.bulk_insert_mappings(Strain, DictReader(strains1))
    db.session.commit()

# Add Base Dummy Seedlings

seed1 = Seedling(strain_id=1, plant_facility_id=1 )
seed2 = Seedling(strain_id=2, plant_facility_id=2 )
seed3 = Seedling(strain_id=3, plant_facility_id=3 )

db.session.add(seed1)
db.session.add(seed2)
db.session.add(seed3)

db.session.commit()



# Add Base Users
whiskey = User(username='Admin', password='password', email='admin@domain.com' )
bowser = User(username='User1', password='password', email='user1@domain.com' )
spike = User(username='spike233', password='password', email='spike233@gmail.com' )


# Add Base Dummy Tags

tag1 = Effect_Tag(name="Uplifting")
tag2 = Effect_Tag(name="Drowsy")
tag3 = Effect_Tag(name="Body-high")
tag4 = Effect_Tag(name="Introspective")
tag5 = Effect_Tag(name="Energetic")
tag6 = Effect_Tag(name="Warming")
tag7 = Effect_Tag(name="Calming")
tag8 = Effect_Tag(name="Creativity")
tag9 = Effect_Tag(name="Limited Edition")

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)
db.session.add(tag5)
db.session.add(tag6)
db.session.add(tag7)
db.session.add(tag8)
db.session.add(tag9)


# Add Base Dummy product tags 
products = Product.query.all()
for product in products:
    tag1 = ProductTag(product_id=product.id, effect_tag_id=choice(range(1,9)))
    tag2 = ProductTag(product_id=product.id, effect_tag_id=choice(range(1,9)))

    if tag1.effect_tag_id == tag2.effect_tag_id:
        tag1.effect_tag_id = 9
    db.session.add(tag1)
    db.session.add(tag2)
    # commit--otherwise, this never gets saved!
    db.session.commit()
    


#new invoices

baskets = Basket.query.all()
for basket in baskets:
    customer = Customer.query.filter_by(user_id=basket.customer_id)
    invoice = Invoice(customer_id=basket.customer_id, date_billed=basket.submitted_at, payment_info=customer[0].payment_info, amount=basket.amount  )
    db.session.add(invoice)
    db.session.commit()


#new bills


vendors = Vendor.query.all()





#new sales capturing from baskets to link basket to customer sale data + accounting entry data

#Here we dynamically generate a years' worth of sales data. Each invoice's randomly generated dollar value is divided into per product sales.

invoices = Invoice.query.all()
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
            db.session.commit()
            amount = 0
            i=i+1
        elif amount > 0:
            newSale=Sale(product_id=rand_products[i].id, basket_id=invoice.id, customer_id=invoice.customer_id)
            db.session.add(newSale)
            db.session.commit()
            i=i+1
                
        

                    
        
        

#############################################################################################################################
# ACCOUNTING DATA GENERATION. DO NOT MODIFY UNLESS YOU UNDERSTAND ACCOUNTING DOUBLE ENTRY PRINCIPLES!!!!!!!!!!!!!!!!  #
#############################################################################################################################

invoices = Invoice.query.all();

for invoice in invoices:

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


