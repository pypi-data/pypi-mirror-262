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
        Problem](/runestone/default/reportabug?course=fopp&page=GlobalVariables)
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
::: {#global-variables .section}
[12.10. ]{.section-number}Global Variables[¶](#global-variables "Permalink to this heading"){.headerlink}
=========================================================================================================

Variable names that are at the *top-level*, not inside any function
definition, are called global.

It is legal for a function to access a global variable. However, this is
considered **bad form** by nearly all programmers and should be avoided.
This subsection includes some examples that illustrate the potential
interactions of global and local variables. These will help you
understand exactly how python works. Hopefully, they will also convince
you that things can get pretty confusing when you mix local and global
variables, and that you really shouldn't do it.

Look at the following, nonsensical variation of the square function.

::: {.runestone .explainer .ac_section}
::: {#ac11_8_1 component="activecode" question_label="12.10.1"}
::: {#ac11_8_1_question .ac_question}
:::
:::
:::

Although the `badsquare`{.docutils .literal .notranslate} function
works, it is silly and poorly written. We have done it here to
illustrate an important rule about how variables are looked up in
Python. First, Python looks at the variables that are defined as local
variables in the function. We call this the **local scope**. If the
variable name is not found in the local scope, then Python looks at the
global variables, or **global scope**. This is exactly the case
illustrated in the code above. `power`{.docutils .literal .notranslate}
is not found locally in `badsquare`{.docutils .literal .notranslate} but
it does exist globally. The appropriate way to write this function would
be to pass power as a parameter. For practice, you should rewrite the
badsquare example to have a second parameter called power.

There is another variation on this theme of local versus global
variables. Assignment statements in the local function cannot change
variables defined outside the function. Consider the following codelens
example:

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.10.2"}
::: {#clens11_8_1_question .ac_question}
:::

::: {#clens11_8_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.10.2 (clens11\_8\_1)]{.runestone_caption_text}
:::
:::

Now step through the code. What do you notice about the values of
variable `power`{.docutils .literal .notranslate} in the local scope
compared to the variable `power`{.docutils .literal .notranslate} in the
global scope?

The value of `power`{.docutils .literal .notranslate} in the local scope
was different than the global scope. That is because in this example
`power`{.docutils .literal .notranslate} was used on the left hand side
of the assignment statement `power = p`{.docutils .literal
.notranslate}. When a variable name is used on the left hand side of an
assignment statement Python creates a local variable. When a local
variable has the same name as a global variable we say that the local
shadows the global. A **shadow** means that the global variable cannot
be accessed by Python because the local variable will be found first.
This is another good reason not to use global variables. As you can see,
it makes your code confusing and difficult to understand.

If you really want to change the value of a global variable inside a
function, you can can do it by explicitly declaring the variable to be
global, as in the example below. Again, you should *not* do this in your
code. The example is here only to cement your understanding of how
python works.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.10.3"}
::: {#clens11_8_2_question .ac_question}
:::

::: {#clens11_8_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.10.3 (clens11\_8\_2)]{.runestone_caption_text}
:::
:::

To cement all of these ideas even further lets look at one final
example. Inside the `square`{.docutils .literal .notranslate} function
we are going to make an assignment to the parameter `x`{.docutils
.literal .notranslate} There's no good reason to do this other than to
emphasize the fact that the parameter `x`{.docutils .literal
.notranslate} is a local variable. If you step through the example in
codelens you will see that although `x`{.docutils .literal .notranslate}
is 0 in the local variables for `square`{.docutils .literal
.notranslate}, the `x`{.docutils .literal .notranslate} in the global
scope remains 2. This is confusing to many beginning programmers who
think that an assignment to a formal parameter will cause a change to
the value of the variable that was used as the actual parameter,
especially when the two share the same name. But this example
demonstrates that that is clearly not how Python operates.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="12.10.4"}
::: {#clens11_8_3_question .ac_question}
:::

::: {#clens11_8_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 12.10.4 (clens11\_8\_3)]{.runestone_caption_text}
:::
:::

**Check your understanding**

::: {.runestone}
-   [Its value]{#question11_8_1_opt_a}
-   Value is the contents of the variable. Scope concerns where the
    variable is \"known\".
-   [The range of statements in the code where a variable can be
    accessed.]{#question11_8_1_opt_b}
-   Correct.
-   [Its name]{#question11_8_1_opt_c}
-   The name of a variable is just an identifier or alias. Scope
    concerns where the variable is \"known\".
:::

::: {.runestone}
-   [A temporary variable that is only used inside a
    function]{#question11_8_2_opt_a}
-   Yes, a local variable is a temporary variable that is only known
    (only exists) in the function it is defined in.
-   [The same as a parameter]{#question11_8_2_opt_b}
-   While parameters may be considered local variables, functions may
    also define and use additional local variables.
-   [Another name for any variable]{#question11_8_2_opt_c}
-   Variables that are used outside a function are not local, but rather
    global variables.
:::

::: {.runestone}
-   [Yes, and there is no reason not to.]{#question11_8_3_opt_a}
-   While there is no problem as far as Python is concerned, it is
    generally considered bad style because of the potential for the
    programmer to get confused.
-   [Yes, but it is considered bad form.]{#question11_8_3_opt_b}
-   it is generally considered bad style because of the potential for
    the programmer to get confused. If you must use global variables
    (also generally bad form) make sure they have unique names.
-   [No, it will cause an error.]{#question11_8_3_opt_c}
-   Python manages global and local scope separately and has clear rules
    for how to handle variables with the same name in different scopes,
    so this will not cause a Python error.
:::

::: {.admonition .note}
Note

WP: Scope

You may be asking yourself at this point when you should make some
object a local variable and when should you make it a global variable.
Generally, we do not recommend making variables global. Imagine you are
trying to write a program that keeps track of money while purchasing
groceries. You may make a variable that represents how much money the
person has, called `wallet`{.docutils .literal .notranslate}. You also
want to make a function called `purchase`{.docutils .literal
.notranslate}, which will take the name of the item and its price, and
then add the item to a list of groceries, and deduct the price from the
amount stored in `wallet`{.docutils .literal .notranslate}. If you
initialize wallet before the function as a variable within the global
scope instead of passing it as a third parameter for
`purchase`{.docutils .literal .notranslate}, then an error would occur
because wallet would not be found in the local scope. Though there are
ways to get around this, as outlined in this page, if your program was
supposed to handle groceries for multiple people, then you would need to
declare each wallet as a global variable in the functions that want to
use wallet, and that would become very confusing and tedious to deal
with.
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

-   [[](Variablesandparametersarelocal.html)]{#relations-prev}
-   [[](Functionscancallotherfunctions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
