"""
This is hereby released completely and irrevocably into the Public Domain.

- Joshua Landau <joshua@landau.ws>
"""


import sublime, sublime_plugin
from itertools import chain, groupby

class SplitSelectionIntoCharsCommand(sublime_plugin.TextCommand):
	"""
	Take a selection and tare it to *shreds*!

	Breaks a selection into characters.
	"""
	def run(self, edit):
		[*old_selections] = selections = self.view.sel()
		selections.clear()

		for selection in old_selections:
			for character_pos in range(selection.begin(), selection.end()):
				selections.add(sublime.Region(character_pos, character_pos+1))


class SplitSelectionIntoWordsCommand(sublime_plugin.TextCommand):
	"""
	Select all the words intersecting each of your current selections.
	"""
	def run(self, edit):
		[*old_selections] = selections = self.view.sel()
		selections.clear()

		for selection in old_selections:
			# Iterate through each of the characters in the selections
			position = selection.begin()
			while position <= selection.end():

				# Get the surrounding word
				word = self.view.word(position)
				word_string = self.view.substr(word)

				# This prevents sublime's pure-spacing or pure-operator "words"
				if any(char.isidentifier() or char.isalnum() for char in word_string):
					selections.add(word)

				# SKIIIPPPP
				position += len(word) or 1

class RemoveBlankLineSelectionsCommand(sublime_plugin.TextCommand):
	"""
	Split all selections by blank lines, discarding all that are on
	blank lines.

	This is useful for filtering cursors as well as splitting regions.
	"""
	def run(self, edit, forward):
		[*old_selections] = selections = self.view.sel()

		selections.clear()

		# For each selection
		for selection in old_selections:
			# Get the lines that it interscts
			lines = self.view.lines(selection)
			# Make a new selection that starts where selection does
			new_selection = sublime.Region(selection.begin(), selection.begin())

			# For each line it intersects
			for line in lines:
				# Add the line if it is nonempty
				if line:
					new_selection.b = line.end()

				# We don't get trailing blank lines, so
				# this can only occur if either the selection is
				# a character or it's in the middle of a block
				else:
					if new_selection:
						selections.add(new_selection)

					new_selection = sublime.Region(line.begin()+1, line.begin()+1)

			# Either this is a block or a single character

			# new_selection.b can be past the end of the original, if it didn't
			# go to the end of the line
			new_selection.b = min(new_selection.b, selection.end())

			# Single characters on blank lines have the odd property of starting
			# on the next line but, due to the line above, ending on the original
			if new_selection.a <= new_selection.b:
				selections.add(new_selection)


class EveryNthSelectionCommand(sublime_plugin.TextCommand):
	"""
	Keep or remove every nth selection.

	This has 0-based indexing, so the first selection will always
	be the "first of the nth".

	If there is only one selection, it is first split into lines.
	"""
	def run(self, edit, n, filter):
		selections = self.view.sel()

		if len(selections) == 1:
			self.view.run_command("split_selection_into_lines")
			selections = self.view.sel()

		old_selections = list(selections)
		selections.clear()

		filter = {"remove": True, "keep": False}[filter]

		for i, selection in enumerate(old_selections):
			if bool(i%n) == filter:
				selections.add(selection)



class CombineSelections(sublime_plugin.TextCommand):
	"""
	Join selections together. Will join within lines
	if within_lines is True (default) and there is
	at least one line with multiple selections.
	"""

	def run(self, edit, within_lines=True):
		[*old_selections] = selections = self.view.sel()
		selections.clear()

		def selection_to_line(selection):
			return self.view.rowcol(selection.begin())[0]

		# Default, no grouping
		grouper = (lambda _: True)

		# Group by lines
		def line_grouper(selection):
			return self.view.rowcol(selection.begin())[0]


		if within_lines:
			# Is there no line with multiple selections?
			for category, group in groupby(old_selections, key=line_grouper):
				if sum(1 for _ in group) > 1:
					grouper = line_grouper


		for category, group in groupby(old_selections, key=grouper):
			first = next(group)
			for last in chain([first], group):
				pass

			selections.add(sublime.Region(first.begin(), last.end()))