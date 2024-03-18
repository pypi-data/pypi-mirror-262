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
        Problem](/runestone/default/reportabug?course=fopp&page=toctree)
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

::: {#iteration .section}
[7. ]{.section-number}Iteration[¶](#iteration "Permalink to this heading"){.headerlink}
=======================================================================================

::: {.toctree-wrapper .compound}
[Iteration]{.caption-text}

-   [7.1. Introduction: Iteration](intro-Iteration.html){.reference
    .internal}
-   [7.2. The **for** Loop](TheforLoop.html){.reference .internal}
-   [7.3. Flow of Execution of the for
    Loop](FlowofExecutionoftheforLoop.html){.reference .internal}
-   [7.4. Strings and `for`{.docutils .literal .notranslate}
    loops](Stringsandforloops.html){.reference .internal}
-   [7.5. Lists and `for`{.docutils .literal .notranslate}
    loops](Listsandforloops.html){.reference .internal}
    -   [7.5.1. Using the range Function to Generate a Sequence to
        Iterate
        Over](Listsandforloops.html#using-the-range-function-to-generate-a-sequence-to-iterate-over){.reference
        .internal}
    -   [7.5.2. Iteration Simplifies our Turtle
        Program](Listsandforloops.html#iteration-simplifies-our-turtle-program){.reference
        .internal}
-   [7.6. The Accumulator
    Pattern](TheAccumulatorPattern.html){.reference .internal}
-   [7.7. Traversal and the `for`{.docutils .literal .notranslate} Loop:
    By Index](TraversalandtheforLoopByIndex.html){.reference .internal}
-   [7.8. Nested Iteration: Image
    Processing](NestedIterationImageProcessing.html){.reference
    .internal}
    -   [7.8.1. The RGB Color
        Model](NestedIterationImageProcessing.html#the-rgb-color-model){.reference
        .internal}
    -   [7.8.2. Image
        Objects](NestedIterationImageProcessing.html#image-objects){.reference
        .internal}
    -   [7.8.3. Image Processing and Nested
        Iteration](NestedIterationImageProcessing.html#image-processing-and-nested-iteration){.reference
        .internal}
-   [7.9. 👩‍💻 Printing Intermediate
    Results](WPPrintingIntermediateResults.html){.reference .internal}
-   [7.10. 👩‍💻 Naming Variables in For
    Loops](WPNamingVariablesinForLoops.html){.reference .internal}
-   [7.11. The Gory Details:
    Iterables](GeneralizedSequences.html){.reference .internal}
-   [7.12. 👩‍💻 Keeping Track of Your Iterator Variable and Your
    Iterable](WPKeepingTrackofYourIteratorVariableYourIterable.html){.reference
    .internal}
-   [7.13. Glossary](Glossary.html){.reference .internal}
-   [7.14. Exercises](Exercises.html){.reference .internal}
    -   [7.14.1. Contributed
        Exercises](Exercises.html#contributed-exercises){.reference
        .internal}
-   [7.15. Chapter Assessment](week2a2.html){.reference .internal}
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

-   [[](../Sequences/week2a1.html)]{#relations-prev}
-   [[](intro-Iteration.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
