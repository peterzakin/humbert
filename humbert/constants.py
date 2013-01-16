import os
diffbot_key = "7b5e613406bc0bb6e709a4f4e7aab917"
mongo_uri = "mongodb://heroku_app10941623:4okohp3jp51pcr1btvsqgntm29@ds047437.mongolab.com:47437/heroku_app10941623"



if os.environ.get('DJANGO_ENVIRONMENT') is not None:
    ENVIRONMENT = 'test'
else:
    ENVIRONMENT = 'production'
