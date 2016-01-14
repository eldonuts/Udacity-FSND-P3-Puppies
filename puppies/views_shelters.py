from puppies import app
from flask import redirect,request,render_template,flash
import functions as db


@app.route('/shelters')
def shelters():
    shelters = db.list_shelters()
    for shelter in shelters:
        if shelter.availability < 0:
            flash(shelter.name + ' is overcrowded. <a href="/rebalance" class="alert-link">Click here</a> to rebalance.')
    return render_template('shelters.html', shelters = shelters)


@app.route('/shelters/<shelter_id>/puppies')
def shelter(shelter_id):
    puppies = db.list_puppies(shelter_id)
    shelters = db.list_shelters()
    return render_template('puppies.html',puppies = puppies, shelters = shelters)

@app.route('/shelters/<shelter_id>/edit', methods = ['POST'])
def edit_shelter(shelter_id):
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zipcode = request.form['zipCode']
    website = request.form['website']
    max_capacity = request.form['max_capacity']
    db.edit_shelter(shelter_id, name, address, city, state, zipcode, website, max_capacity)
    flash(name + " updated.")
    return redirect('/shelters')


@app.route('/rebalance')
def rebalance():
    messages = db.balance_shelters()
    for message in messages:
        flash(message)
    return redirect('/shelters')