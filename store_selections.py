"""
Based off of https://github.com/colinta/SublimeMarkAndMove, thus here is the license.

	Copyright (c) 2012, Colin T.A. Gray
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:

	1. Redistributions of source code must retain the above copyright notice, this
	   list of conditions and the following disclaimer.
	2. Redistributions in binary form must reproduce the above copyright notice,
	   this list of conditions and the following disclaimer in the documentation
	   and/or other materials provided with the distribution.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
	ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

	The views and conclusions contained in the software and documentation are those
	of the authors and should not be interpreted as representing official policies,
	either expressed or implied, of this project.


Because much of this is now mine and I claim no rights to this to the extent that
I can, if you want to "steal" stuff you'll have to check against the original source to see
if you need to include the license above.
"""


import sublime, sublime_plugin

from collections import ChainMap
from itertools import chain

DEFAULT_SETTINGS = 	{
	"icon": "dot",
	"scope": "meta.separator", # Defines colours
	"flags": sublime.DRAW_EMPTY   | sublime.DRAW_SOLID_UNDERLINE |
		 sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE
}

flag_map = {
	"empty": sublime.DRAW_EMPTY,
	"show on minimap": sublime.HIDE_ON_MINIMAP,
	"empty as overwrite": sublime.DRAW_EMPTY_AS_OVERWRITE,
	"fill": sublime.DRAW_NO_FILL,
	"outline": sublime.DRAW_NO_OUTLINE,
	"solid underline": sublime.DRAW_SOLID_UNDERLINE,
	"stippled underline": sublime.DRAW_STIPPLED_UNDERLINE,
	"squiggly underline": sublime.DRAW_SQUIGGLY_UNDERLINE,
	"persistent": sublime.PERSISTENT,
	"hidden": sublime.HIDDEN
}

default_flags = {
	"empty": False,
	"show on minimap": True,
	"empty as overwrite": False,
	"fill": True,
	"outline": True,
	"solid underline": False,
	"stippled underline": False,
	"squiggly underline": False,
	"persistent": False,
	"hidden": False
}

# Should be loaded from settings...
presets = {
	"": {},

	"selection storage": {
		"id": "selection storage",
		"icon": "dot",
		"scope": "meta.separator",
		"flags": {
			"empty": True,
			"solid underline": True,
			"fill": False,
			"outline": False
		}
	},

	"choosy single selection": {
		"id": "choosy single selection",
		"icon": "",
		"scope": "invalid", # Defines colours
		"flags": {
			"empty": True,
			"fill": False
		}
	}
}


def parse_flags(flags={}, preset="", **other) -> "int":
	"""
	Optimised for "parse_flags(**settings)" use-case,
	returns a flags integer suitable for view.add_regions.
	"""
	preset = presets[preset].get("flags", {})

	orsum_flags = 0

	for flag_name, active in ChainMap(flags, preset, default_flags).items():
		flag_int = flag_map[flag_name]

		# OK.. wut?
		# Read: "activate" if the default is False,
		# else it's an inversed flag and activation
		# is actually removal of the flag integer
		if active != default_flags[flag_name]:
			# Add flag
			# 0b10 | 0b01 == 0b11
			orsum_flags |= flag_int

		else:
			# Remove flag
			# 0b11 & ~0b10 == 0b01
			orsum_flags &= ~flag_int

	return orsum_flags


def get_id(settings):
	try:
		return settings["id"]
	except KeyError:
		return presets[settings.get("preset", "")].get("id", "<default id>")


def store_selections(view, selections, replace=False, **settings):
	"""
	Save selections to storage.
	"""
	id = get_id(settings)

	if not replace:
		# Add old selections to selections, so as not to remove them
		selections = list(chain(selections, view.get_regions(id)))

	# Filter "settings" to only have "flags", "scope" and "icon"
	filtered = {"flags": parse_flags(**settings)}

	# Chain settings with preset to provide fallback
	settings = ChainMap(settings, presets[settings.get("preset", "")])

	if "scope" in settings:
		filtered["scope"] = settings["scope"]

	if "icon" in settings:
		filtered["icon"] = settings["icon"]

	# Done! Finish up!

	view.add_regions(id, selections, **filtered)

class StoreSelectionsCommand(sublime_plugin.TextCommand):
	"""
	Save selections to storage.

	If "doubleclick" is True, will activate selections if
	all current selections are in storage.
	"""
	def run(self, edit, doubleclick=False, **settings):
		id = get_id(settings)

		stored = self.view.get_regions(id)

		if doubleclick and all(selection in stored for selection in self.view.sel()):
			self.view.run_command(
				"activate_selections",
				dict(ChainMap({"clear": True}, settings))
			)

		else:
			store_selections(self.view, self.view.sel(), **settings)


class ActivateSelectionsCommand(sublime_plugin.TextCommand):
	"""
	Pop selections from storage.

	Can take a "clear" argument for if you want to change whether to clear the
	storage, defaults to True.
	"""
	def run(self, edit, clear=True, **settings):
		selections = self.view.sel()
		new_selections = self.view.get_regions(get_id(settings))

		if not new_selections:
			return

		selections.clear()
		selections.add_all(new_selections)

		if clear:
			store_selections(self.view, [], replace=True, **settings)


class ActivateSelectedSelectionsCommand(sublime_plugin.TextCommand):
	"""
	Pop selections from storage if they are contained within
	a currently-active selection.

	If there are no contained selections and you have up to one cursor of
	size 0 this will fall back to activate_selections.

	Can take a "clear" argument for if you want to change whether to clear the
	storage, defaults to True.
	"""
	def run(self, edit, **settings):
		selections = self.view.sel()
		old_selections = list(selections)
		selections.clear()

		# Shortcut for single or no curson with no selection
		effectively_empty  = not old_selections
		effectively_empty |= len(old_selections) == 1 and not old_selections[0]

		if effectively_empty:
			self.view.run_command("activate_selections", settings)
			return

		# Else only within  selection
		new_selections = self.view.get_regions(get_id(settings))
		new_storage = []

		# Add to selection
		for new_selection in new_selections:
			if any(old_selection.contains(new_selection) for old_selection in old_selections):
				self.view.sel().add(new_selection)

			else:
				new_storage.append(new_selection)

		if settings.get("clear", True):
			# Replace storage with (storage - selection)
			store_selections(self.view, new_storage,  replace=True, **settings)



class ClearSavedSelectionsCommand(sublime_plugin.TextCommand):
	"""
	Clear selection storage.
	"""
	def run(self, edit, **settings):
		store_selections(self.view, [], replace=True, **settings)