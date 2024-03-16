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
        Problem](/runestone/default/reportabug?course=fopp&page=WPKeepingTrackofYourIteratorVariableYourIterable)
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

::: {#keeping-track-of-your-iterator-variable-and-your-iterable .section}
[7.12. ]{.section-number}👩‍💻 Keeping Track of Your Iterator Variable and Your Iterable[¶](#keeping-track-of-your-iterator-variable-and-your-iterable "Permalink to this heading"){.headerlink}
==============================================================================================================================================================================================

When students first begin using for loops, they sometimes have
difficulty understanding the difference between the iterator variable
(the loop variable) and the iterable.

The iterable is the object that you will parsing through in a for loop.
Generally, this object does not change while the for loop is being
executed.

The iterator (loop) variable is the variable which stores a portion of
the iterable when the for loop is being executed. Each time the loop
iterates, the value of the iterator variable will change to a different
portion of the iterable.

::: {.runestone}
-   [string]{#question6_100_1_opt_a}
-   Incorrect, that is not the type of the iterable.
-   [list]{#question6_100_1_opt_b}
-   Yes, the iterable is n, and it is a list.
-   [tuple]{#question6_100_1_opt_c}
-   Incorrect, that is not the type of the iterable.
-   [iterable]{#question6_100_1_opt_d}
-   Incorrect, that is not the type of the iterable.
-   [error, unable to iterate over the object.]{#question6_100_1_opt_e}
-   Incorrect, Python can iterate over this type.
:::

::: {.runestone}
-   [string]{#question6_100_2_opt_a}
-   Yes, the iterable in this example is a string
-   [list]{#question6_100_2_opt_b}
-   Incorrect, that is not the type of the iterable.
-   [tuple]{#question6_100_2_opt_c}
-   Incorrect, that is not the type of the iterable.
-   [iterable]{#question6_100_2_opt_d}
-   Incorrect, that is not the type of the iterable.
-   [error, unable to iterate over the object.]{#question6_100_2_opt_e}
-   Incorrect, Python can iterate over this type.
:::

::: {.runestone}
-   [string]{#question6_100_3_opt_a}
-   Incorrect, there are no strings present in the code.
-   [list]{#question6_100_3_opt_b}
-   Incorrect, there are no lists present in the code.
-   [tuple]{#question6_100_3_opt_c}
-   Incorrect, there are no tuples in the code.
-   [iterable]{#question6_100_3_opt_d}
-   Incorrect, there are no iterable objects in the code.
-   [error, unable to iterate over the object.]{#question6_100_3_opt_e}
-   Yes, Python is unable to iterate over integers and floats.
:::

::: {.runestone}
-   [string]{#question6_100_4_opt_a}
-   Incorrect, the iterable is not a string.
-   [list]{#question6_100_4_opt_b}
-   Incorrect, there is no list in the code.
-   [tuple]{#question6_100_4_opt_c}
-   Yes, the iterable in this situation is a tuple.
-   [iterable]{#question6_100_4_opt_d}
-   Incorrect, that is not the best answer for this problem.
-   [error, unable to iterate over the object.]{#question6_100_4_opt_e}
-   Incorrect, Python can iterate over this type.
:::

::: {.runestone}
-   [string]{#question6_100_6_opt_a}
-   Correct! Every item in the iterator variable will be a string.
-   [list]{#question6_100_6_opt_b}
-   Incorrect, that is not the type of the iterator variable.
-   [tuple]{#question6_100_6_opt_c}
-   Incorrect, that is not the type of the iterator variable.
-   [integer]{#question6_100_6_opt_d}
-   Incorrect, that is not the type of the iterator variable.
-   [error, unable to iterate and initialize the iterator
    variable]{#question6_100_6_opt_e}
-   Incorrect, the for loop is iterating over an iterable object.
:::

::: {.runestone}
-   [string]{#question6_100_7_opt_a}
-   Incorrect, think about what the for loop will look at first.
-   [list]{#question6_100_7_opt_b}
-   Incorrect, that is the type of the iterable, not the iterator
    variable.
-   [tuple]{#question6_100_7_opt_c}
-   Incorrect, there is no tuple in the code.
-   [integer]{#question6_100_7_opt_d}
-   Yes, the first item in t is an integer.
-   [error, unable to iterate and initialize the iterator
    variable]{#question6_100_7_opt_e}
-   Incorrect, the for loop is iterating over an iterable object.
:::

::: {.runestone}
-   [string]{#question6_100_8_opt_a}
-   Yes, the second item in t is a string.
-   [list]{#question6_100_8_opt_b}
-   Incorrect, that is the type of the iterable, not the iterator
    variable.
-   [tuple]{#question6_100_8_opt_c}
-   Incorrect, there is no tuple in the code.
-   [integer]{#question6_100_8_opt_d}
-   Incorrect, think about what the for loop will look at during the
    second iteration.
-   [error, unable to iterate and initialize the iterator
    variable]{#question6_100_8_opt_e}
-   Incorrect, the for loop is iterating over an iterable object.
:::

::: {.runestone}
-   [string]{#question6_100_9_opt_a}
-   Yes, the last value stored in the iterator variable, blue, is the
    letter \"s\", which is a string (note that even a single character
    is a string in python).
-   [list]{#question6_100_9_opt_b}
-   Incorrect, there is no list in the code.
-   [tuple]{#question6_100_9_opt_c}
-   Incorrect, there is no tuple in the code.
-   [integer]{#question6_100_9_opt_d}
-   Incorrect, there is no integer in the code.
-   [error, unable to iterate and initialize the iterator
    variable]{#question6_100_9_opt_e}
-   Incorrect, the for loop is iterating over an iterable object.
:::

As you go through the codelens window, you will be asked a set of
questions.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="7.12.9"}
::: {#clensQuestion6_100_10_question .ac_question}
:::

::: {#clensQuestion6_100_10 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 7.12.9
(clensQuestion6\_100\_10)]{.runestone_caption_text}
:::
:::

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="7.12.10"}
::: {#clensQuestion6_100_11_question .ac_question}
:::

::: {#clensQuestion6_100_11 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 7.12.10
(clensQuestion6\_100\_11)]{.runestone_caption_text}
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

-   [[](GeneralizedSequences.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
