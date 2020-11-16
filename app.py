from portalsdk import APIContext, APIMethodType, APIRequest
from time import sleep
from flask import Flask , jsonify , request
from flask_restful import Api, Resource, reqparse
import datetime
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
from waitress import serve



# initialize a flask app
app = Flask(__name__)

# intialize a flask-restful api
api = Api(app)


@app.route('/api/v1/test', methods=['GET'])
def api_all():

    if 'id' in request.args:
        id = int(request.args['id'])
        vvalue = id+0.3
print(vvalue)
    else:
        return "Error: No id field provided. Please specify an id."



    return jsonify(vvalue)






@app.route('/api/v1/vschool/subscription', methods=['POST'])
def main():
# Public key on the API listener used to encrypt keys
    public_key = 'MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEArv9yxA69XQKBo24BaF/D+fvlqmGdYjqLQ5WtNBb5tquqGvAvG3WMFETVUSow/LizQalxj2ElMVrUmzu5mGGkxK08bWEXF7a1DEvtVJs6nppIlFJc2SnrU14AOrIrB28ogm58JjAl5BOQawOXD5dfSk7MaAA82pVHoIqEu0FxA8BOKU+RGTihRU+ptw1j4bsAJYiPbSX6i71gfPvwHPYamM0bfI4CmlsUUR3KvCG24rB6FNPcRBhM3jDuv8ae2kC33w9hEq8qNB55uw51vK7hyXoAa+U7IqP1y6nBdlN25gkxEA8yrsl1678cspeXr+3ciRyqoRgj9RD/ONbJhhxFvt1cLBh+qwK2eqISfBb06eRnNeC71oBokDm3zyCnkOtMDGl7IvnMfZfEPFCfg5QgJVk1msPpRvQxmEsrX9MQRyFVzgy2CWNIb7c+jPapyrNwoUbANlN8adU1m6yOuoX7F49x+OjiG2se0EJ6nafeKUXw/+hiJZvELUYgzKUtMAZVTNZfT8jjb58j8GVtuS+6TM2AutbejaCV84ZK58E2CRJqhmjQibEUO6KPdD7oTlEkFy52Y1uOOBXgYpqMzufNPmfdqqqSM4dU70PO8ogyKGiLAIxCetMjjm6FCMEA3Kc8K0Ig7/XtFm9By6VxTJK1Mg36TlHaZKP6VzVLXMtesJECAwEAAQ=='
# Create Context with API to request a Session ID
    api_context = APIContext()
# Api key
    api_context.api_key = '7OCA9qYWyAdaajBsrm46hgwANyqeUGfG'
# Public key
    api_context.public_key = public_key
# Use ssl/https
    api_context.ssl = True
# Method type (can be GET/POST/PUT)
    api_context.method_type = APIMethodType.GET
# API address
    api_context.address = 'openapi.m-pesa.com'
# API Port
    api_context.port = 443
# API Path
    api_context.path = '/sandbox/ipg/v2/vodacomTZN/getSession/'

# Add/update headers
    api_context.add_header('Origin', '3.8.36.235')

# Parameters can be added to the call as well that on POST will be in JSON format and on GET will be URL parameters
# api_context.add_parameter('key', 'value')

#Do the API call and put result in a response packet
    api_request = APIRequest(api_context)

# Do the API call and put result in a response packet
    result = None
    try:
        result = api_request.execute()
    except Exception as e:
        print('Call Failed: ' + e)

    if result is None:
        raise Exception('SessionKey call failed to get result. Please check.')

# Display results
    print(result.status_code)
    # print(result.headers)
    print(result.body)

# The above call issued a sessionID which will be used as the API key in calls that needs the sessionID
    api_context = APIContext()
    api_context.api_key = result.body['output_SessionID']
    api_context.public_key = public_key
    api_context.ssl = True
    api_context.method_type = APIMethodType.POST
    api_context.address = 'openapi.m-pesa.com'
    api_context.port = 443
    api_context.path = '/sandbox/ipg/v2/vodacomTZN/c2bPayment/singleStage/'

    api_context.add_header('Origin','3.8.36.235' )

    api_context.add_parameter('input_Amount', '100')
    api_context.add_parameter('input_Country', 'TZN')
    api_context.add_parameter('input_Currency', 'TZS')
    api_context.add_parameter('input_CustomerMSISDN', '000000000001')
    api_context.add_parameter('input_ServiceProviderCode', '000000')
    api_context.add_parameter('input_ThirdPartyConversationID', 'asv02e5958774f7ba228d83d0d689909')
    api_context.add_parameter('input_TransactionReference', 'T1234T')
    api_context.add_parameter('input_PurchasedItemsDesc', 'Shoes')

    api_request = APIRequest(api_context)

# SessionID can take up to 30 seconds to become 'live' in the system and will be invalid until it is
    # 5sec for testing
    sleep(3) 

    result = None
    try:
        result = api_request.execute()
    except Exception as e:
        print('Call Failed: ' + e)

    if result is None:
        raise Exception('API call failed to get result. Please check.')

    print(result.status_code)
    # print(result.headers)
    print(result.body)    
    return jsonify(result.body,result.status_code)
# if __name__ == '__main__':
    # main()
    # app.run(port=5000,debug=True)
    # serve(app)
    # serve(app, host='0.0.0.0', port=8080)
