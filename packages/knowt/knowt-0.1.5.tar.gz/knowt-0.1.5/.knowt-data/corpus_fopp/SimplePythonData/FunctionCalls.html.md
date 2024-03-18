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
        Problem](/runestone/default/reportabug?course=fopp&page=FunctionCalls)
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
::: {#function-calls .section}
[2.4. ]{.section-number}Function Calls[¶](#function-calls "Permalink to this heading"){.headerlink}
===================================================================================================

The Python interpreter can compute new values with function calls. You
are familiar with the idea of functions from high school algebra. There
you might define a function `f`{.docutils .literal .notranslate} by
specifying how it transforms an input into an output,
`f(x) = 3x + 2`{.docutils .literal .notranslate}. Then, you might write
`f(5)`{.docutils .literal .notranslate} and expect to get the value 17.

Python adopts a similar syntax for invoking functions. If there is a
named function `foo`{.docutils .literal .notranslate} that takes a
single input, we can invoke foo on the value 5 by writing
`foo(5)`{.docutils .literal .notranslate}.

There are many built-in functions available in Python. You'll be seeing
some in this chapter and the next couple of chapters.

Functions are like factories that take in some material, do some
operation, and then send out the resulting object.

![Icon that represents a function. Appears simliar to a factory with
three places on top for inputs to come in and a place on the bottom for
the output/return value to come out.](../_images/function_object.png)

In this case, we refer to the materials as arguments or inputs and the
resulting object is referred to as output or return value. This process
of taking input, doing something, and then sending back the output is
demonstrated in the gif below.

![Animated gif that deomnstrates using the visual representation of a
factory as used above. Shows three arrows coming into the function to
represent that input or arguments that a function can require. It then
shows the function object shaking, representing an action being
completed by the function. Then it shows annother arrow leaving the
function image, which represents a return value or output coming from
the factory.](../_images/function_calls.gif)

::: {.admonition .note}
Note

Don't confuse the "output value" of a function with the output window.
The output of a function is a Python value and we can never really see
the internal representation of a value. But we can draw pictures to help
us imagine what values are, or we can print them to see an external
representation in the output window.

To confuse things even more, `print`{.docutils .literal .notranslate} is
actually a function. All functions produce output values. Only the
`print`{.docutils .literal .notranslate} function causes things to
appear in the output window.
:::

It is also possible for programmers to define new functions in their
programs. You will learn how to do that later in the course. For now,
you just need to learn how to invoke, or call, a function, and
understand that the execution of the function returns a computed value.

::: {.runestone .explainer .ac_section}
::: {#ac2_4_1 component="activecode" question_label="2.4.1"}
::: {#ac2_4_1_question .ac_question}
:::
:::
:::

We've defined two functions above. The code is hidden so as not to
bother you (yet) with how functions are defined. `square`{.docutils
.literal .notranslate} takes a single input parameter, and returns that
input multiplied by itself. `sub`{.docutils .literal .notranslate} takes
two input parameters and returns the result of subtracting the second
from the first. Obviously, these functions are not particularly useful,
since we have the operators `*`{.docutils .literal .notranslate} and
`-`{.docutils .literal .notranslate} available. But they illustrate how
functions work. The visual below illustrates how the `square`{.docutils
.literal .notranslate} function works.

![a visual of the square function. Four is provided as the input, the
function object shakes, and then sixteen comes out from the bottom of
the function object.](../_images/square_function.gif)

::: {.runestone .explainer .ac_section}
::: {#ac2_4_2 component="activecode" question_label="2.4.2"}
::: {#ac2_4_2_question .ac_question}
:::
:::
:::

Notice that when a function takes more than one input parameter, the
inputs are separated by a comma. Also notice that the order of the
inputs matters. The value before the comma is treated as the first
input, the value after it as the second input.

Again, remember that when Python performs computations, the results are
only shown in the output window if there's a print statement that says
to do that. In the activecode window above, `square(5)`{.docutils
.literal .notranslate} produces the value 25 but we never get to see
that in the output window, because it is not printed.

::: {#function-calls-as-part-of-complex-expressions .section}
[2.4.1. ]{.section-number}Function calls as part of complex expressions[¶](#function-calls-as-part-of-complex-expressions "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------------------------------------------------------------------------

Anywhere in an expression that you can write a literal like a number,
you can also write a function invocation that produces a number.

For example:

::: {.runestone .explainer .ac_section}
::: {#ac2_4_3 component="activecode" question_label="2.4.1.1"}
::: {#ac2_4_3_question .ac_question}
:::
:::
:::

Let's take a look at how that last execution unfolds.

::: {#se_ac2_4_1a .runestone .explainer component="showeval" question_label="2.4.1.2" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
Notice that we always have to resolve the expression inside the
innermost parentheses first, in order to determine what input to provide
when calling the functions.\
:::

::: {.evalCont}
:::
:::
:::

::: {#functions-are-objects-parentheses-invoke-functions .section}
[2.4.2. ]{.section-number}Functions are objects; parentheses invoke functions[¶](#functions-are-objects-parentheses-invoke-functions "Permalink to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Remember that earlier we mentioned that some kinds of Python objects
don't have a nice printed representation? Functions are themselves just
objects. If you tell Python to print the function object, rather than
printing the results of invoking the function object, you'll get one of
those not-so-nice printed representations.

Just typing the name of the function refers to the function as an
object. Typing the name of the function followed by parentheses
`()`{.docutils .literal .notranslate} invokes the function.

::: {.runestone .explainer .ac_section}
::: {#ac2_4_4 component="activecode" question_label="2.4.2.1"}
::: {#ac2_4_4_question .ac_question}
:::
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

-   [[](Operators.html)]{#relations-prev}
-   [[](DataTypes.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
