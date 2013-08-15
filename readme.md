Sublime Text Extras
===================

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

<!-- Apologies for this... -->

| ![Store, Align, Combine](http://i.imgur.com/UQ71ZET.png) | ![Selections](http://i.imgur.com/Hk3BLeA.png) |
|---|---|
| This first uses storing selections to "jump" the gap, and immediately follows with a store+align+restore+join idiom to extend the cursor. The cursors are then joined and the process starts again. | This shows off the improved `add_next_line` handling, the `remove_blank_line_selections` command, the `add_next_character` command and the red shows off choosing where "ESC" lands us.
| ![Eval](http://i.imgur.com/yZduaRH.png) | ![Repeat Macro](http://i.imgur.com/L64UVdG.png) |
| First you see how full non-trivial expressions can be evaluated and "print" can be used to output text. Then you see that evaluation can work with expressions as well, and on top of that the `$` symbol injects sequential numbers into the code. | A macro is run... 32 times.
| ![Boundaries](http://i.imgur.com/gRMnDmN.png) | ![Split Selection](http://i.imgur.com/PAEbilM.png) |
| A border of 10 lines is forced above and below. | `run_multiple_commands` is used for the "blocky" selections and the rest is a combination of selection-altering commands.


Some tips on getting set-up
----------------------------

The rest is comming shortly, just getting used to Git in the meantime...