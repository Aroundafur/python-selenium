# python-selenium


# install dependencies

run python setup.py

or manually:

make sure you have pip installed

https://pip.pypa.io/en/stable/installing/

make sure you have selenium installed

pip install selenium


#first.py, By Doron Smoliansky, 2017-1-10

This program crawls through base_url and its sub links using selenium

run with: python first.py


#second.py, By Doron Smoliansky, 2017-1-10

This program crawls through base_url and its sub links
to fill the cart till max_price achieved using selenium

run with: python second.py

#third.py, By Doron Smoliansky, 2017-1-10

program creates API call, and runs tests 3 tests:

1. valid requests that receive a valid response (valid was 400 for me)

2. Invalid request for timestamps out of range

3. Invalid request for threshold out of range

tests are made with doctest module - and written as documentation

run with: python third.py -v
