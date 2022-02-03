import time
from pathlib import Path
from typing import Dict

import requests
from PIL import Image, ImageOps
from hydralit import HydraHeadApp
import streamlit as st
import hydralit as hy
import hydralit_components as hc
from itertools import cycle

API_URL = "http://127.0.0.1:5000/api/v1"


class LandingScreen(HydraHeadApp):
    def __init__(self, title):
        self.title = title

    def run(self):
        st.info('Hello from cool app 1')


class LoginApp(HydraHeadApp):
    """
    This is an example login application to be used to secure access within a HydraApp streamlit application.
    This application implementation uses the allow_access session variable and uses the do_redirect method if the login check is successful.

    """

    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self) -> None:
        """
        Application entry point.
        """

        st.markdown("<h1 style='text-align: center;'>Recommender Login</h1>", unsafe_allow_html=True)

        c1, c2, c3, = st.columns([2, 2, 2])
        c3.image("lock.png", width=100, )
        c3.image("hydra.png", width=100, )

        form_data = self._create_login_form(c2)

        pretty_btn = """
        <style>
        div[class="row-widget stButton"] > button {
            width: 100%;
        }
        </style>
        <br><br>
        """
        c2.markdown(pretty_btn, unsafe_allow_html=True)

        if form_data['submitted']:
            self._do_login(form_data, c2)

    def _create_login_form(self, parent_container) -> Dict:

        login_form = parent_container.form(key="login_form")

        form_state = {}
        form_state['username'] = login_form.text_input('Username', value="673536333")
        form_state['password'] = login_form.text_input('Password', type="password", value="password")
        form_state['submitted'] = login_form.form_submit_button('Login')
        return form_state

    def _do_login(self, form_data, msg_container) -> None:
        response = requests.post(API_URL + "/auth/login",
                                 json={'username': form_data['username'], 'password': form_data['password']})
        if response.status_code == 200:
            st.session_state['user'] = response.json()
            msg_container.success(f"✔️ Login success")
            with st.spinner("🤓 now redirecting to application...."):
                time.sleep(1)
                self.set_access(2, response.json()['first_name'])
                self.do_redirect()
        else:
            st.write("login failed")
            self.session_state.allow_access = 0
            self.session_state.current_user = None
            msg_container.error(f"❌ Login unsuccessful, 😕 please check your username and password and try again.")


def get_recommended_products_for_user(user_id):
    response = requests.get(API_URL + f'/users/{user_id}/recommended-products?algorithm=hybrid')
    return response.json()


class DashboardApp(HydraHeadApp):
    def run(self):
        access, user_name = self.check_access()
        if access == 1:
            st.write("Hello Guest")
        else:
            data = get_recommended_products_for_user(st.session_state['user']['id'])
            st.write("Recommended For You")
            cols = cycle(st.columns(5))
            for i, item in enumerate(data):
                col = next(cols)
                if not item['images']:
                    original_image = Image.open("placeholder.png")
                    size = (256, 256)
                    fit_and_resized_image = ImageOps.fit(original_image, size, Image.ANTIALIAS)
                    col.image(fit_and_resized_image, width=256, caption=item['label'])
                else:
                    col.image(item['images'][0]['256'], width=256, caption=item['label'])
                col.text(item['selling_price'])
                col.button("Detail", key=item['id'])


class LogoutApp(HydraHeadApp):
    def run(self):
        st.write("Logout App")


app = hy.HydraApp(title='Simple Multi-Page App', hide_streamlit_markers=False)

app.add_app("Home", icon="📚", app=DashboardApp(), is_home=True)
app.add_app("Login", app=LoginApp(), is_login=True, logout_label="Logout")

app.enable_guest_access()

user_access_level, username = app.check_access()

if user_access_level == 0:
    complex_nav = {
        'Home': ['Home'],
        'Login': ['Login']
    }
else:
    complex_nav = {
        'Home': ['Home']
    }


@app.login_callback
def after_login():
    # app.run(complex_nav)
    pass


app.run(complex_nav)
