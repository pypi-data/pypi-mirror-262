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
        Problem](/runestone/default/reportabug?course=fopp&page=Length)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [6.1 Introduction: Sequences](intro-Sequences.html){.reference
        .internal}
    -   [6.2 Strings, Lists, and
        Tuples](StringsandLists.html){.reference .internal}
    -   [6.3 Index Operator: Working with the Characters of a
        String](IndexOperatorWorkingwiththeCharactersofaString.html){.reference
        .internal}
    -   [6.4 Disambiguating \[\]: creation vs
        indexing](DisabmiguatingSquareBrackets.html){.reference
        .internal}
    -   [6.5 Length](Length.html){.reference .internal}
    -   [6.6 The Slice Operator](TheSliceOperator.html){.reference
        .internal}
    -   [6.7 Concatenation and
        Repetition](ConcatenationandRepetition.html){.reference
        .internal}
    -   [6.8 Count and Index](CountandIndex.html){.reference .internal}
    -   [6.9 Splitting and Joining
        Strings](SplitandJoin.html){.reference .internal}
    -   [6.10 Exercises](Exercises.html){.reference .internal}
    -   [6.11 Chapter Assessment](week2a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#length .section}
[]{#index-0}

[6.5. ]{.section-number}Length[¶](#length "Permalink to this heading"){.headerlink}
===================================================================================

The `len`{.docutils .literal .notranslate} function, when applied to a
string, returns the number of characters in a string.

::: {.runestone .explainer .ac_section}
::: {#ac5_5_1 component="activecode" question_label="6.5.1"}
::: {#ac5_5_1_question .ac_question}
:::
:::
:::

To get the last letter of a string, you might be tempted to try
something like this:

::: {.runestone .explainer .ac_section}
::: {#ac5_5_2 component="activecode" question_label="6.5.2"}
::: {#ac5_5_2_question .ac_question}
:::
:::
:::

That won't work. It causes the runtime error
`IndexError: string index out of range`{.docutils .literal
.notranslate}. The reason is that there is no letter at index position 6
in `"Banana"`{.docutils .literal .notranslate}. Since we started
counting at zero, the six indexes are numbered 0 to 5. To get the last
character, we have to subtract 1 from the length. Give it a try in the
example above.

::: {.runestone .explainer .ac_section}
::: {#ac5_5_3 component="activecode" question_label="6.5.3"}
::: {#ac5_5_3_question .ac_question}
:::
:::
:::

Typically, a Python programmer would combine lines 2 and 3 from the
above example into a single line:

::: {.highlight-python .notranslate}
::: {.highlight}
    lastch = fruit[len(fruit)-1]
:::
:::

Though, from what you just learned about using negative indices, using
`fruit[-1]`{.docutils .literal .notranslate} would be a more appropriate
way to access the last index in a list.

You can still use the `len`{.docutils .literal .notranslate} function to
access other predictable indices, like the middle character of a string.

::: {.highlight-python .notranslate}
::: {.highlight}
    fruit = "grape"
    midchar = fruit[len(fruit)//2]
    # the value of midchar is "a"
:::
:::

As with strings, the function `len`{.docutils .literal .notranslate}
returns the length of a list (the number of items in the list). However,
since lists can have items which are themselves sequences (e.g.,
strings), it important to note that `len`{.docutils .literal
.notranslate} only returns the top-most length.

::: {.runestone .explainer .ac_section}
::: {#ac5_5_4 component="activecode" question_label="6.5.4"}
::: {#ac5_5_4_question .ac_question}
:::
:::
:::

Note that `alist[0]`{.docutils .literal .notranslate} is the string
`"hello"`{.docutils .literal .notranslate}, which has length 5.

**Check your understanding**

::: {.runestone}
-   [11]{#question5_5_1_opt_a}
-   The blank space counts as a character.
-   [12]{#question5_5_1_opt_b}
-   Yes, there are 12 characters in the string.
:::

::: {.runestone}
-   [4]{#question5_5_2_opt_a}
-   len returns the actual number of items in the list, not the maximum
    index value.
-   [5]{#question5_5_2_opt_b}
-   Yes, there are 5 items in this list.
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_5_5 component="activecode" question_label="6.5.7"}
::: {#ac5_5_5_question .ac_question}
Assign the number of elements in `lst`{.docutils .literal .notranslate}
to the variable `output`{.docutils .literal .notranslate}.
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

-   [[](DisabmiguatingSquareBrackets.html)]{#relations-prev}
-   [[](TheSliceOperator.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
