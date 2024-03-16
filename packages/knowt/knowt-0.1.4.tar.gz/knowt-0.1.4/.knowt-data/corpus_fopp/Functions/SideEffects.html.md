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
        Problem](/runestone/default/reportabug?course=fopp&page=SideEffects)
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
::: {#side-effects .section}
[12.15. ]{.section-number}Side Effects[¶](#side-effects "Permalink to this heading"){.headerlink}
=================================================================================================

We say that the function `changeit`{.docutils .literal .notranslate} has
a **side effect** on the list object that is passed to it. Global
variables are another way to have side effects. For example, similar to
examples you have seen above, we could make `double`{.docutils .literal
.notranslate} have a side effect on the global variable y.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.15.1"}
::: {#clens11_13_1_question .ac_question}
:::

::: {#clens11_13_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.15.1 (clens11\_13\_1)]{.runestone_caption_text}
:::
:::

Side effects are sometimes convenient. For example, it may be convenient
to have a single dictionary that accumulates information, and pass it
around to various functions that might add to it or modify it.

However, programs that have side effects can be very difficult to debug.
When an object has a value that is not what you expected, it can be
difficult to track down exactly where in the code it was set. Wherever
it is practical to do so, it is best to avoid side effects. The way to
avoid using side effects is to use return values instead.

Instead of modifying a global variable inside a function, pass the
global variable's value in as a parameter, and set that global variable
to be equal to a value returned from the function. For example, the
following is a better version of the code above.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.15.2"}
::: {#clens11_13_2_question .ac_question}
:::

::: {#clens11_13_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.15.2 (clens11\_13\_2)]{.runestone_caption_text}
:::
:::

You can use the same coding pattern to avoid confusing side effects with
sharing of mutable objects. To do that, explicitly make a copy of an
object and pass the copy in to the function. Then return the modified
copy and reassign it to the original variable if you want to save the
changes. The built-in `list`{.docutils .literal .notranslate} function,
which takes a sequence as a parameter and returns a new list, works to
copy an existing list. For dictionaries, you can similarly call the
`dict`{.docutils .literal .notranslate} function, passing in a
dictionary to get a copy of the dictionary back as a return value.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.15.3"}
::: {#clens11_13_3_question .ac_question}
:::

::: {#clens11_13_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.15.3 (clens11\_13\_3)]{.runestone_caption_text}
:::
:::

In general, any lasting effect that occurs in a function, not through
its return value, is called a side effect. There are three ways to have
side effects:

-   Printing out a value. This doesn't change any objects or variable
    bindings, but it does have a potential lasting effect outside the
    function execution, because a person might see the output and be
    influenced by it.

-   Changing the value of a mutable object.

-   Changing the binding of a global variable.
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

-   [[](PassingMutableObjects.html)]{#relations-prev}
-   [[](Glossary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
