import os
import pytest
from dotenv import load_dotenv
from selene.support.shared import browser
from tests.ui.test_demoshop_authorize import API_URL, EMAIL, PASSWORD
from utils.base_session import BaseSession

load_dotenv()


@pytest.fixture(scope="session")
def demoshop():
    demoshop_session = BaseSession(API_URL)
    return demoshop_session


@pytest.fixture(scope='session', autouse=True)
def app(demoshop):
    WEB_URL = os.getenv("WEB_URL_DEMOSHOP")
    browser.config.base_url = WEB_URL
    response = demoshop.post(url="/login",
                             json={
                                 "Email": EMAIL,
                                 "Password": PASSWORD
                             },
                             allow_redirects=False
                             )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/Themes/DefaultClean/Content/images/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    yield
    browser.quit()
