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

    return url_str + "?" + params_str

if __name__ == "__main__":
    if len(sys.argv) == 1:
        out_file = "../data/company_data.csv"
    else:
        out_file = sys.argv[1]
    print("Writing data to {}.".format(out_file))