from flask import Flask, request, render_template
from gms_functions import GMS

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def form_submit():
    gtext = ""
    if request.method == "POST":
        bill_no = request.form.get("billNumber", "")
        bill_date = request.form.get("billDate", "")
        cust_name = request.form.get("customerId", "")
        cust_mob = request.form.get("phoneNumber", "")
        item_name = request.form.get("itemName", "")
        price = request.form.get("price", "")
        quantity = request.form.get("quantity", "")

        dbobj = GMS()
        dbobj.ConnectDB()
        dbobj.CreateTable()

        if request.form["action_button"] == "Save Details":
            if bill_no and bill_date and cust_name and cust_mob:
                try:
                    gtext = dbobj.Save_details(int(bill_no), bill_date, cust_name, int(cust_mob))
                except ValueError:
                    gtext = "Invalid input for bill number or phone number."
            else:
                gtext = "Please fill in all the fields."

        elif request.form["action_button"] == "Add an Item":
            if item_name and price and quantity and bill_no:
                try:
                    gtext = dbobj.AddItem(int(bill_no), item_name, int(price), int(quantity))
                except ValueError:
                    gtext = "Invalid input for bill number, price, or quantity."
            else:
                gtext = "Please fill in all the fields."

        elif request.form["action_button"] == "Delete an Item":
            if bill_no:
                try:
                    gtext = dbobj.DeleteItem(int(bill_no))
                except ValueError:
                    gtext = "Invalid input for bill number."
            else:
                gtext = "Please provide a bill number."

        elif request.form["action_button"] == "Generate Bill":
            if bill_no:
                try:
                    ret = dbobj.GenerateBill(int(bill_no))
                    if isinstance(ret, dict):
                        gtext = f">>> Number of items retrieved is: {len(ret['items'])}\n"
                        gtext += "-" * 70 + "\n"
                        gtext += "Bill No\tBill Date\tCustomer Name\tMobile No\tItem Name\tPrice\tQuantity\n"
                        gtext += "-" * 70 + "\n"
                        for item in ret['items']:
                            gtext += f"{ret['bill_no']}\t{ret['date']}\t{ret['customer_name']}\t{ret['customer_no']}\t{item['product_name']}\t{item['price']}\t{item['quantity']}\n"
                        gtext += "-" * 70 + f"\nTotal Price: {ret['total_price']}\n"
                    else:
                        gtext = ret
                except ValueError:
                    gtext = "Invalid input for bill number."
            else:
                gtext = "Please provide a bill number."

    return render_template(
        "gms_html.html",
        b=request.form.get("billNumber", ""),
        d=request.form.get("billDate", ""),
        n=request.form.get("customerId", ""),
        no=request.form.get("phoneNumber", ""),
        i=request.form.get("itemName", ""),
        p=request.form.get("price", ""),
        q=request.form.get("quantity", ""),
        g=gtext
    )

if __name__ == "__main__":
    app.run(debug=True, port=6969)
