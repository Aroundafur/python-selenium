#!/usr/bin/env python
# encoding=utf8


"""first.py, By Doron Smoliansky, 2017-1-10
This program crawls through base_url and its sub links
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException



visited = []
driver = webdriver.Chrome()
base_url = "https://www.perimeterx.com/"


def get_links(addr):
    """return all links on page

    """
    visit_link(addr)
    tovisit = []
    links = driver.find_elements_by_xpath("//a[@href]")
    if links:
        for link in links:
            link_addr = link.get_attribute("href")
            if base_url in link_addr:
                if '#' in link_addr:
                    link_addr = link_addr.split('#')[0]
                if not (link_addr in visited):
                    tovisit.append(link_addr)
    tovisit.pop(0)
    return tovisit


def splitParagraphIntoSentences(paragraphs):
    ''' break a paragraph into sentences
        and return a list '''
    import re
    sentences = []
    for paragraph in paragraphs:
        split_paragraph = re.split(',.?',paragraph.text)
        i = 0
        while i < len(split_paragraph):
            p = split_paragraph[i]
            if len(sentences) ==     3:
                return sentences
            elif p:
                sentences.append(p)
            i+=1

def visit_link(addr):
    """Go to link addr, mark as "visited",
       get 3 santences from visited page
    """

    if not (addr in visited):
        print addr
        driver.get(addr)
        visited.append(addr)
        try:
            paragraph = driver.find_elements_by_xpath("//body//p[text()]")
            paragraph = splitParagraphIntoSentences(paragraph)
            if paragraph is not None:
                for p in paragraph:
                    print p
            else:
                print "No sentences on this page. ($x('//body//p[text()]') = []])"
        except NoSuchElementException:
            pass



def visit_all_links(url):
    """visit all links on page
       visit all links on sub pages
    """
    for i in get_links(url):
        for j in get_links(i):
            visit_link(j)

if __name__=="__main__":
    visit_all_links(base_url)
    driver.close()
