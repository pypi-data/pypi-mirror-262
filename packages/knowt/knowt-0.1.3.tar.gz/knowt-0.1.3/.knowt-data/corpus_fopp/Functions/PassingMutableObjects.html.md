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
        Problem](/runestone/default/reportabug?course=fopp&page=PassingMutableObjects)
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
::: {#passing-mutable-objects .section}
[12.14. ]{.section-number}Passing Mutable Objects[¶](#passing-mutable-objects "Permalink to this heading"){.headerlink}
=======================================================================================================================

Take a look at the following code example. Can you predict what will
happen when you run it?

::: {.runestone .explainer .ac_section}
::: {#ac11_12_1 component="activecode" question_label="12.14.1"}
::: {#ac11_12_1_question .ac_question}
:::
:::
:::

Use **Show CodeLens** to step through the code to see why the assignment
to the formal parameter `y`{.docutils .literal .notranslate} inside
`double`{.docutils .literal .notranslate} did not affect the argument
`num`{.docutils .literal .notranslate}. An assignment to a formal
parameter inside a function **never** affects the argument in the
caller.

On the other hand, if you are passing a mutable object, such as a list,
to a function, and the function alters the object's state, that state
change will be visible to the caller when the function returns. Take a
look at the following example.

::: {.runestone .explainer .ac_section}
::: {#ac11_12_2 component="activecode" question_label="12.14.2"}
::: {#ac11_12_2_question .ac_question}
:::
:::
:::

Try stepping through this in codelens to see what happens. The state of
the list referenced by `lst`{.docutils .literal .notranslate} is altered
by `changeit`{.docutils .literal .notranslate}, and since
`mylst`{.docutils .literal .notranslate} is an alias for `lst`{.docutils
.literal .notranslate}, `mylst`{.docutils .literal .notranslate} is
affected by the actions taken by the function.

Look closely at this line:

::: {.highlight-default .notranslate}
::: {.highlight}
    lst[0] = "Michigan"
:::
:::

That statement modifies the state of `lst`{.docutils .literal
.notranslate} by changing the value in slot 0. Although that line may
appear to contradict the statement above that "an assignment to a formal
parameter inside a function never affects the argument in the caller,"
note that there is a difference between assigning to a *slot* of a list,
and assigning to the list variable itself. To see that difference, try
changing that line to the following:

::: {.highlight-default .notranslate}
::: {.highlight}
    lst = ["Michigan", "Wolverines"]
:::
:::

Then, run again. This time, `mylist`{.docutils .literal .notranslate} is
not altered. To understand why, use CodeLens to step carefully through
the code and observe how the assignment to `lst`{.docutils .literal
.notranslate} causes it to refer to a separate list.

Take a moment to experiment some more with the `changeit`{.docutils
.literal .notranslate} function. Change the body of the function to the
following:

::: {.highlight-default .notranslate}
::: {.highlight}
    lst.append("Michigan Wolverines")
:::
:::

Step through using CodeLens. You should see that `mylst`{.docutils
.literal .notranslate} is affected by this change, since the state of
the list is altered.

Then, try again with this as the body:

::: {.highlight-default .notranslate}
::: {.highlight}
    lst = lst + ["Michigan Wolverines"]
:::
:::

Step through using CodeLens. Here, we create a new list using the
concatenation operator, and `mylst`{.docutils .literal .notranslate} is
not affected by the change.

Understanding the techniques that functions can and cannot use to alter
the state of mutable parameters is important. You may want to take some
time to study the information on this page more thoroughly and play with
the examples until you feel confident about your grasp of the material.

**Check Your Understanding**

::: {.runestone}
-   ::: {#mutobj-q1_opt_a}
    \['a', 'b'\]
    :::

-   ::: {#mutobj-q1_opt_a}
    Correct! `mylist`{.docutils .literal .notranslate} is not changed by
    the assignment in `myfun`{.docutils .literal .notranslate}.
    :::

-   ::: {#mutobj-q1_opt_b}
    \[1, 2, 3\]
    :::

-   ::: {#mutobj-q1_opt_b}
    Incorrect. `mylist`{.docutils .literal .notranslate} is not changed
    by the assignment in `myfun`{.docutils .literal .notranslate}.
    :::
:::

::: {.runestone}
-   ::: {#mutobj-q2_opt_a}
    \['a', 'b'\]
    :::

-   ::: {#mutobj-q2_opt_a}
    Incorrect. `myfun`{.docutils .literal .notranslate} alters the state
    of the list object by removing the value at slot 0.
    :::

-   ::: {#mutobj-q2_opt_b}
    \['b'\]
    :::

-   ::: {#mutobj-q2_opt_b}
    Correct! `myfun`{.docutils .literal .notranslate} alters the state
    of the list object by removing the value at slot 0.
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

-   [[](Printvsreturn.html)]{#relations-prev}
-   [[](SideEffects.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
