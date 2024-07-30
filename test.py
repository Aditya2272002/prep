from flask import Blueprint, request, g, jsonify
from middleware import check_token_decorator

test = Blueprint("test", __name__)


@test.route('/', methods=['GET','POST'])
def testing():
   params = request.args
   print("params", params)
   
   if request.method == 'POST':
      body = request.get_json()
      print("Request Body:", body)
      
   
   headers = request.headers
   print("Request Headers:", headers)
   
   response = {
      "parameters": params.to_dict(),
      "body": body if request.method == 'POST' else "N/A",
      "headers": dict(headers)
   }

   return jsonify(response)
   

# @test.before_request
# def before_request_func():
#    from middleware import check_token
#    check_token()


@test.route("/test/<id>", methods=['GET'])
def getAPI(id):
   return f"Hello :{id}"



@test.route("/test/<id>", methods=['POST'])
@check_token_decorator
def postAPI(id):
   if g.allowed == "yes":
      return f"POST API {id}"
   return jsonify({"error": "unauthorized"})
