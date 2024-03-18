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
        Problem](/runestone/default/reportabug?course=fopp&page=MethodInvocations)
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
::: {#adcopy_1 .adcopy style="display: none;"}
#### Before you keep reading\...

Runestone Academy can only continue if we get support from individuals
like you. As a student you are well aware of the high cost of textbooks.
Our mission is to provide great books to you for free, but we ask that
you consider a \$10 donation, more if you can or less if \$10 is a
burden.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=1){.btn
.btn-info}
:::

::: {#adcopy_2 .adcopy style="display: none;"}
#### Before you keep reading\...

Making great stuff takes time and \$\$. If you appreciate the book you
are reading now and want to keep quality materials free for other
students please consider a donation to Runestone Academy. We ask that
you consider a \$10 donation, but if you can give more thats great, if
\$10 is too much for your budget we would be happy with whatever you can
afford as a show of support.

::: {.donateb}
[Support Runestone Academy Today](/runestone/default/donate?ad=2){.btn
.btn-info}
:::
:::
:::

::: {#method-invocations .section}
[15.5. ]{.section-number}Method Invocations[¶](#method-invocations "Permalink to this heading"){.headerlink}
============================================================================================================

::: {.admonition .note}
Note

This section is a review of material you have already seen, but it may
be helpful to look at it again now that you're focusing on functions and
function calls.
:::

There is one other special type of function called a **method**, which
is invoked slightly differently. Some object types have methods defined
for them. You have already seen some methods that operate on strings
(e.g., `find`{.docutils .literal .notranslate}, `index`{.docutils
.literal .notranslate}, `split`{.docutils .literal .notranslate},
`join`{.docutils .literal .notranslate}) and on lists (e.g.,
`append`{.docutils .literal .notranslate}, `pop`{.docutils .literal
.notranslate}).

We will not learn about how to define methods until later in the course,
when we cover Classes. But it's worth getting a basic understanding now
of how methods are invoked. To invoke a method, the syntax is
`<expr>.<methodname>(<additional parameter values>)`{.docutils .literal
.notranslate}.

The expression to the left of the dot should evaluate to an object of
the correct type, an object for which \<methodname\> is defined. The
method will be applied to that object (that object will be a parameter
value passed to the function/method.) If the method takes additional
parameters (some do, some don't), additional expressions that evaluate
to values are included inside the parentheses.

For example, let's look at an invocation of the split method.

::: {.runestone .explainer .ac_section}
::: {#ac11_6_1 component="activecode" question_label="15.5.1"}
::: {#ac11_6_1_question .ac_question}
:::
:::
:::

The split method operates on a string. Because it is a method rather
than a regular function, the string it operates on appears to the left
of the period, rather than inside the parentheses. The split method
always returns a list. On line 2, that returned value is assigned to the
variable z.

The split method actually takes an optional extra parameter. If no value
is provided inside the parentheses, the split method chops up the list
whenever it encounters a whitespace (a space, a tab, or a newline). But
you can specifying a character or character string to split on. Try
putting "s" inside the parentheses on line 2 above, make a prediction
about what the output will be, and then check it. Try some other things
inside the parentheses.

Note that the thing to the left of the period can be any expression, not
just a variable name. It can even be a return value from some other
function call or method invocation. For example, if we want to remove
the s and t characters from a string, we can do it all on one line as
show below.

::: {.runestone .explainer .ac_section}
::: {#ac11_6_2 component="activecode" question_label="15.5.2"}
::: {#ac11_6_2_question .ac_question}
:::
:::
:::

What's going on there? Start reading left to right. "This is a sentence"
is a string, and the replace method is invoked on it. Two additional
parameter values are provided, "s", and an empty string. So, in the
sentence, all occurrences of "s" are replaced with the empty string. A
new string is returned, "Thi i a entence." There is another period
followed by the word replace, so the replace method is called again on
that string, returning the shorter string, which is printed.
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

-   [[](ProgrammingWithStyle.html)]{#relations-prev}
-   [[](FunctionWrappingAndDecorators.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
