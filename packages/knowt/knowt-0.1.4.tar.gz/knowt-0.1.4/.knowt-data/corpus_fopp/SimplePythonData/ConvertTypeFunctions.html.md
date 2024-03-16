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
        Problem](/runestone/default/reportabug?course=fopp&page=ConvertTypeFunctions)
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
::: {#type-conversion-functions .section}
[2.6. ]{.section-number}Type conversion functions[¶](#type-conversion-functions "Permalink to this heading"){.headerlink}
=========================================================================================================================

Sometimes it is necessary to convert values from one type to another.
Python provides a few simple functions that will allow us to do that.
The functions `int`{.docutils .literal .notranslate}, `float`{.docutils
.literal .notranslate} and `str`{.docutils .literal .notranslate} will
(attempt to) convert their arguments into types `int`{.docutils .literal
.notranslate}, `float`{.docutils .literal .notranslate} and
`str`{.docutils .literal .notranslate} respectively. We call these
**type conversion** functions.

The `int`{.docutils .literal .notranslate} function can take a floating
point number or a string, and turn it into an int. For floating point
numbers, it *discards* the decimal portion of the number - a process we
call *truncation towards zero* on the number line. Let us see this in
action:

::: {.runestone .explainer .ac_section}
::: {#ac2_6_1 component="activecode" question_label="2.6.1"}
::: {#ac2_6_1_question .ac_question}
:::
:::
:::

The last case shows that a string has to be a syntactically legal
number, otherwise you'll get one of those pesky runtime errors. Modify
the example by deleting the `bottles`{.docutils .literal .notranslate}
and rerun the program. You should see the integer `23`{.docutils
.literal .notranslate}.

The type converter `float`{.docutils .literal .notranslate} can turn an
integer, a float, or a syntactically legal string into a float.

::: {.runestone .explainer .ac_section}
::: {#ac2_6_2 component="activecode" question_label="2.6.2"}
::: {#ac2_6_2_question .ac_question}
:::
:::
:::

The type converter `str`{.docutils .literal .notranslate} turns its
argument into a string. Remember that when we print a string, the quotes
are removed in the output window. However, if we print the type, we can
see that it is definitely `str`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac2_6_3 component="activecode" question_label="2.6.3"}
::: {#ac2_6_3_question .ac_question}
:::
:::
:::

One common operation where you might need to do a type conversion is
when you are concatenating several strings together but want to include
a numeric value as part of the final string. Because we can't
concatenate a string with an integer or floating point number, we will
often have to convert numbers to strings before concatenating them.

![a variable stores the value 55. a print statement tries to print \"the
value is\" concatenated with the integer, but a runtime error occurs.
Solution is to convert the integer into a string so that it can be
concatenated.](../_images/type_cast.gif)

**Check your understanding**

::: {.runestone}
-   [Nothing is printed. It generates a runtime
    error.]{#question2_6_1_opt_a}
-   The statement is valid Python code. It calls the int function on
    53.785 and then prints the value that is returned.
-   [53]{#question2_6_1_opt_b}
-   The int function truncates all values after the decimal and prints
    the integer value.
-   [54]{#question2_6_1_opt_c}
-   When converting to an integer, the int function does not round.
-   [53.785]{#question2_6_1_opt_d}
-   The int function removes the fractional part of 53.785 and returns
    an integer, which is then printed.
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

-   [[](DataTypes.html)]{#relations-prev}
-   [[](Variables.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
