from models import User, db, Effect_Tag, ProductTag, Product, Category, Plant_facility, CategoryTag, Strain, Seedling, ProductCategory, ProductSector, Sector
from accounting_models import Account
from app import app
import datetime
from csv import DictReader
from faker import Faker
import random
import math
fake = Faker()


with open('generator/chart_of_accounts.csv') as chart_of_accounts:
    db.session.bulk_insert_mappings(Account, DictReader(chart_of_accounts))
    db.session.commit()

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
#User.query.delete()
with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))
    db.session.commit()

users = User.query.all()
for user in users:
    new_customer=Customer(user_id=user.id, account_number=random.sample(range(5999, 9999), 1), payment_info=fake.credit_card_full())
    db.session.add(new_customer)
    db.session.commit()







# Add Base Categories

cat1 = Category(name="Indica")
cat2 = Category(name="Sativa")
cat3 = Category(name="Hybrid")
cat4 = Category(name="THC")
cat5 = Category(name="CBD")

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

with open('generator/products.csv') as products:
    db.session.bulk_insert_mappings(Product, DictReader(products))
    db.session.commit()

# Add Base Users
whiskey = User(first_name='Whiskey', last_name='Delta', username='Admin', password='password', email='admin@domain.com' )
bowser = User(first_name='Bowser', last_name='Cline', username='User1', password='password', email='user1@domain.com' )
spike = User(first_name='Spike', last_name='Spice', username='spike233', password='password', email='spike233@gmail.com' )

# Add Base Dummy Product

##flower1 = Product(name="Bubble Gum 8th", category_id=1, seedling_id=1, strain_id=1, plant_facility_id=1, sector_id=1)
##flower2 = Product(name="Blue Petrol 8th", category_id=2, seedling_id=1, strain_id=2, plant_facility_id=2, sector_id=2)
##flower3 = Product(name="GG 8th", category_id=3, seedling_id=1, strain_id=3, plant_facility_id=3, sector_id=3)







# Add Base Dummy Tags

tag1 = Effect_Tag(name="Uplifting")
tag2 = Effect_Tag(name="Drowsy")
tag3 = Effect_Tag(name="Body-high")









# Add Base Dummy categories

categorytag1 = CategoryTag(category_id=1, effect_tag_id=1 )
categorytag2 = CategoryTag(category_id=2, effect_tag_id=2 )
categorytag3 = CategoryTag(category_id=3, effect_tag_id=3 )


# Add Base Dummy product tags 

product_tag1 = ProductTag(product_id=1, effect_tag_id=1 )
product_tag2 = ProductTag(product_id=2, effect_tag_id=2 )
product_tag3 = ProductTag(product_id=3, effect_tag_id=3 )

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)
db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)


# commit--otherwise, this never gets saved!
db.session.commit()




# create / commit post after users are created so that the user_id of 1 is valid upon post creation
db.session.add(categorytag1)
db.session.add(categorytag2)
db.session.add(categorytag3)


db.session.commit()




# Commit--otherwise, this never gets saved!
db.session.commit()

# create / commit post after users are created so that the user_id of 1 is valid upon post creation
db.session.add(product_tag1)
db.session.add(product_tag2)
db.session.add(product_tag3)

# Commit--otherwise, this never gets saved!
db.session.commit()

products = Product.query.all()
for prod in products:
    newProdCat = ProductCategory(category_id=prod.category_id, product_id=prod.id)
    newProdSector = ProductSector(sector_id=prod.sector_id, product_id=prod.id)
    db.session.add(newProdCat)
    db.session.add(newProdSector)
    db.session.commit()



#new baskets
customers = Customer.query.all()
for customer in customers:
    basket = Basket(customer_id=customer.id, submitted_at=fake.date_time_between('2023-01-01 11:42:52'), amount=random.sample(range(50, 1000), 1))
    db.session.add(basket)
    db.session.commit()
#new invoices

Baskets = Basket.query.all()
for basket in baskets:
    customer = Customer.query.filter_by(id=basket.customer_id)
    invoice = Invoice(customer_id=basket.customer_id, date_billed=basket.submitted_at, payment_method=customer[0].payment_method, amount=basket.amount  )
    db.session.add(invoice)
    db.session.commit()


#new vendors, bills

for i in range(20):
    vendor = Vendor(name=fake.company(), address=fake.address())
    db.session.add(vendor)
    db.session.commit

#new bills
months = []
for i in range(12):
    num = i+1
    months.append(i)

vendors = Vendor.query.all()


for month in months:

    month_start = '2023-(0+month)-01 11:42:52'
    month_end = '2023-(0+month)-29 12:21:12'

    for vendor in vendors:
        subscription = Bill(vendor_id=vendor.id, date_logged=fake.date_time_between(month_start, month_end ))
        service = Bill(vendor_id=vendor.id, date_logged=fake.date_time_between(month_start, month_end ))
        loan = Bill(vendor_id=vendor.id, date_logged=fake.date_time_between(month_start, month_end ))
        product = Bill(vendor_id=vendor.id, date_logged=fake.date_time_between(month_start, month_end ))
        utility = Bill(vendor_id=vendor.id, date_logged=fake.date_time_between(month_start, month_end ))

        db.session.add(subscription)
        db.session.add(service)
        db.session.add(loan)
        db.session.add(product)
        db.session.add(utility)
        db.session.commit()



#new sales capturing from baskets to link basket to customer sale data + accounting entry data

basket_balance = 0
basket_products = []
discount = 0

for basket in baskets:
    
    basket_products=random.sample(range(products[0], products[89]), 15)


    for product in basket_products:

        if basket_balance > basket.amount:
            print('moving on to next product')
        elif basket_balance <= basket.amount:
            basket_balance = basket_balance + product.price
            sale = Sale(product_id=product.id, basket_id=basket.id, customer_id=basket.customer_id)
            db.session.add(sale)
            db.session.commit()
            if basket_balance > basket.amount:
                
                
                discount = basket_balance - basket.amount
                basket_balance = basket_balance - discount

                if math.isclose(basket_balance, basket.amount, abs_tol = 0.3):

                    sale_discounted = Sale(product_id=product.id, basket_id=basket.id, customer_id=basket.customer_id, discount=discount)
                    db.session.add(sale_discounted)
                    db.session.commit()
        
        


