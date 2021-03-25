from model.group import Group
import random
import string


constant = [Group(name="name1", header="header1", footer="footer1"),
            Group(name="name2", header="header2", footer="footer2")]


# if generated ' symbol (string.punctuation) will cause failed test (it is a bug in the app)
def random_string(prefix, maxlen):
    symbols = string.ascii_letters +string.digits + string.punctuation + " "*10
    return prefix + "".join([random.choice(symbols) for _i in range(random.randrange(maxlen))])


# 1 case with all empty fields and 2 cases with all filled fields
testdata = [Group(name="", header="", footer="")] + \
           [Group(name=random_string("name", 5), header=random_string("header", 5), footer=random_string("footer", 5))
            for i in range(2)]

# 8 cases with combinations empty/filled
# testdata = [Group(name=name, header=header, footer=footer)
#             for name in ["", random_string("name", 5)]
#             for header in ["", random_string("header", 5)]
#             for footer in ["", random_string("footer", 5)]]