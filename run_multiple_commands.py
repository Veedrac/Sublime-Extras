"""
Based off of http://www.sublimetext.com/forum/viewtopic.php?t=8677,
and I see no license there so AFAIK you need to ask there any time you
even think about doing anything to this source. Or you can just duck
and hope, like I have.
"""

import sublime, sublime_plugin

class RunMultipleCommandsCommand(sublime_plugin.TextCommand):
	"""
	"args" for this takes _either_ "command" or "commands", where
	"commands" is a list of what "command" takes. "args" also takes
	an optional "times" parameter, and just runs itself that many
	times.

	"command" takes either a string (such as "store_selections") or
	a dictionary with a "command" attribute, an optional "args"
	attribute and an optional "context" attribute.

	In the above, the "command" and "args" attribute are as expected,
	and the "context" attribute is one of "window", "app" and "text".
	"""
	def run(self, edit, commands=None, command=None, times=1):
		if commands is None:
			commands = [command] if command is not None else []

		for _ in range(times):
			for command in commands:
				self.exec_command(command)


	def exec_command(self, command):
		# Shortcut for simple command described by one string
		if not "command" in command:
			if isinstance(command, str):
				command = {"command": command}

			else:
				raise ValueError("No command name provided.")

		args = command.get("args")

		contexts = {"window": self.view.window(), "app": sublime, "text": self.view}
		context = contexts[command.get("context", "text")]

		context.run_command(command["command"], args)