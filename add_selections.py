"""
BetterFindAllUnder was inspired by https://github.com/simonrad/sublime-selection-tools,
but I didn't use any code from there so the licensing issues are void.

All of this is mine. You can do what the hell you want with it.
"""

import sublime, sublime_plugin


class AddNextCharacterCommand(sublime_plugin.TextCommand):
	"""
	Select then next character.

	This is an additive version of "left" and "right".
	"""
	def run(self, edit, forward):
		selections = self.view.sel()
		for selection in list(selections):
			if forward:
				new = selection.end() + 1

			else:
				new = selection.begin() - 1

			selections.add(sublime.Region(new, new))


class AddNextWordCommand(sublime_plugin.TextCommand):
	"""
	Select the next word.

	This is an additive version of "ctrl+left" and
	"ctrl+right".
	"""
	def run(self, edit, forward):
		selections = self.view.sel()

		for selection in list(selections):

			if forward:
				new = selection.end() + 1

				while not self.view.classify(new) & sublime.CLASS_WORD_END:
					if new >= self.view.size():
						break

					new += 1

			else:
				new = selection.begin() - 1

				while not self.view.classify(new) & sublime.CLASS_WORD_START:
					if new <= 0:
						break

					new -= 1

			selections.add(sublime.Region(new, new))


class AddEndOfLineCommand(sublime_plugin.TextCommand):
	"""
	Select the end of the line.

	This is an additive version of "home" and "end", except
	it will always select the very end of the line, never the
	indented start as with "home".

	Additionally, this will select the line before or after if
	the cursor is already on the end of the line.
	"""
	def run(self, edit, forward):
		selections = self.view.sel()

		for selection in list(selections):

			if forward:
				new = selection.end() + 1

				while not self.view.classify(new) & sublime.CLASS_LINE_END:
					if new >= self.view.size():
						break

					new += 1

			else:
				new = selection.begin() - 1

				while not self.view.classify(new) & sublime.CLASS_LINE_START:
					if new <= 0:
						break

					new -= 1

			selections.add(sublime.Region(new, new))


class AddNextLineCommand(sublime_plugin.TextCommand):
	"""
	Add the next line above or below.

	This is much better than the default implementation, as it doesn't result
	in so many clashes. The only cursors to move are those at the very top or
	bottom, so you don't get "build-up" when you hit a differently-sized line.
	Additionally, blank lines are skipped when there are multiple moving
	selections, which prevents them "blending" together on a blank line.

	Doesn't work for word-wrap because it's hard yet pointless.
	"""
	def run(self, edit, forward):
		selections = self.view.sel()

		row_number = None
		moving_selections = []

		# Find all selections with maximum or minimum row (depending on the forward argument)
		for selection in selections:
			row, col = self.view.rowcol(selection.end() if forward else selection.begin())

			if row == row_number:
				moving_selections.append(selection)

			elif row_number is None or (row > row_number) == forward:
				moving_selections = [selection]
				row_number = row

		# Add the selections
		for selection in moving_selections:
			position = selection.end() if forward else selection.begin()
			row, col = self.view.rowcol(position)

			# Move up or down, skipping if need be
			while True:
				row += 1 if forward else -1

				line = self.view.line(self.view.text_point(row, 0))

				if line or len(moving_selections) == 1:
					break

			# Set xpos
			target_xpos = selection.xpos
			if target_xpos == -1:
				target_xpos = self.view.text_to_layout(position)[0]

			# Move to place closest to xpos
			for new in range(line.begin(), line.end()+1):
				xpos = self.view.text_to_layout(new)[0]

				if xpos >= target_xpos:
					prev_xpos = self.view.text_to_layout(new-1)[0]
					new -= abs(xpos-target_xpos) > abs(prev_xpos-target_xpos)
					break

			# Yeah!
			selections.add(sublime.Region(new, new, target_xpos))


class BetterFindAllUnder(sublime_plugin.TextCommand):
	"""
	Works like find_all_under, except works with initial
	multiple cursors.
	"""
	def run(self, edit):
		[*old_selections] = selections = self.view.sel()

		new_selections = []

		for selection in old_selections:
			selections.clear()
			selections.add(selection)

			self.view.window().run_command("find_all_under")

			new_selections.extend(self.view.sel())

		selections.add_all(new_selections)
