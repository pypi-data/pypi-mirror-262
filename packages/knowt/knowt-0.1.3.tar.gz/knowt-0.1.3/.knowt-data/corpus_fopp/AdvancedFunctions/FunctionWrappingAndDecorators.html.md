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
        Problem](/runestone/default/reportabug?course=fopp&page=FunctionWrappingAndDecorators)
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
::: {#function-wrapping-and-decorators .section}
[]{#decorators}

[15.6. ]{.section-number}Function Wrapping and Decorators[¶](#function-wrapping-and-decorators "Permalink to this heading"){.headerlink}
========================================================================================================================================

This section introduces an advanced python concept called *function
wrapping* and a special syntax for it called *decorators*. It is not
necessary to use decorators in your programming, but they are an elegant
way to do function wrapping, and it will be helpful for you to
understand what they do when you see them in other people's code.

In Python, functions are "first class" objects, meaning they can be
treated like any other object. Beyond calling functions, we can also
reference them, pass them as arguments to other functions, or return
them. Although we cannot directly manipulate the *behavior* of a
function, we can wrap it in another function that does something before
or after the original function is called or change the arguments that a
function takes. This is called *function wrapping*.

We could write a function `compose`{.docutils .literal .notranslate}
that accepts two functions as arguments and returns a new function that
calls the first function with the output of the second function:

::: {.highlight-default .notranslate}
::: {.highlight}
    def compose(func1, func2): # func1 and func2 are functions
        return lambda x: func1(func2(x)) # return a *new* function that calls func1 with the output of func2
:::
:::

For example, below, we had a function `subtract_32`{.docutils .literal
.notranslate} that accepts a number as an argument and returns
`32`{.docutils .literal .notranslate} subtracted from that number, and a
function `multiply_5_9`{.docutils .literal .notranslate} that accepts a
number as an argument and returns the product of that number and
`5/9`{.docutils .literal .notranslate}. We can create a new function
that "composes" these two functions by executing `subtract_32`{.docutils
.literal .notranslate} first and then passing its output to
`multiply_5_9`{.docutils .literal .notranslate} (which happens to be how
we can convert Fahrenheit temperatures to Celsius temperatures):

::: {.runestone .explainer .ac_section}
::: {#ac15_6_1 component="activecode" question_label="15.6.1"}
::: {#ac15_6_1_question .ac_question}
:::
:::
:::

Function wrapping is a powerful idea that can be applied to many
problems but it can be difficult to grasp at first. For example, suppose
we wanted to write a function that adds logging to another function.
That is, we want to write a function `addLogging`{.docutils .literal
.notranslate} that accepts a function as an argument and returns a new
function that calls the original function but prints something before
and after the function is called. In the code below,
`addLogging`{.docutils .literal .notranslate} is analogous to the
`compose`{.docutils .literal .notranslate} function except: 1. it
accepts one argument (rather than two) 2. it is defined using
`def`{.docutils .literal .notranslate} (rather than `lambda`{.docutils
.literal .notranslate}) 3. it calls `print()`{.docutils .literal
.notranslate} before and after the function is called (rather than
calling one function with the output of the other).

::: {.runestone .explainer .ac_section}
::: {#ac15_6_2 component="activecode" question_label="15.6.2"}
::: {#ac15_6_2_question .ac_question}
:::
:::
:::

This kind of function wrapping is common enough that Python provides a
special syntax for it called **decorators**. A decorator is a function
that accepts a function as an argument and returns a new function. The
new function is usually a "wrapped" version of the original function.
The decorator syntax is to place an `@`{.docutils .literal .notranslate}
symbol followed by the name of the decorator function on the line before
the function definition. Now, we can wrap our `double`{.docutils
.literal .notranslate} function with the `addLogging`{.docutils .literal
.notranslate} decorator by placing `@addLogging`{.docutils .literal
.notranslate} on the line before the function definition. This is
equivalent to calling `addLogging`{.docutils .literal .notranslate} with
`double`{.docutils .literal .notranslate} as an argument and assigning
the result to `double`{.docutils .literal .notranslate}:

::: {.runestone .explainer .ac_section}
::: {#ac15_6_3 component="activecode" question_label="15.6.3"}
::: {#ac15_6_3_question .ac_question}
:::
:::
:::

We can now easily "enable" or "disable" logging by commenting out the
`@addLogging`{.docutils .literal .notranslate} line. This is much easier
than having to change the code inside the `double`{.docutils .literal
.notranslate} function itself.

To give another example, suppose we wanted to "password protect" access
to calling a function. We could create a function
`passwordProtect`{.docutils .literal .notranslate} that will wrap our
function inside of code that ensures the user has the correct password.

Try running the code below and entering the correct password
(`password123`{.docutils .literal .notranslate}) when prompted. Then,
try running the code again and entering an incorrect password. Notice
that the `printSecretMessage`{.docutils .literal .notranslate} function
is only called if the user enters the correct password.

::: {.runestone .explainer .ac_section}
::: {#ac15_6_4 component="activecode" question_label="15.6.4"}
::: {#ac15_6_4_question .ac_question}
:::
:::
:::

Although this example is made up for illustration, this kind of function
wrapping can be used in web applications to protect access to sensitive
pages. For example, code for a Web server might wrap code that transmits
personal information with a decorator that checks if the user is logged
in. Decorators give us a convenient syntax for modifying the behavior of
functions we write.
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

-   [[](MethodInvocations.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
