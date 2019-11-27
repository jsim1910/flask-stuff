from flask import Flask,redirect
from flask import render_template 
from flask import request
from flask import session
import database as db
import authentication
import logging

app = Flask(__name__)

# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'

logging.basicConfig(level=logging.DEBUG) 
app.logger.setLevel(logging.INFO)

navbar = """
        <a href='/'>Home</a> | <a href='/products'>Products</a> |
        <a href='/branches'>Branches</a> | <a href='/aboutus'>About
Us</a>
		<p/>
		"""
@app.route('/')
def index():
   return render_template('index.html', page="Index")
   
@app.route('/products')
def products():
    return render_template('products.html', page="Products")
   
@app.route('/productdetails') 
def productdetails():
   code = request.args.get('code', '')
   product = db.get_product(int(code))
   return render_template('productdetails.html', code=code,product=product)

@app.route('/branches')
def branches():
   return render_template('branches.html', page="Branches")
   
@app.route('/aboutus')
def aboutus():
   return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return "Invalid username or password please <a href='/login'>enter again</a>"
    
@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a 
    # quantity of 1 for now

    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/formsubmission', methods = ['POST'])
def form_submission():
    qty = request.form.getlist("qty")
    return render_template('formsubmission.html',qty=qty)

@app.route('/change')
def change():
    return render_template('change.html')

@app.route('/changesubmission', methods = ['POST'])
def change_submission():
    stype = request.form.get("stype")
    return render_template('changesubmission.html',stype=stype)


