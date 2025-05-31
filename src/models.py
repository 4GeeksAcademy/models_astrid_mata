# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import String, Table, Column, Integer, ForeignKey, relationship
# from sqlalchemy.orm import Mapped, mapped_column

# db = SQLAlchemy()

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
#     name: Mapped[str] = mapped_column(String(120), nullable=False)
#     password: Mapped[str] = mapped_column(String(120), nullable=False)
   

# #relacion muchos a muchos con planey atravez de user_planet_favorite
#     favorite_planets: Mapped[list['Planets']]= relationship(
#         secondary=user_planet_favorite,
#         back_populates='user_who_favorited'
#     )



#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             "name": self.name
#             # do not serialize the password, its a security breach
#         }


# class Planets(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(120), nullable=False)
#     climate: Mapped[str] = mapped_column(String(120), nullable=False)
    


#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "climate": self.climate
            
#         }


# #tabla de asociacion 
# user_planet_favorite= Table(
#     'user_planet_favorite', #nombre de la tabla
#     db.Model.metadata, 
#     Column('user_id', Integer, ForeignKey('user_id'), primary_key=True),
#     Column('planet_id', Integer, ForeignKey('planet_id'), primary_key=True)
# )
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship # ¡Importación correcta de relationship!

db = SQLAlchemy()

# --- Tablas de Asociación para las relaciones Many-to-Many ---
# Es importante definir estas tablas ANTES de las clases que las usan.

user_planet_favorite = Table(
    'user_planet_favorite', # Nombre de la tabla de asociación para planetas
    db.Model.metadata, 
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planets.id'), primary_key=True)
)

user_character_favorite = Table(
    'user_character_favorite', # Nombre de la tabla de asociación para personajes
    db.Model.metadata, 
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('characters.id'), primary_key=True)
)

# --- Modelos de la Base de Datos ---

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Relación muchos a muchos con 'Planets' a través de 'user_planet_favorite'
    favorite_planets: Mapped[list['Planets']]= relationship(
        secondary=user_planet_favorite,
        back_populates='user_who_favorited_planets' # Nombre de la relación inversa en 'Planets'
    )

    # Relación muchos a muchos con 'Characters' a través de 'user_character_favorite'
    favorite_characters: Mapped[list['Characters']]= relationship(
        secondary=user_character_favorite,
        back_populates='user_who_favorited_characters' # Nombre de la relación inversa en 'Characters'
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # No serializamos la contraseña por seguridad
        }


class Planets(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    
    # Relación inversa para 'favorite_planets' en 'User'
    user_who_favorited_planets: Mapped[list['User']] = relationship(
        secondary=user_planet_favorite,
        back_populates='favorite_planets'
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
        }


class Characters(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)

    # Relación inversa para 'favorite_characters' en 'User'
    user_who_favorited_characters: Mapped[list['User']] = relationship(
        secondary=user_character_favorite,
        back_populates='favorite_characters'
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year
        }