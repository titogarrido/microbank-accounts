import datetime
from flask import Flask, jsonify
from flask_restplus import Resource, Api, fields, reqparse, inputs
from bson.json_util import dumps
from flask_cors import CORS
from helpers.custom_fields import Integer, Date, DateTime, Email, String, Float, validate_payload


##### Database Connection #####
from pymongo import MongoClient
client = MongoClient('mongo', 27017)
db = client['account-database']
collection = db['account-collection']
##############################

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:5000'
CORS(app)
api = Api(app, version='1.0', title='Microbank')
ns = api.namespace('accounts', description='Accounts related operations')


account = api.model('account', {
    #'_id': fields.String(required=False, description='The account unique identifier'),
    'account_id': Integer(required=True, description='The account unique identifier'),
    'type': String(required=True, description='Account type, checking, saving'),
    'name': String(required=True, description='First name of the account owner'),
    'birthdate': Date(required=True),
    'phone': String(required=True, description='Main phone of the account owner'),
    'email': Email(required=True, description='Email of the account owner'),
    'balance': Float(required=True, default=0.0, description='The account balance'),
    'created_on': DateTime(required=False, dt_format='iso8601', description='Account datetime creation')
})

@ns.route('/accounts')
class ListAllAccounts(Resource):
    '''Shows a list of all accounts, and lets you POST to add new accounts'''
    @ns.doc('list_accounts')
    @ns.marshal_list_with(account)
    def get(self):
        '''List all accounts'''
        accounts = list(collection.find().sort("created_on", -1))
        return accounts

    @ns.doc('create_account')
    @ns.expect(account, validate=True)
    @ns.marshal_with(account, code=201)
    def post(self):
        validate_payload(api.payload, account)
        api.payload['created_on'] = datetime.datetime.now().isoformat()
        collection.insert_one(api.payload)
        return api.payload, 201

@ns.route('/account/<int:account_id>')
@ns.response(404, 'Account not found')
@ns.param('account_id', 'The account identifier')
class AccountOperations(Resource):
    '''Shows a list of all accounts, and lets you POST to add new accounts'''
    @ns.doc('get_account')
    @ns.marshal_list_with(account)
    def get(self, account_id):
        '''Fetch a given resource'''
        account = collection.find_one({"account_id": account_id})
        if not account:
            return account, 404
        else:
            return account, 200

@ns.route('/update_balance/<int:account_id>/<string:amount>')
@ns.response(404, 'Account not found')
@ns.param('account_id', 'The account identifier')
@ns.param('amount', 'Amount to modify the balance')
class UpdateBalance(Resource):
    '''Update value to balance'''
    @ns.doc('add_balance')
    @ns.marshal_list_with(account)
    def patch(self, account_id, amount):
        '''Fetch a given resource'''
        try:
            amount=float(amount)
        except:
            return 'invalid amount', 401
        account = collection.update_one({'account_id': account_id}, {'$inc': {'balance': amount}})
        if not account.matched_count:
            return account, 404
        else:
            return account, 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
