::: {#navbar .navbar .navbar-default .navbar-fixed-top role="navigation"}
::: {.container}
::: {.navbar-header}
[]{.icon-bar} []{.icon-bar} []{.icon-bar}

<div>

[![](../_static/img/RAIcon.png)](/runestone/default/user/login){.brand-logo}
[fopp](../index.html){#rs-book-toc-link .navbar-brand}

</div>
:::

::: {.navbar-collapse .collapse .navbar-ex1-collapse}
-   
-   []{#ad_warning}
-   []{#browsing_warning}
-   
-   [*[Search]{.visuallyhidden
    aria-label="Search"}*](#){.dropdown-toggle}
    -   [Table of Contents](../index.html)

    -   [Book Index](../genindex.html)

    -   

    -   ::: {.input-group}
        :::
-   
-   [*[User]{.visuallyhidden aria-label="User"}*](#){.dropdown-toggle}
    -   []{.loggedinuser}

    -   

    -   [Course Home](/ns/course/index)

    -   [Assignments](/assignment/student/chooseAssignment)

    -   [Practice](/runestone/assignments/practice)

    -   [[Peer Instruction
        (Instructor)](/runestone/peer/instructor.html)]{#inst_peer_link}

    -   [Peer Instruction (Student)](/runestone/peer/student.html)

    -   

    -   [Change Course](/runestone/default/courses)

    -   

    -   [[Instructor\'s
        Page](/runestone/admin/index)]{#ip_dropdown_link}

    -   [Progress Page](/runestone/dashboard/studentreport)

    -   

    -   [Edit Profile](/runestone/default/user/profile){#profilelink}

    -   [Change
        Password](/runestone/default/user/change_password){#passwordlink}

    -   [Register](/runestone/default/user/register){#registerlink}

    -   [Login](#)

    -   ::: {.slider .round}
        :::

        Dark Mode
-   
-   [[*[Scratch Activecode]{.visuallyhidden
    aria-label="Scratch Activecode"}*](javascript:runestoneComponents.popupScratchAC())]{#scratch_ac_link}
-   
-   [*[Help]{.visuallyhidden aria-label="Help"}*](#){.dropdown-toggle}
    -   [FAQ](http://runestoneinteractive.org/pages/faq.html)
    -   [Instructors Guide](https://guide.runestone.academy)
    -   
    -   [About Runestone](http://runestoneinteractive.org)
    -   [Report A
        Problem](/runestone/default/reportabug?course=fopp&page=TheStrategy)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [21.1 Building A Program: A
        Strategy](TheStrategy.html){.reference .internal}
    -   [21.2 👩‍💻 Sketch an Outline](WPSketchanOutline.html){.reference
        .internal}
    -   [21.3 👩‍💻 Code one section at a
        time](WPCodeSectionataTime.html){.reference .internal}
    -   [21.4 👩‍💻 Clean Up](WPCleanCode.html){.reference .internal}
    -   [21.5 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#building-a-program-a-strategy .section}
[21.1. ]{.section-number}Building A Program: A Strategy[¶](#building-a-program-a-strategy "Permalink to this heading"){.headerlink}
===================================================================================================================================

Building on lessons learned in the first debugging interlude, this
chapter offers a strategy for writing a program to solve a problem such
as those that appear in the exercises at the ends of the chapters in
this book. (A similar approach is helpful for writing larger programs,
but that will come later.)

::: {.admonition-warning .admonition}
Warning.

You may find it tempting to start an exercise by copying and pasting a
snippet of code from somewhere in the textbook, and hoping that a small
edit will lead to a solution to the current problem. Often this will
lead to frustration and confusion; after trying a few code substitutions
that feel vaguely familiar to you, you'll find the code looking kind of
complicated and the outputs baffling.

Copying and editing snippets of code is actually a useful element of the
strategy we outline below. But it comes a little later in the process,
not as the first thing. And it requires a fair bit of work to make sure
you understand the code snippet that you've copied. Only then will you
be able to find the *right* small edits to the code snippet to make it
do what you want.
:::

There are three basic steps to the strategy we recommend: Outline; Code
One Section at a Time; Clean Up.

::: {#sketch-an-outline .section}
[21.1.1. ]{.section-number}Sketch an Outline[¶](#sketch-an-outline "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------

We are suggesting you first write down all the steps you want the
program to do. You can do this in any manner you like. We are going to
show you how to outline using comments, but if you are more visual you
might want to sketch on a piece of paper and if you are more spatial try
walking around the room. The big trick is to understand everything you
want to do first in your own words, so then you are translating them to
the computer.
:::

::: {#code-one-section-at-a-time .section}
[21.1.2. ]{.section-number}Code One Section at a Time[¶](#code-one-section-at-a-time "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------

After you outline your program, you should write code one section at a
time, and carefully test that section before you go on. The idea here is
to make sure your program is doing what you think it's doing at each
stage.

Translating your English description of a step into code may be the most
challenging step for you early in your learning about programming. Later
it will come more naturally. Here is a checklist of questions that you
may find useful in trying to find the right python code to express your
idea, based on what you've learned so far:

-   Is this operation pulling out an item from a list or string or
    dictionary? If so, use \[\] to pull out the item you want.

-   Is this operation transforming a string into another string? If so,
    look at the summary of string methods.

-   Is this operation modifying a list? If so, look at the material on
    lists.

-   Is the operation doing something multiple times? If so, you'll want
    a `for`{.docutils .literal .notranslate} loop. Start by making a
    skeleton version of a for loop, and then fill in the parts that are
    in \<brackets\>

::: {.highlight-default .notranslate}
::: {.highlight}
    for <varname> in <seq>:
                    <code block line 1>
                    <code block line 2>
                    ...
:::
:::

-   Is the operation something that should only occur in some
    circumstances and not in others? If so, you'll want an
    `if`{.docutils .literal .notranslate} statement. Start by making a
    skeleton version of an if/then/else code snippet, and then fill in
    the parts that are in \<brackets\>

::: {.highlight-default .notranslate}
::: {.highlight}
    if <boolean exp>:
      <if block here>
      ...
    else:
      <else block here>
      ...
:::
:::

-   Is this an accumulator pattern? If so, start by making a skeleton
    version of it, and then fill it in.

::: {.highlight-default .notranslate}
::: {.highlight}
    #initialize accumulator
    a = <initial value>

    for <varname> in <seq>:
      <some code in for block>
      a = <new_value>
      <other code in for block>
    print(a)
:::
:::

Finally, you may be reminded of a snippet of code somewhere in the
textbook that did something similar to what you want to do. Now is the
time to copy and edit that code. **But wait!** Before you start editing
that code snippet, make sure you understand it. See the section below on
understanding code.
:::

::: {#clean-up .section}
[21.1.3. ]{.section-number}Clean Up[¶](#clean-up "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------

When you are done with outlining and testing your program, delete any
diagnostic print statements from your program. No one really needs to
see the test statements you wrote, and leaving test statements in the
program might confuse you if you add more to the program.

Extra comments do help other people read your code, but try to leave in
only the bits that you think are useful. There is an art to writing good
informative comments, and you can only learn this art by reading other
people's programs and having your peers read your programs. As a rule of
thumb for comments, when in doubt, keep it; it you're worried it won't
make sense to you or someone else later, add more detail to it.

In the next few pages, we'll go through this process using a question
similar to something that you may have already seen before.
:::
:::

::: {style="width: 100%"}
::: {ea-publisher="runestoneacademy" ea-type="image" style="display: flex; justify-content: center"}
:::
:::

::: {#scprogresscontainer}
You have attempted []{#scprogresstotal} of []{#scprogressposs}
activities on this page

::: {#subchapterprogress aria-label="Page progress"}
:::
:::

-   [[](toctree.html)]{#relations-prev}
-   [[](WPSketchanOutline.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
