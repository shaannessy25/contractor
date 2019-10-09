from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
# client = MongoClient(host=f'{host}?retryWrites=false')
client=MongoClient()
db = client.contractor
# db = client.get_default_database()
products = db.products
comments = db.comments

app = Flask(__name__)

@app.route('/')
def contractor_index():
    return render_template('items_index.html', products=products.find())

   
@app.route('/products', methods=['GET'])
def items_new():
    '''Submit a new Item'''
    # print(request.form.to_dict())
    return render_template('items_new.html', products={} )

@app.route('/products', methods=['POST'])
def items_submit():
    product = {
        'title': request.form.get('title'),
        'description': request.form.get('description')
    }
    products.insert_one(product)
    return render_template('items_show.html', products=product)
#     print(product)
#     product_id = products.insert_one(product).inserted_id
#     return redirect(url_for('products_show', product_id=product_id))

# @app.route('/products/<product_id>')
# def contractor_show(product_id):
#     product = products.find_one({'_id': ObjectId(product_id)})
#     product_comments = comments.find({'product_id': ObjectId(product_id)})
#     return render_template('contractor_show.html', product=product, comments=product_comments)



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))