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
        Problem](/runestone/default/reportabug?course=fopp&page=Reassignment)
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
::: {#reassignment .section}
[2.12. ]{.section-number}Reassignment[¶](#reassignment "Permalink to this heading"){.headerlink}
================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#reassignmentvid .align-left .youtube-video component="youtube" video-height="315" question_label="2.12.1" video-width="560" video-videoid="G86akhNFHZA" video-divid="reassignmentvid" video-start="0" video-end="-1"}
:::
:::

As we have mentioned previously, it is legal to make more than one
assignment to the same variable. A new assignment makes an existing
variable refer to a new value (and stop referring to the old value).

::: {.runestone .explainer .ac_section}
::: {#ac2_13_1 component="activecode" question_label="2.12.2"}
::: {#ac2_13_1_question .ac_question}
:::
:::
:::

The first time `bruce`{.docutils .literal .notranslate} is printed, its
value is 5, and the second time, its value is 7. The assignment
statement changes the value (the object) that `bruce`{.docutils .literal
.notranslate} refers to.

Here is what **reassignment** looks like in a reference diagram:

![reassignment](../_images/reassign1.png)

It is important to note that in mathematics, a statement of equality is
always true. If `a is equal to b`{.docutils .literal .notranslate} now,
then `a will always equal to b`{.docutils .literal .notranslate}. In
Python, an assignment statement can make two variables refer to the same
object and therefore have the same value. They appear to be equal.
However, because of the possibility of reassignment, they don't have to
stay that way:

::: {.runestone .explainer .ac_section}
::: {#ac2_13_2 component="activecode" question_label="2.12.3"}
::: {#ac2_13_2_question .ac_question}
:::
:::
:::

Line 4 changes the value of `a`{.docutils .literal .notranslate} but
does not change the value of `b`{.docutils .literal .notranslate}, so
they are no longer equal. We will have much more to say about equality
in a later chapter.

::: {#developing-your-mental-model-of-how-python-evaluates .section}
[2.12.1. ]{.section-number}Developing your mental model of How Python Evaluates[¶](#developing-your-mental-model-of-how-python-evaluates "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Its important to start to develop a good mental model of the steps the
Python interpreter takes when evaluating an assignment statement. In an
assignment statement, the interpreter first evaluates the code on the
right hand side of the assignment operator. It then gives a name to
whatever that is. The (very short) visualization below shows what is
happening.

::: {#se_ac2_13_1a .runestone .explainer component="showeval" question_label="2.12.1.1" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
a = 5\
b = a\
:::

::: {.evalCont}
:::
:::

In the first statement `a = 5`{.docutils .literal .notranslate} the
literal number 5 evaluates to 5, and is given the name `a`{.docutils
.literal .notranslate}. In the second statement, the variable
`a`{.docutils .literal .notranslate} evaluates to 5 and so 5 now ends up
with a second name `b`{.docutils .literal .notranslate}.

You can step through the code and see how the variable assignments
change below.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="2.12.1.2"}
::: {#clens2_13_1_question .ac_question}
:::

::: {#clens2_13_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 2.12.1.2 (clens2\_13\_1)]{.runestone_caption_text}
:::
:::

::: {.admonition .note}
Note

In some programming languages, a different symbol is used for
assignment, such as `<-`{.docutils .literal .notranslate} or
`:=`{.docutils .literal .notranslate}. The intent is that this will help
to avoid confusion. Python chose to use the tokens `=`{.docutils
.literal .notranslate} for assignment, and `==`{.docutils .literal
.notranslate} for equality. This is a popular choice also found in
languages like C, C++, Java, and C\#.
:::

**Check your understanding**

::: {.runestone}
-   [x is 15 and y is 15]{#question2_13_1_opt_a}
-   Look at the last assignment statement which gives x a different
    value.
-   [x is 22 and y is 22]{#question2_13_1_opt_b}
-   No, x and y are two separate variables. Just because x changes in
    the last assignment statement, it does not change the value that was
    copied into y in the second statement.
-   [x is 15 and y is 22]{#question2_13_1_opt_c}
-   Look at the last assignment statement, which reassigns x, and not y.
-   [x is 22 and y is 15]{#question2_13_1_opt_d}
-   Yes, x has the value 22 and y the value 15.
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

-   [[](OrderofOperations.html)]{#relations-prev}
-   [[](UpdatingVariables.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
