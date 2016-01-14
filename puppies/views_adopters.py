from puppies import app
from flask import redirect,request,render_template
from puppies.email import send_email
import functions as db


@app.route('/adopters')
def adopters():
    adopter_list = db.list_adopters()
    return render_template('adopters.html', adopters=adopter_list)


@app.route('/adopt/<puppy_id>', methods=['GET', 'POST'])
def adopt(puppy_id):
    puppy = db.get_puppy(puppy_id)
    if request.method == 'GET':
        adopters = db.list_adopters()
        return render_template('adopt.html', puppy=puppy, adopters=adopters)
    if request.method == 'POST':
        adopters = request.form.getlist('adopters')
        db.adopt_puppy(puppy_id,adopters)
        for adopter in adopters:
            print adopter
            x = db.get_adopter(adopter)
            send_email(x.email, 'You have just adopted ' + puppy.name)
        return redirect('/adopters')