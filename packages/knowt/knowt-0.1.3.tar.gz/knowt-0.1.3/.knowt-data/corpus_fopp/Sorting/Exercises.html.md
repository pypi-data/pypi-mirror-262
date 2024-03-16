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
        Problem](/runestone/default/reportabug?course=fopp&page=Exercises)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [16.1 Introduction: Sorting with Sort and
        Sorted](intro-SortingwithSortandSorted.html){.reference
        .internal}
    -   [16.2 Optional reverse
        parameter](Optionalreverseparameter.html){.reference .internal}
    -   [16.3 Optional key
        parameter](Optionalkeyparameter.html){.reference .internal}
    -   [16.4 Sorting a Dictionary](SortingaDictionary.html){.reference
        .internal}
    -   [16.5 Breaking Ties: Second
        Sorting](SecondarySortOrder.html){.reference .internal}
    -   [16.6 👩‍💻 When to use a Lambda
        Expression](WPWhenToUseLambdaVsFunction.html){.reference
        .internal}
    -   [16.7 Glossary](Glossary.html){.reference .internal}
    -   [16.8 Exercises](Exercises.html){.reference .internal}
    -   [16.9 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#exercises .section}
[16.8. ]{.section-number}Exercises[¶](#exercises "Permalink to this heading"){.headerlink}
==========================================================================================

::: {#q1 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac18_8_1 component="activecode" question_label="16.8.1"}
::: {#ac18_8_1_question .ac_question}
You're going to write a function that takes a string as a parameter and
returns a list of the five most frequent characters in the string.
Eventually, you will be able to do this sort of problem without a lot of
coaching. But we're going to step you through it as a series of
exercises.

First, the function will count the frequencies of all the characters, as
we've done before, using a dictionary and the accumulator pattern. Then,
it will sort the (key, value) pairs. Finally, it will take a slice of
the sorted list to get just the top five. That slice will be returned.

Step 1. Suppose you had this list, \[8, 7, 6, 6, 4, 4, 3, 1, 0\],
already sorted, how would you make a list of just the best 5? (Hint:
take a slice).
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer16_8_1 component="activecode" question_label="16.8.2"}
::: {#answer16_8_1_question .ac_question}
:::
:::
:::
:::
:::

::: {#q2 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac18_8_2 component="activecode" question_label="16.8.3"}
::: {#ac18_8_2_question .ac_question}
Now suppose the list wasn't sorted yet. How would get those same five
elements from this list?
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer16_8_2 component="activecode" question_label="16.8.4"}
::: {#answer16_8_2_question .ac_question}
:::
:::
:::
:::
:::

::: {#q3 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac18_8_3 component="activecode" question_label="16.8.5"}
::: {#ac18_8_3_question .ac_question}
Now take a list L and make a dictionary of counts for how often these
numbers appear in the list.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer16_8_3 component="activecode" question_label="16.8.6"}
::: {#answer16_8_3_question .ac_question}
:::
:::
:::
:::
:::

::: {#q4 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac18_8_4 component="activecode" question_label="16.8.7"}
::: {#ac18_8_4_question .ac_question}
Now sort the keys (numbers) based on their frequencies. Review *Sorting
a Dictionary* if you're not sure how to do this. Keep just the top five
keys.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer16_8_4 component="activecode" question_label="16.8.8"}
::: {#answer16_8_4_question .ac_question}
:::
:::
:::
:::
:::

::: {#q5 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac18_8_5 component="activecode" question_label="16.8.9"}
::: {#ac18_8_5_question .ac_question}
Finally, generalize what you've done. Write a function that takes a
string instead of a list as a parameter and returns a list of the five
most frequent characters in the string.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.runestone .explainer .ac_section}
::: {#answer16_8_5 component="activecode" question_label="16.8.10"}
::: {#answer16_8_5_question .ac_question}
:::
:::
:::
:::
:::

::: {#contributed-exercises .section}
[16.8.1. ]{.section-number}Contributed Exercises[¶](#contributed-exercises "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------
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

-   [[](Glossary.html)]{#relations-prev}
-   [[](ChapterAssessment.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
