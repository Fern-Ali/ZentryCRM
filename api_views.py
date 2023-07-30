from flask import Flask, request, jsonify, render_template, json
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Product
from models import db, connect_db, Message, Follows, Likes, Favorites, Effect_Tag, ProductTag, Product, Category, Plant_facility, Strain, Seedling, User, Sector, Account, Customer, Invoice, Bill, Vendor, Sale, Basket, Double_Entry, Journal_Entry, TransactionCR, TransactionDB, Direct_Message, ProductRating
from random import choice
from formulas import get_past_date, get_product_sale_data, get_timedelta
from sqlalchemy import func, select, column, text
import datetime
from collections import OrderedDict
from formulas import random_products
from flask import Blueprint
# ...
api = Blueprint("api", __name__)


##############################
#------TABLE OF CONTENTS-----#
##############################

##############################
#     A. INVENTORY API       #
##############################

#1A. Products
#2A. Sectors 
#3A. Categories 
#4A. Strains 
#5A. Facilities 
#6A. Seedlings 

##############################
#     B. ACCOUNTING API      #
##############################

#1B. Accounts
#2B. Double Entries
#3B. Credit Transations
#4B. Debit Transactions
#5B. Journal Entries
#6B. Invoices
#7B. Customers
#8B. Vendors

##############################
#     C. ECOMMERCE API      #
##############################

#1C. Sales by product (Sales)
#2C. Sales by cart (Baskets)

##############################
#       D. SOCIAL API        #
##############################

#1D. Users
#2D. Posts
#3D. Reviews
#4D. Likes
#5D. Favorites
#6D. Follows

##############################
#------ZENTRY API DOCS-------#
##############################

@api.route('/api')
def get_home_page():
    '''Renders ZentryAPI docs'''
    return render_template('api_docs.html')


@api.route('/api/schema')
def get_schema_image():
    '''shows full-sized db schema image'''
    return render_template('schema.html')







##################################
#--A---INVENTORY API SECTION-----#
##################################

#1A. Products
#2A. Sectors 
#3A. Categories 
#4A. Strains 
#5A. Facilities 
#6A. Seedlings 

##################################
#                                #
##################################


##############################
#-------1A. Products---------#
##############################

@api.route('/api/products', methods=["GET"]) 
def list_products():
    '''List all products in database'''
    products = Product.query.order_by(Product.price.desc()).all()
    data = {}
    data_list = enumerate(products)
    for prod in data_list: 
        data[f'{prod[0]}']={
            'id': prod[1].id,
            'name': prod[1].name,
            'description': prod[1].description,
            'category_id': prod[1].category_id,
            'sector_id': prod[1].sector_id,
            'updated_at': prod[1].updated_at,
            'image_url': prod[1].image_url,
            'seedling_id': prod[1].seedling_id,
            'strain_id': prod[1].strain_id,
            'plant_facility_id': prod[1].plant_facility_id,
            'price': prod[1].price
        }


    return jsonify(data)


    
@api.route('/api/products', methods=["POST"])
def create_product():
    '''Create a new product via POST request. Must provide params below.'''

    new_product = Product(name=request.json["name"],
                            description=request.json["description"],
                            price=request.json["price"],
                            category_id=request.json["category_id"],
                            sector_id=request.json["sector_id"],
                            image_url=request.json["image_url"],
                            seedling_id=request.json["seedling_id"],
                            strain_id=request.json["strain_id"],
                            plant_facility_id=request.json["plant_facility_id"]
                            
                            )
    db.session.add(new_product)
    db.session.commit()

    data = {}
    data[f'{new_product.name}']={
        'id': new_product.id,
        'name': new_product.name,
        'description': new_product.description,
        'category_id': new_product.category_id,
        'sector_id': new_product.sector_id,
        'updated_at': new_product.updated_at,
        'image_url': new_product.image_url,
        'seedling_id': new_product.seedling_id,
        'strain_id': new_product.strain_id,
        'plant_facility_id': new_product.plant_facility_id,
        'price': new_product.price
    }
    

    return jsonify((data), 201)   



@api.route('/api/products/<int:id>', methods=["GET"])
def get_product(id):
    '''Get data for specific product, supply ID in header'''
    product=[]
    product.append(Product.query.get_or_404(id))
    data = {}
    data_list = enumerate(product)

    for product in data_list: 
        data[product[0]]={
                'id': product[1].id,
                'name': product[1].name,
                'description': product[1].description,
                'category_id': product[1].category_id,
                'sector_id': product[1].sector_id,
                'updated_at': product[1].updated_at,
                'image_url': product[1].image_url,
                'seedling_id': product[1].seedling_id,
                'strain_id': product[1].strain_id,
                'plant_facility_id': product[1].plant_facility_id,
                'price': product[1].price
            }


    return jsonify(data)

@api.route('/api/products/<int:id>', methods=["PATCH"]) 
def update_product(id):
    '''Update a specific product via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the product.'''

    product = Product.query.get_or_404(id)
    
    #db.session.query(Cupcake).filter_by(id=id).update(request.json) solution in one line to update from user. dont have to update things line by line.


    product.name = request.json.get('name', product.name)
    product.description = request.json.get('description', product.description)
    product.category_id = request.json.get('category_id', product.category_id)
    product.sector_id = request.json.get('sector_id', product.sector_id)
    product.image_url = request.json.get('image_url', product.image_url)
    product.seedling_id = request.json.get('seedling_id', product.seedling_id)
    product.strain_id = request.json.get('strain_id', product.strain_id)
    product.plant_facility_id = request.json.get('plant_facility_id', product.plant_facility_id)
    product.price = request.json.get('rating', product.price)

    db.session.commit()

    data = {}
    
    data[f'{product.name}']={
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category_id': product.category_id,
        'sector_id': product.sector_id,
        'updated_at': product.updated_at,
        'image_url': product.image_url,
        'seedling_id': product.seedling_id,
        'strain_id': product.strain_id,
        'plant_facility_id': product.plant_facility_id,
        'price': product.price
    }


    return jsonify(data)  


@api.route('/api/products/<int:id>', methods=["DELETE"]) 
def delete_product(id):
    '''Delete a specific product. Specify via ID in header'''
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify(message="deleted")


@api.route('/api/products/sectors/<int:id>', methods=["GET"]) 
def get_products_by_sector(id):
    '''Get all products by specified category id'''
    
    query = text("SELECT * FROM products WHERE (sector_id=:id)")
    res1 = db.session.execute(query, {"id": id}).fetchall()
    
    data = {}
    data_list = enumerate(res1)

    for product in data_list: 
        data[f'{product[0]}']={
        'id': product[1].id,
        'name': product[1].name,
        'description': product[1].description,
        'category_id': product[1].category_id,
        'sector_id': product[1].sector_id,
        'updated_at': product[1].updated_at,
        'image_url': product[1].image_url,
        'seedling_id': product[1].seedling_id,
        'strain_id': product[1].strain_id,
        'plant_facility_id': product[1].plant_facility_id,
        'price': product[1].price
        }
    return jsonify(data)

##############################
#--------2A. Sectors---------#
##############################

@api.route('/api/sectors', methods=["GET"]) 
def list_sectors():

    sectors = Sector.query.all()
    data = {}
    data_list = enumerate(sectors)

    for sector in data_list: 
        data[sector[0]+1]={
            'id': sector[1].id,
            'name': sector[1].name
        }

    return jsonify(data)
    
@api.route('/api/sectors', methods=["POST"]) 
def create_sector():
    '''Create a new sector via POST request. Must provide params below.'''

    new_product = Product(name=request.json["name"]
                            )
    db.session.add(new_product)
    db.session.commit()

    data = {}
    data[f'{new_product.name}']={
        'id': new_product.id,
        'name': new_product.name
        
    }
    

    return jsonify((data), 201)   


@api.route('/api/sectors/<int:id>', methods=["GET"])
def get_sector(id):
    '''Get data for specific sector, supply ID in header'''    
    sector = Sector.query.get_or_404(id)
    data = {}
    
    data[f'{sector.name}']={
        'id': sector.id,
        'name': sector.name
        
    }


    return jsonify(data)

@api.route('/api/sectors/<int:id>', methods=["PATCH"]) 
def update_sector(id):
    '''Update a specific sector via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the sector.'''

    sector = Sector.query.get_or_404(id)
 
    sector.name = request.json.get('name', sector.name)

    db.session.commit()

    data = {}
    
    data[f'{sector.name}']={
        'id': sector.id,
        'name': sector.name
    }


    return jsonify(data)  


@api.route('/api/sectors/<int:id>', methods=["DELETE"]) 
def delete_sector(id):
    '''Delete a specific sector. Specify via ID in header'''
    sector = Sector.query.get_or_404(id)
    db.session.delete(sector)
    db.session.commit()
    return jsonify(message="deleted")


##############################
#------3A. Categories--------#
##############################

@api.route('/api/categories', methods=["GET"]) 
def list_categories():
    '''List all categories'''
    categories = Category.query.all()
    data = {}
    data_list = enumerate(categories)

    for category in data_list: 
        data[category[0]+1]={
            'id': category[1].id,
            'name': category[1].name
        }

    return jsonify(data)
    
@api.route('/api/categories', methods=["POST"]) 
def create_category():
    '''Create a new category via POST request. Must provide params below.'''

    new_category = Category(name=request.json["name"]
                            )
    db.session.add(new_category)
    db.session.commit()

    data = {}
    data[f'{new_category.name}']={
        'id': new_category.id,
        'name': new_category.name
        
    }
    

    return jsonify((data), 201)   
  

@api.route('/api/categories/<int:id>', methods=["GET"])
def get_category(id):
    '''Get data for specific category, supply ID in header'''    
    category = Category.query.get_or_404(id)
    data = {}
    
    data[f'{category.name}']={
        'id': category.id,
        'name': category.name
        
    }


    return jsonify(data)

@api.route('/api/categories/<int:id>', methods=["PATCH"]) 
def update_category(id):
    '''Update a specific category via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the category.'''

    category = Category.query.get_or_404(id)
 
    category.name = request.json.get('name', category.name)

    db.session.commit()

    data = {}
    
    data[f'{category.name}']={
        'id': category.id,
        'name': category.name
    }


    return jsonify(data)  


@api.route('/api/categories/<int:id>', methods=["DELETE"]) 
def delete_category(id):
    '''Delete a specific category. Specify via ID in header'''
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify(message="deleted")


##############################
#--------4A. Strains---------#
##############################

@api.route('/api/strains', methods=["GET"]) 
def list_strains():
    '''List all strains'''
    strains = Strain.query.all()
    data = {}
    data_list = enumerate(strains)

    for strain in data_list: 
        data[strain[0]+1]={
            'id': strain[1].id,
            'name': strain[1].name
        }

    return jsonify(data)
    
@api.route('/api/strains', methods=["POST"]) 
def create_strain():
    '''Create a new strain via POST request. Must provide params below.'''

    new_strain = Strain(name=request.json["name"]
                            )
    db.session.add(new_strain)
    db.session.commit()

    data = {}
    data[f'{new_strain.name}']={
        'id': new_strain.id,
        'name': new_strain.name
        
    }
    

    return jsonify((data), 201)   
  

@api.route('/api/strains/<int:id>', methods=["GET"])
def get_strain(id):
    '''Get data for specific strain, supply ID in header'''    
    strain = Strain.query.get_or_404(id)
    data = {}
    
    data[f'{strain.name}']={
        'id': strain.id,
        'name': strain.name
        
    }


    return jsonify(data)

@api.route('/api/strains/<int:id>', methods=["PATCH"]) 
def update_strain(id):
    '''Update a strain category via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the strain.'''

    strain = Strain.query.get_or_404(id)
 
    strain.name = request.json.get('name', strain.name)

    db.session.commit()

    data = {}
    
    data[f'{strain.name}']={
        'id': strain.id,
        'name': strain.name
    }


    return jsonify(data)  


@api.route('/api/strains/<int:id>', methods=["DELETE"]) 
def delete_strain(id):
    '''Delete a specific strain. Specify via ID in header'''
    strain = Strain.query.get_or_404(id)
    db.session.delete(strain)
    db.session.commit()
    return jsonify(message="deleted")




##############################
#------5A. Facilities--------#
##############################

@api.route('/api/facilities', methods=["GET"]) 
def list_facilities():
    '''List all facilities'''
    facilities = Plant_facility.query.all()
    data = {}
    data_list = enumerate(facilities)

    for facility in data_list: 
        data[facility[0]+1]={
            'id': facility[1].id,
            'name': facility[1].name
        }

    return jsonify(data)
    
@api.route('/api/facilities', methods=["POST"]) 
def create_facility():
    '''Create a new facility via POST request. Must provide params below.'''

    new_facility = Plant_facility(name=request.json["name"]
                            )
    db.session.add(new_facility)
    db.session.commit()

    data = {}
    data[f'{new_facility.name}']={
        'id': new_facility.id,
        'name': new_facility.name
        
    }
    

    return jsonify((data), 201)   
  

@api.route('/api/facilities/<int:id>', methods=["GET"])
def get_facility(id):
    '''Get data for specific facility, supply ID in header'''    
    facility = Plant_facility.query.get_or_404(id)
    data = {}
    
    data[f'{facility.name}']={
        'id': facility.id,
        'name': facility.name
        
    }


    return jsonify(data)

@api.route('/api/facilities/<int:id>', methods=["PATCH"]) 
def update_facility(id):
    '''Update a specific facility via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the facility.'''

    facility = Plant_facility.query.get_or_404(id)
 
    facility.name = request.json.get('name', facility.name)

    db.session.commit()

    data = {}
    
    data[f'{facility.name}']={
        'id': facility.id,
        'name': facility.name
    }


    return jsonify(data)  


@api.route('/api/facilities/<int:id>', methods=["DELETE"]) 
def delete_facility(id):
    '''Delete a specific facility. Specify via ID in header'''
    facility = Plant_facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    return jsonify(message="deleted")



##############################
#-------6A. Seedlings--------#
##############################

@api.route('/api/seedlings', methods=["GET"]) 
def list_seedlings():
    '''List all seedlings'''
    seedlings = Seedling.query.all()
    data = {}
    data_list = enumerate(seedlings)

    for seedling in data_list: 
        data[seedling[0]+1]={
            'id': seedling[1].id,
            'name': seedling[1].name
        }

    return jsonify(data)
    
@api.route('/api/seedlings', methods=["POST"]) 
def create_seedling():
    '''Create a new seedling via POST request. Must provide params below.'''

    new_seedling = Seedling(strain_id=request.json["strain_id"],
                            plant_facility_id=request.json["plant_facility_id"]
                            )
    db.session.add(new_seedling)
    db.session.commit()

    data = {}
    data[f'new seedling - id {new_seedling.id}']={
        'id': new_seedling.name,
        'strain_id': new_seedling.name,
        'plant_facility_id': new_seedling.name
        
    }
    

    return jsonify((data), 201)   
  

@api.route('/api/seedlings/<int:id>', methods=["GET"])
def get_seedling(id):
    '''Get data for specific seedling, supply ID in header'''    
    seedling = Seedling.query.get_or_404(id)
    data = {}
    
    data[f'seedling - id {seedling.id}']={
        'id': seedling.id,
        'strain_id': seedling.strain_id,
        'plant_facility_id': seedling.plant_facility_id
        
    }


    return jsonify(data)

@api.route('/api/seedlings/<int:id>', methods=["PATCH"]) 
def update_seedling(id):
    '''Update a specific seedling via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the facility.'''

    seedling = Seedling.query.get_or_404(id)
 
    seedling.plant_facility_id = request.json.get('plant_facility_id', seedling.plant_facility_id)
    seedling.strain_id = request.json.get('strain_id', seedling.strain_id)

    db.session.commit()

    data = {}
    
    data[f'seedling - id {seedling.id}']={
        'id': seedling.id,
        'plant_facility_id': seedling.plant_facility_id,
        'strain_id': seedling.strain_id
    }


    return jsonify(data)  


@api.route('/api/seedlings/<int:id>', methods=["DELETE"]) 
def delete_seedling(id):
    '''Delete a specific seedling. Specify via ID in header'''
    seedling = Seedling.get_or_404(id)
    db.session.delete(seedling)
    db.session.commit()
    return jsonify(message="deleted")


##################################
#---B--ACCOUNTING API SECTION----#
##################################

#1B. Accounts
#2B. Double Entries
#3B. Credit Transations
#4B. Debit Transactions
#5B. Journal Entries
#6B. Invoices
#7B. Bills
#(vendors and customers are not queryable via public api for privacy)

##################################
#                                #
##################################


##############################
#-------1B. Accounts---------#
##############################


###################  WHILE THIS FUNCTIONALITY IS INCLUDED IN THE APP -- ADDING OR DELETING ACCOUNTS WILL AFFECT THE ACCOUNTING EQUATION AND THUS THE FINANCIAL RECORDS FOR THE COMPANY. DO NOT MODIFY. ###############

@api.route('/api/accounts', methods=["GET"]) 
def list_accounts():
    '''List all accounts'''
    accounts = Account.query.all()
    data = {}
    data_list = enumerate(accounts)

    for account in data_list: 
        data[account[0]+1]={
            'id': account[1].id,
            'name': account[1].name,
            'number': account[1].number,
            'normal': account[1].normal,
        }

    return jsonify(data)
    
@api.route('/api/accounts', methods=["POST"]) 
def create_account():
    '''Create a new account via POST request. Must provide params below. NORMAL param refers to the normal balance of the account. Normal credit balance = -1, Normal debit balance =1.'''
    
    new_account = Account(name=request.json["name"],
                          number=request.json["number"],
                          normal=request.json["normal"]
                            )
    db.session.add(new_account)
    db.session.commit()

    data = {}
    data[f'{new_account.name}']={
        'id': new_account.id,
        'name': new_account.name,
        'number': new_account.number,
        'normal': new_account.normal,
        
    }
    

    return jsonify((data), 201)   
  

@api.route('/api/accounts/<int:id>', methods=["GET"])
def get_account(id):
    '''Get data for specific account, supply ID in header'''    
    account = Account.query.get_or_404(id)
    data = {}
    
    data[f'{account.name}']={
        'id': account.id,
        'name': account.name,
        'number': account.number,
        'normal': account.normal,
        
    }

    return jsonify(data)


#THIS ROUTE IS COMMENTED OUT. DEVELOPER ACCESS ONLY. SHOULD NOT NEED TO MODIFY ACCOUNTS. 

#@api.route('/api/accounts/<int:id>', methods=["PATCH"]) 
#def update_account(id):
#    '''Update a specific account via PATCH request. Can provide one or more params to update - filling missing values w/ whats already in the db for the account.'''

#    account = Account.query.get_or_404(id)
 
#    account.name = request.json.get('name', account.name)
#    account.number = request.json.get('number', account.number)
#    account.normal = request.json.get('normal', account.normal)
    

#    db.session.commit()

#    data = {}
    
#    data[f'{account.name}']={
#        'id': account.id,
#        'name': account.name,
#        'number': account.number,
#        'normal': account.normal,
#    }


#    return jsonify(data)  


@api.route('/api/accounts/<int:id>', methods=["DELETE"]) 
def delete_account(id):
    '''Delete a specific account. Specify via ID in header'''
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify(message="deleted")



####################################
#-------2B. Double Entries---------#
####################################

# I did not include method to create double_entry within the public API - because double entries are only generated when db and cr transactions are processed concurrently within the application. 
## Double entries are then automatically generated, as with the associated journal entry.
### Can only list all double entries, or specific entries.

@api.route('/api/double_entries', methods=["GET"]) 
def list_double_entries():
    '''List all double_entries'''
    double_entries = Double_Entry.query.all()
    data = {}
    data_list = enumerate(double_entries)

    for entry in data_list: 
        data[entry[0]+1]={
            'db_id': entry[1].db_id,
            'cr_id': entry[1].cr_id,
            'jr_id': entry[1].jr_id
        }

    return jsonify(data)
    
  

@api.route('/api/double_entries/<int:id>', methods=["GET"])
def get_double_entry(id):
    '''Get data for specific double_entries, supply ID in header'''    
    double_entry = Double_Entry.query.get_or_404(id)
    data = {}
    
    data[f'Entry ID - {double_entry.id}']={
        'id': double_entry.id,
        'db_id': double_entry.db_id,
        'cr_id': double_entry.cr_id,
        'jr_id': double_entry.jr_id
        
    }


    return jsonify(data)

####################################
#-------3B. Credit Entries---------#
####################################



# I did not include method to create TransactionCR (credit entry)  within the public API - because TransactionCR entries are only generated when transaction events are recorded within the application. 
## TransactionCR are then automatically generated, as with the associated TransactionDB, and eventually double_entry.
### Can only list all TransactionCR entries, or specific TransactionCR entry.



@api.route('/api/credit_entries', methods=["GET"]) 
def list_credit_entries():
    '''List all credit_entries'''
    credit_entries = TransactionCR.query.all()
    data = {}
    data_list = enumerate(credit_entries)

    for entry in data_list: 
        data[entry[0]+1]={
            'id': entry[1].id,
            'date': entry[1].date,
            'amount': entry[1].amount,
            'account_number': entry[1].account_number,
            'direction': entry[1].direction
        }

    return jsonify(data)
    
  

@api.route('/api/credit_entries/<int:id>', methods=["GET"])
def get_credit_entry(id):
    '''Get data for specific credit_entry, supply ID in header'''    
    credit_entry = TransactionCR.query.filter_by(id=id)
    credit_entry = credit_entry[0]
    data = {}
    
    data[f'Entry ID - {credit_entry.id} - {credit_entry.date}']={
        'id': credit_entry.id,
        'date': credit_entry.date,
        'amount': credit_entry.amount,
        'account_number': credit_entry.account_number,
        'direction': credit_entry.direction
        
    }


    return jsonify(data)


####################################
#-------4B. Debit Entries---------#
####################################



# I did not include method to create TransactionDB (debit entry)  within the public API - because TransactionDB entries are only generated when transaction events are recorded within the application. 
## TransactionDB are then automatically generated, as with the associated TransactionCR, and eventually double_entry.
### Can only list all TransactionDB entries, or specific TransactionDB entry.



@api.route('/api/debit_entries', methods=["GET"]) 
def list_debit_entries():
    '''List all debit_entries'''
    debit_entries = TransactionDB.query.all()
    data = {}
    data_list = enumerate(debit_entries)

    for entry in data_list: 
        data[entry[0]+1]={
            'id': entry[1].id,
            'date': entry[1].date,
            'amount': entry[1].amount,
            'account_number': entry[1].account_number,
            'direction': entry[1].direction
        }

    return jsonify(data)
    
  

@api.route('/api/debit_entries/<int:id>', methods=["GET"])
def get_debit_entry(id):
    '''Get data for specific debit_entry, supply ID in header'''    
    debit_entry = TransactionDB.query.filter_by(id=id)
    debit_entry = debit_entry[0]
    data = {}
    
    data[f'Entry ID - {debit_entry.id} - {debit_entry.date}']={
        'id': debit_entry.id,
        'date': debit_entry.date,
        'amount': debit_entry.amount,
        'account_number': debit_entry.account_number,
        'direction': debit_entry.direction
        
    }


    return jsonify(data)




####################################
#-------5B. Journal Entries--------#
####################################



# I did not include method to create journal entries  within the public API - because journal entries are only generated when double_entry events are recorded within the application. 
## Journal entries are then automatically generated, as with the associated Invoice.
### Can only list all Journal entries, or specific journal entry.



@api.route('/api/journal_entries', methods=["GET"]) 
def list_journal_entries():
    '''List all journal_entries'''
    journal_entries = Journal_Entry.query.all()
    data = {}
    data_list = enumerate(journal_entries)

    for entry in data_list: 
        data[entry[0]+1]={
            'id': entry[1].id,
            'description': entry[1].description,
            'journalized_date': entry[1].journalized_date
            
        }

    return jsonify(data)
    
  

@api.route('/api/journal_entries/<int:id>', methods=["GET"])
def get_journal_entries(id):
    '''Get data for specific journal_entries, supply ID in header'''    
    journal_entry = Journal_Entry.query.get_or_404(id)
    data = {}
    
    data[f'Entry ID - {journal_entry.id} - {journal_entry.journalized_date}']={
        'id': journal_entry.id,
        'description': journal_entry.description,
        'journalized_date': journal_entry.journalized_date
        
    }


    return jsonify(data)



####################################
#-----------6B. Invoices-----------#
####################################



# I did not include method to create invoices within the public API - because invoices are only generated when sales events are recorded within the application. 
## Invoices are then automatically generated, based upon the associated cart/basket ID.
### Can only list all invoices, or specific invoices. Deleting can be achieved only as admin and logged into the app.


@api.route('/api/invoices', methods=["GET"]) 
def list_invoices():
    '''List all invoices'''
    invoices = Invoice.query.all()
    data = {}
    data_list = enumerate(invoices)

    for invoice in data_list: 
        data[invoice[0]+1]={
            'id': invoice[1].id,
            'customer_id': invoice[1].customer_id,
            'date_billed': invoice[1].date_billed,
            'amount': invoice[1].amount
            
            
        }

    return jsonify(data)
    
  

@api.route('/api/invoices/<int:id>', methods=["GET"])
def get_invoice(id):
    '''Get data for specific invoice, supply ID in header'''    
    invoice = Invoice.query.get_or_404(id)
    data = {}
    
    data[f'invoice ID - {invoice.id} - {invoice.date_billed}']={
        'id': invoice.id,
        'customer_id': invoice.customer_id,
        'date_billed': invoice.date_billed,
        'amount': invoice.amount
        
    }


    return jsonify(data)




####################################
#-----------7B. Bills-----------#
####################################



# I did not include method to create bills within the public API - because bills are only generated when billing events are recorded within the application. 
## Bills are then automatically generated, based upon the associated vendor ID.
### Can only list all bills, or specific bills. Deleting can be achieved only as admin and logged into the app.


@api.route('/api/bills', methods=["GET"]) 
def list_bills():
    '''List all bills'''
    bills = Bill.query.all()
    data = {}
    data_list = enumerate(bills)

    for bill in data_list: 
        data[bill[0]+1]={
            'id': bill[1].id,
            'vendor_id': bill[1].vendor_id,
            'date_logged': bill[1].date_logged,
            'date_billed': bill[1].date_billed,
            'amount': bill[1].amount
            
            
        }

    return jsonify(data)
    
  

@api.route('/api/bills/<int:id>', methods=["GET"])
def get_bill(id):
    '''Get data for specific bill, supply ID in header'''    
    bill = Bill.query.get_or_404(id)
    data = {}
    
    data[f'Bill ID - {bill.id} - {bill.date_billed}']={
        'id': bill.id,
        'vendor_id': bill.vendor_id,
        'date_logged': bill.date_logged,
        'date_billed': bill.date_billed,
        'amount': bill.amount
        
    }


    return jsonify(data)




##################################
#--C---ECOMMERCE API SECTION-----#
##################################

#1C. Sales by product (Sales)
#2C. Sales by cart (Baskets)

##################################
#                                #
##################################

#only GET requests - sales are generated via purchase within app


####################################
#------1C. Sales by product--------#
####################################


@api.route('/api/sales', methods=["GET"]) 
def list_sales():
    '''List all sales '''
    sales = Sale.query.all()
    data = {}
    data_list = enumerate(sales)

    for sale in data_list: 
        data[sale[0]+1]={
            'id': sale[1].id,
            'product_id': sale[1].product_id,
            'basket_id': sale[1].basket_id,
            'customer_id': sale[1].customer_id,
            'discount': sale[1].discount
            
            
        }

    return jsonify(data)
    
  

@api.route('/api/sales/<int:id>', methods=["GET"])
def get_sale(id):
    '''Get data for specific sale, supply ID in header'''    
    sale = Sale.query.filter_by(id=id)
    sale = sale[0]
    data = {}
    
    data[f'Sale ID - {sale.id}']={
        'id': sale.id,
        'product_id': sale.product_id,
        'basket_id': sale.basket_id,
        'customer_id': sale.customer_id,
        'discount': sale.discount
        
    }


    return jsonify(data)




####################################
#---2C. Baskets (Shopping Carts)---#
####################################


@api.route('/api/carts', methods=["GET"]) 
def list_carts():
    '''List all carts '''
    baskets = Basket.query.all()
    data = {}
    data_list = enumerate(baskets)

    for basket in data_list: 
        data[basket[0]+1]={
            'id': basket[1].id,
            'customer_id': basket[1].customer_id,
            'amount': basket[1].amount,
            'submitted_at': basket[1].submitted_at
            
        }

    return jsonify(data)
    
  

@api.route('/api/carts/<int:id>', methods=["GET"])
def get_cart(id):
    '''Get data for specific cart, supply ID in header'''    
    basket = Basket.query.filter_by(id=id)
    basket = basket[0]
    data = {}
    
    data[f'Cart ID - {basket.id}']={
        'id': basket.id,
        'customer_id': basket.customer_id,
        'amount': basket.amount,
        'submitted_at': basket.submitted_at
        
    }


    return jsonify(data)








#Dynamic Routes#


@api.route('/api/products/random/<int:num_items>', methods=["GET"])
def get_random_products(num_items):
    '''Get random list of products, number of items provided in header'''
    products = Product.query.all()
    res = []
    for x in range(num_items):
        prod = choice(products)
        res.append(prod)
    res = list(set(res))
    while len(res) < num_items:
        prod2=choice(products)
        res.append(prod2)
        res = list(set(res))

    data = {}
    data_list = enumerate(res)

    for product in data_list: 
        data[product[0]]={
                'id': product[1].id,
                'name': product[1].name,
                'description': product[1].description,
                'category_id': product[1].category_id,
                'sector_id': product[1].sector_id,
                'updated_at': product[1].updated_at,
                'image_url': product[1].image_url,
                'seedling_id': product[1].seedling_id,
                'strain_id': product[1].strain_id,
                'plant_facility_id': product[1].plant_facility_id,
                'price': product[1].price
            }


    return jsonify(data)


#Dynamic Data Generation Dashboard API Routes


@api.route('/api/dashboard_data')
def get_dashboard_home_data():

    #DATA FOR REVENUE VS EXPENSES VS PROJECTIONS GRAPH
    this_month=get_past_date(80).strftime('%m-%d-%y')
    last_month=get_past_date(110).strftime('%m-%d-%y')
    two_months_ago=get_past_date(140).strftime('%m-%d-%y')
    three_months_ago=get_past_date(170).strftime('%m-%d-%y')

    query = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300) AND (date <= :this_month) AND (date > :last_month)")
    res1 = db.session.execute(query, {"this_month": this_month, "last_month": last_month}).fetchall()
    query1 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300) AND (date <= :last_month) AND (date > :two_months_ago)")
    res2 = db.session.execute(query1, {"two_months_ago": two_months_ago, "last_month": last_month}).fetchall()
    query2 = text("SELECT SUM(ALL amount) FROM transactions_cr WHERE (account_number=300)  AND (date <= :two_months_ago) AND (date > :three_months_ago)")
    res3 = db.session.execute(query2, {"two_months_ago": two_months_ago, "three_months_ago": three_months_ago}).fetchall()
    real_revenue=[]
    real_revenue.append(res1)
    real_revenue.append(res2)
    real_revenue.append(res3)
    data = {}
    data_list = enumerate(real_revenue)
    for rev in data_list: 
        data[f'{rev[0]}']={
            'monthly_revenue': f"{rev[1][0][0]}"
        }
    #DATA FOR TOP SELLING TABLE
    #popular_products = get_product_sale_data()
    #for product in popular_products:
    #    data[f'TOP SELLING - {product.name}']={
    #        'id': product.id,
    #        'name': product.name,
    #        'description': product.description,
    #        'category_id': product.category_id,
    #        'sector_id': product.sector_id,
    #        'updated_at': product.updated_at,
    #        'image_url': product.image_url,
    #        'seedling_id': product.seedling_id,
    #        'strain_id': product.strain_id,
    #        'plant_facility_id': product.plant_facility_id,
    #        'price': product.price,
    #        'revenue_all_time': len(product.baskets)*product.price
    #    }


    #DATA FOR RECENT SALES TABLE
    #data generation for recent sales - enter number of days in the past you want data to be generated for.

    #recent_sales = get_timedelta(100)
   
    #for sale in recent_sales:
    #    for product in sale.products:
    #        data[f' RECENT SALES - {product.name}']={
    #        'id': product.id,
    #        'name': product.name,
    #        'description': product.description,
    #        'category_id': product.category_id,
    #        'sector_id': product.sector_id,
    #        'updated_at': product.updated_at,
    #        'image_url': product.image_url,
    #        'seedling_id': product.seedling_id,
    #        'strain_id': product.strain_id,
    #        'plant_facility_id': product.plant_facility_id,
    #        'price': product.price,
            
    #    }
    return jsonify(data)
    
@api.route('/api/join')
def join_info():
    
    query = text("SELECT Customers.first_name, Customers.last_name, Invoices.id FROM Customers FULL OUTER JOIN Invoices ON Customers.user_id=Invoices.customer_id ORDER BY Customers.first_name")
    res1 = db.session.execute(query).fetchall()
    result=[]
    result.append(res1)
    data_list = enumerate(result)
    now = datetime.datetime.now().strftime('%m-%d-%y')
    
@api.route('/api/sales_delta/<int:days>')
def join_info_dales_time_delta(days):
    '''Homepage data gen. Can dynamically alter this value to request product/sale data for past "days" days.'''
    since_date=get_past_date(days).strftime('%m-%d-%y')
    
    query = text("SELECT Products.name, Baskets.id, Baskets.submitted_at, Sales.discount, Customers.first_name, Customers.last_name, Sales.product_id, Products.price FROM Sales FULL OUTER JOIN Customers ON Sales.customer_id=Customers.user_id FULL OUTER JOIN Products ON Sales.product_id=Products.id FULL OUTER JOIN Baskets ON Sales.basket_id=Baskets.id WHERE Baskets.submitted_at >= :since_date ORDER BY Baskets.submitted_at DESC")
    res1 = db.session.execute(query, {"since_date" : since_date}).fetchall()
    result=[]
    result.append(res1)
    data_list = enumerate(res1)
    now = datetime.datetime.now().strftime('%m-%d-%y') 

    #query2 = text("DELETE * FROM transactions_cr WHERE (account_number=300) AND (date <= :now) AND (date > :since_april)")
    #res2 = db.session.execute(query2, {"now": now, "since_april": since_april}).fetchall()
    
    data = {}
    for row in data_list:
        data[f'{row[0]} : Invoice ID - {row[1][1]}']={
            f'Product Name': row[1][0],
            f'Cart': row[1][1],
            f'Date': row[1][2],
            f'Discount?': row[1][3],
            f'Customer': f'{row[1][4]} {row[1][5]}',
            f'Product ID': row[1][6],
            f'Price': row[1][7]
            
        }


    return jsonify(data)



@api.route('/api/top_sales/<int:num_products>')
def join_info_top_sales(num_products):
    '''default num_products is 10 on homepage. Can dynamically alter this value to request top "num_products" selling products'''
    
    query = text("SELECT Sales.product_id, Products.name, Products.price, COUNT(Sales.product_id) FROM Sales FULL OUTER JOIN Products ON Products.id=Sales.product_id GROUP BY Sales.product_id, Products.name, Products.price ORDER BY COUNT DESC LIMIT :num_products")
    res1 = db.session.execute(query, {"num_products" : num_products}).fetchall()
    result=[]
    result.append(res1)
    data_list = enumerate(res1)
    now = datetime.datetime.now().strftime('%m-%d-%y') 

    data = {}
    #for row in res1:
    #    data[f'{row[0]}{row[1]}']={
    #        f'Product Name': row[1],            
    #        f'Product ID': row[0],
    #        f'Price': row[2],
    #        'Total Sales': row[3]
            
    #    }
    for row in data_list:
        data[f'{row[0]} : {row[1][1]}']={
            f'Product Name': row[1][1],            
            f'Product ID': row[1][0],
            f'Price': row[1][2],
            'Total Sales': row[1][3]
            
        }


    return jsonify(data)

@api.route('/api/testing_join')
def join_info_sales():
    
    query = text("SELECT Customers.first_name, Customers.last_name, Products.name, Sales.basket_id, Baskets.submitted_at, Baskets.amount FROM Customers FULL OUTER JOIN Sales ON Customers.user_id=Sales.customer_id FULL OUTER JOIN products ON Sales.product_id=Products.id FULL OUTER JOIN baskets ON Sales.basket_id=Baskets.id ORDER BY Baskets.submitted_at DESC")
    res1 = db.session.execute(query).fetchall()
    #result=[]
    #result.append(res1)
    #data_list = enumerate(result)
    
    
    
    data = {}
    for count, row in enumerate(res1):
        data[count]={
            f'first_name': row[0],
            f'last_name': row[1],
            f'product': row[2],
            f'invoice_id': row[3],
            f'submitted_at': row[4],
            f'amount': row[5]
            
        }
 
    return jsonify(data)

@api.route('/api/sales/<int:days_ago>')
def join_info_all_sales(days_ago):
    date=get_past_date(days_ago).strftime('%m-%d-%y')
    query = text("SELECT Sales.basket_id, Sales.product_id, Baskets.submitted_at, Baskets.amount FROM Sales FULL OUTER JOIN Baskets ON Sales.basket_id=Baskets.id WHERE Baskets.submitted_at > :date ORDER BY Baskets.submitted_at DESC")
    res1 = db.session.execute(query, {"date": date} ).fetchall()
    #result=[]
    #result.append(res1)
    #data_list = enumerate(result)
    

    
    data = {}
    for count, row in enumerate(res1):
        data[count]={
            f'BASKET ID': row[0],
            f'PRODUCT ID': row[1],
            f'DATE': row[2],
            f'AMOUNT OF CART': row[3]
            
        }
 
    return jsonify(data)




#Example Cupcake API Routes for developer reference

@api.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    
    if request.json["image"]:
        new_cupcake = Cupcake(flavor=request.json["flavor"],
                              size=request.json["size"],
                              rating=request.json["rating"],
                              image=request.json["image"])
        db.session.add(new_cupcake)
        db.session.commit()
        print(request.json)
    
        return (jsonify(cupcake=new_cupcake.serialize()), 201)
    else:
        new_cupcake = Cupcake(flavor=request.json["flavor"],
                              size=request.json["size"],
                              rating=request.json["rating"]
                              )
        db.session.add(new_cupcake)
        db.session.commit()
        print(request.json)


@api.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    
    #db.session.query(Cupcake).filter_by(id=id).update(request.json) solution in one line to update from user. dont have to update things line by line.
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)

    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

    #you can type one things or all things, and itll update, filling missing values w/ whats already there.


@api.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
    
