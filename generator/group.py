from model.group import Group
import random
import string
import os.path
import jsonpickle
import getopt
import sys


try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

# default parameters
n = 2
f = "data/groups.json"
# in parameters of script specify "-n 10 -f data/test.json"
for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


# if generated ' symbol (string.punctuation) will cause failed test (it is a bug in the app)
def random_string(prefix, maxlen):
    symbols = string.ascii_letters +string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for _i in range(random.randrange(maxlen))])


# 1 case with all empty fields and 2 cases with all filled fields
testdata = [Group(name="", header="", footer="")] + \
           [Group(name=random_string("name", 5), header=random_string("header", 5), footer=random_string("footer", 5))
            for i in range(n)]

# 8 cases with combinations empty/filled
# testdata = [Group(name=name, header=header, footer=footer)
#             for name in ["", random_string("name", 5)]
#             for header in ["", random_string("header", 5)]
#             for footer in ["", random_string("footer", 5)]]


file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

with open(file, "w") as out:
    # out.write(json.dumps(testdata, default=lambda x: x.__dict__, indent=4))
    # instead of 'json' using 'jsonpickle'
    jsonpickle.set_encoder_options("json", indent=4)
    out.write(jsonpickle.encode(testdata))
