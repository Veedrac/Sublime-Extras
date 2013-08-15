"""
This one is mine. You can do what the hell you want with it.

This needs to be polished before you can use it, btw. It also
requres a generated file that, well, you don't have.

The idea is more complicated than the others -- on my keyboard
on my Linux installation, "ALT-GR" + most keys makes a Unicode
symbol (such as þ, ø, ĸ and ł). This make a very clever auto-
complete for words starting in any non-ASCII symbol, such as
øinf (which can autocomplete to ∞, ℹ, ⧞, and many more). This
is really useful for quick Unicode, and doesn't cause any
slowdown except at load (about ¼𝗌) and when actually using it
(mostly unnoticeable), AFAICT.

I *will* clean up the code sometime. Just not right now.
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