from flask import Flask,request,jsonify
import Database_code
app = Flask(__name__)

@app.route("/Ecommerce/")
def doc():
    return "<b>This is an Ecommerce website""</b>" \
           "please visit attached docs for API documentation"

@app.route("/Ecommerce/add_Customer",methods=["POST","GET"])
def add_Customer():
    if request.method == "GET" :
        return "Try POSTing instead"
    param = request.get_json()
    result=Database_code.register_cust(param)
    return jsonify(result)

@app.route("/Ecommerce/login",methods=["POST","GET"])
def login():
    if request.method == "GET" :
        return "Try POSTing instead"
    param = request.get_json()
    result=Database_code.login(param)
    return jsonify(result)

@app.route("/Ecommerce/add_Vendor",methods=["POST","GET"])
def add_Vendor():
    if request.method == "GET" :
        return "Try POSTing instead"
    param = request.get_json()
    result=Database_code.add_vendor(param)
    return jsonify(result)

@app.route("/Ecommerce/add_items",methods=["POST","GET"])
def add_items():
    if request.method == "GET" :
        return "Try POSTing instead"
    param = request.get_json()
    result=Database_code.add_items(param)
    return jsonify(result)

@app.route("/Ecommerce/Search_item_by_name",methods=["POST","GET"])
def Search_item_by_name():
    param = request.get_json()
    result=Database_code.search_By_Item_Name(param)
    return jsonify(result)

@app.route("/Ecommerce/Place_order",methods=["POST","GET"])
def Place_order():
    if request.method == "GET" :
        return "Try POSTing instead"
    param = request.get_json()
    result=Database_code.place_Order(param)
    return jsonify(result)

@app.route("/Ecommerce/Get_all_orders_by_customer",methods=["POST","GET"])
def Get_all_orders_by_customer():
    param = request.get_json()
    result=Database_code.get_All_Orders_By_Customer(param)
    return jsonify(result)

@app.route("/Ecommerce/Get_all_orders",methods=["POST","GET"])
def Get_all_orders():
    result=Database_code.get_All_Orders()
    return jsonify(result)

@app.route("/Ecommerce/Get_all_vendors",methods=["POST","GET"])
def Get_all_vendors():
    result=Database_code.get_All_Vendors()
    return jsonify(result)

@app.route("/Ecommerce/Logout",methods=["POST","GET"])
def Logout():
    result=Database_code.logout()
    return jsonify(result)

# below was just written to view customers and vendors tables
@app.route("/Ecommerce/view_table/customers")
def list_all():
    result=Database_code.list_all()
    return jsonify(result)

@app.route("/Ecommerce/view_table/vendors")
def list_all_vendors():
    result=Database_code.list_all_vendors()
    return jsonify(result)

if __name__=='__main__':
    app.run()
