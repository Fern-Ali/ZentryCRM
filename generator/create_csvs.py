"""Generate CSVs of random data for Warbler.

Students won't need to run this for the exercise; they will just use the CSV
files that this generates. You should only need to run this if you wanted to
tweak the CSV formats or generate fewer/more rows.
"""

import csv
import json
import random
from random import choice, randint, sample
from itertools import permutations
import requests
from faker import Faker
from helpers import get_random_datetime

MAX_WARBLER_LENGTH = 140

USERS_CSV_HEADERS = ['email', 'username', 'image_url', 'password', 'bio', 'header_image_url', 'location']
MESSAGES_CSV_HEADERS = ['text', 'timestamp', 'user_id']
FOLLOWS_CSV_HEADERS = ['user_being_followed_id', 'user_following_id']
CHART_OF_ACCOUNTS_CSV_HEADERS = ['name', 'number', 'normal']
PRODUCTS_CSV_HEADERS = ['name', 'description', 'category_id', 'sector_id', 'image_url', 'seedling_id', 'strain_id', 'plant_facility_id', 'price']
STRAINS_CSV_HEADERS = ['name', 'category_id']
CUSTOMERS_CSV_HEADERS = ['user_id', 'account_number', 'payment_info', 'address', 'first_name', 'last_name', 'phone']
BASKETS_CSV_HEADERS = ['customer_id', 'amount', 'submitted_at']
VENDORS_CSV_HEADERS = ['name', 'address']
BILLS_CSV_HEADERS = ['vendor_id', 'date_billed', 'amount']


NUM_USERS = 300
NUM_MESSAGES = 1000
NUM_FOLLWERS = 5000

fake = Faker()

# Generate random profile image URLs to use for users

image_urls = [
    f"https://randomuser.me/api/portraits/{kind}/{i}.jpg"
    for kind, count in [("lego", 10), ("men", 100), ("women", 100)]
    for i in range(count)
]


# Generate random header image URLs to use for users

#header_image_urls = [
#    requests.get(f"http://www.splashbase.co/api/v1/images/{i}").json()['url']
#    for i in range(1, 46)
#]

header_image_urls = ['https://images.unsplash.com/photo-1604651901258-822bd831b594?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2172&q=80',
                     'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80',
                     'https://images.unsplash.com/photo-1619426017013-0d6db7b74d1a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2071&q=80',
                     'https://images.unsplash.com/photo-1604651901125-8efdee8f2f7f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2171&q=80',
                     'https://images.unsplash.com/photo-1614034178871-d038bce3b763?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3884&q=80',
                     'https://images.unsplash.com/photo-1499728603263-13726abce5fd?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                     'https://images.unsplash.com/photo-1647871938169-646b37980440?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1931&q=80',
                     'https://images.unsplash.com/photo-1658010383393-ca6a19f1dea7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                     'https://images.unsplash.com/photo-1638809264876-63bf0a05f4c7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80',
                     'https://images.unsplash.com/photo-1637077866376-554630bea022?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80']

# Generate random flower image URLs to use for products

flower_images = [];
flower_sizes = ['Qtr', 'Half', 'Oz']

for i in range(2, 30):
    flower_images.append(f"https://images.leafly.com/flower-images/defaults/generic/strain-{i}.png?auto=compress,format&w=215&dpr=1")


# Generate strains to use for products

my_strains = ['Granddaddy Purple', 'Northern Lights',
'Papaya',
'Triangle Kush',
'Sunset',
'Zkittlez',
'Sour Diesel',
'Mango Haze',
'French Cookies',
'Guava Kush',
'Sunrise',
'Candyland',
'Biscotti',
'Gelonade',
'Sundae Delight',
'Banana Kush',
'Grapes & Cream',
'Jungle Cake']

indicas = ['Granddaddy Purple', 'Northern Lights',
'Papaya',
'Triangle Kush',
'Sunset',
'Zkittlez']

sativas = ['Sour Diesel',
'Mango Haze',
'French Cookies',
'Guava Kush',
'Sunrise',
'Candyland']

hybrids = ['Biscotti',
'Gelonade',
'Sundae Delight',
'Banana Kush',
'Grapes & Cream',
'Jungle Cake']


with open('strains1.csv', 'w') as strains1_csv:
        users_writer = csv.DictWriter(strains1_csv, fieldnames=STRAINS_CSV_HEADERS)
        users_writer.writeheader()
        for strain in my_strains:

            if my_strains.index(strain) <= 5:

                users_writer.writerow(dict(
                    name=strain,
                    category_id=1
                ))

            elif my_strains.index(strain) <= 11:

                users_writer.writerow(dict(
                    name=strain,
                    category_id=2         
                ))

            elif my_strains.index(strain) <= 17:

                users_writer.writerow(dict(
                    name=strain,
                    category_id=3          
                ))










#############################################################################################################################
# DYNAMIALLY GENERATE PRODUCTS.  #
#############################################################################################################################

gummy_pics = ['https://images.unsplash.com/photo-1626640791286-0fb9e407aab6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1579803988215-7a9ac7d5b988?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1626123552399-8cd6cc8bc36c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1579803987949-4cd894b2210c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2080&q=80',
               'https://images.unsplash.com/photo-1605125207928-0b878b4a6570?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
               'https://images.unsplash.com/photo-1605125208383-694750af8f5b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=765&q=80',
               'https://images.unsplash.com/photo-1670580387191-4d118359faae?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1605125207433-a67e404afc0f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=765&q=80',
               'https://images.unsplash.com/photo-1610740657130-a651af0642a3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1597093218359-06440f36cb6f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1523374311137-07f0aa18832b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=951&q=80',
               'https://images.unsplash.com/photo-1666595162656-5dda41328ba5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
               'https://images.unsplash.com/photo-1666595162324-df6f452108e7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
               'https://images.unsplash.com/photo-1666595162349-e1f596d2b112?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
               'https://images.unsplash.com/photo-1605188229547-20d40f18e35c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
               'https://images.unsplash.com/photo-1605125207615-333a7af27bfd?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=765&q=80',
               'https://images.unsplash.com/photo-1668440246393-e0b8b19a0bb7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
               'https://images.unsplash.com/photo-1605188613470-0e2e29ce1873?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=736&q=80']

cookie_pics = ['https://images.unsplash.com/photo-1551844547-043f512dc4d9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=730&q=80',
               'https://images.unsplash.com/photo-1600147566401-c2056eb69479?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1597895139322-0a1ef77b3c30?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1610562275255-03b7fa0d4655?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=766&q=80',
               'https://images.unsplash.com/photo-1577110633170-873dbc1bf2bc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80',
               'https://images.unsplash.com/photo-1597895139270-a5dee112224d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1611837837645-48d1bfdb093f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1615408393752-28d552ef9673?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1624204928490-3dea2d558f5c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1542310503-ff8da9c02372?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1558312657-b2dead03d494?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1570099573975-950375a9e431?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1580959402038-d46d12ca41cb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=688&q=80',
               'https://images.unsplash.com/photo-1579005213577-3d71eecd728d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
               'https://images.unsplash.com/photo-1606913084603-3e7702b01627?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1612713996532-81e2a10ac5d2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1575993051801-d5a7940d78a2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=736&q=80']

sweets_pics = ['https://images.unsplash.com/photo-1582293041079-7814c2f12063?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1541717872011-9d16b87a5551?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1521886655570-97530ff9454b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1611586360741-930bc2c731bc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1541718118468-cf7bcde0196f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1654648662300-82daeea37b8b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
               'https://images.unsplash.com/photo-1670220591949-930e033d40da?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1587899576587-766a2afea5c6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1516478379578-ea8bea43365f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1551106652-a5bcf4b29ab6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=765&q=80',
               'https://images.unsplash.com/photo-1514517521153-1be72277b32f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1585653621032-a5fec164ee92?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
               'https://images.unsplash.com/photo-1618411640018-972400a01458?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1578508053827-fe06d4dc2457?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1598533877603-1bb7bc9bc746?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
               'https://images.unsplash.com/photo-1612240498936-65f5101365d2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1586769412527-ab0855979b2e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
               'https://images.unsplash.com/photo-1525059337994-6f2a1311b4d4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=711&q=80',
               'https://images.unsplash.com/photo-1570727624862-3008fe67a6be?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80']
          
vapes_pics = ['https://images.unsplash.com/photo-1629169544250-f1d828754ced?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
              'https://images.unsplash.com/photo-1676914880962-0e7b40cf6743?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=980&q=80',
              'https://images.unsplash.com/photo-1613392083937-f68bcff3bf10?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80',
              'https://images.unsplash.com/photo-1635481753580-7c1defd2679f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1031&q=80',
              'https://images.unsplash.com/photo-1626246825787-64e6691107fc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
              'https://images.unsplash.com/photo-1599177749654-b8f5fe0b016a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1043&q=80',
              'https://images.unsplash.com/photo-1605117891722-c27b90f2a774?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
              'https://images.unsplash.com/photo-1605118883347-acb83475a3cb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1605118363618-757344cd6efb?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1616093052603-f8a8acf54f7c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1605117913123-1f455435b384?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1666402667102-a647c86ee4ee?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1616093052603-f8a8acf54f7c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1664904527347-f90ff2940fb6?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
              'https://images.unsplash.com/photo-1545095088-26a59e3f2717?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
              'https://images.unsplash.com/photo-1635347319127-6a064615dedf?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80',
              'https://images.unsplash.com/photo-1620788952956-5f88cd454325?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
              'https://images.unsplash.com/photo-1522741070277-b1b2ba3a7bd3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1579165466814-e646cfa4a3be?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1637303115143-68779e1b2f6b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80',
              'https://images.unsplash.com/photo-1594189736781-f75b5dbcd4c9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
              'https://images.unsplash.com/photo-1625125875922-dd44b1ec9b1f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=765&q=80',
              'https://images.unsplash.com/photo-1654259532997-e54bbe025800?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80',
              'https://images.unsplash.com/photo-1676914880282-bfc320b2e4f8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=760&q=80',
              'https://images.unsplash.com/photo-1676914879737-bd4d957393f2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=761&q=80',
              'https://images.unsplash.com/photo-1646926554474-771eb312f71b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
              'https://images.unsplash.com/photo-1676914880547-474b570c4646?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=791&q=80',
              'https://images.unsplash.com/photo-1646926555480-479d4c948a20?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
              'https://images.unsplash.com/photo-1599752597653-156992574668?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2060&q=80',
              'https://images.unsplash.com/photo-1648144107041-d532074940db?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80']

concentrates_pics = ['https://images.unsplash.com/photo-1636759174740-93fb9523f835?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                     'https://images.unsplash.com/photo-1556228578-8c89e6adf883?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                     'https://images.unsplash.com/photo-1598052163236-4ec4140c4c49?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                     'https://images.unsplash.com/photo-1598052162878-37283c569e5a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1130&q=80',
                     'https://images.unsplash.com/photo-1598052162874-e41952203254?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1188&q=80']

apparel_pics = ['https://images.unsplash.com/photo-1543163521-1bf539c55dd2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
                'https://images.unsplash.com/photo-1562157873-818bc0726f68?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=627&q=80',
                'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1072&q=80',
                'https://images.unsplash.com/photo-1620799139834-6b8f844fbe61?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1072&q=80',
                'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
                'https://images.unsplash.com/photo-1560769629-975ec94e6a86?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80',
                'https://images.unsplash.com/photo-1602810320073-1230c46d89d4?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1516762689617-e1cffcef479d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=711&q=80',
                'https://images.unsplash.com/photo-1601980265524-04468b355ac3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=675&q=80',
                'https://images.unsplash.com/photo-1584539696499-bff0b4768e4e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80',
                'https://images.unsplash.com/photo-1605518216938-7c31b7b14ad0?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1609&q=80',
                'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                'https://images.unsplash.com/photo-1618554776245-6b23d506c3e1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1592876569776-12718fae30f1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1026&q=80',
                'https://images.unsplash.com/photo-1608667508764-33cf0726b13a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
                'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1025&q=80',
                'https://images.unsplash.com/photo-1525507119028-ed4c629a60a3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80',
                'https://images.unsplash.com/photo-1565379793984-e65b51b33b37?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80',
                'https://images.unsplash.com/photo-1612215033154-0f12117b1de2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1591946600248-29d495003cac?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1601233216647-4fb22eb08425?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80',
                'https://images.unsplash.com/photo-1605812860427-4024433a70fd?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=735&q=80',
                'https://images.unsplash.com/photo-1617483535565-c255e235002b?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80',
                'https://images.unsplash.com/photo-1584609226397-de5612afdfea?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80',
                'https://images.unsplash.com/photo-1604163546180-039a1781c0d2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=764&q=80']


with open('products.csv', 'w') as products_csv:
    users_writer = csv.DictWriter(products_csv, fieldnames=PRODUCTS_CSV_HEADERS)
    users_writer.writeheader()

    sectors = ['Smokeables', 'Vapes', 'Concentrates', 'Edibles', 'Apparel',  'Merchandise', 'Hardware' ]

    
    for x in range(3):
        for i in range(5):
            users_writer.writerow(dict(
                name=f'Specialty Concentrates {fake.emoji()}',
                description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
                category_id=choice(range(1, 4)),
                sector_id=3,
                image_url=concentrates_pics[i],
                seedling_id=choice(range(1, 4)),
                strain_id=choice(range(1, 19)),
                plant_facility_id=choice(range(1, 4)),
                price=choice(range(15, 200))
            
                #header_image_url=choice(header_image_urls),
                #location=fake.city()
            ))

    
    for i in range(26):
        users_writer.writerow(dict(
            name=f'Blogly Apparel {fake.emoji()}',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=6,
            sector_id=5,
            image_url=apparel_pics[i],
            seedling_id=choice(range(1, 4)),
            strain_id=choice(range(1, 18)),
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))
    
    
    
    
    for strain in indicas:

        idx = indicas.index(strain)
        for i in range(3):
            users_writer.writerow(dict(
                name=f'{strain} {flower_sizes[i]}',
                description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
                category_id=1,
                sector_id=1,
                image_url=choice(flower_images),
                seedling_id=choice(range(1, 4)),
                strain_id=indicas.index(strain)+1,
                plant_facility_id=choice(range(1, 4)),
                price=choice(range(15, 200))
            
                #header_image_url=choice(header_image_urls),
                #location=fake.city()
            ))
        
        users_writer.writerow(dict(
            name=f'{strain} Gummies',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=1,
            sector_id=4,
            image_url=choice(gummy_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=indicas.index(strain)+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))

        users_writer.writerow(dict(
            name=f'{strain} Vaporizer',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=1,
            sector_id=2,
            image_url=choice(vapes_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=indicas.index(strain)+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))
        




    for strain in sativas:
    
        idx = sativas.index(strain)
        
        users_writer.writerow(dict(
            name=f'{strain} {flower_sizes[i]}',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=2,
            sector_id=1,
            image_url=choice(flower_images),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))

        users_writer.writerow(dict(
            name=f'{strain} Cookies',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=2,
            sector_id=4,
            image_url=choice(cookie_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))

        users_writer.writerow(dict(
            name=f'{strain} Vaporizer',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=2,
            sector_id=2,
            image_url=choice(vapes_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))

    for strain in hybrids:

        idx = hybrids.index(strain)
        
        users_writer.writerow(dict(
            name=f'{strain} {flower_sizes[i]}',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=3,
            sector_id=1,
            image_url=choice(flower_images),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))

        users_writer.writerow(dict(
            name=f'{strain} Donuts',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=3,
            sector_id=4,
            image_url=choice(sweets_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))


        users_writer.writerow(dict(
            name=f'{strain} Vaporizer',
            description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
            category_id=3,
            sector_id=2,
            image_url=choice(vapes_pics),
            seedling_id=choice(range(1, 4)),
            strain_id=idx+1,
            plant_facility_id=choice(range(1, 4)),
            price=choice(range(15, 200))
            
            #header_image_url=choice(header_image_urls),
            #location=fake.city()
        ))






with open('users.csv', 'w') as users_csv:
    users_writer = csv.DictWriter(users_csv, fieldnames=USERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(NUM_USERS):
        users_writer.writerow(dict(
            email=fake.email(),
            
            username=fake.user_name(),
            image_url=choice(image_urls),
            password='$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe',
            bio=fake.sentence(),
            
            header_image_url=choice(header_image_urls),
            location=fake.city()
        ))



with open('messages.csv', 'w') as messages_csv:
    messages_writer = csv.DictWriter(messages_csv, fieldnames=MESSAGES_CSV_HEADERS)
    messages_writer.writeheader()

    for i in range(NUM_MESSAGES):
        messages_writer.writerow(dict(
            text=fake.paragraph()[:MAX_WARBLER_LENGTH],
            timestamp=get_random_datetime(),
            user_id=randint(1, NUM_USERS)
        ))

# Generate follows.csv from random pairings of users

with open('follows.csv', 'w') as follows_csv:
    all_pairs = list(permutations(range(1, NUM_USERS + 1), 2))

    users_writer = csv.DictWriter(follows_csv, fieldnames=FOLLOWS_CSV_HEADERS)
    users_writer.writeheader()

    for followed_user, follower in sample(all_pairs, NUM_FOLLWERS):
        users_writer.writerow(dict(user_being_followed_id=followed_user, user_following_id=follower))



# Generate chart of accounts

with open('chart_of_accounts.csv', 'w') as chart_of_accounts_csv:
    
    coa = ['Assets', 100, 1, 
           'Cash', 110, 1, 
           'Merchandise', 120, 1, 
           'Liabilities', 200, -1, 
           'Deferred Revenue', 210, -1,
           'Revenue', 300, -1,
           'Expenses', 400, 1,
           'Cost of Goods Sold', 410, 1,
           'Equity', 500, -1,
           'Capital', 510, -1]

    users_writer = csv.DictWriter(chart_of_accounts_csv, fieldnames=CHART_OF_ACCOUNTS_CSV_HEADERS)
    users_writer.writeheader()

    
    users_writer.writerow(dict(name=coa[0], number=coa[1], normal=coa[2]))
    users_writer.writerow(dict(name=coa[3], number=coa[4], normal=coa[5]))
    users_writer.writerow(dict(name=coa[6], number=coa[7], normal=coa[8]))
    users_writer.writerow(dict(name=coa[9], number=coa[10], normal=coa[11]))
    users_writer.writerow(dict(name=coa[12], number=coa[13], normal=coa[14]))
    users_writer.writerow(dict(name=coa[15], number=coa[16], normal=coa[17]))
    users_writer.writerow(dict(name=coa[18], number=coa[19], normal=coa[20]))
    users_writer.writerow(dict(name=coa[21], number=coa[22], normal=coa[23]))
    users_writer.writerow(dict(name=coa[24], number=coa[25], normal=coa[26]))
    users_writer.writerow(dict(name=coa[27], number=coa[28], normal=coa[29]))



#############################################################################################################################
# DYNAMIALLY GENERATE CUSTOMERS.  #
#############################################################################################################################



with open('customers.csv', 'w') as customers_csv:
    users_writer = csv.DictWriter(customers_csv, fieldnames=CUSTOMERS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(1, 301):
        users_writer.writerow(dict(
            user_id=i,
            account_number=random.sample(range(199999, 999999), 1)[0],
            payment_info=fake.credit_card_full(),
            address=fake.address(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number()
        ))




##############################################################################################################################
# DYNAMIALLY GENERATE BASKETS.  #
#############################################################################################################################


#new baskets table
with open('baskets.csv', 'w') as baskets_csv:
    users_writer = csv.DictWriter(baskets_csv, fieldnames=BASKETS_CSV_HEADERS)
    users_writer.writeheader()


    for x in range(12):

        for i in range(1, 301):
            users_writer.writerow(dict(
                customer_id=i,
                submitted_at=fake.date_time_between(start_date='-360d', end_date='now'),
                amount=random.sample(range(50, 1000), 1)[0]
            ))


#new baskets
#customers = Customer.query.all()
#for customer in customers:
#    basket = Basket(customer_id=customer.id, submitted_at=fake.date_time_between('2023-01-01 11:42:52'), amount=random.sample(range(50, 1000), 1))
#    db.session.add(basket)
#    db.session.commit()

#############################################################################################################################
# DYNAMIALLY GENERATE BILLS TABLE.  #
#############################################################################################################################



with open('bills.csv', 'w') as bills_csv:
    users_writer = csv.DictWriter(bills_csv, fieldnames=BILLS_CSV_HEADERS)
    users_writer.writeheader()


    for vendor_id in range(1,21):

        for i in range(1,6):

            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-365d', end_date='-336d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-335d', end_date='-306d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-305d', end_date='-276d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-275d', end_date='-246d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-245d', end_date='-216d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-215d', end_date='-186d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-185d', end_date='-156d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-155d', end_date='-126d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-125d', end_date='-96d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-95d', end_date='-66d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-65d', end_date='-36d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))
            users_writer.writerow(dict(
                    vendor_id=vendor_id,
                    date_billed=fake.date_time_between(start_date='-35d', end_date='-6d'),
                    amount=random.sample(range(50, 1000), 1)[0]
                ))




#############################################################################################################################
# DYNAMICALLY GENERATE VENDORS TABlE.  #
#############################################################################################################################


#new vendors table
with open('vendors.csv', 'w') as vendors_csv:
    users_writer = csv.DictWriter(vendors_csv, fieldnames=VENDORS_CSV_HEADERS)
    users_writer.writeheader()

    for i in range(20):
        users_writer.writerow(dict(
            name=fake.company(),
            address=fake.address()
            
        ))







