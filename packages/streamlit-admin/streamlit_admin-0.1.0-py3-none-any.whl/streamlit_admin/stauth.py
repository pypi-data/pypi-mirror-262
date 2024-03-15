""" stauth - Authenticator for Streamlit using pydal to save user info in database.
"""
import re
import bcrypt
import pandas as pd
from .model import model
import streamlit as st

__AUTHOR = "Eduardo S. Pereira"
__EMAIL = "eduardo.spereira@sp.senai.br"
__DATE = "09/10/2023"

__version__ = "0.1.0"

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class STAuth:
    def __init__(self, dbinfo, folder):
        self._model = model(dbinfo, folder)
        self._logged = False
        self._user = None
        if self.database(self.database.users).isempty():
            self._has_user = False
        else:
            self._has_user = True

        self._session_state = st.session_state

        if 'user' not in self._session_state:
            self._session_state.user = None

    @property
    def database(self):
        return self._model

    @property
    def logged(self):
        return self._logged

    @property
    def user(self):
        return self._session_state.user

    @property
    def is_admin(self):
        return self.user['role'] == 'admin'

    @property
    def has_users(self):
        return self._has_user

    def login(self, user: str, password: str):
        "Verify if user exist in database"
        query = self.database(self.database.users.username == user)
        user_info = query.select(self.database.users.password).first()
        if user_info is not None:
            if bcrypt.checkpw(password.encode("utf8"), user_info.password.encode("utf8")):
                self._user = query.select(self.database.users.id,
                                          self.database.users.role,
                                          self.database.users.active
                                          ).first().as_dict()
                self._session_state.user = self._user
                if self._logged is False:
                    self._logged = True

                return True
        return False

    def logout(self):
        if self._logged is True:
            self._logged = False

    def hash_pass(self, password: str):
        return bcrypt.hashpw(
            password.encode("utf8"), bcrypt.gensalt())

    def create_user(self, username: str, password: str, email: str):
        "Create a user"

        query = self.database(self.database.users.username == username)

        user_info = query.select(self.database.users.ALL).first()
        if user_info is None:
            if re.fullmatch(REGEX, email) is False:
                return {"id": None,
                        "created": False,
                        "error": "Invalid email"
                        }

            query = self.database(self.database.users.email == email)
            user_info = query.select(self.database.users.ALL).first()
            if user_info is not None:
                return {"id": None,
                        "created": False,
                        "error": "E-mail already registered"
                        }

            hashedpass = self.hash_pass(password)

            if self.has_users is False:
                role = "admin"
                active = True
            else:
                role = "guest"
                active = False

            user = self.database.users.insert(
                username=username,
                email=email,
                password=hashedpass,
                role=role,
                active=active
            )

            self.database.commit()

            return {"id": user,
                    "created": True,
                    "error": None}

        return {"id": None,
                "created": False,
                "error": "User exist"}

    def update_users(self, df_users):
        error = []
        for _, row in df_users.iterrows():
            if self.user['id'] == row['id']:
                continue

            if len(row['password']) >= 8:
                hashedpass = self.hash_pass(row['password'])
            elif len(row['password']) == 0:
                hashedpass = None
            else:
                error = {"id": row['id'],
                         "error": "Password must be at least 8 characters"}
            self.update(row['id'], row['role'], row['active'], hashedpass)
        self.database.commit()
        return error
    

    def update_password(self, id, password):
        hashedpass = self.hash_pass(password)
        query = self.database(self.database.user.id == id)
        query.update(
            password=hashedpass
        )
        self.database.commit()


    def delete_users(self, df_users):
        for _, row in df_users.iterrows():
            if self.user['id'] != row['id']:
                self.database(self.database.users.id ==  row['id']).delete()
        self.database.commit()

    def update(self, id, role, active, hashedpass=None):
        query = self.database(self.database.users.id == id)

        if hashedpass is not None:
            query.update(
                role=role,
                active=active,
                password=hashedpass
            )
        else:
            query.update(
                role=role,
                active=active
            )

    def search_user_by_username(self, username):
        query = self.database(self.database.users.username == username)
        user = query.select(self.database.users.id,
                            self.database.users.username,
                            self.database.users.email,
                            self.database.users.role,
                            self.database.users.active).as_list()
        return pd.DataFrame(user)
    
    def search_user_by_id(self, id):
        query = self.database(self.database.users.id == id)
        user = query.select(self.database.users.id,
                            self.database.users.username,
                            self.database.users.email,
                            self.database.users.role,
                            self.database.users.active).as_list()
        return pd.DataFrame(user)

    def search_user_by_email(self, email):
        query = self.database(self.database.users.email == email)
        user = query.select(self.database.users.id,
                            self.database.users.username,
                            self.database.users.email,
                            self.database.users.role,
                            self.database.users.active).as_list()
        return pd.DataFrame(user)

    def search_user_by_role(self, role):
        query = self.database(self.database.users.role == role)
        user = query.select(self.database.users.id,
                            self.database.users.username,
                            self.database.users.email,
                            self.database.users.role,
                            self.database.users.active).as_list()
        return pd.DataFrame(user)

    def get_users(self):
        users = self.database().select(self.database.users.id,
                                       self.database.users.username,
                                       self.database.users.email,
                                       #    self.database.users.password,
                                       self.database.users.role,
                                       self.database.users.active)
        return pd.DataFrame(users.as_list())
