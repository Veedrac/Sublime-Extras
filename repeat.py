"""
Officially based off of https://github.com/sivakumar-kailasam/Repeat-Macro with this license:

	Copyright (c) 2012-2013 Sivakumar Kailasam

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to
	deal in the Software without restriction, including without limitation the
	rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
	sell copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in
	all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
	 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
	FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
	DEALINGS IN THE SOFTWARE.

This is basically a "lite" version of that using the same code-base.

My changes are hereby released completely and irrevocably into the
Public Domain. THE ORIGINAL CODE, THAT OF REPEAT-MACRO, IS NOT PUBLIC
DOMAIN AND THUS THIS CODE SHOULD NOT BE THOUGHT OF AS PUBLIC DOMAIN.

- Joshua Landau <joshua@landau.ws>
"""

import sublime, sublime_plugin

class RepeatMacroCommand(sublime_plugin.TextCommand):
	"""
	Run a macro many times.

	If you want to use a macro once per selection the normal command
	is sufficient.

	If you want to repeat, say, once per line, reduce to the above problem.
	"""

	def run(self, edit):
		self.view.window().show_input_panel(
			" № of repeats: ",
			initial_text = "",
			on_done   = self.repeat_macro,
			on_change = None,
			on_cancel = None
		)

	def repeat_macro(self, input):
		for _ in range(int(input)):
			self.view.run_command("run_macro")