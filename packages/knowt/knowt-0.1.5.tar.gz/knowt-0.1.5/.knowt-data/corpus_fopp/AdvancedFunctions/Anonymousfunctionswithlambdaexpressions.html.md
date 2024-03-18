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
        Problem](/runestone/default/reportabug?course=fopp&page=Anonymousfunctionswithlambdaexpressions)
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
::: {#anonymous-functions-with-lambda-expressions .section}
[15.3. ]{.section-number}Anonymous functions with lambda expressions[¶](#anonymous-functions-with-lambda-expressions "Permalink to this heading"){.headerlink}
==============================================================================================================================================================

To further drive home the idea that we are passing a function object as
a parameter to the sorted object, let's see an alternative notation for
creating a function, a **lambda expression**. The syntax of a lambda
expression is the word "lambda" followed by parameter names, separated
by commas but not inside (parentheses), followed by a colon and then an
expression. `lambda arguments: expression`{.docutils .literal
.notranslate} yields a function object. This unnamed object behaves just
like the function object constructed below.

::: {.highlight-python .notranslate}
::: {.highlight}
    def fname(arguments):
        return expression
:::
:::

![image showing how elements of a lambda expression are like a function
definition.](../_images/lambda.gif)

Consider the following code

::: {.runestone .explainer .ac_section}
::: {#ac15_3_1 component="activecode" question_label="15.3.1"}
::: {#ac15_3_1_question .ac_question}
:::
:::
:::

Note the paralells between the two. At line 4, f is bound to a function
object. Its printed representation is "\<function f\>". At line 8, the
lambda expression produces a function object. Because it is unnamed
(anonymous), its printed representation doesn't include a name for it,
"\<function \<lambda\>\>". Both are of type 'function'.

A function, whether named or anonymous, can be called by placing
parentheses () after it. In this case, because there is one parameter,
there is one value in parentheses. This works the same way for the named
function and the anonymous function produced by the lambda expression.
The lambda expression had to go in parentheses just for the purposes of
grouping all its contents together. Without the extra parentheses around
it on line 10, the interpreter would group things differently and make a
function of x that returns x - 2(6).

Some students find it more natural to work with lambda expressions than
to refer to a function by name. Others find the syntax of lambda
expressions confusing. It's up to you which version you want to use
though you will need to be able to read and understand lambda
expressions that are written by others. In all the examples below, both
ways of doing it will be illustrated.

Say we want to create a function that takes a string and returns the
last character in that string. What might this look like with the
functions you've used before?

::: {.runestone .explainer .ac_section}
::: {#ac15_3_2 component="activecode" question_label="15.3.2"}
::: {#ac15_3_2_question .ac_question}
:::
:::
:::

To re-write this using lambda notation, we can do the following:

::: {.runestone .explainer .ac_section}
::: {#ac15_3_3 component="activecode" question_label="15.3.3"}
::: {#ac15_3_3_question .ac_question}
:::
:::
:::

Note that neither function is actually invoked. Look at the parallels
between the two structures. The parameters are defined in both functions
with the variable `s`{.docutils .literal .notranslate}. In the typical
function, we have to use the keyword `return`{.docutils .literal
.notranslate} to send back the value. In a lambda function, that is not
necessary - whatever is placed after the colon is what will be returned.

**Check Your Understanding**

::: {.runestone}
-   [A string with a - in front of the number.]{#question15_3_1_opt_a}
-   The number would be assigned to the variable x and there is no type
    conversion used here, so the number would stay a number.
-   [A number of the opposite sign (positive number becomes negative,
    negative becomes positive).]{#question15_3_1_opt_b}
-   Correct!
-   [Nothing is returned because there is no return
    statement.]{#question15_3_1_opt_c}
-   Remember, lambda functions do not use return statements.
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

-   [[](KeywordParameters.html)]{#relations-prev}
-   [[](ProgrammingWithStyle.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
