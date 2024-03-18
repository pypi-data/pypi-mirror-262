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
        Problem](/runestone/default/reportabug?course=fopp&page=TheAccumulatorPatternwithLists)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [9.1 Introduction: Transforming
        Sequences](intro-SequenceMutation.html){.reference .internal}
    -   [9.2 Mutability](Mutability.html){.reference .internal}
    -   [9.3 List Element Deletion](ListDeletion.html){.reference
        .internal}
    -   [9.4 Objects and
        References](ObjectsandReferences.html){.reference .internal}
    -   [9.5 Aliasing](Aliasing.html){.reference .internal}
    -   [9.6 Cloning Lists](CloningLists.html){.reference .internal}
    -   [9.7 Mutating Methods](MutatingMethods.html){.reference
        .internal}
    -   [9.8 Append versus
        Concatenate](AppendversusConcatenate.html){.reference .internal}
    -   [9.9 Non-mutating Methods on
        Strings](NonmutatingMethodsonStrings.html){.reference .internal}
    -   [9.10 String Format Method](StringFormatting.html){.reference
        .internal}
    -   [9.11 f-Strings](FStrings.html){.reference .internal}
    -   [9.12 The Accumulator Pattern with
        Lists](TheAccumulatorPatternwithLists.html){.reference
        .internal}
    -   [9.13 The Accumulator Pattern with
        Strings](TheAccumulatorPatternwithStrings.html){.reference
        .internal}
    -   [9.14 👩‍💻 Accumulator Pattern
        Strategies](WPAccumulatorPatternStrategies.html){.reference
        .internal}
    -   [9.15 👩‍💻 Don't Mutate A List That You Are Iterating
        Through](WPDontMutateAListYouIterateThrough.html){.reference
        .internal}
    -   [9.16 Summary](Glossary.html){.reference .internal}
    -   [9.17 Exercises](Exercises.html){.reference .internal}
    -   [9.18 Chapter Assessment - List
        Methods](week4a1.html){.reference .internal}
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

::: {#the-accumulator-pattern-with-lists .section}
[9.12. ]{.section-number}The Accumulator Pattern with Lists[¶](#the-accumulator-pattern-with-lists "Permalink to this heading"){.headerlink}
============================================================================================================================================

We can accumulate values into a list rather than accumulating a single
numeric value. Consider, for example, the following program which
transforms a list into a new list by squaring each of the values.

::: {.runestone .explainer .ac_section}
::: {#ac8_9_1 component="activecode" question_label="9.12.1"}
::: {#ac8_9_1_question .ac_question}
:::
:::
:::

Here, we **initialize** the accumulator variable to be an empty list, on
line 2.

We **iterate** through the sequence (line 3). On each iteration we
transform the item by squaring it (line 4).

The **update** step appends the new item to the list which is stored in
the accumulator variable (line 5). The update happens using the
.append(), which mutates the list rather than using a reassignment.
Instead, we could have written `accum = accum + [x]`{.docutils .literal
.notranslate}, or `accum += [x]`{.docutils .literal .notranslate}. In
either case, we'd need to concatenate a list containing x, not just x
itself.

At the end, we have accumulated a new list of the same length as the
original, but with each item transformed into a new item. This is called
a mapping operation, and we will revisit it in a later chapter.

Note how this differs from mutating the original list, as you saw in a
previous section.

**Check your understanding**

::: {.runestone}
-   [\[4,2,8,6,5\]]{#question8_9_1_opt_a}
-   5 is added to each item before the append is performed.
-   [\[4,2,8,6,5,5\]]{#question8_9_1_opt_b}
-   There are too many items in this list. Only 5 append operations are
    performed.
-   [\[9,7,13,11,10\]]{#question8_9_1_opt_c}
-   Yes, the for loop processes each item of the list. 5 is added before
    it is appended to blist.
-   [Error, you cannot concatenate inside an
    append.]{#question8_9_1_opt_d}
-   5 is added to each item before the append operation is performed.
:::

::: {.runestone}
-   [\[8,5,14,9,6\]]{#question8_9_2_opt_a}
-   Don\'t forget the last item!
-   [\[8,5,14,9,6,12\]]{#question8_9_2_opt_b}
-   Yes, the for loop processes each item in lst. 5 is added before
    lst\[i\] is appended to new\_list.
-   [\[3,0,9,4,1,7,5\]]{#question8_9_2_opt_c}
-   5 is added to each item before the append operation is performed.
-   [Error, you cannot concatenate inside an
    append.]{#question8_9_2_opt_d}
-   It is OK to have a complex expression inside the call to the append
    method. The expression \`lst\[i\]+5\` is fully evaluated before the
    append operation is performed.
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_9_2 component="activecode" question_label="9.12.4"}
::: {#ac8_9_2_question .ac_question}
2.  For each word in the list `verbs`{.docutils .literal .notranslate},
    add an -ing ending. Save this new list in a new list,
    `ing`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_9_3 component="activecode" question_label="9.12.5"}
::: {#ac8_9_3_question .ac_question}
Given the list of numbers, `numbs`{.docutils .literal .notranslate},
create a new list of those same numbers increased by 5. Save this new
list to the variable `newlist`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_9_4 component="activecode" question_label="9.12.6"}
::: {#ac8_9_4_question .ac_question}
Given the list of numbers, `numbs`{.docutils .literal .notranslate},
modifiy the list `numbs`{.docutils .literal .notranslate} so that each
of the original numbers are increased by 5. Note this is not an
accumulator pattern problem, but its a good review.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_9_5 component="activecode" question_label="9.12.7"}
::: {#ac8_9_5_question .ac_question}
For each number in `lst_nums`{.docutils .literal .notranslate}, multiply
that number by 2 and append it to a new list called
`larger_nums`{.docutils .literal .notranslate}.
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

-   [[](FStrings.html)]{#relations-prev}
-   [[](TheAccumulatorPatternwithStrings.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
