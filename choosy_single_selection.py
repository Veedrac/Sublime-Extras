"""
The method for writing this was inspired from writing store_selections,
which has code based off of (and taken from) https://github.com/colinta/SublimeMarkAndMove,
but the idea (and I think all the code) in this is mine. As such, you can do what the hell
you want with it.

store_selections has it's own license, so remember to look there.
"""


import sublime, sublime_plugin

from .store_selections import get_id, store_selections

# Dict of id: settings pairs for KeepStoredSelectionsClear
# Used to remove all relevant reagions and remake with unchanged settings
to_clear = {}

class ChoosySingleSelectionCommand(sublime_plugin.TextCommand):
	"""
	Remove all but one selection, keeping the choice from "index",
	default 0 (first). Negative indexes also work.

	Adds other selections to a visible cache, which you can cycle
	though with choosy_selection_select.
	"""
	def run(self, edit, index=0, **settings):
		to_clear[get_id(settings)] = settings

		selections = self.view.sel()
		old_selections = list(selections)
		store_selections(self.view, old_selections, **settings)
		selections.clear()

		selections.add(old_selections[index])


class ChoosySelectionSelectCommand(sublime_plugin.TextCommand):
	"""
	Cycles through the cache created by choosy_single_selection.
	"""
	def run(self, edit, forward=True, **settings):
		id = get_id(settings)
		to_clear[id] = settings

		stored_selections = self.view.get_regions(id)

		# This can happen due to unwanted fallback in the keybindings,
		# just ignore it
		if not stored_selections:
			return

		# Remove the current cursor
		selections = self.view.sel()
		[old_selection] = selections
		selections.clear()

		# Move (index, shift, wrap)
		index = stored_selections.index(old_selection)
		index += 1 if forward else -1
		index %= len(stored_selections)

		# Add back in new position
		selections.add(stored_selections[index])

class KeepStoredSelectionsClear(sublime_plugin.EventListener):
	"""
	Gets rid of the cache created by choosy_single_selection in a greedy
	but intelligent way.
	"""

	def on_selection_modified(self, view):
		"""
		If the selection is modified by anything other than us, remove the
		cache.
		"""
		command, args, repeat_count = view.command_history(0)

		if command not in ("choosy_single_selection", "choosy_selection_select"):
			for id in to_clear:
				store_selections(view, [], replace=True, id=id)


	def on_deactivated(self, view):
		"""
		If we move away, on_selection_modified does not work. We have to add a cache
		which will let us check whether the selection has changed manually.

		Also, hide the cache, because it's silly to see it during, say, a find dialogue.
		"""

		for id in to_clear:
			#  Move the stored selections to a hidden buffer
			selections = view.get_regions(id)
			store_selections(view, selections, replace=True, id=id+" <cache>")

			# Remove from view
			store_selections(view, [], replace=True, id=id)

		# Add the current selections to a buffer to check whether we can resume the stored selections
		store_selections(view, view.sel(), replace=True, id="<check>")


	def on_activated(self, view):
		"""
		If the selection has changed since the last look, clear the cache. Otherwise, restore it.
		"""
		selection_check = view.get_regions("<check>")

		# Check if the selection has changed from cache
		if view.sel() == selection_check:
			for id in to_clear:
				selections = view.get_regions(id+" <cache>")

				# Add the region back
				# "to_clear[id]" is its original settings dict
				store_selections(view, selections, replace=True, **to_clear[id])