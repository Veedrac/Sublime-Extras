"""
This is basically a polished version of https://github.com/vim/MiniPy,
and I see no license there so AFAIK you need to ask there any time you
even think about doing anything to this source. Or you can just duck
and hope, like I have.
"""


import sublime, sublime_plugin

import os, sys
from code import compile_command
from io import StringIO

# For eval
import math, random, itertools, operator, functools, os
from collections import ChainMap

modules = {
	"functools": functools,
	"itertools": itertools,
	"math": math,
	"operator": operator,
	"os": os,
	"random": random,
}

class EvaluateSelectionCommand(sublime_plugin.TextCommand):
	"""
	Based of Minipy, this evaluates your selected text.

	If "execute" is True, it "$"s are replaced with consecutive
	numbers (incrementing once per selection) and then it
	is run through Python.

	If "execute" is False, no evaluating is done but "{}"-
	formatters are also  passed up to 100 instances of the number;
	this allows you to do things like add padding to the number.
	"""
	def run(self, edit, execute):
		old_stdout = sys.stdout

		try:
			exec_globals = dict(ChainMap(modules.copy(), *map(vars, modules.values())))
			exec_locals = {}

			# i is the value for each $
			for i, region in enumerate(self.view.sel(), start=1):
				output = sys.stdout = StringIO()

				# Get and substitute "$"s
				text = self.view.substr(region)
				text = text.replace("$", str(i))

				if execute:
					# Wrap in case of failure -- a failure should not stop
					# later evaluations
					try:
						to_exec = ""
						for line in text.splitlines(keepends=True):
							previous_to_exec, to_exec = to_exec, to_exec + line

							try:
								# Returns None if it is "incomplete", so the except block
								# is not triggered. This prevents early execution.
								#
								# Additionally, this runs by default in "single" mode, which
								# is the same thing the REPL uses. We get results for free
								# from the automatic printing that goes on
								compile_command(to_exec)

							except SyntaxError:
								# We must have gone too far, execute the previous to_exec
								#
								# Allow errors to fall though
								#
								# compile_command is more lenient than compile in "single" mode for
								# some reason, so having used it above we have to use it here too.
								command = compile_command(previous_to_exec)

								# Double-check that it works
								if not command:
									raise

								exec(command, exec_globals, exec_locals)

								# This allows some functions, mainly recursive ones, to work better
								exec_globals.update(exec_locals)
								exec_locals = {}

								to_exec = line

						if to_exec:
							# Allow errors to fall though
							#
							# compile_command is more lenient than compile in "single" mode for
							# some reason, so having used it above we have to use it here too.
							command = compile_command(to_exec + "\n")

							# Double-check that it works
							if not command:
								raise SyntaxError

							exec(command, exec_globals, exec_locals)

						output.seek(0)
						text = output.read()

						if text.endswith("\n"):
							text = text[:-1]

					except Exception as e:
						print("Evaluate Selection Error:", e, file=old_stdout)

				else:
					# Don't use .format unless not evalling or you block
					# use of .format from within Python
					text = text.format(*[i]*100)

				# Woo! Commit!
				self.view.replace(edit, region, text)

		finally:
			sys.stdout = old_stdout