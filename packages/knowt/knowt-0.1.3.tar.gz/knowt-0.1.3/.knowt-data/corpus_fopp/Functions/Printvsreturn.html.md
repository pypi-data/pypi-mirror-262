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
        Problem](/runestone/default/reportabug?course=fopp&page=Printvsreturn)
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
::: {#print-vs-return .section}
[12.13. ]{.section-number}👩‍💻 Print vs. return[¶](#print-vs-return "Permalink to this heading"){.headerlink}
============================================================================================================

Many beginning programmers find the distinction between print and return
very confusing, especially since most of the illustrations of return
values in intro texts like this one show the returned value from a
function call by printing it, as in `print(square(g(2)))`{.docutils
.literal .notranslate}.

The print statement is fairly easy to understand. It takes a python
object and outputs a printed representation of it in the output window.
You can think of the print statement as something that takes an object
from the land of the program and makes it visible to the land of the
human observer.

::: {.admonition .note}
Note

**Print is for people**. Remember that slogan. Printing has no effect on
the ongoing execution of a program. It doesn't assign a value to a
variable. It doesn't return a value from a function call.
:::

If you're confused, chances are the source of your confusion is really
about returned values and the evaluation of complex expressions. A
function that returns a value is producing a value for use *by the
program*, in particular for use in the part of the code where the
function was invoked. Remember that when a function is invoked, the
function's code block is executed -- all that code indented under the
`def`{.docutils .literal .notranslate} statement gets executed,
following the rules of the Python formal language for what should and
should not execute as it goes. But when the function returns, control
goes back to the calling location, and a return value may come back with
it.

You've already seen some function calls in Chapter 1. When we told you
about the function `square`{.docutils .literal .notranslate} that we
defined, you saw that the expression `square(2)`{.docutils .literal
.notranslate} evaluated to the integer value `4`{.docutils .literal
.notranslate}.

That's because the `square`{.docutils .literal .notranslate} function
*returns* a value: the square of whatever input is passed into it.

If a returned value is for use *by the program*, why did you make that
function invocation to return a value? What do you use the result of the
function call for? There are three possibilities.

1.  

    Save it for later.

    :   The returned value may be:

        -   Assigned to a variable. For example,
            `w = square(3)`{.docutils .literal .notranslate}

        -   Put in a list. For example, `L.append(square(3))`{.docutils
            .literal .notranslate}

        -   Put in a dictionary. For example,
            `d[3] = square(3)`{.docutils .literal .notranslate}

2.  

    Use it in a more complex expression.

    :   In that case, think of the return value as replacing the entire
        text of the function invocation. For example, if there is a line
        of code `w = square(square(3) + 7) - 5`{.docutils .literal
        .notranslate}, think of the return value 9 replacing the text
        square(3) in that invocation, so it becomes
        `square(9 + 7) -5`{.docutils .literal .notranslate}.

3.  

    Print it for human consumption.

    :   For example, `print(square(3))`{.docutils .literal .notranslate}
        outputs 9 to the output area. Note that, unless the return value
        is first saved as in possibility 1, it will be available only to
        the humans watching the output area, not to the program as it
        continues executing.

If your only purpose in running a function is to make an output visible
for human consumption, there are two ways to do it. You can put one or
more print statements inside the function definition and not bother to
return anything from the function (the value None will be returned). In
that case, invoke the function without a print statement. For example,
you can have an entire line of code that reads `f(3)`{.docutils .literal
.notranslate}. That will run the function f and throw away the return
value. Of course, if square doesn't print anything out or have any side
effects, it's useless to call it and do nothing with the return value.
But with a function that has print statements inside it, it can be quite
useful.

The other possibility is to return a value from the function and print
it, as in `print(f(3))`{.docutils .literal .notranslate}. As you start
to write larger, more complex programs, this will be more typical.
Indeed the print statement will usually only be a temporary measure
while you're developing the program. Eventually, you'll end up calling f
and saving the return value or using it as part of a more complex
expression.

You will know you've really internalized the idea of functions when you
are no longer confused about the difference between print and return.
Keep working at it until it makes sense to you!

**Check your understanding**

::: {.runestone}
-   [2]{#question11_11_1_opt_a}
-   2 is the input; the value returned from h is what will be printed.
-   [5]{#question11_11_1_opt_b}
-   Don\'t forget that 2 gets squared.
-   [7]{#question11_11_1_opt_c}
-   First square 2, then add 3.
-   [25]{#question11_11_1_opt_d}
-   3 is added to the result of squaring 2
-   [Error: y has a value but x is an unbound variable inside the square
    function]{#question11_11_1_opt_e}
-   When square is called, x is bound to the parameter value that is
    passed in, 2.
:::

::: {.runestone}
-   [2]{#question11_11_2_opt_a}
-   Better read the section above one more time.
-   [5]{#question11_11_2_opt_b}
-   Better read the section above one more time.
-   [7]{#question11_11_2_opt_c}
-   That\'s h(2), but it is passed to g.
-   [10]{#question11_11_2_opt_d}
-   h(2) returns 7, so y is bound to 7 when g is invoked.
-   [Error: you can\'t nest function calls]{#question11_11_2_opt_e}
-   Ah, but you can nest function calls.
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

-   [[](FlowofExecutionSummary.html)]{#relations-prev}
-   [[](PassingMutableObjects.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
