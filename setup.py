from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies.models import Base, Shelter, Puppy, Human

from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", website = "oaklandanimalservices.org", max_capacity = 20)
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", website = "sfspca.org", max_capacity = 20)
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", website = "http://wonderdogrescue.org", max_capacity = 20)
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", website = "hsalameda.org", max_capacity = 20)
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "paloaltohumane.org", max_capacity = 20)
session.add(shelter5)


#Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["static/1.jpg","static/2.jpg","static/3.jpg","static/4.jpg","static/5.jpg","static/6.jpg","static/7.jpg","static/8.jpg","static/9.jpg","static/10.jpg","static/11.jpg"]

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

for i,x in enumerate(male_names):
	new_puppy = Puppy(name = x, gender = "male", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images) ,shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()


for i,x in enumerate(female_names):
	new_puppy = Puppy(name = x, gender = "female", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images),shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()

#Add Humans

human_names = ['Vera Plouffe', 'Sterling Towler', 'Nevada Kopf', 'Deann Jenks', 'Teresa Kittredge', 'Yvonne Combest', 'Caridad Kram', 'Shantelle Kirton', 'Garnet Groseclose', 'Corazon Moynihan', 'Andera Waldron', 'Isis Buenrostro', 'Winston Mcmorrow']

for i,x in enumerate(human_names):
	new_human = Human(name = x)
	session.add(new_human)
	session.commit()