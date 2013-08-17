"""
When first started with this extension Sublime Text will take a few
seconds to generate a half-megabyte ".sublime/unicode cache.picke.gz"
file. Afterwards Unicode autocomplete should *just work*. If you have
"Alt Gr" on your keyboard, on Linux you should be able to do "Alt Gr+p"
to write "þ". When a word starts with a non-ASCII character it will be
autocompleted into Unicode, searching by name.

If you don't have "Alt Gr", a "£", "€" or "¬" may be relevant
non-ASCII characters you do have.

The project that inspired this was UnicodeMath, an alternate
TeX-like input mechanism. (https://github.com/mvoidex/UnicodeMath)

This is hereby released completely and irrevocably into the Public Domain.

- Joshua Landau <joshua@landau.ws>
"""

import sublime
import sublime_plugin

import pickle
import gzip

from os.path import exists, expanduser, join
from unicodedata import lookup as unilookup

# Setup for autocomplete data

cache_file_path = join(expanduser("~"), ".sublime", "unicode cache.pickle.gz")

if not exists(cache_file_path):
	from . import unicodecomplete_create_cache
	unicodecomplete_create_cache.main()

# Load cache
with gzip.GzipFile(cache_file_path, 'rb') as cache:
	unicode_names, unicode_extras = pickle.load(cache)


#############################################################################

# Autocomplete service


def get_prefixed(view, location) -> "(str, str)":
	"""Get the 'trigger' from the current location.

	In running text a word where the first character is
	non-ASCII will trigger autocomplete, this returns
	a 2-tuple of the prefix and the rest of the word.
	"""
	line_before_cursor = view.substr(sublime.Region(view.line(location).a, location))
	current_word = line_before_cursor.split()[-1]

	if not current_word:
		return "", ""

	prefix, word = current_word[0], current_word[1:]

	# If not ASCII
	if ord(prefix) > 128:
		return prefix, word

	else:
		return "", ""

def make_completion(unicode_name, prefix, character=None):
	"""Make a nicely formatted tuple that on_query_completions will accept as a completion."""
	if character is None:
		character = unilookup(unicode_name)

	return "{} {}\t{}".format(prefix, unicode_name.title(), character), character

class UnicodeMathComplete(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		prefix, word = get_prefixed(view, locations[0])

		if len(word) <= 1:
			return None

		completions = [make_completion(completion, prefix) for completion in unicode_names[word[:2].upper()]]

		completions.extend(make_completion(completion, prefix, character) for character, completion in unicode_extras[word[:2].upper()])

		return completions, 0

	def on_query_context(self, view, key, operator, operand, match_all):
		# I'm not sure why, but everything else is just bad, so do this
		return False