from puppies import app
from flask import redirect,request,render_template,flash
from datetime import datetime
from puppies.forms import PuppiesForm
import functions as db


@app.route('/puppies', methods = ['GET', 'POST'])
def puppies():
    if request.method == 'POST':
        print 'post'
    else:
        shelters = db.list_shelters()
        puppies = db.list_puppies()
        return render_template('puppies.html',puppies = puppies, shelters = shelters)


@app.route('/puppy/<puppy_id>')
def puppy(puppy_id):
    puppy = db.get_puppy(puppy_id)
    return render_template('puppy.html',puppy = puppy)


@app.route('/puppy/<puppy_id>/delete', methods = ['POST'])
def delete_puppy(puppy_id):
    delete_puppy(puppy_id)
    return redirect('/puppies')


@app.route('/puppy/<puppy_id>/edit', methods = ['GET', 'POST'])
def edit_puppy(puppy_id):
    puppy = db.get_puppy(puppy_id)

    form = PuppiesForm(request.form)

    form.gender.choices = [('male','Male'),('female','Female')]
    form.shelter.choices = [(shelter.id, (shelter.name + ' ' + str(shelter.current_occupancy) + '/' + str(shelter.max_capacity))) for shelter in db.list_shelters()]

    if request.method == 'GET':
        form.name.data = puppy.name
        form.gender.data = puppy.gender
        form.shelter.data = puppy.shelter_id
        form.dateofbirth.data = puppy.dateOfBirth

    if request.method == 'POST' and form.validate():
        name = form.name.data
        gender = form.gender.data
        dateofbirth = datetime.strptime(form.dateofbirth.data.strftime('%Y-%m-%d'), '%Y-%m-%d')
        shelter = form.shelter.data
        app.logger.info('edited puppy ' + puppy_id + ', arguments: ' + name + ", " + gender + ", " + str(dateofbirth) + ", " + str(shelter))
        flash(form.name.data + ' has now been updated.')
        db.edit_puppy(puppy_id,name, gender, dateofbirth, shelter)
    return render_template('edit_puppy.html', form = form, puppy_id = puppy_id)


@app.route('/puppy/add', methods = ['GET', 'POST'])
def add_puppy():

    form = PuppiesForm(request.form)

    form.gender.choices = [('male', 'Male'), ('female', 'Female')]
    form.shelter.choices = [(shelter.id, (shelter.name + ' ' + str(shelter.current_occupancy) + '/' + str(shelter.max_capacity))) for shelter in db.list_shelters()]

    if request.method == 'GET':
        form.dateofbirth.data = datetime.today()

    if request.method == 'POST' and form.validate():
        name = form.name.data
        gender = form.gender.data
        dateofbirth = datetime.strptime(form.dateofbirth.data.strftime('%Y-%m-%d'), '%Y-%m-%d')
        shelter = form.shelter.data
        print(name + " - " + gender + " - " + str(dateofbirth) + " - " + str(shelter))
        app.logger.info('added new puppy: ' + name + ", " + gender + ", " + str(dateofbirth) + ", " + str(shelter))
        flash(form.name.data + ' has been added to database.')
        shelters = db.list_shelters()
        for x in shelters:
            if x.availability < 0:
                flash(x.name + ' is overcrowded. <a href="/rebalance" class="alert-link">Click here</a> to rebalance.')
        db.add_puppy(name, gender, dateofbirth, shelter)
    return render_template('add_puppy.html', form = form)