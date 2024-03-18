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
        Problem](/runestone/default/reportabug?course=fopp&page=FunctionParameters)
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
::: {#function-parameters .section}
[12.4. ]{.section-number}Function Parameters[¶](#function-parameters "Permalink to this heading"){.headerlink}
==============================================================================================================

Named functions are nice because, once they are defined and we
understand what they do, we can refer to them by name and not think too
much about what they do. With parameters, functions are even more
powerful, because they can do pretty much the same thing on each
invocation, but not exactly the same thing. The parameters can cause
them to do something a little different.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#goog_function_parms .align-left .youtube-video component="youtube" video-height="315" question_label="12.4.1" video-width="560" video-videoid="Ndw_EgFO_tw" video-divid="goog_function_parms" video-start="0" video-end="-1"}
:::
:::

The figure below shows this relationship. A function needs certain
information to do its work. These values, often called **arguments** or
**actual parameters** or **parameter values**, are passed to the
function by the user.

![](../_images/blackboxproc.png)

This type of diagram is often called a **black-box diagram** because it
only states the requirements from the perspective of the user (well, the
programmer, but the programmer who uses the function, who may be
different than the programmer who created the function). The user must
know the name of the function and what arguments need to be passed. The
details of how the function works are hidden inside the "black-box".

You have already been making function invocations with parameters. For
example, when you write `len("abc")`{.docutils .literal .notranslate} or
`len([3, 9, "hello"])`{.docutils .literal .notranslate}, len is the name
of a function, and the value that you put inside the parentheses, the
string "abc" or the list \[3, 9, "hello"\], is a parameter value.

When a function has one or more parameters, the names of the parameters
appear in the function definition, and the values to assign to those
parameters appear inside the parentheses of the function invocation.
Let's look at each of those a little more carefully.

In the definition, the parameter list is sometimes referred to as the
**formal parameters** or **parameter names**. These names can be any
valid variable name. If there is more than one, they are separated by
commas.

In the function invocation, inside the parentheses one value should be
provided for each of the parameter names. These values are separated by
commas. The values can be specified either directly, or by any python
expression including a reference to some other variable name.

That can get kind of confusing, so let's start by looking at a function
with just one parameter. The revised hello function personalizes the
greeting: the person to greet is specified by the parameter.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.4.2"}
::: {#clens11_3_1_question .ac_question}
:::

::: {#clens11_3_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.4.2 (clens11\_3\_1)]{.runestone_caption_text}
:::
:::

First, notice that hello2 has one formal parameter, s. You can tell that
because there is exactly one variable name inside the parentheses on
line 1.

Next, notice what happened during Step 2. Control was passed to the
function, just like we saw before. But in addition, the variable s was
bound to a value, the string "Iman". When it got to Step 7, for the
second invocation of the function, s was bound to "Jackie".

Function invocations always work that way. The expression inside the
parentheses on the line that invokes the function is evaluated before
control is passed to the function. The value is assigned to the
corresponding formal parameter. Then, when the code block inside the
function is executing, it can refer to that formal parameter and get its
value, the value that was 'passed into' the function.

::: {#eval11_3_1 .runestone .explainer component="showeval" question_label="12.4.3" tracemode="true"}
Next Step

Reset

::: {.evalCont style="background-color: #FDFDFD;"}
def hello2(s):\
   print(\"Hello \" + s)\
   print(\"Glad to meet you\")\
\
hello2(\"Nick\")\
:::

::: {.evalCont}
:::
:::

To get a feel for that, let's invoke hello2 using some more complicated
expressions. Try some of your own, too.

::: {.runestone .explainer .ac_section}
::: {#ac11_3_1 component="activecode" question_label="12.4.4"}
::: {#ac11_3_1_question .ac_question}
:::
:::
:::

Now let's consider a function with two parameters. This version of hello
takes a parameter that controls how many times the greeting will be
printed.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.4.5"}
::: {#clens11_3_2_question .ac_question}
:::

::: {#clens11_3_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.4.5 (clens11\_3\_2)]{.runestone_caption_text}
:::
:::

At Step 3 of the execution, in the first invocation of hello3, notice
that the variable s is bound to the value "Wei" and the variable n is
bound to the value 4.

That's how function invocations always work. Each of the expressions,
separated by commas, that are inside the parentheses are evaluated to
produce values. Then those values are matched up positionally with the
formal parameters. The first parameter name is bound to the first value
provided. The second parameter name is bound to the second value
provided. And so on.

**Check your understanding**

::: {.runestone}
-   [def greet(t):]{#question11_3_1_opt_a}
-   A function may take zero or more parameters. In this case it has
    one.
-   [def greet:]{#question11_3_1_opt_b}
-   A function needs to specify its parameters in its header. If there
    are no paramters, put () after the function name.
-   [greet(t, n):]{#question11_3_1_opt_c}
-   A function definition needs to include the keyword def.
-   [def greet(t, n)]{#question11_3_1_opt_d}
-   A function definition header must end in a colon (:).
:::

::: {.runestone}
-   [def print\_many(x, y):]{#question11_3_2_opt_a}
-   This line is the complete function header (except for the
    semi-colon) which includes the name as well as several other
    components.
-   [print\_many]{#question11_3_2_opt_b}
-   Yes, the name of the function is given after the keyword def and
    before the list of parameters.
-   [print\_many(x, y)]{#question11_3_2_opt_c}
-   This includes the function name and its parameters
-   [Print out string x, y times.]{#question11_3_2_opt_d}
-   This is a comment stating what the function does.
:::

::: {.runestone}
-   [i]{#question11_3_3_opt_a}
-   i is a variable used inside of the function, but not a parameter,
    which is passed in to the function.
-   [x]{#question11_3_3_opt_b}
-   x is only one of the parameters to this function.
-   [x, y]{#question11_3_3_opt_c}
-   Yes, the function specifies two parameters: x and y.
-   [x, y, i]{#question11_3_3_opt_d}
-   the parameters include only those variables whose values that the
    function expects to receive as input. They are specified in the
    header of the function.
:::

::: {.runestone}
-   [print\_many(x, y)]{#question11_3_4_opt_a}
-   No, x and y are the names of the formal parameters to this function.
    When the function is called, it requires actual values to be passed
    in.
-   [print\_many]{#question11_3_4_opt_b}
-   A function call always requires parentheses after the name of the
    function.
-   [print\_many(\"Greetings\")]{#question11_3_4_opt_c}
-   This function takes two parameters (arguments)
-   [print\_many(\"Greetings\", 10):]{#question11_3_4_opt_d}
-   A colon is only required in a function definition. It will cause an
    error with a function call.
-   [print\_many(\"Greetings\", z)]{#question11_3_4_opt_e}
-   Since z has the value 3, we have passed in two correct values for
    this function. \"Greetings\" will be printed 3 times.
:::

::: {.runestone}
-   [True]{#question11_3_5_opt_a}
-   Yes, you can call a function multiple times by putting the call in a
    loop.
-   [False]{#question11_3_5_opt_b}
-   One of the purposes of a function is to allow you to call it more
    than once. Placing it in a loop allows it to executed multiple times
    as the body of the loop runs multiple times.
:::

::: {.runestone}
-   [Hello]{#question11_3_6_opt_a}
-   \"Hello\" is shorter than \"Goodbye\"
-   [Goodbye]{#question11_3_6_opt_b}
-   \"Goodbye\" is longer than \"Hello\"
-   [s1]{#question11_3_6_opt_c}
-   s1 is a variable name; its value would print out, not the variable
    name.
-   [s2]{#question11_3_6_opt_d}
-   s2 is a variable name; its value would print out, not the variable
    name.
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

-   [[](FunctionInvocation.html)]{#relations-prev}
-   [[](Returningavaluefromafunction.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
