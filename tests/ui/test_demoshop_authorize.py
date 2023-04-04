import os
import allure
from dotenv import load_dotenv
from selene.support.conditions import have
from selene.support.shared import browser


load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
API_URL = os.getenv("API_URL_DEMOSHOP")
WEB_URL = os.getenv("WEB_URL_DEMOSHOP")
browser.config.base_url = WEB_URL


def test_login_successful():
    with allure.step("Open login page"):
        browser.open("/login")

    with allure.step("Fill login form"):
        browser.element("#Email").send_keys(EMAIL)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(EMAIL))


def test_login_through_api(demoshop):
    response = demoshop.post(
        url="/login",
        json={
            "Email": f'{EMAIL}',
            "Password": f'{PASSWORD}',
            "RememberMe": True
        },
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/Themes/DefaultClean/Content/Image/logo.png")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})
    browser.open("")

    with allure.step("Verify successful authorization"):
        browser.element(".account").should(have.text(f'{EMAIL}'))


def test_add_product_to_cart(demoshop):
    response = demoshop.post(
        url="/login",
        json={
            "Email": f'{EMAIL}',
            "Password": f'{PASSWORD}',
            "RememberMe": True
        },
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/books")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})

    with allure.step("Add product to cart"):
        demoshop.post(url="/addproducttocart/catalog/13/1/1")

    with allure.step("Open cart"):
        browser.open("/cart")

    with allure.step("Check added product"):
        browser.element(".product-name").should(have.text("Computing and Internet"))


def test_add_product_to_wishlist(demoshop):
    response = demoshop.post(
        url="/login",
        json={
            "Email": f'{EMAIL}',
            "Password": f'{PASSWORD}',
            "RememberMe": True
        },
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/album-3")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})

    with allure.step("Add product to wishlist"):
        demoshop.post(url="/addproducttocart/details/53/2")

    with allure.step("Open wishlist"):
        browser.open("/wishlist")

    with allure.step("Check added product"):
        browser.element('.wishlist-content').should(have.text("3rd Album"))


def test_remove_product_from_wishlist(demoshop):
    response = demoshop.post(
        url="/login",
        json={
            "Email": f'{EMAIL}',
            "Password": f'{PASSWORD}',
            "RememberMe": True
        },
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/album-3")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})

    with allure.step("Add product to wishlist"):
        demoshop.post(url="/addproducttocart/details/53/2")

    with allure.step("Open wishlist"):
        browser.open("/wishlist")

    with allure.step("Check added product"):
        browser.element('.wishlist-content').should(have.text("3rd Album"))

    with allure.step("Remove item from wishlist"):
        browser.element('[name="removefromcart"]').click()
        browser.element('.update-wishlist-button').click()

    with allure.step("Check removed products"):
        browser.open("/wishlist")
        browser.element('.wishlist-content').should(have.text('The wishlist is empty!'))


def test_remove_product_from_cart(demoshop):
    response = demoshop.post(
        url="/login",
        json={
            "Email": f'{EMAIL}',
            "Password": f'{PASSWORD}',
            "RememberMe": True
        },
        allow_redirects=False
    )
    authorization_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
    browser.open("/books")
    browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie})

    with allure.step("Add product to cart"):
        demoshop.post(url="/addproducttocart/catalog/13/1/1")

    with allure.step("Open cart"):
        browser.open("/cart")

    with allure.step("Check added product"):
        browser.element(".product-name").should(have.text("Computing and Internet"))

    with allure.step("Remove item from wishlist"):
        browser.element('[name="removefromcart"]').click()
        browser.element('.update-cart-button').click()

    with allure.step("Check removed products"):
        browser.open("/cart")
        browser.element('.order-summary-content').should(have.text('Your Shopping Cart is empty!'))

