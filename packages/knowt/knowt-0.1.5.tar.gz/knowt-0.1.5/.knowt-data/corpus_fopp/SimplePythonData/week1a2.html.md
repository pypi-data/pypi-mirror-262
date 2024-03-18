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
        Problem](/runestone/default/reportabug?course=fopp&page=week1a2)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [2.1
        Introduction](intro-VariablesExpressionsandStatements.html){.reference
        .internal}
    -   [2.2 Values and Data Types](Values.html){.reference .internal}
    -   [2.3 Operators and Operands](Operators.html){.reference
        .internal}
    -   [2.4 Function Calls](FunctionCalls.html){.reference .internal}
    -   [2.5 Data Types](DataTypes.html){.reference .internal}
    -   [2.6 Type conversion
        functions](ConvertTypeFunctions.html){.reference .internal}
    -   [2.7 Variables](Variables.html){.reference .internal}
    -   [2.8 Variable Names and
        Keywords](VariableNamesandKeywords.html){.reference .internal}
    -   [2.9 👩‍💻 Choosing the Right Variable
        Name](WPChoosingtheRightVariableName.html){.reference .internal}
    -   [2.10 Statements and
        Expressions](StatementsandExpressions.html){.reference
        .internal}
    -   [2.11 Order of Operations](OrderofOperations.html){.reference
        .internal}
    -   [2.12 Reassignment](Reassignment.html){.reference .internal}
    -   [2.13 Updating Variables](UpdatingVariables.html){.reference
        .internal}
    -   [2.14 👩‍💻 Hard-Coding](HardCoding.html){.reference .internal}
    -   [2.15 Input](Input.html){.reference .internal}
    -   [2.16 Glossary](Glossary.html){.reference .internal}
    -   [2.17 Exercises](Exercises.html){.reference .internal}
    -   [2.18 Chapter Assessment](week1a2.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#chapter-assessment .section}
[2.18. ]{.section-number}Chapter Assessment[¶](#chapter-assessment "Permalink to this heading"){.headerlink}
============================================================================================================

**Check your understanding**

::: {.runestone .explainer .ac_section}
::: {#assess_ps_01_01 component="activecode" question_label="2.18.1"}
::: {#assess_ps_01_01_question .ac_question}
There is a function we are providing in for you in this problem called
`square`{.docutils .literal .notranslate}. It takes one integer and
returns the square of that integer value. Write code to assign a
variable called `xyz`{.docutils .literal .notranslate} the value
`5*5`{.docutils .literal .notranslate} (five squared). Use the square
function, rather than just multiplying with `*`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#assess_ps_01_02 component="activecode" question_label="2.18.2"}
::: {#assess_ps_01_02_question .ac_question}
Write code to assign the number of *characters* in the string
`rv`{.docutils .literal .notranslate} to a variable
`num_chars`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone}
-   [a = len(\"hello worldwelcome!\")]{#assess_question1_1_1_3_opt_a}
-   Though we are using the len function here, we are hardcoding what
    len should return the length of. We are not referencing z or y.
-   [a = 11 + 8]{#assess_question1_1_1_3_opt_b}
-   This is hardcoding, we are writing in the value without referencing
    z or y.
-   [a = len(z) + len(y)]{#assess_question1_1_1_3_opt_c}
-   This is not considered hard coding. We are using the function len to
    determine the length of what is stored in z and y, which is a
    correct way to approach this problem.
-   [a = len(\"hello world\") +
    len(\"welcome!\")]{#assess_question1_1_1_3_opt_d}
-   Though we are using the len function here, we are hardcoding what
    len should return the length of each time we call len. We are not
    referencing z or y.
-   [none of the above are hardcoding.]{#assess_question1_1_1_3_opt_e}
-   At least one of these solutions is considered hardcoding. Take
    another look.
:::

::: {.runestone .explainer .ac_section}
::: {#assess_addl_functions component="activecode" question_label="2.18.4"}
::: {#assess_addl_functions_question .ac_question}
(This is not an assessment question) The code below defines functions
used by one of the questions above. Do not modify the code, but feel
free to take a look.
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
-   [[](../Debugging/toctree.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
