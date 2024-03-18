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
        Problem](/runestone/default/reportabug?course=fopp&page=OptionalParameters)
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
::: {#introduction-optional-parameters .section}
[]{#optional-params-chap}

[15.1. ]{.section-number}Introduction: Optional Parameters[¶](#introduction-optional-parameters "Permalink to this heading"){.headerlink}
=========================================================================================================================================

In the treatment of functions so far, each function definition specifies
zero or more formal parameters and each function invocation provides
exactly that many values. Sometimes it is convenient to have **optional
parameters** that can be specified or omitted. When an optional
parameter is omitted from a function invocation, the formal parameter is
bound to a **default value**. When the optional parameter is included,
then the formal parameter is bound to the value provided. Optional
parameters are convenient when a function is almost always used in a
simple way, but it's nice to allow it to be used in a more complex way,
with non-default values specified for the optional parameters.

Consider, for example, the `int`{.docutils .literal .notranslate}
function, which you have used previously. Its first parameter, which is
required, specifies the object that you wish to convert to an integer.
For example, if you call in on a string, `int("100")`{.docutils .literal
.notranslate}, the return value will be the integer 100.

That's the most common way programmers want to convert strings to
integers. Sometimes, however, they are working with numbers in some
other "base" rather than base 10. For example, in base 8, the rightmost
digit says how many ones, the next digit to the left says how many 8s,
and the one to the left of that says how many 64s (64 is 8 squared).

::: {.admonition .note}
Note

New Math

Some math educators believe that elementary school students will get a
much deeper understanding of the place-value system, and set a
foundation for learning algebra later, if they learn to do arithmetic
not only in base-10 but also in base-8 and other bases. This was part of
a movement called [New
Math](https://en.wikipedia.org/wiki/New_Math){.reference .external},
though it's not so new now. It was popular in the 1960s and 1970s in the
USA. One of the authors of this textbook (Resnick) had some version of
it in elementary school and credits it with ruining his mind, in a good
way. Tom Lehrer wrote a really funny song about it in 1965, and it's now
set with visuals in several YouTube renditions. Try this very nice
[lip-synched
version](http://www.youtube.com/watch?v=DfCJgC2zezw){.reference
.external}.
:::

The int function provides an optional parameter for the base. When it is
not specified, the number is converted to an integer assuming the
original number was in base 10. We say that 10 is the default value. So
`int("100")`{.docutils .literal .notranslate} is the same as invoking
`int("100", 10)`{.docutils .literal .notranslate}. We can override the
default of 10 by supplying a different value.

::: {.runestone .explainer .ac_section}
::: {#ac15_1_1 component="activecode" question_label="15.1.1"}
::: {#ac15_1_1_question .ac_question}
:::
:::
:::

When defining a function, you can specify a default value for a
parameter. That parameter then becomes an optional parameter when the
function is called. The way to specify a default value is with an
assignment statement inside the parameter list. Consider the following
code, for example.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="15.1.2"}
::: {#clens15_1_1_question .ac_question}
:::

::: {#clens15_1_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 15.1.2 (clens15\_1\_1)]{.runestone_caption_text}
:::
:::

Notice the different bindings of x, y, and z on the three invocations of
f. The first time, y and z have their default values, 3 and 7. The
second time, y gets the value 5 that is passed in, but z still gets the
default value of 7. The last time, z gets the value 8 that is passed in.

If you want to provide a non-default value for the third parameter (z),
you also need to provide a value for the second item (y). We will see in
the next section a mechanism called keyword parameters that lets you
specify a value for z without specifying a value for y.

::: {.admonition .note}
Note

This is a second, related but slightly different use of = than we have
seen previously. In a stand-alone assignment statement, not part of a
function definition, `y=3`{.docutils .literal .notranslate} assigns 3 to
the variable y. As part of specifying the parameters in a function
definition, `y=3`{.docutils .literal .notranslate} says that 3 is the
*default* value for y, used *only when* no value is provided during the
function invocation.
:::

There are two tricky things that can confuse you with default values.
The first is that the default value is determined at the time that the
function is defined, not at the time that it is invoked. So in the
example above, if we wanted to invoke the function f with a value of 10
for z, we cannot simply set initial = 10 right before invoking f. See
what happens in the code below, where z still gets the value 7 when f is
invoked without specifying a value for z.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="15.1.3"}
::: {#clens15_1_2_question .ac_question}
:::

::: {#clens15_1_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 15.1.3 (clens15\_1\_2)]{.runestone_caption_text}
:::
:::

The second tricky thing is that if the default value is set to a mutable
object, such as a list or a dictionary, that object will be shared in
all invocations of the function. This can get very confusing, so I
suggest that you never set a default value that is a mutable object. For
example, follow the execution of this one carefully.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="15.1.4"}
::: {#opt_params_4_question .ac_question}
:::

::: {#opt_params_4 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 15.1.4 (opt\_params\_4)]{.runestone_caption_text}
:::
:::

When the default value is used, the same list is shared. But on lines 8
and 9 two different copies of the list \["Hello"\] are provided, so the
4 that is appended is not present in the list that is printed on line 9.

**Check your understanding**

::: {.runestone}
-   [0]{#question15_1_1_opt_a}
-   Since no parameters are specified, x is 0 and y is 1, so 0 is
    returned.
-   [1]{#question15_1_1_opt_b}
-   0 \* 1 is 0.
-   [None]{#question15_1_1_opt_c}
-   The function does return a value.
-   [Runtime error since no parameters are passed in the call
    to f.]{#question15_1_1_opt_d}
-   Because both parameters have default values specified in the
    definition, they are both optional.
:::

::: {.runestone}
-   [0]{#question15_1_2_opt_a}
-   Since one parameter value is specified, it is bound to x; y gets the
    default value of 1.
-   [1]{#question15_1_2_opt_b}
-   Since one parameter value is specified, it is bound to x; y gets the
    default value of 1.
-   [None]{#question15_1_2_opt_c}
-   The function does return a value.
-   [Runtime error since the second parameter value is
    missing.]{#question15_1_2_opt_d}
-   Because both parameters have default values specified in the
    definition, they are both optional.
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_1_2 component="activecode" question_label="15.1.7"}
::: {#ac15_1_2_question .ac_question}
**3.** Write a function called `str_mult`{.docutils .literal
.notranslate} that takes in a required string parameter and an optional
integer parameter. The default value for the integer parameter should be
3. The function should return the string multiplied by the integer
parameter.
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

-   [[](toctree.html)]{#relations-prev}
-   [[](KeywordParameters.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
