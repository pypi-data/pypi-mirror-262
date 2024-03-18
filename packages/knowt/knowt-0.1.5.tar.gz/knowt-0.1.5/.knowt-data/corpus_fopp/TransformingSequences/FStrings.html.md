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
        Problem](/runestone/default/reportabug?course=fopp&page=FStrings)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [9.1 Introduction: Transforming
        Sequences](intro-SequenceMutation.html){.reference .internal}
    -   [9.2 Mutability](Mutability.html){.reference .internal}
    -   [9.3 List Element Deletion](ListDeletion.html){.reference
        .internal}
    -   [9.4 Objects and
        References](ObjectsandReferences.html){.reference .internal}
    -   [9.5 Aliasing](Aliasing.html){.reference .internal}
    -   [9.6 Cloning Lists](CloningLists.html){.reference .internal}
    -   [9.7 Mutating Methods](MutatingMethods.html){.reference
        .internal}
    -   [9.8 Append versus
        Concatenate](AppendversusConcatenate.html){.reference .internal}
    -   [9.9 Non-mutating Methods on
        Strings](NonmutatingMethodsonStrings.html){.reference .internal}
    -   [9.10 String Format Method](StringFormatting.html){.reference
        .internal}
    -   [9.11 f-Strings](FStrings.html){.reference .internal}
    -   [9.12 The Accumulator Pattern with
        Lists](TheAccumulatorPatternwithLists.html){.reference
        .internal}
    -   [9.13 The Accumulator Pattern with
        Strings](TheAccumulatorPatternwithStrings.html){.reference
        .internal}
    -   [9.14 👩‍💻 Accumulator Pattern
        Strategies](WPAccumulatorPatternStrategies.html){.reference
        .internal}
    -   [9.15 👩‍💻 Don't Mutate A List That You Are Iterating
        Through](WPDontMutateAListYouIterateThrough.html){.reference
        .internal}
    -   [9.16 Summary](Glossary.html){.reference .internal}
    -   [9.17 Exercises](Exercises.html){.reference .internal}
    -   [9.18 Chapter Assessment - List
        Methods](week4a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#f-strings .section}
[9.11. ]{.section-number}f-Strings[¶](#f-strings "Permalink to this heading"){.headerlink}
==========================================================================================

There is another (more modern) approach for generating
fill-in-the-blanks, **f-strings**. They were introduced in version 3.6
of python. f-strings are a Python-specific way of formatting strings.

You should develop the skill of reading code that uses both
`.format()`{.docutils .literal .notranslate} and f-strings, because you
may encounter both. You will probably find that it's easier to write
code using f-strings, and we encourage you to use them for your own
code, except when you have a specific reason to use
`.format()`{.docutils .literal .notranslate} instead.

Let's revisit the example we used before. Pay attention to how the same
outcome can be obtained first with the `.format()`{.docutils .literal
.notranslate} method and then with the f-string approach.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_1 component="activecode" question_label="9.11.1"}
::: {#ac8_f_1_question .ac_question}
:::
:::
:::

In the above example, using the *f-strings* approach, we fill each
placeholder (i.e., each pair of braces) with a variable name whose value
we want to display.

Note that to use an f-string, we must type the character "f" before the
string content. We can then enter expressions within the string between
curly braces ({}). Whenever the python interpreter encounters curly
braces inside an f-string, it will evaluate the expression and
substitute the resulting value into the string.

We can use almost any expression inside the braces. It can be: a value;
a variable that contains or references a value; an arithmetic
expression; a string expression; a method call that returns a value such
as a string or a number. See the following examples illustrating these.
Each `print()`{.docutils .literal .notranslate} statement produces the
exact same output.

First, we can use values directly inside the braces.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_2 component="activecode" question_label="9.11.2"}
::: {#ac8_f_2_question .ac_question}
:::
:::
:::

We can use expressions (i.e., string operations and arithmetic
operations) directly inside the braces.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_3 component="activecode" question_label="9.11.3"}
::: {#ac8_f_3_question .ac_question}
:::
:::
:::

We can use expressions consisting of variables directly inside the
braces.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_4 component="activecode" question_label="9.11.4"}
::: {#ac8_f_4_question .ac_question}
:::
:::
:::

We can call a function or a method directly inside the braces. Note that
in this example, we use `max()`{.docutils .literal .notranslate}, a
built-in function that will return the highest value among the values we
provide. Since the value `96.75`{.docutils .literal .notranslate} is
assigned to the variable `score`{.docutils .literal .notranslate} and is
greater than `60`{.docutils .literal .notranslate}, the value returned
from `max(score, 60)`{.docutils .literal .notranslate} will be
`96.75`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_5 component="activecode" question_label="9.11.5"}
::: {#ac8_f_5_question .ac_question}
:::
:::
:::

Similar to the `format()`{.docutils .literal .notranslate} approach, we
can use format specifiers (e.g., `:.2f`{.docutils .literal
.notranslate}) to further fine-tune the value being displayed. For
instance, if we want to display a floating-point number with one decimal
place, we can use `:.1f`{.docutils .literal .notranslate} inside the
braces and after the expression. The example below shows how we can
apply the format specifiers with both a variable and a method call
inside the braces.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_6 component="activecode" question_label="9.11.6"}
::: {#ac8_f_6_question .ac_question}
:::
:::
:::

At this point, we might ask, are *f-strings* the best approach to use
for formatting strings?

Generally, yes, f-strings make for code that's easier to read, and thus,
also easier to write and debug. But there a couple things to watch out
for.

First, note that we need to pay attention to using quotes inside
*f-strings*. If we use quotes, that means we are embedding quotes inside
the quotes required by f-strings. If we use the same type of quotes,
such as double quotes, the Python interpreter will have trouble
determining how these double-quotes are paired with one another, and it
will have trouble understanding what we want a computer to do. A
solution is to use a different kind of quotes, such as single quotes, so
that the Python interpreter knows how to pair those quotes (e.g., double
with double, single with single) and properly execute our code. Take a
look at the following example, which produces an error, and see if we
can fix the bug to have the correct output similar to the previous
example (hint: replacing a pair of double quotes).

::: {.runestone .explainer .ac_section}
::: {#ac8_f_7 component="activecode" question_label="9.11.7"}
::: {#ac8_f_7_question .ac_question}
:::
:::
:::

Note that, as the `.format()`{.docutils .literal .notranslate} approach
does not require using expressions directly inside the *format string*,
we don't have to worry about the quotes-inside-quotes problem when using
the `.format()`{.docutils .literal .notranslate} approach. The following
example uses double quotes throughout.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_8 component="activecode" question_label="9.11.8"}
::: {#ac8_f_8_question .ac_question}
:::
:::
:::

Second, we need to pay attention when using braces inside *f-string*, as
*f-strings* already require the use of braces as placeholders. To
display a pair of braces inside f-strings, we need to double the pair of
braces.

This is also true with format strings used with `.format()`{.docutils
.literal .notranslate}. However, since the `.format()`{.docutils
.literal .notranslate} approach does not require using expressions
directly inside the *format string*, we can avoid the
braces-inside-braces problem by including the braces in the substitution
values instead, as we can see in the following example.

::: {.runestone .explainer .ac_section}
::: {#ac8_f_9 component="activecode" question_label="9.11.9"}
::: {#ac8_f_9_question .ac_question}
:::
:::
:::

In summary, different string formatting methods have their own
advantages and disadvantages in terms of readability and caveats. There
are other considerations (e.g., speed), but we won't discuss them here.
One of the potential solutions to mitigate the issues raised above is to
pre-calculate the values using different expressions and store them in
variables. We can then use mostly these variables with either
`.format()`{.docutils .literal .notranslate} or *f-strings*, without
using complex expressions directly. See the example inside the question
below.

We have introduced various string methods in Python. Use the following
question to check if you understand what has been discussed.

::: {.runestone}
-   [The percentage of r characters (upper or lower case): 6.061%. The
    number of r: 4.]{#question8_f_10_opt_a}
-   Check how many decimal places, sentence order, and how many lower
    case 'r' characters there are.
-   [The number of r: 4. The percentage of r characters (upper or lower
    case): 6.061%.]{#question8_f_10_opt_b}
-   Check how many decimal places and how many lower case 'r' characters
    there are.
-   [The percentage of r characters (upper or lower case): 6.06%. The
    number of r: 3.]{#question8_f_10_opt_c}
-   Check the sentence order.
-   [The number of r: 3. The percentage of r characters (upper or lower
    case): 6.06%.]{#question8_f_10_opt_d}
-   Yes, the numbers and the order of sentences are correct.
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

-   [[](StringFormatting.html)]{#relations-prev}
-   [[](TheAccumulatorPatternwithLists.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
