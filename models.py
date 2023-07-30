"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()
import datetime


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)    
    name = db.Column(db.Text, 
                      nullable=False)
    number = db.Column(db.Integer, 
                      nullable=False,
                      unique=True)
    normal = db.Column(db.Integer, 
                      nullable=False)
    transactions_db = db.relationship(
        'TransactionDB',
        lazy=True,
        cascade="all,delete",
        backref="accounts",
    )
    transactions_cr = db.relationship(
        'TransactionCR',
        lazy=True,
        cascade="all,delete",
        backref="accounts",
    )

    
class TransactionDB(db.Model):
    __tablename__ = "transactions_db"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)    
    date = db.Column(db.DateTime,
                           nullable=False,
                           unique=False,
                           default=datetime.datetime.now)
    amount = db.Column(db.Integer, 
                      nullable=False)
    account_number = db.Column(db.Integer, 
                    db.ForeignKey('accounts.number', ondelete="cascade"), 
                    primary_key=True)
    direction = db.Column(db.Integer, 
                      nullable=False)   


#class Debit_Entry(db.Model):
#    __tablename__ = "debit_entries"

#    account_number = db.Column(db.Integer, 
#                        db.ForeignKey('accounts.number', ondelete="cascade"), 
#                        primary_key=True)
#    transactionDB_id = db.Column(db.Integer, 
#                       db.ForeignKey('transactions_db.id', ondelete="cascade"), 
#                       primary_key=True)



class TransactionCR(db.Model):
    __tablename__ = "transactions_cr"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)    
    date = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    amount = db.Column(db.Integer, 
                      nullable=False)
    account_number = db.Column(db.Integer, 
                    db.ForeignKey('accounts.number', ondelete="cascade"), 
                    primary_key=True)
    direction = db.Column(db.Integer, 
                      nullable=False)
    transactions_db = db.relationship(
        'TransactionCR',
        secondary="double_entries",
        cascade="all,delete",
        backref="transactions_cr",
    )


    

#class Credit_Entry(db.Model):
#    __tablename__ = "credit_entries"

#    account_number = db.Column(db.Integer, 
#                        db.ForeignKey('accounts.number', ondelete="cascade"), 
#                        primary_key=True)
#    transactionCR_id = db.Column(db.Integer, 
#                       db.ForeignKey('transactions_cr.id', ondelete="cascade"), 
#                       primary_key=True)


class Double_Entry(db.Model):
    __tablename__ = "double_entries"

    
    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True)  
    
    db_id = db.Column(db.Integer, 
                        db.ForeignKey('transactions_db.id', ondelete="cascade"), 
                        primary_key=True)
    cr_id = db.Column(db.Integer, 
                       db.ForeignKey('transactions_cr.id', ondelete="cascade"), 
                       primary_key=True)
    jr_id = db.Column(db.Integer, 
                       db.ForeignKey('journal_entries.id', ondelete="cascade"), 
                       nullable=True)


class Journal_Entry(db.Model):
    __tablename__ = "journal_entries"

    
    id = db.Column(db.Integer,
            primary_key=True,
            autoincrement=True)    
    #delete me
    #double_entry_id = db.Column(db.Integer, 
    #                    db.ForeignKey('double_entries.id', ondelete="cascade", name='journal_entries_double_entry_id_fkey'), 
    #                    primary_key=True)
    
    description = db.Column(db.Text,
                         nullable=True)
    
    journalized_date = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    double_entries = db.relationship(
        'Double_Entry',
        #secondary="double_entries_catalogue",
        cascade="all,delete",
        lazy=True,
        backref="journal_entries",
    )



class Invoice(db.Model):
    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
    __tablename__ = "invoices"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique = True)

    customer_id = db.Column(db.Integer, 
                        db.ForeignKey('customers.user_id', ondelete="cascade"), 
                        primary_key=False)
    
    date_billed = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    payment_info = db.Column(db.Text, 
                        db.ForeignKey('customers.payment_info', ondelete="cascade"), 
                        primary_key=False)
    amount = db.Column(db.Integer,
                       nullable=False,
                       )


class Bill(db.Model):
    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
    __tablename__ = "bills"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    vendor_id = db.Column(db.Integer, 
                        db.ForeignKey('vendors.id', ondelete="cascade"), 
                        primary_key=False)
    date_logged = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    date_billed = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    amount = db.Column(db.Integer,
                       nullable=False,
                       )


class Basket(db.Model):
    __tablename__ = "baskets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    customer_id = db.Column(db.Integer, 
                    db.ForeignKey('customers.user_id', ondelete="cascade"), 
                    primary_key=True)
    amount = db.Column(db.Integer,
                    nullable=False,
                    )
    submitted_at = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)
    products = db.relationship(
        'Product',
        secondary="sales",
         cascade="all,delete",
        backref="baskets",
    )


    

class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)
    product_id = db.Column(db.Integer, 
                        db.ForeignKey('products.id', ondelete="cascade"), 
                        primary_key=True)
    basket_id = db.Column(db.Integer, 
                        db.ForeignKey('baskets.id', ondelete="cascade"), 
                        primary_key=True)
    customer_id = db.Column(db.Integer, 
                    db.ForeignKey('customers.user_id', ondelete="cascade"), 
                    primary_key=True)
    discount = db.Column(db.Integer,
                         nullable=True,
                         unique=False)


class Customer(db.Model):
    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
    __tablename__ = "customers"

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete="cascade"), 
                        primary_key=True,
                        unique=True)

    account_number = db.Column(db.Integer,
                   unique=True,
                   nullable=False
                   )
    payment_info = db.Column(db.Text,
                             nullable=True,
                             unique=True)    
    address = db.Column(db.String(200),
                         nullable=True,
                         unique=False)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    last_name = db.Column(db.String(50),
                        nullable=False,
                        unique=False)
    phone = db.Column(db.Text, nullable=True)


class Vendor(db.Model):
    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
    __tablename__ = "vendors"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    name = db.Column(db.String(50),
                         nullable=False,
                         unique=True)
    address = db.Column(db.String(200),
                         nullable=True,
                         unique=False)




#class User(db.Model):
#    """user model for blogly. Include: id PK, first_name, last_name, image_url"""
#    __tablename__ = "users"

#    id = db.Column(db.Integer,
#                   primary_key=True,
#                   autoincrement=True,
#                   unique=True)

#    username = db.Column(db.String(20),
#                         nullable=False,
#                         unique=True)

#    password = db.Column(db.Text,
#                         nullable=False)
#    #first_name = db.Column(db.String(50),
#    #                 nullable=False,
#    #                 unique=False)
#    #last_name = db.Column(db.String(50),
#    #                    nullable=False,
#    #                    unique=False)
#    email = db.Column(db.String(50),
#                         nullable=False)

#    image_url = db.Column(db.String(200),
#                          nullable=True,
#                          unique=False,
#                          default="https://w7.pngwing.com/pngs/205/731/png-transparent-default-avatar.png")
#    bio = db.Column(db.Text,
#                         nullable=True)
#    #address = db.Column(db.String(200),
#    #                     nullable=True,
#    #                     unique=False)
#        #start_Register

#    @classmethod
#    def register(cls, username, pwd, first_name, last_name, email):
#        '''register user w/ hashed password and return user'''

#        hashed = bcrypt.generate_password_hash(pwd)
#        #turn bytestring into normal (unicode utf8) string
#        hashed_utf8 = hashed.decode("utf8")

#        #return instance of user w/ username and hashed pwd
#        return cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

#    @classmethod
#    def authenticate(cls, username, pwd):
#        '''validate that user exists, and password is correct.

#        Return user if valid; else return False.'''

#        user = User.query.filter_by(username=username).first()

#        if user and bcrypt.check_password_hash(user.password, pwd):
#            return user
#        else: 
#            return False
    
class Product(db.Model):
    """POST model for blogly. Containing id as primary key, title, content, created_at, and user_id from USER model as FOREIGN KEY"""

    __tablename__ = "products"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    description = db.Column(db.String(500),
                     nullable=True,
                     unique=False)

    category_id = db.Column(db.Integer,
                        db.ForeignKey('categories.id', ondelete="cascade"),                        
                        nullable=True)
    sector_id = db.Column(db.Integer,
                        db.ForeignKey('sectors.id', ondelete="cascade"),                        
                        nullable=False)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    image_url = db.Column(db.String(200),
                          nullable=True,
                          unique=False,
                          default="https://99designs-blog.imgix.net/blog/wp-content/uploads/2018/11/attachment_78456430-e1541654366936.jpeg?auto=format&q=60&fit=max&w=930")
    seedling_id = db.Column(db.Integer,
                        db.ForeignKey('seedlings.id', ondelete="cascade"),
                        #FIGURE OUT HOW TO ADD CASCADE. ASK PUSHPITA. FOR NOW SET NULLABLE TO TRUE SO WE CAN RESET TABLE. Ok that doesnt work anyway. figure it out later.
                        nullable=True)
    strain_id = db.Column(db.Integer,
                        db.ForeignKey('strains.id', ondelete="cascade"),
                        #FIGURE OUT HOW TO ADD CASCADE. ASK PUSHPITA. FOR NOW SET NULLABLE TO TRUE SO WE CAN RESET TABLE. Ok that doesnt work anyway. figure it out later.
                        nullable=True)
    plant_facility_id = db.Column(db.Integer,
                        db.ForeignKey('plant_facilities.id', ondelete="cascade"),
                        #FIGURE OUT HOW TO ADD CASCADE. ASK PUSHPITA. FOR NOW SET NULLABLE TO TRUE SO WE CAN RESET TABLE. Ok that doesnt work anyway. figure it out later.
                        nullable=True)
    price = db.Column(db.Integer,
                      nullable=False)
    messages = db.relationship('Message')
    
    
    


class Plant_facility(db.Model):
    """plant facility"""

    __tablename__ = "plant_facilities"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    location = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    medical_cert = db.Column(db.Boolean,
                     nullable=False,
                     default=True)
    packaged_date = db.Column(db.DateTime,
                        nullable=False,
                        default=datetime.datetime.now)

class Seedling(db.Model):
    """seedling model - strain and facility included as PFK."""

    __tablename__ = "seedlings"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   unique=True)

    

    strain_id = db.Column(db.Integer, 
                       db.ForeignKey('strains.id'), 
                       primary_key=True)
    
    
    plant_facility_id = db.Column(db.Integer, 
                       db.ForeignKey('plant_facilities.id'), 
                       primary_key=True)

class Strain(db.Model):
    """Tag on a post."""

    __tablename__ = "strains"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True, 
                   unique=True)

    name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    category_id = db.Column(db.Integer, 
                       db.ForeignKey('categories.id'), 
                       primary_key=True)
    #effect_tag_id = db.Column(db.Integer, 
    #                   db.ForeignKey('effects_tags.id') 
    #                   )

class ProductTag(db.Model):
    """Tag on a product."""

    __tablename__ = "products_tags"

    product_id = db.Column(db.Integer, 
                        db.ForeignKey('products.id', ondelete="cascade"),
                        
                        primary_key=True,
                        )
    effect_tag_id = db.Column(db.Integer, 
                       db.ForeignKey('effects_tags.id', ondelete="cascade"), 
                       primary_key=True)

#class CategoryTag(db.Model):
#    """Tag on a category."""

#    __tablename__ = "categories_tags"

#    category_id = db.Column(db.Integer, 
#                        db.ForeignKey('categories.id', ondelete="cascade"), 
#                        primary_key=True
#                       )
#    effect_tag_id = db.Column(db.Integer, 
#                       db.ForeignKey('effects_tags.id', ondelete="cascade"), 
#                       primary_key=True)

#class ProductCategory(db.Model):
#    """TDELETE ME"""

#    __tablename__ = "products_categories"

#    product_id = db.Column(db.Integer, 
#                        db.ForeignKey('products.id', ondelete="cascade"), 
#                        primary_key=True)
#    category_id = db.Column(db.Integer, 
#                       db.ForeignKey('categories.id', ondelete="cascade"), 
#                       primary_key=True)

#class ProductSector(db.Model):
#    """TDELETE ME"""

#    __tablename__ = "products_sectors"

#    product_id = db.Column(db.Integer, 
#                        db.ForeignKey('products.id', ondelete="cascade"), 
#                        primary_key=True)
#    sector_id = db.Column(db.Integer, 
#                       db.ForeignKey('sectors.id', ondelete="cascade"), 
#                       primary_key=True)


class Effect_Tag(db.Model):
    """Tag to be added to products."""
    __tablename__ = "effects_tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    products = db.relationship(
        'Product',
        secondary="products_tags",
        # cascade="all,delete",
        backref="effects_tags",
    )





class Category(db.Model):
    """Tag to be added to products."""
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    products = db.relationship(
        'Product',
        lazy=True,
         cascade="all,delete",
        backref="categories",
    )

class Sector(db.Model):
    """Tag to be added to products."""
    __tablename__ = "sectors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    products = db.relationship(
        'Product',
        lazy=True,
         cascade="all,delete",
        backref="sectors",
    )

  

    
"""SQLAlchemy models for Warbler."""


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )


class Likes(db.Model):
    """Mapping user likes to chatters."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id', ondelete='cascade'),
        unique=False
    )

class Favorites(db.Model):
    """Mapping user favorites to products."""

    __tablename__ = 'favorites' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='cascade'),
        unique=False
    )

class Direct_Message(db.Model):
    """An individual direct message ("dm")."""

    __tablename__ = 'direct_messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    text = db.Column(
        db.String(600),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

class ProductRating(db.Model):
    """Rating on a product."""

    __tablename__ = "product_ratings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    product_id = db.Column(db.Integer, 
                        db.ForeignKey('products.id', ondelete="cascade"),
                        
                        primary_key=True,
                        )
    rating = db.Column(db.Integer, 
                       nullable=False,
                       unique=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete="cascade"),
                        primary_key=True)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    admin = db.Column(
        db.Boolean,
        nullable=True,
        unique=False,
        default=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default="/static/images/warbler-hero.jpg"
    )

    bio = db.Column(
        db.Text,
    )

    location = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    messages = db.relationship('Message')

    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    dms_sent = db.relationship(
        "Direct_Message",
        secondary="direct_messages",
        primaryjoin=(Direct_Message.sender_id == id),
        secondaryjoin=(Direct_Message.recipient_id == id)
    )

    dms_received = db.relationship(
        "Direct_Message",
        secondary="direct_messages",
        primaryjoin=(Direct_Message.recipient_id == id),
        secondaryjoin=(Direct_Message.sender_id == id)
    )

    likes = db.relationship(
        'Message',
        secondary="likes"
    )

    favorites = db.relationship(
        'Product',
        secondary="favorites"
    )

    ratings = db.relationship(
        'Product',
        secondary="product_ratings"
    )


    #def __repr__(self):
    #    return f"<User #{self.id}: {self.username}, {self.email}>"

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, pwd)
            if is_auth:
                return user

        return False


class Message(db.Model):
    """An individual message ("chatter")."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')


    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.id', ondelete='CASCADE'),
        nullable=True,
    )

    product = db.relationship('Product')




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
