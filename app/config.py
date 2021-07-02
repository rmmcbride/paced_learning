import os
username = os.environ['LEARN_USERNAME']
password = os.environ['LEARN_PASSWORD']
userpass = 'postgresql://' + username + ':' + password + '@'
server = '127.0.0.1'
dbname = '/paced_learning'
SQLALCHEMY_DATABASE_URI = userpass + server + dbname
SQLALCHEMY_TRACK_MODIFICATIONS = False
