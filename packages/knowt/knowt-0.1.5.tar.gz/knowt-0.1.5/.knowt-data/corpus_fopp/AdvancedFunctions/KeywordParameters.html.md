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
        Problem](/runestone/default/reportabug?course=fopp&page=KeywordParameters)
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
::: {#keyword-parameters .section}
[15.2. ]{.section-number}Keyword Parameters[¶](#keyword-parameters "Permalink to this heading"){.headerlink}
============================================================================================================

In the previous section, on [[Optional Parameters]{.std
.std-ref}](OptionalParameters.html#optional-params-chap){.reference
.internal} you learned how to define default values for formal
parameters, which made it optional to provide values for those
parameters when invoking the functions.

In this chapter, you'll see one more way to invoke functions with
optional parameters, with keyword-based parameter passing. This is
particularly convenient when there are several optional parameters and
you want to provide a value for one of the later parameters while not
providing a value for the earlier ones.

The online official python documentation includes a tutorial on optional
parameters which covers the topic quite well. Please read the content
there: [Keyword
arguments](http://docs.python.org/3/tutorial/controlflow.html#keyword-arguments){.reference
.external}

Don't worry about the
`def cheeseshop(kind, *arguments, **keywords):`{.docutils .literal
.notranslate} example. You should be able to get by without
understanding `*parameters`{.docutils .literal .notranslate} and
`**parameters`{.docutils .literal .notranslate} in this course. But do
make sure you understand the stuff above that.

The basic idea of passing arguments by keyword is very simple. When
invoking a function, inside the parentheses there are always 0 or more
values, separated by commas. With keyword arguments, some of the values
can be of the form `paramname = <expr>`{.docutils .literal .notranslate}
instead of just `<expr>`{.docutils .literal .notranslate}. Note that
when you have `paramname = <expr>`{.docutils .literal .notranslate} in a
function definition, it is defining the default value for a parameter
when no value is provided in the invocation; when you have
`paramname = <expr>`{.docutils .literal .notranslate} in the invocation,
it is supplying a value, overriding the default for that paramname.

To make it easier to follow the details of the examples in the official
python tutorial, you can step through them in CodeLens.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="15.2.1"}
::: {#keyword_params_1_question .ac_question}
:::

::: {#keyword_params_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 15.2.1
(keyword\_params\_1)]{.runestone_caption_text}
:::
:::

As you step through it, each time the function is invoked, make a
prediction about what each of the four parameter values will be during
execution of lines 2-5. Then, look at the stack frame to see what they
actually are during the execution.

::: {.admonition .note}
Note

Note that we have yet another, slightly different use of the = sign
here. As a stand-alone, top-level statement, `x=3`{.docutils .literal
.notranslate}, the variable x is set to 3. Inside the parentheses that
invoke a function, `x=3`{.docutils .literal .notranslate} says that 3
should be bound to the local variable x in the stack frame for the
function invocation. Inside the parentheses of a function definition,
`x=3`{.docutils .literal .notranslate} says that 3 should be the value
for x in every invocation of the function where no value is explicitly
provided for x.
:::

::: {#keyword-parameters-with-format .section}
[15.2.1. ]{.section-number}Keyword Parameters with .format[¶](#keyword-parameters-with-format "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------------------------

Earlier you learned how to use the `format`{.docutils .literal
.notranslate} method for strings, which allows you to structure strings
like fill-in-the-blank sentences. Now that you've learned about optional
and keyword parameters, we can introduce a new way to use the
`format`{.docutils .literal .notranslate} method.

This other option is to specifically refer to keywords for interpolation
values, like below.

::: {.runestone .explainer .ac_section}
::: {#ac15_2_1 component="activecode" question_label="15.2.1.1"}
::: {#ac15_2_1_question .ac_question}
:::
:::
:::

Sometimes, you may want to use the `.format`{.docutils .literal
.notranslate} method to insert the same value into a string multiple
times. You can do this by simply passing the same string into the format
method, assuming you have included `{}`{.docutils .literal .notranslate}
s in the string everywhere you want to interpolate them. But you can
also use positional passing references to do this! The order in which
you pass arguments into the `format`{.docutils .literal .notranslate}
method matters: the first one is argument `0`{.docutils .literal
.notranslate}, the second is argument `1`{.docutils .literal
.notranslate}, and so on.

For example,

::: {.runestone .explainer .ac_section}
::: {#ac15_2_2 component="activecode" question_label="15.2.1.2"}
::: {#ac15_2_2_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [2]{#question15_2_1_opt_a}
-   2 is bound to x, not z
-   [3]{#question15_2_1_opt_b}
-   3 is the default value for y, not z
-   [5]{#question15_2_1_opt_c}
-   5 is bound to y, not z
-   [7]{#question15_2_1_opt_d}
-   2 is bound x, 5 to y, and z gets its default value, 7
-   [Runtime error since not enough values are passed in the call to
    f]{#question15_2_1_opt_e}
-   z has a default value in the function definition, so it\'s optional
    to pass a value for it.
:::

::: {.runestone}
-   [2]{#question15_2_2_opt_a}
-   2 is bound to x, not y
-   [3]{#question15_2_2_opt_b}
-   3 is the default value for y, and no value is specified for y,
-   [5]{#question15_2_2_opt_c}
-   say what?
-   [10]{#question15_2_2_opt_d}
-   10 is the second value passed, but it is bound to z, not y.
-   [Runtime error since no value is provided for y, which comes before
    z]{#question15_2_2_opt_e}
-   That\'s the beauty of passing parameters with keywords; you can skip
    some parameters and they get their default values.
:::

::: {.runestone}
-   [2]{#question15_2_3_opt_a}
-   2 is bound to x since it\'s the first value, but so is 5, based on
    keyword.
-   [3]{#question15_2_3_opt_b}
-   
-   [5]{#question15_2_3_opt_c}
-   5 is bound to x by keyword, but 2 is also bound to it by virtue of
    being the value and not having a keyword. In the online environment,
    it actually allows this, but not in a proper python interpreter.
-   [7]{#question15_2_3_opt_d}
-   
-   [Runtime error since two different values are provided for
    x]{#question15_2_3_opt_e}
-   2 is bound to x since it\'s the first value, but so is 5, based on
    keyword.
:::

::: {.runestone}
-   [2]{#question15_2_4_opt_a}
-   2 is bound to x, no z
-   [7]{#question15_2_4_opt_b}
-   the default value for z is determined at the time the function is
    defined; at that time initial has the value 7.
-   [0]{#question15_2_4_opt_c}
-   the default value for z is determined at the time the function is
    defined, not when it is invoked.
-   [Runtime error since two different values are provided for
    initial.]{#question15_2_4_opt_d}
-   there\'s nothing wrong with reassigning the value of a variable at a
    later time.
:::

::: {.runestone}
-   [\'first!\' she yelled. \'Come here, first! f\_one, f\_two, and
    f\_three are here!\']{#question15_2_5_opt_a}
-   Remember, the values inside of {} are variable names. The values of
    the variables will be used.
-   [\'Alexey!\' she yelled. \'Come here, Alexey! Catalina, Misuki, and
    Pablo are here!\']{#question15_2_5_opt_b}
-   Look again at what value is set to the variable first.
-   [\'Catalina!\' she yelled. \'Come here, Catalina! Alexey, Misuki,
    and Pablo are here!\']{#question15_2_5_opt_c}
-   Yes, the keyword parameters will determine the order of the strings.
-   [There is an error. You cannot repeatedly use the keyword
    parameters.]{#question15_2_5_opt_d}
-   This is not an error, you can do that in Python!
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_2_3 component="activecode" question_label="15.2.1.8"}
::: {#ac15_2_3_question .ac_question}
**5.** Define a function called `multiply`{.docutils .literal
.notranslate}. It should have one required parameter, a string. It
should also have one optional parameter, an integer, named
`mult_int`{.docutils .literal .notranslate}, with a default value of 10.
The function should return the string multiplied by the integer. (i.e.:
Given inputs "Hello", mult\_int=3, the function should return
"HelloHelloHello")
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac15_2_4 component="activecode" question_label="15.2.1.9"}
::: {#ac15_2_4_question .ac_question}
**6.** Currently the function is supposed to take 1 required parameter,
and 2 optional parameters, however the code doesn't work because a
parameter name without a default value follows a parameter name with a
default value. Fix the code so that it passes the test. This should only
require changing one line of code.
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

-   [[](OptionalParameters.html)]{#relations-prev}
-   [[](Anonymousfunctionswithlambdaexpressions.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
