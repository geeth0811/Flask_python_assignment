import sqlite3
#ititial values for the id generate start values used inside tables later
id_start_val=10004
vid_start_val=100001
item_id_start=100
order_id_start=80000100
#one time execute to create tables initially hence put in if not exists
conn=sqlite3.connect('Ecommerce01.db')
c = conn.cursor()
c.execute("CREATE TABLE if not exists customers (Cust_id integer PRIMARY KEY, Cust_name text,Username text NOT NULL UNIQUE,password text NOT NULL,level integer NOT NULL)")
c.execute("CREATE TABLE if not exists vendors (Vendor_id int PRIMARY KEY, C_id int references customers(Cust_id) on delete cascade,Store_name text)")
c.execute("CREATE TABLE if not exists items (item_id int PRIMARY KEY, V_id int references vendors(Vendor_id) on delete cascade, item_name text,store_id integer, Available_qty integer,unit_price real)")
c.execute("CREATE TABLE if not exists orders (order_id int PRIMARY KEY,customer_id int references customers(Cust_id), It_id int references items(item_id), ordered_qty integer,total_amount real)")

#this is function used to add a customer to customer table.
def register_cust(param):
    global id_start_val
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    #This helps in fetching max value everytime and insert max val plus 1 as the primary key id generations used in all insert functions.
    query1="select max(Cust_id) from customers"
    c.execute(query1)
    temp=c.fetchone()[0]
    if temp is not None:
        id_start_val=temp+1
    sqlquery="insert into customers values({},'{}','{}','{}',{})".format(id_start_val,param["name"],param["username"],param["password"],param["level"])
    try:
        c.execute(sqlquery)
        conn.commit()
    except Exception as e:
        conn.close()
        return {"msg":str(e),"status":403}
    else:
        conn.commit()
        conn.close()
        return {"msg":"Row inserted, registered customer successfully","status":201}

# this functions checks for login by taking username and password, initially it checks if username is present or not then further
# matches with password and returns login conditions.
def login(param):
    sqlquery="select * from customers where Username=('{}')".format(param["username"])
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {"msg": "Username invalid,try sign up if not created", "status": 406}
        else:
            sqlquery1 = "select * from customers where Username=('{}') and password=('{}')".format(param["username"],param["pwd"])
            try:
                c.execute(sqlquery1)
            except Exception as e:
                conn.close()
                return {"msg": str(e), "status": 403}
            else:
                res1 = c.fetchall()
                if len(res1) == 0:
                    return {"msg": "login failed due to invalid password", "status": 406}
                else:
                    return {"msg": "Sucessfully logged in", "status": 201}
                conn.close()

#this function adds a vendor to the vendor table by checking first if the account is registered as a customer in the customer table.
def add_vendor(param):
    global vid_start_val
    query1 = "select max(Vendor_id) from vendors"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    c.execute(query1)
    temp = c.fetchone()[0]
    if temp is not None:
        vid_start_val = temp + 1
    sqlquery = "select * from customers where Cust_id=({}) and level=1".format(param["customer_id"])
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {"msg": "customer_id not found as valid vendor,enter valid customer_id Or please register as customer first to get customer_id ", "status": 406}
        else:
            sqlquery1 = "insert into vendors values({},{},'{}')".format(vid_start_val,param["customer_id"],param["store_name"])
            try:
                c.execute(sqlquery1)
                conn.commit()
            except Exception as e:
                conn.close()
                return {"msg": str(e), "status": 403}
            else:
                conn.commit()
                conn.close()
                return {"msg": "Row inserted, added vendor details successfully", "status": 201}


#this function helps in adding items by checking if the vendor is a valid registered vendor
def add_items(param):
    global item_id_start
    query1 = "select max(item_id) from items"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    c.execute(query1)
    temp = c.fetchone()[0]
    if temp is not None:
        item_id_start = temp + 1
    sqlquery = "select * from vendors where Vendor_id=({})".format(param["vendor_id"])
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {
                "msg": "vendor_id not found,enter valid vendor_id Or please register as vendor first to get vendor_id ",
                "status": 406}
        else:
            sqlquery1 = "insert into items values({},{},'{}',{},{},{})".format(item_id_start, param["vendor_id"],param["item_name"],param["store_id"],param["available_quantity"],param["unit_price"])
            try:
                c.execute(sqlquery1)
                conn.commit()
            except Exception as e:
                conn.close()
                return {"msg": str(e), "status": 403}
            else:
                conn.commit()
                conn.close()
                return {"msg": "Row inserted, added item successfully", "status": 201}

#This functions searches for items by name and firstly validates the customer.it returns empty list if no item is present
def search_By_Item_Name(param):
    sqlquery = "select * from customers where Cust_id=({})".format(param["customer_id"])
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {"msg": "customer_id not found, login with valid customer", "status": 406}
        else:
            sqlquery1 = "select * from items where item_name=('{}')".format(param["item_name"])
            try:
                res1 = c.execute(sqlquery1)
            except Exception as e:
                return {"msg": str(e), "status": 403}
            else:
                return {"result": list(res1), "status": 200}
            finally:
                conn.close()

#this function helps in insertion of rows in order table and verifies only valid registered customers can place the orders.
def place_Order(param):
    global order_id_start
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    query1 = "select max(order_id) from orders"
    c.execute(query1)
    temp = c.fetchone()[0]
    if temp is not None:
        id_start_val = temp + 1
    sqlquery = "select * from customers where Cust_id=({}) and level=0".format(param["customer_id"])
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {
                "msg": "customer_id not found, login with valid customer to place order","status": 406}
        else:
            sqlquery1 = "insert into orders values({},{},{},{},{})".format(order_id_start, param["customer_id"],param["item_id"], param["quantity"],param["total_price"])
            try:
                c.execute(sqlquery1)
                conn.commit()
            except Exception as e:
                conn.close()
                return {"msg": str(e), "status": 403}
            else:
                conn.commit()
                conn.close()
                return {"msg": "Row inserted, order placed successfully", "status": 201}

#this functions helps in getting all order detials of a verified customer.
def get_All_Orders_By_Customer(param):
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    sqlquery = "select * from customers where Cust_id=({}) and level=0".format(param["customer_id"])
    try:
        c.execute(sqlquery)
    except Exception as e:
        conn.close()
        return {"msg": str(e), "status": 403}
    else:
        res = c.fetchall()
        if len(res) == 0:
            return {
                "msg": "customer_id not found, login with valid customer to check order details", "status": 406}
        else:
            sqlquery1 = "select * from orders where customer_id=('{}')".format(param["customer_id"])
            try:
                res1 = c.execute(sqlquery1)
            except Exception as e:
                return {"msg": str(e), "status": 403}
            else:
                res2= c.fetchall()
                if len(res2) ==0:
                    return {"result": "No order was placed by this customer", "status": 200}
                else:
                    return {"result": list(res2), "status": 200}
            finally:
                conn.close()

# this function is to see all the order placed without any input parameters
def get_All_Orders():
    sqlquery = "select * from orders"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        res = c.execute(sqlquery)
    except Exception as e:
        return {"msg": str(e), "status": 403}
    else:
        return {"result": list(res), "status": 200}
    finally:
        conn.close()

#this functions is to see all the vendors and thier respective items sold without any input parameters.
def get_All_Vendors():
    sqlquery = "select * from vendors,items where vendors.Vendor_id=items.V_id"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        res = c.execute(sqlquery)
    except Exception as e:
        return {"msg": str(e), "status": 403}
    else:
        return {"result": list(res), "status": 200}
    finally:
        conn.close()
#this is just function where we just loggout as no sessions were used just returning msg.
def logout():
    return {"msg":"User logged out sucessfully", "status": 203}
# the below are just writtern by me not in task just to test the values in customers and vendors tables.
def list_all():
    sqlquery="select * from customers"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        res= c.execute(sqlquery)
    except Exception as e:
        return {"msg":str(e),"status":403}
    else:
        return {"result":list(res),"status":200}
    finally:
        conn.close()
# follow above comments.
def list_all_vendors():
    sqlquery="select * from vendors"
    conn = sqlite3.connect("Ecommerce01.db")
    c = conn.cursor()
    try:
        res= c.execute(sqlquery)
    except Exception as e:
        return {"msg":str(e),"status":403}
    else:
        return {"result":list(res),"status":200}
    finally:
        conn.close()


# unit testing purpose.
#if __name__ == '__main__':
 #   param = {'customer_id':10004}
  #  print((get_All_Orders_By_Customer(param)))







