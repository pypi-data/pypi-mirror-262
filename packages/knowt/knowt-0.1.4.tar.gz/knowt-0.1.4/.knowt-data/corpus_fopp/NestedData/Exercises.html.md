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
    -   [17.1 Introduction: Nested Data and Nested
        Iteration](ListswithComplexItems.html){.reference .internal}
    -   [17.2 Nested Dictionaries](NestedDictionaries.html){.reference
        .internal}
    -   [17.3 Processing JSON results](jsonlib.html){.reference
        .internal}
    -   [17.4 Nested Iteration](NestedIteration.html){.reference
        .internal}
    -   [17.5 👩‍💻 Structuring Nested
        Data](WPStructuringNestedData.html){.reference .internal}
    -   [17.6 Deep and Shallow
        Copies](DeepandShallowCopies.html){.reference .internal}
    -   [17.7 👩‍💻 Extracting from Nested
        Data](WPExtractFromNestedData.html){.reference .internal}
    -   [17.8 Exercises](Exercises.html){.reference .internal}
    -   [17.9 Chapter Assessment](ChapterAssessment.html){.reference
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
[17.8. ]{.section-number}Exercises[¶](#exercises "Permalink to this heading"){.headerlink}
==========================================================================================

::: {#q17_5_1 .full-width .container .question component="question" question_label="17.8.1"}
8.  ::: {#q1 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac17_5_1 component="activecode" question_label="17.8.2"}
    ::: {#ac17_5_1_question .ac_question}
    Iterate through the list so that if the character 'm' is in the
    string, then it should be added to a new list called
    `m_list`{.docutils .literal .notranslate}. Hint: Because this isn't
    just a list of lists, think about what type of object you want your
    data to be stored in. Conditionals may help you.
    :::
    :::
    :::
    :::
    :::
:::

::: {#q17_5_2 .full-width .container .question component="question" question_label="17.8.3"}
9.  ::: {#q2 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac17_5_2 component="activecode" question_label="17.8.4"}
    ::: {#ac17_5_2_question .ac_question}
    The nested dictionary, `pokemon`{.docutils .literal .notranslate},
    shows the number of various Pokemon that each person has caught
    while playing Pokemon Go. Find the total number of rattatas, dittos,
    and pidgeys caught and assign to the variables `r`{.docutils
    .literal .notranslate}, `d`{.docutils .literal .notranslate}, and
    `p`{.docutils .literal .notranslate} respectively. Do not hardcode.
    Note: Be aware that not every trainer has caught a ditto.
    :::
    :::
    :::
    :::
    :::
:::

::: {#q17_5_3 .full-width .container .question component="question" question_label="17.8.5"}
10. ::: {#q3 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac17_5_3 component="activecode" question_label="17.8.6"}
    ::: {#ac17_5_3_question .ac_question}
    Below, we have provided a nested list called `big_list`{.docutils
    .literal .notranslate}. Use nested iteration to create a dictionary,
    `word_counts`{.docutils .literal .notranslate}, that contains all
    the words in `big_list`{.docutils .literal .notranslate} as keys,
    and the number of times they occur as values.
    :::
    :::
    :::
    :::
    :::
:::

::: {#q17_5_4 .full-width .container .question component="question" question_label="17.8.7"}
11. ::: {#q4 .alert .alert-warning component="tabbedStuff"}
    ::: {component="tab" tabname="Question"}
    ::: {.runestone .explainer .ac_section}
    ::: {#ac17_5_4 component="activecode" question_label="17.8.8"}
    ::: {#ac17_5_4_question .ac_question}
    Provided is a dictionary that contains pokemon go player data, where
    each player reveals the amount of candy each of their pokemon have.
    If you pooled all the data together, which pokemon has the highest
    number of candy? Assign that pokemon to the variable
    `most_common_pokemon`{.docutils .literal .notranslate}.
    :::
    :::
    :::
    :::
    :::
:::

::: {#contributed-exercises .section}
[17.8.1. ]{.section-number}Contributed Exercises[¶](#contributed-exercises "Permalink to this heading"){.headerlink}
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

-   [[](WPExtractFromNestedData.html)]{#relations-prev}
-   [[](ChapterAssessment.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
