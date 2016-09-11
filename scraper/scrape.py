from __future__ import print_function

import sys

if __name__ == "__main__":
    if len(sys.argv) == 1:
        out_file = "../data/company_data.csv"
    else:
        out_file = sys.argv[1]
    print("Writing data to {}.".format(out_file))