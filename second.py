#!/usr/bin/env python

"""second.py, By Doron Smoliansky, 2017-1-10
This program crawls through base_url and its sub links
to fill the cart till max_price achieved using selenium
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
base_url = "http://www.iherb.com/Face-Lotions-Cream"
max_price = 500



def go_to_checkout():
    """
    just go to checkout
    """
    driver.get('https://checkout.iherb.com/transactions/checkout')
    form = driver.find_element_by_xpath("//*[@id='login-password-form']")
    form.find_element_by_xpath(".//*[@id='UserName']").send_keys('test@company.com')
    form.find_element_by_xpath(".//*[@id='Password']").send_keys('test@company.com')
    form.find_element_by_xpath(".//*[@name='save']").click()



def add_products_to_cart():
    """
    adjust balance according to actual cart summary, there are discounts that are received only in checkout
    go through products that are in stock, add to cart
    continue till max_price achieved or all products in category were seen
    """
    balance = max_price
    while balance <= max_price:
        wait = WebDriverWait(driver, 5)
        discount = wait.until(EC.element_to_be_clickable((By.ID,'cart-subtotal')))
        discount = discount.text
        discount = float(discount.split('$')[1])
        balance = max_price - discount
        products = driver.find_elements_by_xpath("//*[@itemtype='http://schema.org/Product']")
        for product in products:
            try:
                price = product.find_element_by_xpath(".//*[@class='price ' or @class='price discount-green' ]").text
                price = float(price.split('$')[1])
                add_to_cart = product.find_element_by_xpath(".//*[@name='AddToCart']")
                if balance - price >= 0:
                    balance -= price
                    add_to_cart.click()
            except NoSuchElementException:
                continue
        pagination_last = driver.find_elements_by_xpath("//*[@class='pagination-link']")
        pagination_last = pagination_last[-1].get_attribute('data-url')
        next_page = driver.find_element_by_xpath("//*[@class='pagination-next']").get_attribute('data-url')
        if next_page != pagination_last:
            driver.get(next_page)
        else:
            break


def main():
    driver.get(base_url)
    add_products_to_cart()
    go_to_checkout()
    driver.close()


if __name__=="__main__":
    main()
