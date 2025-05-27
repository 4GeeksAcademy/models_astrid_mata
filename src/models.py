from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, Column, Integer, ForeignKey, relationship
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
   

#relacion muchos a muchos con planey atravez de user_planet_favorite
    favorite_planets: Mapped[list['Planets']]= relationship(
        secondary=user_planet_favorite,
        back_populates='user_who_favorited'
    )



    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
            
        }


#tabla de asociacion 
user_planet_favorite= Table(
    'user_planet_favorite', #nombre de la tabla
    db.Model.metadata, 
    Column('user_id', Integer, ForeignKey('user_id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet_id'), primary_key=True)
)
