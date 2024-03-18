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
        Problem](/runestone/default/reportabug?course=fopp&page=zip)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [23.1 Introduction: Map, Filter, List Comprehensions, and
        Zip](intro.html){.reference .internal}
    -   [23.2 Map](map.html){.reference .internal}
    -   [23.3 Filter](filter.html){.reference .internal}
    -   [23.4 List Comprehensions](listcomp.html){.reference .internal}
    -   [23.5 Zip](zip.html){.reference .internal}
    -   [23.6 Exercises](Exercises.html){.reference .internal}
    -   [23.7 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#zip .section}
[23.5. ]{.section-number}Zip[¶](#zip "Permalink to this heading"){.headerlink}
==============================================================================

One more common pattern with lists, besides accumulation, is to step
through a pair of lists (or several lists), doing something with all of
the first items, then something with all of the second items, and so on.
For example, given two lists of numbers, you might like to add them up
pairwise, taking \[3, 4, 5\] and \[1, 2, 3\] to yield \[4, 6, 8\].

One way to do that with a for loop is to loop through the possible index
values.

::: {.runestone .explainer .ac_section}
::: {#ac21_5_1 component="activecode" question_label="23.5.1"}
::: {#ac21_5_1_question .ac_question}
:::
:::
:::

You have seen this idea previously for iterating through the items in a
single list. In many other programming languages that's really the only
way to iterate through the items in a list. In Python, however, we have
gotten used to the for loop where the iteration variable is bound
successively to each item in the list, rather than just to a number
that's used as a position or index into the list.

Can't we do something similar with pairs of lists? It turns out we can.

The `zip`{.docutils .literal .notranslate} function takes multiple lists
and turns them into a list of tuples (actually, an iterator, but they
work like lists for most practical purposes), pairing up all the first
items as one tuple, all the second items as a tuple, and so on. Then we
can iterate through those tuples, and perform some operation on all the
first items, all the second items, and so on.

::: {.runestone .explainer .ac_section}
::: {#ac21_5_2 component="activecode" question_label="23.5.2"}
::: {#ac21_5_2_question .ac_question}
:::
:::
:::

Here's what happens when you loop through the tuples.

::: {.runestone .explainer .ac_section}
::: {#ac21_5_3 component="activecode" question_label="23.5.3"}
::: {#ac21_5_3_question .ac_question}
:::
:::
:::

Or, simplifying and using a list comprehension:

::: {.runestone .explainer .ac_section}
::: {#ac21_5_4 component="activecode" question_label="23.5.4"}
::: {#ac21_5_4_question .ac_question}
:::
:::
:::

Or, using `map`{.docutils .literal .notranslate} and not unpacking the
tuple (our online environment has trouble with unpacking the tuple in a
lambda expression):

::: {.runestone .explainer .ac_section}
::: {#ac21_5_5 component="activecode" question_label="23.5.5"}
::: {#ac21_5_5_question .ac_question}
:::
:::
:::

Consider a function called possible, which determines whether a word is
still possible to play in a game of hangman, given the guesses that have
been made and the current state of the blanked word.

Below we provide function that fulfills that purpose.

::: {.runestone .explainer .ac_section}
::: {#ac21_5_6 component="activecode" question_label="23.5.6"}
::: {#ac21_5_6_question .ac_question}
:::
:::
:::

However, we can rewrite that using `zip`{.docutils .literal
.notranslate}, to be a little more comprehensible.

::: {.runestone .explainer .ac_section}
::: {#ac21_5_7 component="activecode" question_label="23.5.7"}
::: {#ac21_5_7_question .ac_question}
:::
:::
:::

**Check Your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac21_5_8 component="activecode" question_label="23.5.8"}
::: {#ac21_5_8_question .ac_question}
**1.** Below we have provided two lists of numbers, `L1`{.docutils
.literal .notranslate} and `L2`{.docutils .literal .notranslate}. Using
zip and list comprehension, create a new list, `L3`{.docutils .literal
.notranslate}, that sums the two numbers if the number from
`L1`{.docutils .literal .notranslate} is greater than 10 and the number
from `L2`{.docutils .literal .notranslate} is less than 5. This can be
accomplished in one line of code.
:::
:::
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

-   [[](listcomp.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
