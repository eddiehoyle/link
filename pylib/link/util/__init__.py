# import os
# __files = os.listdir(os.path.dirname(__file__))
# __modules = [os.path.basename(os.path.splitext(f)[0]) for f in __files if os.path.splitext(f)[1] == ".py" and not f.startswith("__")]

# for __mod in __modules:
#     __import__('link.util.%s' % __mod)
from link.util import attr, common, name, part, anno, shape
