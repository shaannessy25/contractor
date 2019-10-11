from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
client = MongoClient()
db = client.contractor
# db = client.get_default_database()
products = db.products
comments = db.comments
products.drop()

app = Flask(__name__)

@app.route('/')
def contractor_index():
    return render_template('home.html', products=products.find())

def index():
    '''Return Homepage '''
    return render_template('home.html')

   
@app.route('/products/new')
def items_new():
    '''Submit a new Item'''
    # print(request.form.to_dict())
    return render_template('items_new.html', products={})

@app.route('/products', methods=['POST'])
def items_submit():
    product = {
        'title': request.form.get('title'),
        'quantity': request.form.get('quantity')
    }
    
    product_id = products.insert_one(product).inserted_id
    return redirect(url_for('items_show', product_id=product_id))



@app.route('/products/<product_id>', methods=['GET','POST'])
def items_show(product_id):
    '''Shows a single product Item'''

    if request.method == 'POST':
        products.update_one({"_id": ObjectId(product_id)}, {"$set": {"title": request.form.get("title")}}) 

    product = products.find_one({'_id': ObjectId(product_id)})
    return render_template('items_show.html', product=product)
    
@app.route('/products/<product_id>/edit')
def item_edit(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    return render_template('items_edit.html', product=product)

@app.route("/products/<product_id>/delete", methods=["POST"])
def items_delete(product_id):
	products.delete_one({"_id" : ObjectId(product_id)})
	return redirect(url_for("contractor_index"))




if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))