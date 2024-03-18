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
        Problem](/runestone/default/reportabug?course=fopp&page=GeneralizedSequences)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [7.1 Introduction: Iteration](intro-Iteration.html){.reference
        .internal}
    -   [7.2 The for Loop](TheforLoop.html){.reference .internal}
    -   [7.3 Flow of Execution of the for
        Loop](FlowofExecutionoftheforLoop.html){.reference .internal}
    -   [7.4 Strings and for loops](Stringsandforloops.html){.reference
        .internal}
    -   [7.5 Lists and for loops](Listsandforloops.html){.reference
        .internal}
    -   [7.6 The Accumulator
        Pattern](TheAccumulatorPattern.html){.reference .internal}
    -   [7.7 Traversal and the for Loop: By
        Index](TraversalandtheforLoopByIndex.html){.reference .internal}
    -   [7.8 Nested Iteration: Image
        Processing](NestedIterationImageProcessing.html){.reference
        .internal}
    -   [7.9 👩‍💻 Printing Intermediate
        Results](WPPrintingIntermediateResults.html){.reference
        .internal}
    -   [7.10 👩‍💻 Naming Variables in For
        Loops](WPNamingVariablesinForLoops.html){.reference .internal}
    -   [7.11 The Gory Details:
        Iterables](GeneralizedSequences.html){.reference .internal}
    -   [7.12 👩‍💻 Keeping Track of Your Iterator Variable and Your
        Iterable](WPKeepingTrackofYourIteratorVariableYourIterable.html){.reference
        .internal}
    -   [7.13 Glossary](Glossary.html){.reference .internal}
    -   [7.14 Exercises](Exercises.html){.reference .internal}
    -   [7.15 Chapter Assessment](week2a2.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#the-gory-details-iterables .section}
[]{#iter-iterators}

[7.11. ]{.section-number}The Gory Details: Iterables[¶](#the-gory-details-iterables "Permalink to this heading"){.headerlink}
=============================================================================================================================

The general syntax of a for loop is:

::: {.highlight-python .notranslate}
::: {.highlight}
    for iter_var_name in some_seq:
        # code block line 1
        # code block line 2
        # ...
:::
:::

After the word `in`{.docutils .literal .notranslate}, there can be any
Python expression that evaluates to a sequence. You have already seen
iteration over strings and lists. A string is a sequence whose items are
single characters. A list is a sequence whose items can be any kind of
Python object.

Actually, the for loop is a little more general. It can iterate not just
over strings and lists, but any kind of Python object that acts like a
sequence. So far, strings, lists, and tuples are all we have seen.

We will also see later some Python objects that act like sequences for
the purposes of iteration with a for loop. These include file objects
and iterators.

In fact, we have actually already seen one of these without noticing,
because it hardly matters. Technically, the `range`{.docutils .literal
.notranslate} function doesn't actually return a list. That is,
`range(3)`{.docutils .literal .notranslate} doesn't actually create the
list `[0, 1, 2]`{.docutils .literal .notranslate}. It returns an object
that acts just like the list `[0, 1, 2]`{.docutils .literal
.notranslate}, when used in a for loop. The difference is that the
numbers 0, 1, and 2 are produced as they are needed rather than all
created in advance. This hardly matters when there are only three items.
For `range(10000000)`{.docutils .literal .notranslate} it makes a little
difference for how fast the program runs and how much memory is used.
That's why the items are produced as needed rather than all produced in
advance.

For the purposes of this book, however, the difference will rarely
matter. You will be safe to think of the range function as if it returns
a list object. Indeed, the Python interpreter that's built into the
textbook cheats a little bit and makes the range function actually
produce a list. When you run a native Python interpreter on your
computer it won't cheat in that way. Still, when you run code of the
form, `for x in range(y)`{.docutils .literal .notranslate} you will
usually do just fine to think of range(y) returning a list.

Don't worry about understanding these details right now. The important
point is that in the activecode window above, instead of
`some_seq`{.docutils .literal .notranslate} you can have any Python
expression that evaluates to a string, a list, or certain other Python
objects that act like sequences for the purposes of use in for loops.
It's just something to keep in mind for later, when we see some of those
other Python objects that act like sequences but aren't quite.
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

-   [[](WPNamingVariablesinForLoops.html)]{#relations-prev}
-   [[](WPKeepingTrackofYourIteratorVariableYourIterable.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
