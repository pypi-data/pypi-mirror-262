""" stauth - Authenticator for Streamlit using pydal to save user info in database.
"""
import streamlit as st
from .stauth import STAuth
__AUTHOR = "Eduardo S. Pereira"
__EMAIL = "eduardo.spereira@sp.senai.br"
__DATE = "09/10/2023"

__version__ = "0.1.0"


class AdminUsers:
    def __init__(self, auth: STAuth):
        self._auth = auth

        self._session_state = st.session_state
        self._login_section = st.container()
        self._logout_section = st.container()

        self._start()

    def _start(self):

        if 'createUser' not in self._session_state:
            self._session_state.createUser = False

        if 'user' not in self._session_state:
            self._session_state.user = None

        if 'has_users' not in self._session_state:
            self._session_state.has_users = self.auth.has_users

        if 'loggedIn' not in self._session_state:
            self._session_state['loggedIn'] = False

        if 'sign' not in self._session_state:
            self._session_state['sign'] = False

    @property
    def session_state(self):
        return self._session_state

    @property
    def login_section(self):
        return self._login_section

    @property
    def logout_section(self):
        return self._logout_section

    @property
    def auth(self):
        return self._auth

    @property
    def user(self):
        return self._session_state.user

    @property
    def has_users(self):
        if 'has_users' not in self._session_state:
            self._session_state.has_users = False
        self._session_state.has_users = self.auth.has_users
        return self._session_state.has_users

    def login_button(self, username, password):
        if self.auth.login(username, password):
            st.empty()
            self._session_state.user = self.auth.user
            self._session_state['loggedIn'] = True
        else:
            st.error("Wrong User or Password")

    def logout(self):
        # Not use in callback
        st.empty()
        self._session_state['sign'] = False
        self._session_state['loggedIn'] = False
        st.rerun()

    def logout_button(self):
        # logout for callback
        st.empty()
        self._session_state['sign'] = False
        self._session_state['loggedIn'] = False
        st.rerun

    def sign_button(self):
        if self._session_state['loggedIn'] is False:
            self._session_state['sign'] = True

    def button_createUser_pressed(self):
        if self._session_state.createUser is False:
            self._session_state.createUser = True
            return
    def button_update_my_user_pressed(self):
        if self._session_state.update_my_user is False:
            self._session_state.update_my_user = True
            return

    def create_user(self, username, email, password, rpassword):

        if  self.has_users is False or self.user['role'] == 'admin':
            if password != rpassword:
                st.error("Password is not equals!")
                return
            elif len(password) < 8:
                st.error("Password must have at least 8 characters!")
                return

            new_user = self.auth.create_user(username, password, email)
            self._session_state.createUser = False

            if new_user["error"]:
                st.error(new_user["error"])
        else:
            st.error("Forbiden Operation! Only Admin")
        
        if  self.has_users is False:
            st.rerun()

    def update_my_user(self, id, password, rpassword):

        if self.user is not None and self.user['id'] == id:
            if password != rpassword:
                st.error("Password is not equals!")
                return
            elif len(password) < 8:
                st.error("Password must have at least 8 characters!")
                return
            error = self.auth.update_password(id, password)


    def page_to_create_user_as_admin(self):

        if self.has_users is True and self.user is None:
            self.logout()
            return
            
    
        if  self.has_users is False or self.user['role'] == 'admin':
            st.markdown("## Add New User: ")

            with st.form("login-form"):
                username = st.text_input(
                    label="User Name", value="", placeholder="Enter your user name")

                email = st.text_input(
                    label="e-mail", value="", placeholder="Enter your e-mail")

                password = st.text_input(
                    label="Password", value="", placeholder="Enter password", type="password")

                rpassword = st.text_input(
                    label="Password", value="", placeholder="Repit the password", type="password")

                if st.form_submit_button("Create",
                                         on_click=self.button_createUser_pressed
                                         ):
                    self.create_user(username, email, password, rpassword)

    def page_to_admin_users(self):
        if self.user['role'] == 'admin':

            if 'dfuser' not in self._session_state:
                self._session_state.dfuser = None

            if 'changesuser' not in self._session_state:
                self._session_state.changesuser = None

            self._session_state.dfuser = self.auth.get_users()
            self._session_state.dfuser = self._session_state.dfuser[self._session_state.dfuser['id'] != self.user['id']]
            self._session_state.dfuser["password"] = ''

            def update_users():
                if self._session_state.changesuser is not None:                    
                    error = self.auth.update_users(self._session_state.changesuser)
                    st.success("Update Completed!")
                else:
                    st.success("No changes to Update!")

            st.markdown("## Update Users")

            st.button("Update", on_click=update_users)

            users = st.data_editor(self._session_state.dfuser,
                                   column_config={
                                       "role": st.column_config.SelectboxColumn(
                                           "role",
                                           help="The role of user",
                                           width="medium",
                                           options=[
                                                "admin",
                                                "guest",
                                           ],
                                           required=True,
                                       )
                                   },
                                   disabled=["id", "email", "username"],
                                   hide_index=True)

            is_equal = users.equals(self._session_state.dfuser)
            if is_equal is False:
                self._session_state.changesuser = users[users.ne(
                    self._session_state.dfuser).any(axis=1)]

    def page_to_delete_user(self):
        if self.user['role'] == 'admin':

            if 'dfuserdel' not in self._session_state:
                self._session_state.dfuserdel = None

            if 'changesuserdel' not in self._session_state:
                self._session_state.changesuserdel = None

            self._session_state.dfuserdel = self.auth.get_users()
            self._session_state.dfuserdel = self._session_state.dfuserdel[self._session_state.dfuserdel['id'] != self.user['id']]
            self._session_state.dfuserdel["delete"] = False

            def update_users():
                error = self.auth.delete_users(
                    self._session_state.changesuserdel)
                st.success("Users Deleted!")
                

            st.markdown("## Delete Users")

            st.button("Delete Selected Users", on_click=update_users)

            users = st.data_editor(self._session_state.dfuserdel,
                                   column_config={
                                       "role": st.column_config.SelectboxColumn(
                                           "role",
                                           help="The role of user",
                                           width="medium",
                                           options=[
                                                "admin",
                                                "guest",
                                           ],
                                           required=True,
                                       )
                                   },
                                   disabled=["id", "email",
                                             "username", 'role',
                                             'active'],
                                   hide_index=True)

            is_equal = users.equals(self._session_state.dfuserdel)

            if is_equal is False:
                self._session_state.changesuserdel = users[users.ne(
                    self._session_state.dfuserdel).any(axis=1)]

    def login_page(self):

        with self._login_section:

            if self.has_users is False:
                self._session_state['sign'] = True

            if self._session_state['loggedIn'] is False and self._session_state['sign'] is False:
                if self.has_users is False:
                    self._session_state['sign'] = True

                # with st.form("login-form"):
                username = st.text_input(
                    label="Name", value="", placeholder="Enter your user name")
                password = st.text_input(
                    label="Password", value="", placeholder="Enter password", type="password")

                cols = st.columns(5)

                with cols[2]:
                    st.button("Login",
                              on_click=self.login_button,
                              args=(username, password)
                              )

            elif self._session_state['sign'] is True:
                self.page_to_create_user_as_admin()

    def logout_page(self):

        with self._logout_section:
            cols = st.columns(5)

            with cols[4]:
                st.button("Logout",
                          on_click=self.logout_button
                          )
                
    def page_my_account(self):
        st.markdown("## My Account Informations")
        df = self.auth.search_user_by_id(self.user['id'])[['username', 'email', 'role']]
        st.dataframe(df, hide_index=True)

        st.markdown("## Change Password!")

        if 'update_my_user' not in self._session_state:
            self._session_state.update_my_user = False
        
        with st.form("login-form"):

                password = st.text_input(
                    label="Password", value="", placeholder="Enter password", type="password")

                rpassword = st.text_input(
                    label="Password", value="", placeholder="Repit the password", type="password")

                if st.form_submit_button("Update Password",
                                         on_click=self.button_update_my_user_pressed
                                         ):
                    self.update_my_user(self.user['id'], password, rpassword)

