import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from tests.ui.test_demoshop_authorize import API_URL_DEMOSHOP, EMAIL_DEMOSHOP, PASSWORD_DEMOSHOP
from tests.test_api import API_URL_REQRES
from utils.base_session import BaseSession

load_dotenv()


@pytest.fixture(scope="session")
def demoshop():
    demoshop_session = BaseSession(API_URL_DEMOSHOP)
    return demoshop_session


@pytest.fixture(scope="session")
def reqres():
    reqres_session = BaseSession(API_URL_REQRES)
    return reqres_session


@pytest.fixture(scope='session', autouse=True)
def app(demoshop):
    WEB_URL_DEMOSHOP = os.getenv("WEB_URL_DEMOSHOP")
    browser.config.base_url = WEB_URL_DEMOSHOP
    response = demoshop.post(url="/login",
                             json={
                                 "Email": EMAIL_DEMOSHOP,
                                 "Password": PASSWORD_DEMOSHOP
                             },
                             allow_redirects=False
                             )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    yield
    browser.quit()
