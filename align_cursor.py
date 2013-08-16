"""
All of this is mine. You can do what the hell you want with it.
"""


import sublime, sublime_plugin

class AlignCursor(sublime_plugin.TextCommand):
	"""
	Align the cursors to the first cursor, using the characters in the selection
	if possible, otherwise using the characters on either side of the cursor.

	It will extend if any cursor is a selection, otherwise it will move.
	"""
	def run(self, edit, extend=False):
		selections = self.view.sel()

		if not selections:
			return

		first_selection, *rest = selections
		selections.clear()
		selections.add(first_selection)

		first_selection_line = self.view.line(first_selection.b)
		first_selection_line_chars = self.view.substr(first_selection_line)
		row, column = self.view.rowcol(first_selection.b)


		# Get where each cursor aims to be
		if first_selection and not extend:
			str_end = first_selection.end() - first_selection_line.begin()
			target = self.view.substr(first_selection)

			# I can't handle this!
			# What's a good, easy-to understand behaviour?
			# Exactly - there isn't one.
			if "\n" in target:
				return

			side = "left" if first_selection.a > first_selection.b else "right"

		else:

			if column == 0:
				target = first_selection_line_chars[:1]
				side = "left"

			elif column == len(first_selection_line):
				target = first_selection_line_chars[-1:]
				side = "right"

			else:
				target = first_selection_line_chars[column-1:column+1]
				side = "center"

			str_end = column + 1

		# str.startswith(sub, start) == str[start:].startswith(sub)
		# This method accepts overlapping substrings so is better than str.count
		possible_indexes = range(len(first_selection_line_chars) - len(target) + 1)
		count = sum(first_selection_line_chars.startswith(target, i, str_end) for i in possible_indexes)


		# Put them there
		for selection in rest:
			line = self.view.line(selection.b)
			line_chars = self.view.substr(line)

			# Just like with generating count, except a filtered list rather than a boolean generator
			possible_indexes = range(len(line_chars) - len(target) + 1)
			positions = [i for i in possible_indexes if line_chars.startswith(target, i)]

			try:
				# Get "count-1"th item, defauling to last
				[start] = positions[count-1:count] or positions[-1:]

			except ValueError:
				continue

			start += line.begin()
			end = start + len(target)

			if side == "left":
				start, end = end, start

			elif side == "center":
				start = end = (start + end) / 2

			selections.add(sublime.Region(start, end))