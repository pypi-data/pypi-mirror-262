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
        Problem](/runestone/default/reportabug?course=fopp&page=Stringsandforloops)
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
::: {#strings-and-for-loops .section}
[7.4. ]{.section-number}Strings and `for`{.docutils .literal .notranslate} loops[¶](#strings-and-for-loops "Permalink to this heading"){.headerlink}
====================================================================================================================================================

Since a string is simply a sequence of characters, the `for`{.docutils
.literal .notranslate} loop iterates over each character automatically.
(As always, try to predict what the output will be from this code before
your run it.)

::: {.runestone .explainer .ac_section}
::: {#ac6_4_1 component="activecode" question_label="7.4.1"}
::: {#ac6_4_1_question .ac_question}
:::
:::
:::

The loop variable `achar`{.docutils .literal .notranslate} is
automatically reassigned each character in the string "Go Spot Go". We
will refer to this type of sequence iteration as **iteration by item**.
Note that the for loop processes the characters in a string or items in
a sequence one at a time from left to right.

**Check your understanding**

::: {.runestone}
-   [10]{#question6_4_1_opt_a}
-   Iteration by item will process once for each item in the sequence.
-   [11]{#question6_4_1_opt_b}
-   The blank is part of the sequence.
-   [12]{#question6_4_1_opt_c}
-   Yes, there are 12 characters, including the blank.
-   [Error, the for statement needs to use the range
    function.]{#question6_4_1_opt_d}
-   The for statement can iterate over a sequence item by item.
:::

::: {.runestone}
-   [4]{#question6_4_2_opt_a}
-   Slice returns a sequence that can be iterated over.
-   [5]{#question6_4_2_opt_b}
-   Yes, The blank is part of the sequence returned by slice.
-   [6]{#question6_4_2_opt_c}
-   Check the result of s\[3:8\]. It does not include the item at
    index 8.
-   [Error, the for statement cannot use slice.]{#question6_4_2_opt_d}
-   Slice returns a sequence.
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

-   [[](FlowofExecutionoftheforLoop.html)]{#relations-prev}
-   [[](Listsandforloops.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
