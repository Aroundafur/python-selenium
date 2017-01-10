#!/usr/bin/env python

"""main.py, By Doron Smoliansky, 2017-1-10
This program crawls through base_url and its sub links
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


visited = []
driver = webdriver.Chrome()
base_url = "https://www.perimeterx.com/"

def get_links(addr):
    tovisit = []
    links = visit_link(addr)
    if links:
        for link in links:
            link_addr = link.get_attribute("href")
            if base_url in link_addr:
                tovisit.append(link_addr)
    return tovisit

def visit_all_links(addr_list):
    if len(addr_list) > 1:
        for link in addr_list:
            visit_all_links(get_links(link))
    else:
         driver.execute_script("window.history.go(-1)")

def visit_link(addr):
    if not (addr in visited):
        driver.get(addr)
        visited.append(addr)
        print addr
        return driver.find_elements_by_xpath("//a[@href]")

def main():
    visit_all_links(get_links(base_url))
    driver.close()


if __name__=="__main__":
    main()
