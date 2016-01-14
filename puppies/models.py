from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('human_id', Integer, ForeignKey('human.id')),
    Column('puppy_id', Integer, ForeignKey('puppy.id'))
)

class Human(Base):
    __tablename__ = 'human'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=True)
    email = Column(String(80))
    puppies = relationship("Puppy",
                           secondary=association_table,
                           backref="Human")

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)
    max_capacity = Column(Integer)

    puppies = relationship("Puppy", backref="shelter_test")

    @hybrid_property
    def current_occupancy(self):
        all_puppies = self.puppies
        filtered_puppies = [i for i in all_puppies if i.shelter_id == self.id]
        return len(filtered_puppies)

    @hybrid_property
    def availability(self):
        return self.max_capacity - self.current_occupancy
    
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))
    breed = Column(String(80))


engine = create_engine('sqlite:///puppies.db')

Base.metadata.create_all(engine)