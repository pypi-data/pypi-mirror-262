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
        Problem](/runestone/default/reportabug?course=fopp&page=ChapterAssessment)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [19.1 What is an exception?](intro-exceptions.html){.reference
        .internal}
    -   [19.3 👩‍💻 When to use
        try/except](using-exceptions.html){.reference .internal}
    -   [19.4 Standard Exceptions](standard-exceptions.html){.reference
        .internal}
    -   [19.5 Exercises](Exercises.html){.reference .internal}
    -   [19.6 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#chapter-assessment .section}
[19.6. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_01 component="activecode" question_label="19.6.1"}
::: {#ac_exceptions_01_question .ac_question}
The code below takes the list of country, `country`{.docutils .literal
.notranslate}, and searches to see if it is in the dictionary
`gold`{.docutils .literal .notranslate} which shows some countries who
won gold during the Olympics. However, this code currently does not
work. Correctly add try/except clause in the code so that it will
correctly populate the list, `country_gold`{.docutils .literal
.notranslate}, with either the number of golds won or the string "Did
not get gold".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_011 component="activecode" question_label="19.6.2"}
::: {#ac_exceptions_011_question .ac_question}
Provided is a buggy for loop that tries to accumulate some values out of
some dictionaries. Insert a try/except so that the code passes.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_02 component="activecode" question_label="19.6.3"}
::: {#ac_exceptions_02_question .ac_question}
The list, `numb`{.docutils .literal .notranslate}, contains integers.
Write code that populates the list `remainder`{.docutils .literal
.notranslate} with the remainder of 36 divided by each number in
`numb`{.docutils .literal .notranslate}. For example, the first element
should be 0, because 36/6 has no remainder. If there is an error, have
the string "Error" appear in the `remainder`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_021 component="activecode" question_label="19.6.4"}
::: {#ac_exceptions_021_question .ac_question}
Provided is buggy code, insert a try/except so that the code passes.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_03 component="activecode" question_label="19.6.5"}
::: {#ac_exceptions_03_question .ac_question}
Write code so that the buggy code provided works using a try/except.
When the codes does not work in the try, have it append to the list
`attempt`{.docutils .literal .notranslate} the string "Error".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_031 component="activecode" question_label="19.6.6"}
::: {#ac_exceptions_031_question .ac_question}
The following code tries to append the third element of each list in
`conts`{.docutils .literal .notranslate} to the new list
`third_countries`{.docutils .literal .notranslate}. Currently, the code
does not work. Add a try/except clause so the code runs without errors,
and the string 'Continent does not have 3 countries' is appended to
`third_countries`{.docutils .literal .notranslate} instead of producing
an error.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_04 component="activecode" question_label="19.6.7"}
::: {#ac_exceptions_04_question .ac_question}
The buggy code below prints out the value of the sport in the list
`sport`{.docutils .literal .notranslate}. Use try/except so that the
code will run properly. If the sport is not in the dictionary,
`ppl_play`{.docutils .literal .notranslate}, add it in with the value of
1.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac_exceptions_041 component="activecode" question_label="19.6.8"}
::: {#ac_exceptions_041_question .ac_question}
Provided is a buggy for loop that tries to accumulate some values out of
some dictionaries. Insert a try/except so that the code passes. If the
key is not there, initialize it in the dictionary and set the value to
zero.
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

-   [[](Exercises.html)]{#relations-prev}
-   [[](../Classes/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
