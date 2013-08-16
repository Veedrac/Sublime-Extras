Sublime Text Extras
===================

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

* + _A tentative hope that this may one day be customizable._



Pics or GTFO
------------

The following are **APNG**s; if you're using Chrome (or Opera) you'll need [an extension](https://chrome.google.com/webstore/detail/apng/ehkepjiconegkhpodgoaeamnpckdbblp), if you're using IE you need to stop it.

**[The "album" collects these all in one other place.](http://imgur.com/a/8NmF0)**

---

![Store, Align, Combine](http://i.imgur.com/UQ71ZET.png)

This first uses storing selections to "jump" the gap, and immediately follows with a store+align+restore+join idiom to extend the cursor. The cursors are then joined and the process starts again.

---

![Selections](http://i.imgur.com/Hk3BLeA.png)

This shows off the improved `add_next_line` handling, the `remove_blank_line_selections` command, the `add_next_character` command and the red shows off choosing where "ESC" lands us.

---

![Eval](http://i.imgur.com/yZduaRH.png)

First you see how full non-trivial expressions can be evaluated and "print" can be used to output text. Then you see that evaluation can work with expressions as well, and on top of that the `$` symbol injects sequential numbers into the code.

---

![Repeat Macro](http://i.imgur.com/L64UVdG.png)

A macro is run... 32 times.

---

![Boundaries](http://i.imgur.com/gRMnDmN.png)

A border of 10 lines is forced above and below.

---

![Split Selection](http://i.imgur.com/PAEbilM.png)

`run_multiple_commands` is used for the "blocky" selections and the rest is a combination of selection-altering commands.

---



Some tips on getting set-up
----------------------------

Sublime Extras comes with no shortcuts by default. Additionally the `.sublime-commands` file has yet to be developed.


### Repeat macro

```javascript
{ "keys": [KEYBINDING], "command": "repeat_macro" },
```

Run a macro many times. If you want to use a macro once per selection the normal command is sufficient. If you want to repeat, say, once per line, reduce to the above problem. This comes in to play any time vim's quantifier would be useful, albeit this is clumsier. I'm still thinking of a good way to do that... maybe I'll check what Vintage does.

Thanks to Sivakumar Kailasam for the basis of this code. In fact there seems to be no true advantage to my code except that it is simpler by removing some of the redundancy that the original had.


### Better add_next_line

```javascript
{ "keys": [KEYBINDING], "command": "add_next_line", "args": {"forward": false} },
{ "keys": [KEYBINDING], "command": "add_next_line", "args": {"forward": true} },
```

These would replace the default <kbd>Alt+Shift+</kbd> and <kbd>Alt+Shift+Down</kbd>. Instead of being truly awful, these work and they do so well. In essence, all they do is move the top or bottom row, avoiding cascades from cursors that fall into the gutter.


### More add_next_\*

```javascript
{ "keys": [KEYBINDING], "command": "add_next_character", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_next_character", "args": {"forward": false} },

{ "keys": [KEYBINDING], "command": "add_end_of_line", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_end_of_line", "args": {"forward": false} },

{ "keys": [KEYBINDING], "command": "add_next_word", "args": {"forward": true} },
{ "keys": [KEYBINDING], "command": "add_next_word", "args": {"forward": false} },
```

Just some more `add_next`s. They're useful on occasion.


### Remove blank lines

```javascript
{ "keys": [KEYBINDING], "command": "remove_blank_line_selections", "args": {"forward": false} },
```

Split all selections by blank lines, discarding all that are on blank lines. This is useful for filtering cursors as well as splitting regions because a cursor that is just a blank line will be removed entirely.

This works well with add_next_line because in combination your selections won't often be troubled be blank lines (the lines in the gutter don't spawn more cursors and they can be removed at the end with a single `remove_blank_line_selections`).

This is also useful, as expected, for selecting paragraphs.


### Keep or remove every nth selection

```javascript
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

```javascript
{ "keys": [KEYBINDING], "command": "split_selection_into_words" },
{ "keys": [KEYBINDING], "command": "split_selection_into_chars" },
```

Select all of the characters or all of the words in the current selections. This can be useful when you want to sort the selected words or replace every character in a selection with a single ([`hello`] → [`=====`]). It can also be quicker than trimming a selection by hand ([`, "hello"`] → [, "`hello`"]).






### Inline evaluation

```javascript
{ "keys": [KEYBINDING], "command": "evaluate_selection", "args": { "execute": false } },
{ "keys": [KEYBINDING], "command": "evaluate_selection", "args": { "execute": true } },
```

The *bestest* evaluation-subtitution-autonumbering command **evah**.

This deserves a lot more than a few lines so TODO.



### Combine selections

```javascript
{ "keys": ["alt+j"], "command": "combine_selections" },
```


### Save and restore selections

```javascript
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

The "preset" section will eventually be customisable, so don't worry about that. The other customizations will be described when that is done.

`store_selections` saves selections to storage. If "doubleclick" is True, it will activate selections if all current selections are in storage.

`activate_selections` pops selections from storage. It can take a "clear" argument for if you want to change whether to clear the storage, which defaults to True.

`activate_selected_selections` pops selections from storage if they are contained within a currently-active selection. If there are no contained selections and you have up to one cursor of size 0 this will fall back to activate_selections. It can take a "clear" argument for if you want to change whether to clear the storage, defaults to True.

`clear_saved_selections` does what it says on the tin.

Many thanks to Colin T.A. Gray for the idea, strategy and original code.


### Better escape

```javascript
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

You don't have to choose these keybindings. This uses the same backend as with saving and restoring selections.

Now when you press <kbd>ESC</kbd> an "afterimage" will be left. Continuing to press <kbd>ESC</kbd> will cycle forward. At all times <kbd>Shift-ESC</kbd> is the inverse of <kbd>ESC</kbd>.



### Useful bonuses using run_multiple_commands

Thanks to Nilium who posted the original version for run_multiple_commands on the forums.

#### A duplicate that selects the just-duplicated line if done on a line

```javascript
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

This duplicate makes there always a selection after its execution. This is useful, for example, to duplicate a line, split into charcters, write "=" (and, *WHAM*, you have a header!).

#### Larger jumps

```javascript
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


### Aligning cursors

```javascript
{ "keys": [KEYBINDING], "command": "align_cursor"},
```

Align the cursors to the first cursor, using the characters in the selection if possible, otherwise using the characters on either side of the cursor.

It will extend if any cursor is a selection, otherwise it will move.

If it cannot find a match, it will go to the line's end.
