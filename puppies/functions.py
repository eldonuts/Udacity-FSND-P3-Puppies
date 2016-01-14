from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
from models import Base, Shelter, Puppy, Human

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def list_puppies(shelter_id=None):
    if shelter_id:
        puppies = session.query(Puppy).filter(Puppy.shelter_id == shelter_id).all()
    else:
        puppies = session.query(Puppy).order_by(desc(Puppy.shelter_id)).filter(Puppy.shelter_id != None).all()
    return puppies


def list_shelters():
    shelters = session.query(Shelter).all()
    return shelters


def get_shelter(shelter_id):
    shelter = session.query(Shelter).filter(Shelter.id == shelter_id).one()
    return shelter


def get_puppy(puppy_id):
    puppy = session.query(Puppy).filter(Puppy.id == puppy_id).one()
    return puppy


def delete_puppy(puppy_id):
    puppy = get_puppy(puppy_id)
    session.delete(puppy)
    session.commit()


def edit_puppy(puppy_id,name,gender,dob,shelter_id):
    puppy = get_puppy(puppy_id)
    puppy.name = name
    puppy.gender = gender
    puppy.dateOfBirth = dob
    puppy.shelter_id = shelter_id
    session.commit()


def add_puppy(name,gender,dob,shelter_id):
    puppy = Puppy(name=name,gender=gender,dateOfBirth=dob,shelter_id=shelter_id)
    session.add(puppy)
    session.commit()


def edit_shelter(shelter_id,name,address,city,state,zipCode,website,max_capacity):
    shelter = get_shelter(shelter_id)
    shelter.name = name
    shelter.address = address
    shelter.city = city
    shelter.state = state
    shelter.zipCode = zipCode
    shelter.website = website
    shelter.max_capacity = max_capacity
    session.commit()


def balance_shelters():
    shelters = list_shelters()
    messages = []
    for shelter in shelters:
        if shelter.availability < 0:
            availability = abs(shelter.availability)
            puppies_to_move = session.query(Puppy).filter(Puppy.shelter_id == shelter.id).limit(availability).all()
            for puppy in puppies_to_move:
                availabile_shelters = [i for i in shelters if i.availability > 0]
                if len(availabile_shelters) > 0:
                    new_shelter = availabile_shelters[0]
                    print 'Moved ' + puppy.name + ' from ' + puppy.shelter.name + ' to ' + new_shelter.name
                    messages.append('Moved <b>' + puppy.name + '</b> from <b>' + puppy.shelter.name + '</b> to <b>' + new_shelter.name + '</b>.')
                    puppy.shelter_id = new_shelter.id
                    session.commit()
                else:
                    print 'There are no available shelter for ' + puppy.name + '.'
                    messages.append('There are no available shelter for ' + puppy.name + '.')
    return messages


def list_adopters():
    adopters = session.query(Human).all()
    return adopters


def adopt_puppy(puppy_id, *human_list):
    puppy = session.query(Puppy).filter(Puppy.id == puppy_id).one()

    puppy.shelter_id = None

    for i,human_id in enumerate(*human_list):
        human = session.query(Human).filter(Human.id == human_id).one()
        human.puppies.append(puppy)

    session.commit()


def add_adopter(name,email):
    adopter = Human(name = name, email = email)
    session.add(adopter)
    session.commit()


def get_adopter(adopter_id):
    adopter = session.query(Human).filter(Human.id == adopter_id).one()
    return adopter


def createUser(login_session):
    newUser = Human(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(Human).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(Human).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(Human).filter_by(email=email).one()
        return user.id
    except:
        return None