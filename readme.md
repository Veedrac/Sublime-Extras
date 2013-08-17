<!--
This readme is hereby released completely and irrevocably into the Public Domain.

- Joshua Landau <joshua@landau.ws>
-->

Sublime Text Extras
===================

TODO: Properly attribute sources

Interjection
------------

*Sublime Text Extras*, also known as *Sublime Extras* or just *Extras* **only** works on **Sublime Text version 3**.


...Back to the good part
-------------------------

A truly awesome set of enhancements to your Sublime Text life!

**Contains many "borrowed" ideas and much "borrowed" code.**


* Create a new cursor at next character, word or the end of the line

* Sane `add_next_line` command — don't "lose" cursors in the gutter on empty lines!

* A `find_all_under` that really works with multiple cursors

* Align your cursors across lines

* "Esc" that lets you choose which cursor to escape to

* Inline eval (Python) with format-able auto-numbering and multi-line input and output

* Repeat a macro a specified number of times

* Combine multiple commands in a shortcut with `run_multiple_commands`

* Keep workspace quasi-centered with "spacing borders" on above and below

* Split selections into characters and words

* Split selections *by* lines and remove blank lines from selections

* Keep or dump every nth selection

* Intelligently combine selections

* Store and retrieve selections

* Easily write any named Unicode character using Sublime Text's autocomplete



Pics or GTFO
------------

#### The following are **APNG**s; if you're using Chrome (or Opera) you'll need [an extension](https://chrome.google.com/webstore/detail/apng/ehkepjiconegkhpodgoaeamnpckdbblp), if you're using IE you need to stop it.

*[The "album" collects these all in one other place.](http://imgur.com/a/9oCqY)*

---

![Autocomplete Unicode](http://i.imgur.com/BppUqdc.png)

If you have <kbd>Alt Gr</kbd> on your keyboard, on linux you should be able to do <kbd>Alt Gr+p</kbd> to write "þ". When a word starts with a non-ASCII character it will be autocompleted into Unicode, searching by name. That's what's happening here.

---

![Store, Align, Combine](http://i.imgur.com/fuPyeG6.png)

This first uses storing selections to "jump" the gap, and immediately follows with a store+align+restore+join idiom to extend the cursor. The cursors are then joined and the process starts again.

---

![Selections](http://i.imgur.com/ckm8l5o.png)

This shows off the improved `add_next_line` handling, the `remove_blank_line_selections` command, the `add_next_character` command and the red shows off choosing where "ESC" lands us.

---

![Eval](http://i.imgur.com/9LDt2yU.png)

First you see how full non-trivial expressions can be evaluated and "print" can be used to output text. Then you see that evaluation can work with expressions as well, and on top of that the `$` symbol injects sequential numbers into the code.

---

![Repeat Macro](http://i.imgur.com/oaZjrs4.png)

A macro is run... 32 times.

---

![Boundaries](http://i.imgur.com/gz2MkQQ.png)

A border of 10 lines is forced above and below.

---

![Split Selection](http://i.imgur.com/64ZI3RY.png)

`run_multiple_commands` is used for the "blocky" selections and the rest is a combination of selection-altering commands.

---



Some tips on getting set-up
----------------------------

Sublime Extras comes with no shortcuts by default. Additionally the `.sublime-commands` file has yet to be developed.


### Using Unicode autocomplete

When first started with this extension Sublime Text will take a few seconds to generate a half-megabyte `.sublime/unicode cache.picke.gz` file. Afterwards Unicode autocomplete should *just work*. If you have <kbd>Alt Gr</kbd> on your keyboard, on Linux you should be able to do <kbd>Alt Gr+p</kbd> to write "þ". When a word starts with a non-ASCII character it will be autocompleted into Unicode, searching by name.

If you don't have <kbd>Alt Gr</kbd>, a `£`, `€` or `¬` may be relevant non-ASCII characters you do have.

You will need to change your settings to be able to see autocompletes in plain text files; I use

```json
"auto_complete_selector": "text, source, meta.tag - punctuation.definition.tag.begin",
```

in my `Preferences.sublime-settings`.


The project that inspired this was (UnicodeMath)[https://github.com/mvoidex/UnicodeMath], an alternate TeX-like input mechanism.


### Using boundaries

This just happens. A boundary is created at the top and bottom that keeps some space clear for viewing.

To customize the border's size, in your user Extras.sublime-settings add and configure:

```json
// The size of the border cleared at the top and bottom
// of the screen; units are summed
//
// All of the units are optional — if not given they
// default to 0
//
// Drop or leave empty to default to no border
"border": {
	"pixels": 0,
	"ems": 0,
	"lines": 10,
	"viewports": 0
},
```


### Repeat macro

```json
{ "keys": [KEYBINDING], "command": "repeat_macro" },
```

Run a macro many times. If you want to use a macro once per selection the normal command is sufficient. If you want to repeat, say, once per line, reduce to the above problem. This comes in to play any time vim's quantifier would be useful, albeit this is clumsier. I'm still thinking of a good way to do that... maybe I'll check what Vintage does and scrap this...

Thanks to Sivakumar Kailasam for the [basis of this code](https://github.com/sivakumar-kailasam/Repeat-Macro). In fact my version's just a cropped version of his.


### Better add_next_line

```json
{ "keys": [KEYBINDING], "command": "add_next_line", "args": {"forward": false} },
{ "keys": [KEYBINDING], "command": "add_next_line", "args": {"forward": true} },
```

These would replace the default <kbd>Alt+Shift+</kbd> and <kbd>Alt+Shift+Down</kbd>. Instead of being truly awful, these work and they do so well. In essence, all they do is move the top or bottom row, avoiding cascades from cursors that fall into the gutter.

BetterFindAllUnder is an implementation of the same command from Sublime Selection Tools, https://github.com/simonrad/sublime-selection-tools. Thank you, Simonrad!


### More add_next_\*

```json
{ "keys": [KEYBINDING], "command": "add_next_character", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_next_character", "args": {"forward": false} },

{ "keys": [KEYBINDING], "command": "add_end_of_line", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_end_of_line", "args": {"forward": false} },

{ "keys": [KEYBINDING], "command": "add_next_word", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_next_word", "args": {"forward": false} },
```

Just some more `add_next`s. They're useful on occasion.


### Remove blank lines

```json
{ "keys": [KEYBINDING], "command": "remove_blank_line_selections", "args": {"forward": false} },
```

Split all selections by blank lines, discarding all that are on blank lines. This is useful for filtering cursors as well as splitting regions because a cursor that is just a blank line will be removed entirely.

This works well with add_next_line because in combination your selections won't often be troubled be blank lines (the lines in the gutter don't spawn more cursors and they can be removed at the end with a single `remove_blank_line_selections`).

This is also useful, as expected, for selecting paragraphs.


### Keep or remove every nth selection

```json
{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 2, "filter": "keep"   } },
{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 2, "filter": "remove" } },

{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 3, "filter": "keep"   } },
{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 3, "filter": "remove" } },

{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 4, "filter": "keep"   } },
{ "keys": [KEYBINDING], "command": "every_nth_selection", "args": {"n": 4, "filter": "remove" } },

...
```

Keep or remove every nth selection. This has 0-based indexing, so the first selection will always be the "first of the nth". If there is only one selection, it is first split into lines.

Although this seems esoteric, it's useful because you often get code of alternating patterns; select each line and run one of these commands. But I admit it's somewhat unusual.


### Split selection into chars or words

```json
{ "keys": [KEYBINDING], "command": "split_selection_into_words" },
{ "keys": [KEYBINDING], "command": "split_selection_into_chars" },
```

Select all of the characters or all of the words in the current selections. This can be useful when you want to sort the selected words or replace every character in a selection with a single ([`hello`] → [`=====`]). It can also be quicker than trimming a selection by hand ([`, "hello"`] → [, "`hello`"]).


### Inline evaluation

```json
{ "keys": [KEYBINDING], "command": "evaluate_selection", "args": { "execute": false } },
{ "keys": [KEYBINDING], "command": "evaluate_selection", "args": { "execute": true } },
```

The *bestest* evaluation-subtitution-autonumbering command **evah**.

The first version is non-executing -- Python won't try and evaluate the selection. All `$`s in the text will be replaced by consecutive numbers, starting from 1. The value of a `$` increments once per *selection*, not per `$`, so [`$$` `$$`] formats to [`11` `22`].

But it's cooler than that.

Python's [formatting system](http://docs.python.org/3/library/string.html#format-string-syntax) is used so that `{}` is equivalent to `$` — only now it accepts [the whole formatting mini-language](http://docs.python.org/3/library/string.html#format-specification-mini-language)!

This would mainly be useful for, say, [`{:02}` `{:02}` `{:02}` ...] → [`01` `02` `03` ...] in order to align `01` and `10` but it's as flexible as the mini-language gets.

You can even do [`{:{}>{}}` `{:{}>{}}` `{:{}>{}}` `{:{}>{}}`] → [`1` `22` `333` `4444`]!


**But we're not even at the evaluation step!**

When evaluation is enabled the formatting as above is disabled in order to prevent interference.

There's a simple rule for evaluation -- if you typed the same thing at the REPL (changing spacing so that the REPL doesn't get confused) the output will be the same.

Thus:

`for x in range(3): x`

evaluates to

```
0
1
2
```

`print(10, 20)` goes to `10 20`. `123 + 4324 ** 2` goes to `18697099`.

`$` are substituted too, so `print("my number is", $)` goes to `my number is 1`.

And finally, everything withing the `functools`, `itertools`, math, `operator`, `os` and `random` modules are available unpacked, to `choice([1, 2, 3])` will evaluate to `1`, `2` or `3` depending on the mood of the gods.

This is basically a polished version of [MiniPy](https://github.com/vim/MiniPy). Thanks Vim (author's name on Github)!


### Save and restore selections

```json
{
	"keys": [KEYBINDING],
	"command": "store_selections",
	"args": { "preset": "selection storage", "doubleclick": true }
},

{
	"keys": [KEYBINDING],
	"command": "activate_selections",
	"args": { "preset": "selection storage" }
},

{
	"keys": [KEYBINDING],
	"command": "activate_selected_selections",
	"args": { "preset": "selection storage" }
},

{
	"keys": [KEYBINDING],
	"command": "clear_saved_selections",
	"args": { "preset": "selection storage" }
},
```

For `"args"` *all* commnds can take `"preset"`, `"id"`, `"icon"`, `"scope"` and `"flags"`. `store_selections` can also take a `doubleclick` parameter and `activate_selections` can take a `clear` parameter.

`"preset"` is the name of a preset as defined by `Extras.sublime-settings`. They are defined by `"presets"`, a dictionary mapping names to sub-dictionaries. Those sub-dictionaries in turn define defaults for any or all of `"id"`, `"icon"`, `"scope"` and `"flags"`.

`"id"` defines the key under which the selections are stored. You could have one set of keybindings with one `id` and another with another `id` and they could not affect each-other.

`"icon"` defines an icon for the gutter on lines where selections are stored. This can be `"dot"`, `"circle"`, `"bookmark"` "or" `"cross"`, or `""` for blank. It may also be a full package relative path, such as `Packages/Theme - Default/dot.png`. A bad choice gives a block of noise as the icon, which may be useful on occasion.

`"scope"` defines the color from the used theme. Some choices are `"comment"`, `"string"`, `"meta.separator"` and `"invalid"`. I do not believe there is any guarantee that these will work on any particular theme.

`"flags"` is a dictionary whose keys are any of `"empty"`, `"show on minimap"`, `"empty as overwrite"`, `"fill"`, `"outline"`, `"solid underline"`, `"stippled underline"`, `"squiggly underline"`, `"persistent"` and `"hidden"`. It's values are booleans, and decide whether the chosen attribute is active. All have defaults.

* `empty`: Draw empty regions with a vertical bar. By default, they aren't drawn at all.
* `show on minimap`: Don't show the regions on the minimap.
* `empty as overwrite`: Draw empty regions with a horizontal bar instead of a vertical one.
* `fill`: Enable filling the regions, leaving only the outline.
* `outline`: Enable drawing the outline of the regions.
* `solid underline`: Draw a solid underline below the regions.
* `stippled underline`: Draw a stippled underline below the regions.
* `squiggly underline`: Draw a squiggly underline below the regions.
* `persistent`: Save the regions in the session.
* `hidden`: Don't draw the regions.

---

`store_selections` saves selections to storage. If "doubleclick" is True, it will activate selections if all current selections are in storage.

`activate_selections` pops selections from storage. It can take a "clear" argument for if you want to change whether to clear the storage, which defaults to True.

`activate_selected_selections` pops selections from storage if they are contained within a currently-active selection. If there are no contained selections and you have up to one cursor of size 0 this will fall back to activate_selections. It can take a "clear" argument for if you want to change whether to clear the storage, defaults to True.

`clear_saved_selections` does what it says on the tin.


This is really useful when you want to have lots of selections at different places and none of the other methods can get you the right subset. Normally you'd be forced to use a mouse which can at times be very suboptimal. Now just use `store_selections`!

`activate_selected_selections` is better than `activate_selections` so I advise not using the first — `activate_selected_selections` will fall back on it cleanly. `activate_selected_selections` is mainly useful when you can use `[better_]find_all_under`, store all of those, select a region containing some of them and "pop" that region.

Derived from [Mark And Move](https://github.com/colinta/SublimeMarkAndMove). Many thanks to Colin T.A. Gray for the idea, strategy and original code!


### Aligning cursors

```json
{ "keys": [KEYBINDING], "command": "align_cursor"},
```

Align the cursors to the first cursor, using the characters in the selection if possible, otherwise using the characters on either side of the cursor. It counts how many occurrences of those chosen characters preceded and tries to make that equal for each selection.

It will extend if any cursor is a selection, otherwise it will move.

Say you're editing this file (`▮` represents cursor):

```json
{ "keys": [▮"alt+2"],       "command": "every_nth_selection", "args": {"n": 2, "filter": "keep"   } },
{ "keys": [▮"alt+shift+2"], "command": "every_nth_selection", "args": {"n": 2, "filter": "remove" } },
{ "keys": [▮"alt+3"],       "command": "every_nth_selection", "args": {"n": 3, "filter": "keep"   } },
{ "keys": [▮"alt+shift+3"], "command": "every_nth_selection", "args": {"n": 3, "filter": "remove" } },
...
```

and you want to select the last "]" on all of the lines. Instead of cancelling the selection and creating a new one from `command` like you'd traditionally do, you can scroll to the "]" on the first line...

```json
{ "keys": ["alt+2"▮],       "command": "every_nth_selection", "args": {"n": 2, "filter": "keep"   } },
{ "keys": ["alt+sh▮ift+2"], "command": "every_nth_selection", "args": {"n": 2, "filter": "remove" } },
{ "keys": ["alt+3"▮],       "command": "every_nth_selection", "args": {"n": 3, "filter": "keep"   } },
{ "keys": ["alt+sh▮ift+3"], "command": "every_nth_selection", "args": {"n": 3, "filter": "remove" } },
...
```

and use `align_cursor`! It will see the `"]` around the cursor and align all selections to the fisrt occurance of that pair...

```json
{ "keys": ["alt+2"▮],       "command": "every_nth_selection", "args": {"n": 2, "filter": "keep"   } },
{ "keys": ["alt+shift+2"▮], "command": "every_nth_selection", "args": {"n": 2, "filter": "remove" } },
{ "keys": ["alt+3"▮],       "command": "every_nth_selection", "args": {"n": 3, "filter": "keep"   } },
{ "keys": ["alt+shift+3"▮], "command": "every_nth_selection", "args": {"n": 3, "filter": "remove" } },
...
```

Nice!


### Combine selections

```json
{ "keys": ["alt+j"], "command": "combine_selections" },
```

This joins selections together. It will join within lines if within_lines is True (default) and there is at least one line with multiple selections.

This will, therefore, turn [som`e` te`x`t] into [som`e tex`t]. The main uses for this involve creating selections with selection storage, aligning and restoring. In the example above with aligning cursors, if the selections had been saved beforehand and restored afterwards you'd have something like this:

```json
{ "keys": [▮"alt+2"▮],       "command": "every_nth_selection", "args": {"n": 2, "filter": "keep"   } },
{ "keys": [▮"alt+shift+2"▮], "command": "every_nth_selection", "args": {"n": 2, "filter": "remove" } },
{ "keys": [▮"alt+3"▮],       "command": "every_nth_selection", "args": {"n": 3, "filter": "keep"   } },
{ "keys": [▮"alt+shift+3"▮], "command": "every_nth_selection", "args": {"n": 3, "filter": "remove" } },
...
```

If you used `combine_selections` each of `"alt+2"`, `"alt+shift+2"`, `"alt+3"` and `"alt+shift+3"` would be selected.


### Better escape

```json
{
	"keys": ["escape"],
	"command": "choosy_selection_select",
	"args": { "preset": "choosy single selection", "forward": true  }
},

{
	"keys": ["shift+escape"],
	"command": "choosy_selection_select",
	"args": { "preset": "choosy single selection", "forward": false }
},

{
	"keys": ["escape"], "command": "choosy_single_selection",
	"args": { "preset": "choosy single selection", "index": 0 },
	"context": [ { "key": "num_selections", "operator": "not_equal", "operand": 1 } ]
},
{
	"keys": ["shift+escape"], "command": "choosy_single_selection",
	"args": { "preset": "choosy single selection", "index": -1 },
	"context": [ { "key": "num_selections", "operator": "not_equal", "operand": 1 } ]
},

// Add back the old contexts, which were hidden by the above
{ "keys": ["escape"], "command": "clear_fields", "context":
	[
		{ "key": "has_next_field", "operator": "equal", "operand": true }
	]
},
{ "keys": ["escape"], "command": "clear_fields", "context":
	[
		{ "key": "has_prev_field", "operator": "equal", "operand": true }
	]
},
{ "keys": ["escape"], "command": "hide_panel", "args": {"cancel": true},
	"context":
	[
		{ "key": "panel_visible", "operator": "equal", "operand": true }
	]
},
{ "keys": ["escape"], "command": "hide_overlay", "context":
	[
		{ "key": "overlay_visible", "operator": "equal", "operand": true }
	]
},
{ "keys": ["escape"], "command": "hide_auto_complete", "context":
	[
		{ "key": "auto_complete_visible", "operator": "equal", "operand": true }
	]
},
```

**You don't have to choose these keys; they were chosen to highlight the extras you would have to tack on if you do.** This uses the same back end as with saving and restoring selections.

Now when you press <kbd>ESC</kbd> an "afterimage" will be left. Continuing to press <kbd>ESC</kbd> will cycle forward. At all times <kbd>Shift-ESC</kbd> is the inverse of <kbd>ESC</kbd>.

This is really useful for escaping to the *last* selection (<kbd>Shift+ESC</kbd>), for example. It's just nice.

The `"args"` accept the same `"preset"`, `"id"`, `"icon"`, `"scope"` and `"flags"` as with saving and restoring selections.



### Useful bonuses using run_multiple_commands

Thanks to Nilium who posted the original version for run_multiple_commands [on the forums](http://www.sublimetext.com/forum/viewtopic.php?t=8677)!

#### A duplicate that selects the just-duplicated line if done on a line

```json
{ "keys": [KEYBINDING], "command": "duplicate_line" },

{
	"keys": [KEYBINDING],
	"command": "run_multiple_commands",
	"context":
	[
		{ "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
		{ "key": "num_selections", "operator": "equal", "operand": 1 }
	],
	"args": {
		"commands": [
			{ "command": "expand_selection", "args": {"to": "line"} },
			{ "command": "duplicate_line" },
		]
	},
},
```

Note that the two instances of `KEYBINDING` have to be the same, and should probably be that of your current duplication shortcut.

This duplicate makes there always a selection after its execution. This is useful, for example, to duplicate a line, split into characters, write "=" (and, *WHAM*, you have a header!).

#### Larger jumps

```json
{
	"keys": [KEYBINDING],
	"command": "run_multiple_commands",
	"args": { "command": { "command": "move", "args": {"by": "lines", "forward": false } }, "times": 8 },
},
{
	"keys": [KEYBINDING],
	"command": "run_multiple_commands",
	"args": { "command": { "command": "move", "args": {"by": "lines", "forward": true  } }, "times": 8 },
},
{
	"keys": [KEYBINDING],
	"command": "run_multiple_commands",
	"args": { "command": { "command": "move", "args": {"by": "lines", "forward": false, "extend": true} }, "times": 8 },
},
{
	"keys": [KEYBINDING],
	"command": "run_multiple_commands",
	"args": { "command": { "command": "move", "args": {"by": "lines", "forward": true,  "extend": true} }, "times": 8 },
},
```
These four commands let you jump up or down, the last two extending the selection, by 8 lines. This is a really nice way to travel as the jumps are small and controlled but much quicker than what you'd otherwise resort to.
