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
        Problem](/runestone/default/reportabug?course=fopp&page=Variablesandparametersarelocal)
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
::: {#variables-and-parameters-are-local .section}
[]{#index-0}

[12.9. ]{.section-number}Variables and parameters are local[¶](#variables-and-parameters-are-local "Permalink to this heading"){.headerlink}
============================================================================================================================================

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#goog_local_vars .align-left .youtube-video component="youtube" video-height="315" question_label="12.9.1" video-width="560" video-videoid="HdFujZpLFVg" video-divid="goog_local_vars" video-start="0" video-end="-1"}
:::
:::

An assignment statement in a function creates a **local variable** for
the variable on the left hand side of the assignment operator. It is
called local because this variable only exists inside the function and
you cannot use it outside. For example, consider again the
`square`{.docutils .literal .notranslate} function:

::: {.runestone .explainer .ac_section}
::: {#ac11_7_1 component="activecode" question_label="12.9.2"}
::: {#ac11_7_1_question .ac_question}
:::
:::
:::

Try running this in Codelens. When a function is invoked in Codelens,
the local scope is separated from global scope by a blue box. Variables
in the local scope will be placed in the blue box while global variables
will stay in the global frame. If you press the 'last \>\>' button you
will see an error message. When we try to use `y`{.docutils .literal
.notranslate} on line 6 (outside the function) Python looks for a global
variable named `y`{.docutils .literal .notranslate} but does not find
one. This results in the error:
`Name Error: 'y' is not defined.`{.docutils .literal .notranslate}

The variable `y`{.docutils .literal .notranslate} only exists while the
function is being executed --- we call this its **lifetime**. When the
execution of the function terminates (returns), the local variables are
destroyed. Codelens helps you visualize this because the local variables
disappear after the function returns. Go back and step through the
statements paying particular attention to the variables that are created
when the function is called. Note when they are subsequently destroyed
as the function returns.

Formal parameters are also local and act like local variables. For
example, the lifetime of `x`{.docutils .literal .notranslate} begins
when `square`{.docutils .literal .notranslate} is called, and its
lifetime ends when the function completes its execution.

So it is not possible for a function to set some local variable to a
value, complete its execution, and then when it is called again next
time, recover the local variable. Each call of the function creates new
local variables, and their lifetimes expire when the function returns to
the caller.

**Check Your Understanding**

::: {.runestone}
-   [True]{#question11_7_1_opt_a}
-   Local variables cannot be referenced outside of the function they
    were defined in.
-   [False]{#question11_7_1_opt_b}
-   Local variables cannot be referenced outside of the function they
    were defined in.
:::

::: {.runestone}
::: {#question11_7_2 component="fillintheblank" question_label="12.9.4" style="visibility: hidden;"}
Which of the following are local variables? Please, write them in order
of what line they are on in the code.

::: {.highlight-python .notranslate}
::: {.highlight}
    numbers = [1, 12, 13, 4]
    def foo(bar):
        aug = str(bar) + "street"
        return aug

    addresses = []
    for item in numbers:
        addresses.append(foo(item))
:::
:::

The local variables are
:::
:::

::: {.runestone}
-   [4]{#question11_7_3_opt_a}
-   Correct, the output is right because the subtract function takes in
    x as the global variable for the z parameter and puts it into the
    function. The subtract function uses the local variable y for its
    return.
-   [6]{#question11_7_3_opt_b}
-   Incorrect, look again at what is being produced in the subtract
    function.
-   [10]{#question11_7_3_opt_c}
-   Incorrect, look again at what is being produced in the subtract
    function.
-   [Code will give an error because x and z do not
    match.]{#question11_7_3_opt_d}
-   Incorrect, there shouldn\'t be any error.
:::

::: {.runestone}
-   [33]{#question11_7_4_opt_a}
-   Incorrect, look again at what is happening in producing.
-   [12]{#question11_7_4_opt_b}
-   Incorrect, look again at what is happening in producing.
-   [There is an error in the code.]{#question11_7_4_opt_c}
-   Yes! There is an error because we reference y in the producing
    function, but it was defined in adding. Because y is a local
    variable, we can\'t use it in both functions without initializing it
    in both. If we initialized y as 3 in both though, the answer would
    be 33.
:::

::: {.runestone}
-   [1]{#question11_7_5_opt_a}
-   Incorrect, pay attention to the local scope in the function.
-   [9]{#question11_7_5_opt_b}
-   Incorrect, pay attention to the local scope in the function.
-   [10]{#question11_7_5_opt_c}
-   Incorrect, pay attention to the local scope in the function.
-   [Error, local variable \'x\' is referenced before
    assignment.]{#question11_7_5_opt_d}
-   This code gives an error because the local variable \'x\' was
    referenced in the local scope before it was assigned a value.
:::

::: {.highlight-python .notranslate}
::: {.highlight}
        v1 += 1
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    NameError: name 'v1' is not defined
        def foo():
            v1 += 1
        foo()
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "<stdin>", line 2, in foo
    UnboundLocalError: local variable 'v1' referenced before assignment
:::
:::

In the code above, notice and understand the different error messages.
The local variables are created at the same time the local namespace is
created. That is **any** variable that is assigned to anywhere in the
function gets added to the local namespace immediately but it will
remain **unbound** until the assignment statement is executed.
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

-   [[](Afunctionthataccumulates.html)]{#relations-prev}
-   [[](GlobalVariables.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
