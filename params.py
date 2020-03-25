"""Streamlined parameter handling with the *Params* object. From the usual
   *__main__* conditional, usage naturally follows the *sys.argv* input:
    > p = params.Params(sys.argv, ['flag1', 'flag2'])
	
   The *flags* list defines what parameters the parser should anticipate as
   key-only arguments. All others are expected to be key=value strings, except
   the first (which will be the name of the invoked Python file). All parameter
   keys are assumed to be case-insensitive.
   
   The *Params* object provides a *get* method for accessing required,
   optional, and flag (key-only) parameters. Required parameters are accessed
   by invoking *get* with the key::
   
   > value1 = p.get('key1')
   
   If the required value is not in the parsed argument dictionary, an exception
   will be raised.
   
   Developers indicate a parameter is optional by providing a second argument,
   the default value of the parameter:
    > value2 = p.get('key2', 'value2')
	
   If the key does not exist in the parsed argument dictionary, the default
   value will be returned instead.
   
   Flags (key-only) parameters are stored with the value *True* in the parsed
   argument dictionary if they are included in the original argument vector. If
   they were not included, the value *False* will be returned instead:
    > flag1 = p.get('flag1')
	
   Recall that parameters are interpreted as flags (key-only) if the key was
   listed in the original constructor invocation.
"""

import warnings

class Params(object):
	"""Encapsulation for parsing and extending argument vector (a la *sys.argv*)
	   with required and optional argument accessor. By default, all arguments
	   are assumed to be key-value pairs. Flagged parameters (key-only) can be
	   provided as an optional constructor argument.
	"""
	
	def __init__(self, argv, flags=[]):
		"""Parses an *argv* list into an *args* dictionary, which is then saved
		   as the object state for later queries. Optional argument *flags*
		   indicates key-only parameters, interpreted as *True* if included in
		   the argument list. Accessor methods will return *False* if these
		   parameters are not included in *argv* but are included in *flags*.
		"""
		self.flags = [f.lower() for f in flags]
		self.argv = argv # useful for debugging, fallback flags
		keys = []
		values = []
		for arg in argv[1:]:
			parts = arg.split('=')
			if len(parts) == 2:
				# key=value parameter
				keys.append(parts[0].lower())
				values.append(parts[1])
			elif arg.lower() in self.flags:
				# key-only parameter
				keys.append(arg.lower())
				values.append(True)
			else:
				# Not key=value, not in flags
				#warnings.warn('Unable to parse argument "%s"; skipping...' % arg)
				pass
		self.args = dict(zip(keys, values))
		
	def get(self, key, default=None):
		"""Returns value of the given parameter. If the key is not in the
		   argument dictionary (i.e., it was not provided), there are three
		   possible outcomes:
		   #. If a default value is provided, it will be returned instead.
		   #. If the key is in the *flags* list, *False* will be returned (as
		      the flag was not included in the argument vector).
		   #. Lastly, an error will be raised because a required parameter was
		      not included in the argument vector.
		"""
		key = key.lower()
		if key in self.args:
			return self.args[key]
		if default is not None:
			return default
		if key in self.flags:
			return False
		raise Exception('Parameter "%s" is required' % key)
