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
        Problem](/runestone/default/reportabug?course=fopp&page=TypeAnnotations)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [12.1 Introduction to
        Functions](intro-Functions.html){.reference .internal}
    -   [12.2 Function Definition](FunctionDefinitions.html){.reference
        .internal}
    -   [12.3 Function Invocation](FunctionInvocation.html){.reference
        .internal}
    -   [12.4 Function Parameters](FunctionParameters.html){.reference
        .internal}
    -   [12.5 Returning a value from a
        function](Returningavaluefromafunction.html){.reference
        .internal}
    -   [12.6 👩‍💻 Decoding a
        Function](DecodingaFunction.html){.reference .internal}
    -   [12.7 Type Annotations](TypeAnnotations.html){.reference
        .internal}
    -   [12.8 A function that
        accumulates](Afunctionthataccumulates.html){.reference
        .internal}
    -   [12.9 Variables and parameters are
        local](Variablesandparametersarelocal.html){.reference
        .internal}
    -   [12.10 Global Variables](GlobalVariables.html){.reference
        .internal}
    -   [12.11 Functions can call other functions
        (Composition)](Functionscancallotherfunctions.html){.reference
        .internal}
    -   [12.12 Flow of Execution
        Summary](FlowofExecutionSummary.html){.reference .internal}
    -   [12.13 👩‍💻 Print vs. return](Printvsreturn.html){.reference
        .internal}
    -   [12.14 Passing Mutable
        Objects](PassingMutableObjects.html){.reference .internal}
    -   [12.15 Side Effects](SideEffects.html){.reference .internal}
    -   [12.16 Glossary](Glossary.html){.reference .internal}
    -   [12.17 Exercises](Exercises.html){.reference .internal}
    -   [12.18 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#type-annotations .section}
[]{#index-0}

[12.7. ]{.section-number}Type Annotations[¶](#type-annotations "Permalink to this heading"){.headerlink}
========================================================================================================

In the previous section, we discussed the decoding work that is required
when you look at a function and are trying to determine the types of its
parameters. In this section, we'll introduce a feature that can help
reduce the amount of sleuthing that is needed.

Consider the following function definition:

::: {.highlight-python .notranslate}
::: {.highlight}
    def duplicate(msg):
        """Returns a string containing two copies of `msg`"""

        return msg + msg
:::
:::

This function is intended to duplicate a message; if called with the
value 'Hello', it returns the value 'HelloHello'. If called with other
types of data, however, it will not work properly. (What will the
function do if given an `int`{.docutils .literal .notranslate} or a
`float`{.docutils .literal .notranslate} value?)

Python allows you to indicate the intended type of the function
parameters and the type of the function return value in a function
definition using a special notation demonstrated in this example:

::: {.runestone .explainer .ac_section}
::: {#ac_annotate1 component="activecode" question_label="12.7.1"}
::: {#ac_annotate1_question .ac_question}
:::
:::
:::

This definition of `duplicate`{.docutils .literal .notranslate} makes
use of type annotations that indicate the function's parameter type and
return type. A **type annotation**, sometimes called a type hint, is an
optional notation that specifies the type of a parameter or function
result. It tells the programmer using the function what kind of data to
pass to the function, and what kind of data to expect when the function
returns a value.

In the definition above, the annotation `: str`{.docutils .literal
.notranslate} in `msg: str`{.docutils .literal .notranslate} indicates
that the caller should pass a `str`{.docutils .literal .notranslate}
value as an argument. The annotation `-> str`{.docutils .literal
.notranslate} indicates that the function will produce a `str`{.docutils
.literal .notranslate} result.

Here are some more examples of functions with type annotations:

::: {.runestone .explainer .ac_section}
::: {#ac_annotate2 component="activecode" question_label="12.7.2"}
::: {#ac_annotate2_question .ac_question}
:::
:::
:::

It's important to understand that adding type annotations to a function
definition does not cause the Python interpreter to check that the
values passed to a function are the expected types, or cause the
returned value to be converted to the expected type. For example, if the
function `add`{.docutils .literal .notranslate} in the example above is
called like this:

::: {.highlight-default .notranslate}
::: {.highlight}
    result = add('5', '15')
:::
:::

the function will receive two string values, concatenate them, and
return the resulting string '515'. The `int`{.docutils .literal
.notranslate} annotations are completely ignored by the Python
interpreter. Think of type annotations as a kind of function
documentation, and remember that they have no effect on the program's
behavior.

Type annotations are an optional aspect of documenting functions. Still,
type annotations are an important tool to increase the readability of
your code, and you should use them in your programs.

::: {.admonition .note}
Note

Although type annotations are ignored by the Python interpreter, there
are tools such as [mypy](http://mypy-lang.org/){.reference .external}
that can analyze your code containing type annotations and flag
potential problems.
:::

Type hints can be especially useful for container types, like lists and
dictionaries. When type hinting was first introduced into python, in
version 3.5, it was possible to specify them, but a little clunky. Later
versions made it a little easier.

For example, in the following code, which is valid in python version
3.10, the count\_words function takes a string as input and returns a
dictionary. That dictionary's keys should all be strings and the value
associated with every key should be an integer.

::: {.runestone .explainer .ac_section}
::: {#ac_annotate3 component="activecode" question_label="12.7.3"}
::: {#ac_annotate3_question .ac_question}
:::
:::
:::

In the code below, the function add\_em\_up takes an input that is
expected to be a list of numbers. It returns the sum of all of them.

::: {.runestone .explainer .ac_section}
::: {#ac_annotate4 component="activecode" question_label="12.7.4"}
::: {#ac_annotate4_question .ac_question}
:::
:::
:::

Actually, this code should work just fine if the inputs are either
integers or floats. If any are floats, then the return value will be a
float. The more recent versions of type annotations in python allow the
use the \| symbol (pronounced "pipe") to specify a union, that either of
two types is permitted. You may find that it's not permitted in the
current runestone interpreter, though.

::: {.runestone .explainer .ac_section}
::: {#ac_annotate5 component="activecode" question_label="12.7.5"}
::: {#ac_annotate5_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [The value 4.5 is displayed on the screen.]{#question_ta_1_opt_a}
-   Correct! Python ignores the \': str\' annotation and returns the sum
    of msg (the float 2.5) + 2.
-   [The value 2.52 is displayed on the screen.]{#question_ta_1_opt_b}
-   Incorrect. In this call, msg contains the float value 2.5; the \':
    str\' annotation serves only as documentation.
-   [A runtime error occurs when the function is invoked because 2.5 is
    not a string.]{#question_ta_1_opt_c}
-   Incorrect. Python ignores the \': str\' annotation and allows the
    float value 2.5 to be passed to msg.
-   [A runtime error occurs because the expression \'msg + 2\' illegally
    attempts to concatenate a str and an int.]{#question_ta_1_opt_d}
-   Incorrect. In this call, msg contains the float value 2.5, not a
    str, so the + operation is legal.
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

-   [[](DecodingaFunction.html)]{#relations-prev}
-   [[](Afunctionthataccumulates.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
