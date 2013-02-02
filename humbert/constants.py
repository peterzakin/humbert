import os
diffbot_key = "7b5e613406bc0bb6e709a4f4e7aab917"
mongo_uri = "mongodb://heroku_app10941623:4okohp3jp51pcr1btvsqgntm29@ds047437.mongolab.com:47437/heroku_app10941623"
client_id = '470297626362026'
client_secret = '19bde156d8fa8a68f56a1800e34f8aa0'

if os.environ.get('DJANGO_ENVIRONMENT') is not None:
    ENVIRONMENT = 'test'
else:
    ENVIRONMENT = 'production'
