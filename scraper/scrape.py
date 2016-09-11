from __future__ import print_function

import sys

from string import ascii_uppercase

import urllib2
import bs4

def get_url_params_kv(url_str):
    """
    In a url, the parameters are everything after the first question mark in a GET request.
    So in www.example.com/yyy?zzz=123&yyy=456 the params_kv will be {"zzz": "123", "yyy": "456"}.
    kv stands for key/value.
    """
    try:
        params_str = url_str.split("?")[1:][0]
    except IndexError:
        # No parameters in the url.
        return {}
    params = params_str.split("&")
    params = list(map(lambda param_str: param_str.split("="), params))
    params_kv = {
        param: value for param, value in params
    }

    return params_kv

def construct_url_with_params(url_str, params_kv):
    # Get the list of params in the format ["a=1", "b=2"...].
    params_list = [k+"="+v for k, v in params_kv.items()]

    # Get the parameters string in the format a=1&b=2...
    params_str = "&".join(params_list)

    return url_str.split("?")[0] + "?" + params_str

def get_next_page(url_str):
    """
    In our case, the url looks like this: http://www.ic.gc.ca/app/ccc/sld/cmpny.do?letter=0&lang=eng&profileId=2059&tag=025015.
    The page part is the letter parameter, which goes from 0-9 and A-Z. So going to the next page just means incrementing that
    parameter. When at the last page, None is returned.
    """
    def get_char_after(curr_char):
        """
        Gets the character right after the current one.
        For example, the character after '0' is '1', the one after '9' is 'A', and the one after 'Z' is None.
        """
        # Get the list of numbers and letters to determine the next character.
        nums    = list(map(str, range(0,10)))
        letters = list(ascii_uppercase)
        all_chars = nums+letters

        curr_index = all_chars.index(curr_char)
        if curr_index == len(all_chars)-1:
            # We are on the last page.
            return None
            
        return all_chars[curr_index+1]

    url_params = get_url_params_kv(url_str)
    try:
        current_page_char = url_params["letter"]
    except:
        return None
    
    next_page_char = get_char_after(current_page_char)
    if next_page_char is None:
        return None

    # Change the value of the parameter and construct the new url.
    url_params["letter"] = next_page_char
    return construct_url_with_params(url_str, url_params)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        out_file = "../data/company_data.csv"
    else:
        out_file = sys.argv[1]
    print("Writing data to {}.".format(out_file))