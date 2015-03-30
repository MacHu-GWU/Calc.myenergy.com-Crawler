##encoding=UTF-8

"""
This is a script to crawl monthly average bill cost in 2014 by state or city from:
    http://calc.myenergy.com/average
"""

from constant import state_abbr, month_name_map
from util.LINEARSPIDER import *
from util.DATA import *
from bs4 import BeautifulSoup as BS4
import itertools

def parse_cost_from_html(html):
    """get average bill cost value from html
    """
    try:
        soup = BS4(html)
        article = soup.find("article", class_="sub_details")
        h3 = article.find("h3")
        strong = h3.find("strong")
        text = strong.text.strip()
        text = text.replace("$", "")
        text = text[:-1]
        cost = float(text)
        return cost
    except:
        return None
    
def averagebill_search_by_city(month, city, state):
    """a data call by month, city and its state
    """
    spider = Crawler()
    url = "http://calc.myenergy.com/average-bill/%s+%s/%s" % (
        city, state, month_name_map[month])
    url = url.lower()
    html = spider.html(url)
    return parse_cost_from_html(html)

def averagebill_search_by_state(month, state):
    """a data call by month and state
    """
    spider = Crawler()
    url = "http://calc.myenergy.com/average-bill/%s/%s" % (
        state, month_name_map[month])
    url = url.lower()
    html = spider.html(url)
    return parse_cost_from_html(html)

def crawl_all_city():
    """crawl all city average bill cost for every month
    key = "city-state-month"
    """
    averagebill_data_by_county = load_js("averagebill_data_by_county.json")
    county_list = load_js("county_list.json")
    cycle_counter = itertools.cycle(range(12))
    
    for county in county_list:
        for month in range(1, 12+1):
            key = "{0}_{1}_{2}".format(county["city_fullname"], county["state_shortname"], month)
            if key not in averagebill_data_by_county:
                print("crawling %s %s %s" % (month, county["city_fullname"], county["state_shortname"]))
                cost = averagebill_search_by_city(month, county["city_fullname"], county["state_shortname"])
                if cost:
                    averagebill_data_by_county[key] = cost
                    if next(cycle_counter) == 11:
                        safe_dump_js(averagebill_data_by_county, "averagebill_data_by_county.json")
                    
    safe_dump_js(averagebill_data_by_county, "averagebill_data_by_county.json")
     
def crawl_all_state():
    """crawl all state average bill cost for every month
    key = "state-month"
    """
    averagebill_data_by_state = load_js("averagebill_data_by_state.json")
    cycle_counter = itertools.cycle(range(12))
    
    for state in state_abbr.keys():
        state = state.replace(" ", "-")
        for month in range(1, 12+1):
            key = "{0}_{1}".format(state, month)
            if key not in averagebill_data_by_state:
                print("crawling %s %s" % (month, state))
                cost = averagebill_search_by_state(month, state)
                if cost:
                    averagebill_data_by_state[key] = cost
                    if next(cycle_counter) == 11:
                        safe_dump_js(averagebill_data_by_state, "averagebill_data_by_state.json")
    
    safe_dump_js(averagebill_data_by_state, "averagebill_data_by_state.json")

if __name__ == "__main__":
    """uncomment one at one time
    """
    crawl_all_city()
#     crawl_all_state()
    
     
    print("Complete")