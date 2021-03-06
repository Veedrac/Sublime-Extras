"""
This one is mine. You can do what the hell you want with it.

There are other versions that I found after I wrote this, but
this is by far the quickest, cleanest implementation, as far
as I have seen.
"""


import sublime, sublime_plugin


def get_margin_size(view):
	"""Get the size of the border from the settings file."""

	partsizes = {
		"pixels": 1,
		"ems": view.em_width(),
		"lines": view.line_height(),
		"viewports": view.viewport_extent()[1],
	}

	border_parts = sublime.load_settings("Extras.sublime-settings").get("border", {})

	return sum(number*partsizes[part] for part, number in border_parts.items())


class ForceMargin(sublime_plugin.EventListener):
	"""
	Force there to be a margin at the bottom and top
	by scrolling when the selection gets too high or
	low.
	"""

	def on_selection_modified(self, view):
		# Only deal with single empty cursors
		try:
			cursor, *rest = view.sel()
		except ValueError:
			return

		if cursor or rest: return

		# Get its position
		cursor_x, cursor_y = view.text_to_layout(cursor.a)

		# Amount of space to keep clear at top and bottom
		border = get_margin_size(view)

		# Viewport poisions
		view_x, view_y = view.viewport_position()
		view_w, view_h = view.viewport_extent()

		if 2*border >= view_h - view.line_height():
			view.show_at_center(cursor)
			return

		view_top, view_bottom = view_y, view_y + view_h

		# Distance from cursor to top and bottom
		cursor_headroom = + cursor_y - border - view_top
		cursor_footroom = - cursor_y - border + view_bottom

		# Nudge viewport, but only if distances are negative
		view_y += min(0, cursor_headroom)
		view_y -= min(0, cursor_footroom)


		# We're done! YAY!
		view.set_viewport_position((view_x, view_y))