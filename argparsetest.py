#the first step in creating an argparse script... importing argparse
import argparse


#   for custom actions, it becomes necessary to create an Action child class
#   'def __call__(self, parser, namespace, values):' is necessary.
#   As the name might suggest, option_string isn't.

class FooAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
       print('Hello, world!')
       setattr(namespace, self.dest, values)
class BarAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
       print('%r %r %r' % (namespace, values, option_string))
       setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser()
parser.add_argument('--foo', action=FooAction)
parser.add_argument('--bar', action=BarAction)

#   parse_args passes the arguments given by the user into the ArgumentParser
#   that was created above.  It can also be used to call actions manually:
#      parser.parse_args('--foo 1 bar'.split())

args = parser.parse_args()
print(args)
