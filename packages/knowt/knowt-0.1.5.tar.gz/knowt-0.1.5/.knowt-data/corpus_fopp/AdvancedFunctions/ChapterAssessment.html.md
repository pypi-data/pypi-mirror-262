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
    -   [15.1 Introduction: Optional
        Parameters](OptionalParameters.html){.reference .internal}
    -   [15.2 Keyword Parameters](KeywordParameters.html){.reference
        .internal}
    -   [15.3 Anonymous functions with lambda
        expressions](Anonymousfunctionswithlambdaexpressions.html){.reference
        .internal}
    -   [15.4 👩‍💻 Programming With
        Style](ProgrammingWithStyle.html){.reference .internal}
    -   [15.5 Method Invocations](MethodInvocations.html){.reference
        .internal}
    -   [15.6 Function Wrapping and
        Decorators](FunctionWrappingAndDecorators.html){.reference
        .internal}
    -   [15.7 Exercises](Exercises.html){.reference .internal}
    -   [15.8 Chapter Assessment](ChapterAssessment.html){.reference
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
[15.8. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.runestone .explainer .ac_section}
::: {#ac15_5_1 component="activecode" question_label="15.8.1"}
::: {#ac15_5_1_question .ac_question}
Create a function called `mult`{.docutils .literal .notranslate} that
has two parameters, the first is required and should be an integer, the
second is an optional parameter that can either be a number or a string
but whose default is 6. The function should return the first parameter
multiplied by the second.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_5_2 component="activecode" question_label="15.8.2"}
::: {#ac15_5_2_question .ac_question}
The following function, `greeting`{.docutils .literal .notranslate},
does not work. Please fix the code so that it runs without error. This
only requires one change in the definition of the function.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_5_3 component="activecode" question_label="15.8.3"}
::: {#ac15_5_3_question .ac_question}
Below is a function, `sum`{.docutils .literal .notranslate}, that does
not work. Change the function definition so the code works. The function
should still have a required parameter, `intx`{.docutils .literal
.notranslate}, and an optional parameter, `intz`{.docutils .literal
.notranslate} with a defualt value of 5.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_5_4 component="activecode" question_label="15.8.4"}
::: {#ac15_5_4_question .ac_question}
Write a function, `test`{.docutils .literal .notranslate}, that takes in
three parameters: a required integer, an optional boolean whose default
value is `True`{.docutils .literal .notranslate}, and an optional
dictionary, called `dict1`{.docutils .literal .notranslate}, whose
default value is `{2:3, 4:5, 6:8}`{.docutils .literal .notranslate}. If
the boolean parameter is True, the function should test to see if the
integer is a key in the dictionary. The value of that key should then be
returned. If the boolean parameter is False, return the boolean value
"False".
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_5_5 component="activecode" question_label="15.8.5"}
::: {#ac15_5_5_question .ac_question}
Write a function called `checkingIfIn`{.docutils .literal .notranslate}
that takes three parameters. The first is a required parameter, which
should be a string. The second is an optional parameter called
`direction`{.docutils .literal .notranslate} with a default value of
`True`{.docutils .literal .notranslate}. The third is an optional
parameter called `d`{.docutils .literal .notranslate} that has a default
value of
`{'apple': 2, 'pear': 1, 'fruit': 19, 'orange': 5, 'banana': 3, 'grapes': 2, 'watermelon': 7}`{.docutils
.literal .notranslate}. Write the function `checkingIfIn`{.docutils
.literal .notranslate} so that when the second parameter is
`True`{.docutils .literal .notranslate}, it checks to see if the first
parameter is a key in the third parameter; if it is, return
`True`{.docutils .literal .notranslate}, otherwise return
`False`{.docutils .literal .notranslate}.

But if the second paramter is `False`{.docutils .literal .notranslate},
then the function should check to see if the first parameter is *not* a
key of the third. If it's *not*, the function should return
`True`{.docutils .literal .notranslate} in this case, and if it is, it
should return `False`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_5_6 component="activecode" question_label="15.8.6"}
::: {#ac15_5_6_question .ac_question}
We have provided a function below and the skeleton of three invocations
of the function. Fill in the parameters of the invocations to produce
the specified outputs
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
-   [[](../Sorting/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
