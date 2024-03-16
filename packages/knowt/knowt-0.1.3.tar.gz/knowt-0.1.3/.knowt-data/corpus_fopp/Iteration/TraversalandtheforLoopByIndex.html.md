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
        Problem](/runestone/default/reportabug?course=fopp&page=TraversalandtheforLoopByIndex)
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

::: {#traversal-and-the-for-loop-by-index .section}
[]{#for-by-index}

[7.7. ]{.section-number}Traversal and the `for`{.docutils .literal .notranslate} Loop: By Index[¶](#traversal-and-the-for-loop-by-index "Permalink to this heading"){.headerlink}
=================================================================================================================================================================================

With a for loop, the loop variable is bound, on each iteration, to the
next item in a sequence. Sometimes, it is natural to think about
iterating through the *positions*, or *indexes* of a sequence, rather
than through the items themselves.

For example, consider the list
`['apple', 'pear', 'apricot', 'cherry', 'peach']`{.docutils .literal
.notranslate}. 'apple' is at position 0, 'pear' at position 1, and
'peach' at position 4.

Thus, we can iterate through the indexes by generating a sequence of
them, using the `range`{.docutils .literal .notranslate} function.

::: {.runestone .explainer .ac_section}
::: {#ac14_6_5a component="activecode" question_label="7.7.1"}
::: {#ac14_6_5a_question .ac_question}
:::
:::
:::

In order to make the iteration more general, we can use the
`len`{.docutils .literal .notranslate} function to provide the bound for
`range`{.docutils .literal .notranslate}. This is a very common pattern
for traversing any sequence by position. Make sure you understand why
the range function behaves correctly when using `len`{.docutils .literal
.notranslate} of the string as its parameter value.

::: {.runestone .explainer .ac_section}
::: {#ac14_6_5 component="activecode" question_label="7.7.2"}
::: {#ac14_6_5_question .ac_question}
:::
:::
:::

In some other programming languages, that's the only way to iterate
through a sequence, by iterating through the positions and extracting
the items at each of the positions. Python code is often easier to read
because we don't have to do iteration that way. Compare the iteration
above with the more "pythonic" approach below.

::: {.runestone .explainer .ac_section}
::: {#ac14_6_5c component="activecode" question_label="7.7.3"}
::: {#ac14_6_5c_question .ac_question}
:::
:::
:::

If we really want to print the indexes (positions) along with the fruit
names, then iterating through the indexes as in the previous versions is
available to us. Python also provides an `enumerate`{.docutils .literal
.notranslate} function which provides a more "pythonic" way of
enumerating the items in a list, but we will delay the explanation of
how to use `enumerate`{.docutils .literal .notranslate} until we cover
the notions of [[tuple packing and unpacking]{.std
.std-ref}](../Tuples/TupleAssignmentwithunpacking.html#pythonic-enumeration){.reference
.internal}.

**Check your understanding**

::: {.runestone}
-   [0]{#question14_6_1_opt_a}
-   idx % 2 is 0 whenever idx is even
-   [1]{#question14_6_1_opt_b}
-   idx % 2 is 0 whenever idx is even
-   [2]{#question14_6_1_opt_c}
-   idx % 2 is 0 whenever idx is even
-   [3]{#question14_6_1_opt_d}
-   idx % 2 is 0 whenever idx is even
-   [6]{#question14_6_1_opt_e}
-   idx % 2 is 0 whenever idx is even
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

-   [[](TheAccumulatorPattern.html)]{#relations-prev}
-   [[](NestedIterationImageProcessing.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
