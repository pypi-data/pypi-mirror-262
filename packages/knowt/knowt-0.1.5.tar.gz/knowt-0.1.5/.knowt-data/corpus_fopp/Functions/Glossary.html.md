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
        Problem](/runestone/default/reportabug?course=fopp&page=Glossary)
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
::: {#glossary .section}
[12.16. ]{.section-number}Glossary[¶](#glossary "Permalink to this heading"){.headerlink}
=========================================================================================

argument[¶](#term-argument "Permalink to this term"){.headerlink}

:   A value provided to a function when the function is called. This
    value is assigned to the corresponding parameter in the function.
    The argument can be the result of an expression which may involve
    operators, operands and calls to other fruitful functions.

body[¶](#term-body "Permalink to this term"){.headerlink}

:   The second part of a compound statement. The body consists of a
    sequence of statements all indented the same amount from the
    beginning of the header. The standard amount of indentation used
    within the Python community is 4 spaces.

calling stack[¶](#term-calling-stack "Permalink to this term"){.headerlink}

:   A sequence (stack) of frames, showing all the function calls that
    are in process but not yet complete. When one function's code
    invokes another function call, there will be more than one frame on
    the stack.

compound statement[¶](#term-compound-statement "Permalink to this term"){.headerlink}

:   A statement that consists of two parts:

    1.  header - which begins with a keyword determining the statement
        type, and ends with a colon.

    2.  body - containing one or more statements indented the same
        amount from the header.

    The syntax of a compound statement looks like this:

    ::: {.highlight-python .notranslate}
    ::: {.highlight}
        keyword expression:
            statement
            statement
            ...
    :::
    :::

docstring[¶](#term-docstring "Permalink to this term"){.headerlink}

:   If the first thing in a function body is a string (or, we'll see
    later, in other situations too) that is attached to the function as
    its `__doc__`{.docutils .literal .notranslate} attribute.

flow of execution[¶](#term-flow-of-execution "Permalink to this term"){.headerlink}

:   The order in which statements are executed during a program run.

function[¶](#term-function "Permalink to this term"){.headerlink}

:   A named sequence of statements that performs some useful operation.
    Functions may or may not take parameters and may or may not produce
    a result.

function call[¶](#term-function-call "Permalink to this term"){.headerlink}

:   A statement that executes a function. It consists of the name of the
    function followed by a list of arguments enclosed in parentheses.

function composition[¶](#term-function-composition "Permalink to this term"){.headerlink}

:   Using the output from one function call as the input to another.

function definition[¶](#term-function-definition "Permalink to this term"){.headerlink}

:   A statement that creates a new function, specifying its name,
    parameters, and the statements it executes.

fruitful function[¶](#term-fruitful-function "Permalink to this term"){.headerlink}

:   A function that returns a value when it is called.

global variable[¶](#term-global-variable "Permalink to this term"){.headerlink}

:   A variable defined at the top level, not inside any function.

header line[¶](#term-header-line "Permalink to this term"){.headerlink}

:   The first part of a compound statement. A header line begins with a
    keyword and ends with a colon (:)

lifetime[¶](#term-lifetime "Permalink to this term"){.headerlink}

:   Variables and objects have lifetimes --- they are created at some
    point during program execution, and will be destroyed at some time.
    In python, objects live as long as there is some variable pointing
    to it, or it is part of some other compound object, like a list or a
    dictionary. In python, local variables live only until the function
    finishes execution.

local variable[¶](#term-local-variable "Permalink to this term"){.headerlink}

:   A variable defined inside a function. A local variable can only be
    used inside its function. Parameters of a function are also a
    special kind of local variable.

method[¶](#term-method "Permalink to this term"){.headerlink}

:   A special kind of function that is invoked on objects of particular
    types of objects, using the syntax
    `<expr>.<methodname>(<additional parameter values>)`{.docutils
    .literal .notranslate}

None[¶](#term-None "Permalink to this term"){.headerlink}

:   A special Python value. One use in Python is that it is returned by
    functions that do not execute a return statement with a return
    argument.

parameter[¶](#term-parameter "Permalink to this term"){.headerlink}

:   A name used inside a function to refer to the value which was passed
    to it as an argument.

return value[¶](#term-return-value "Permalink to this term"){.headerlink}

:   The value provided as the result of a function call.

side effect[¶](#term-side-effect "Permalink to this term"){.headerlink}

:   Some lasting effect of a function call, other than its return value.
    Side effects include print statements, changes to mutable objects,
    and changes to the values of global variables.

stack frame[¶](#term-stack-frame "Permalink to this term"){.headerlink}

:   A frame that keeps track of the values of local variables during a
    function execution, and where to return control when the function
    execution completes.

type annotation[¶](#term-type-annotation "Permalink to this term"){.headerlink}

:   An optional notation that specifies the type of a function parameter
    or function result.
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

-   [[](SideEffects.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
