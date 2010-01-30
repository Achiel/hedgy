#!/opt/local/bin/python2.5

import sys

def _function_id(obj, nFramesUp):
    """ Create a string naming the function n frames up on the stack. """
    fr = sys._getframe(nFramesUp+1)
    co = fr.f_code
    return "%s.%s" % (obj.__class__, co.co_name)

def abstract_method(obj=None):
    """ Use this instead of 'pass' for the body of abstract methods. """
    raise Exception("Unimplemented abstract method: %s" % _function_id(obj, 1))

class Parser:
	
	# need to override this method to conform to interface:
	def parse(self, url, out):
		abstract_method(self)
		
	def calc_odds(self, string):
		if string == "evens":
			return 1.0
		odds = string.partition("/")
		return float(odds[0])/float(odds[2])
		