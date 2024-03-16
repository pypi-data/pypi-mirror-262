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
        Problem](/runestone/default/reportabug?course=fopp&page=TupleAssignmentwithunpacking)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [13.1 Introduction](TuplePacking-Intro.html){.reference
        .internal}
    -   [13.2 Tuple Packing](TuplePacking.html){.reference .internal}
    -   [13.3 Tuple Assignment with
        Unpacking](TupleAssignmentwithunpacking.html){.reference
        .internal}
    -   [13.4 Tuples as Return
        Values](TuplesasReturnValues.html){.reference .internal}
    -   [13.5 Unpacking Tuples as Arguments to Function
        Calls](UnpackingArgumentsToFunctions.html){.reference .internal}
    -   [13.6 Glossary](Glossary.html){.reference .internal}
    -   [13.7 Exercises](Exercises.html){.reference .internal}
    -   [13.8 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#tuple-assignment-with-unpacking .section}
[]{#index-0}

[13.3. ]{.section-number}Tuple Assignment with Unpacking[¶](#tuple-assignment-with-unpacking "Permalink to this heading"){.headerlink}
======================================================================================================================================

Python has a very powerful **tuple assignment** feature that allows a
tuple of variable names on the left of an assignment statement to be
assigned values from a tuple on the right of the assignment. Another way
to think of this is that the tuple of values is **unpacked** into the
variable names.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_1 component="activecode" question_label="13.3.1"}
::: {#ac12_4_1_question .ac_question}
:::
:::
:::

This does the equivalent of seven assignment statements, all on one easy
line.

Naturally, the number of variables on the left and the number of values
on the right have to be the same.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_4 component="activecode" question_label="13.3.2"}
::: {#ac12_4_4_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

Unpacking into multiple variable names also works with lists, or any
other sequence type, as long as there is exactly one value for each
variable. For example, you can write `x, y = [3, 4]`{.docutils .literal
.notranslate}.
:::

::: {#swapping-values-between-variables .section}
[13.3.1. ]{.section-number}Swapping Values between Variables[¶](#swapping-values-between-variables "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------

This feature is used to enable swapping the values of two variables.
With conventional assignment statements, we have to use a temporary
variable. For example, to swap `a`{.docutils .literal .notranslate} and
`b`{.docutils .literal .notranslate}:

::: {.runestone .explainer .ac_section}
::: {#ac12_4_2 component="activecode" question_label="13.3.1.1"}
::: {#ac12_4_2_question .ac_question}
:::
:::
:::

Tuple assignment solves this problem neatly:

::: {.runestone .explainer .ac_section}
::: {#ac12_4_3 component="activecode" question_label="13.3.1.2"}
::: {#ac12_4_3_question .ac_question}
:::
:::
:::

The left side is a tuple of variables; the right side is a tuple of
values. Each value is assigned to its respective variable. All the
expressions on the right side are evaluated before any of the
assignments. This feature makes tuple assignment quite versatile.
:::

::: {#unpacking-into-iterator-variables .section}
[13.3.2. ]{.section-number}Unpacking Into Iterator Variables[¶](#unpacking-into-iterator-variables "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------------------

Multiple assignment with unpacking is particularly useful when you
iterate through a list of tuples. You can unpack each tuple into several
loop variables. For example:

::: {.runestone .explainer .ac_section}
::: {#ac12_4_8a component="activecode" question_label="13.3.2.1"}
::: {#ac12_4_8a_question .ac_question}
:::
:::
:::

On the first iteration the tuple `('Paul', 'Resnick')`{.docutils
.literal .notranslate} is unpacked into the two variables
`first_name`{.docutils .literal .notranslate} and `last_name`{.docutils
.literal .notranslate}. One the second iteration, the next tuple is
unpacked into those same loop variables.
:::

::: {#the-pythonic-way-to-enumerate-items-in-a-sequence .section}
[]{#pythonic-enumeration}

[13.3.3. ]{.section-number}The Pythonic Way to Enumerate Items in a Sequence[¶](#the-pythonic-way-to-enumerate-items-in-a-sequence "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

When we first introduced the for loop, we provided an example of how to
iterate through the indexes of a sequence, and thus enumerate the items
and their positions in the sequence.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_8b component="activecode" question_label="13.3.3.1"}
::: {#ac12_4_8b_question .ac_question}
:::
:::
:::

We are now prepared to understand a more pythonic approach to
enumerating items in a sequence. Python provides a built-in function
`enumerate`{.docutils .literal .notranslate}. It takes a sequence as
input and returns a sequence of tuples. In each tuple, the first element
is an integer and the second is an item from the original sequence. (It
actually produces an "iterable" rather than a list, but we can use it in
a for loop as the sequence to iterate over.)

::: {.runestone .explainer .ac_section}
::: {#ac12_4_8c component="activecode" question_label="13.3.3.2"}
::: {#ac12_4_8c_question .ac_question}
:::
:::
:::

The pythonic way to consume the results of enumerate, however, is to
unpack the tuples while iterating through them, so that the code is
easier to understand.

::: {.runestone .explainer .ac_section}
::: {#ac12_4_8d component="activecode" question_label="13.3.3.3"}
::: {#ac12_4_8d_question .ac_question}
:::
:::
:::

**Check your Understanding**

::: {.runestone}
-   [You can\'t use different variable names on the left and right side
    of an assignment statement.]{#question12_4_2_opt_a}
-   Sure you can; you can use any variable on the right-hand side that
    already has a value.
-   [At the end, x still has it\'s original value instead of y\'s
    original value.]{#question12_4_2_opt_b}
-   Once you assign x\'s value to y, y\'s original value is gone.
-   [Actually, it works just fine!]{#question12_4_2_opt_c}
-   Once you assign x\'s value to y, y\'s original value is gone.
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_4_9 component="activecode" question_label="13.3.3.5"}
::: {#ac12_4_9_question .ac_question}
With only one line of code, assign the variables `water`{.docutils
.literal .notranslate}, `fire`{.docutils .literal .notranslate},
`electric`{.docutils .literal .notranslate}, and `grass`{.docutils
.literal .notranslate} to the values "Squirtle", "Charmander",
"Pikachu", and "Bulbasaur"
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_4_10 component="activecode" question_label="13.3.3.6"}
::: {#ac12_4_10_question .ac_question}
With only one line of code, assign four variables, `v1`{.docutils
.literal .notranslate}, `v2`{.docutils .literal .notranslate},
`v3`{.docutils .literal .notranslate}, and `v4`{.docutils .literal
.notranslate}, to the following four values: 1, 2, 3, 4.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_4_11 component="activecode" question_label="13.3.3.7"}
::: {#ac12_4_11_question .ac_question}
If you remember, the .items() dictionary method produces a sequence of
tuples. Keeping this in mind, we have provided you a dictionary called
`pokemon`{.docutils .literal .notranslate}. For every key value pair,
append the key to the list `p_names`{.docutils .literal .notranslate},
and append the value to the list `p_number`{.docutils .literal
.notranslate}. Do not use the .keys() or .values() methods.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac12_4_12 component="activecode" question_label="13.3.3.8"}
::: {#ac12_4_12_question .ac_question}
The .items() method produces a sequence of key-value pair tuples. With
this in mind, write code to create a list of keys from the dictionary
`track_medal_counts`{.docutils .literal .notranslate} and assign the
list to the variable name `track_events`{.docutils .literal
.notranslate}. Do **NOT** use the .keys() method.
:::
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

-   [[](TuplePacking.html)]{#relations-prev}
-   [[](TuplesasReturnValues.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
