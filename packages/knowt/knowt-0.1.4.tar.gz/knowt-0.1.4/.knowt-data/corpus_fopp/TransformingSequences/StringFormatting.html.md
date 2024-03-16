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
        Problem](/runestone/default/reportabug?course=fopp&page=StringFormatting)
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

::: {#string-format-method .section}
[]{#format-strings}

[9.10. ]{.section-number}String Format Method[¶](#string-format-method "Permalink to this heading"){.headerlink}
================================================================================================================

Until now, we have created strings with variable content using the +
operator to concatenate partial strings together. That works, but it's
very hard for people to read or debug a code line that includes variable
names and strings and complex expressions. Consider the following:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_4 component="activecode" question_label="9.10.1"}
::: {#ac8_8_4_question .ac_question}
:::
:::
:::

Or perhaps more realistically:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_5 component="activecode" question_label="9.10.2"}
::: {#ac8_8_5_question .ac_question}
:::
:::
:::

In this section, you will learn to write that in a more readable way:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_6 component="activecode" question_label="9.10.3"}
::: {#ac8_8_6_question .ac_question}
:::
:::
:::

In grade school quizzes a common convention is to use fill-in-the
blanks. For instance,

> <div>
>
> Hello \_\_\_\_\_!
>
> </div>

and you can fill in the name of the person greeted, and combine given
text with a chosen insertion. *We use this as an analogy:* Python has a
similar construction, better called fill-in-the-braces. The string
method `format`{.docutils .literal .notranslate}, makes substitutions
into places in a string enclosed in braces. Run this code:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_7 component="activecode" question_label="9.10.4"}
::: {#ac8_8_7_question .ac_question}
:::
:::
:::

There are several new ideas here!

The string for the `format`{.docutils .literal .notranslate} method has
a special form, with braces embedded. Such a string is called a *format
string*. Places where braces are embedded are replaced by the value of
an expression taken from the parameter list for the `format`{.docutils
.literal .notranslate} method. There are many variations on the syntax
between the braces. In this case we use the syntax where the first (and
only) location in the string with braces has a substitution made from
the first (and only) parameter.

In the code above, this new string is assigned to the identifier
`greeting`{.docutils .literal .notranslate}, and then the string is
printed.

The identifier `greeting`{.docutils .literal .notranslate} was
introduced to break the operations into a clearer sequence of steps.
However, since the value of `greeting`{.docutils .literal .notranslate}
is only referenced once, it can be eliminated with the more concise
version:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_8 component="activecode" question_label="9.10.5"}
::: {#ac8_8_8_question .ac_question}
:::
:::
:::

There can be multiple substitutions, with data of any type. Next we use
floats. Try original price \$2.50 with a 7% discount:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_9 component="activecode" question_label="9.10.6"}
::: {#ac8_8_9_question .ac_question}
:::
:::
:::

It is important to pass arguments to the `format`{.docutils .literal
.notranslate} method in the correct order, because they are matched
*positionally* into the `{}`{.docutils .literal .notranslate} places for
interpolation where there is more than one.

If you used the data suggested, this result is not satisfying. Prices
should appear with exactly two places beyond the decimal point, but that
is not the default way to display floats.

Format strings can give further information inside the braces showing
how to specially format data. In particular floats can be shown with a
specific number of decimal places. For two decimal places, put
`:.2f`{.docutils .literal .notranslate} inside the braces for the
monetary values:

::: {.runestone .explainer .ac_section}
::: {#ac8_8_10 component="activecode" question_label="9.10.7"}
::: {#ac8_8_10_question .ac_question}
:::
:::
:::

The 2 in the format modifier can be replaced by another integer to round
to that specified number of digits.

This kind of format string depends directly on the order of the
parameters to the format method. There are other approaches that we will
skip here, such as explicitly numbering substitutions.

It is also important that you give `format`{.docutils .literal
.notranslate} the same amount of arguments as there are `{}`{.docutils
.literal .notranslate} waiting for interpolation in the string. If you
have a `{}`{.docutils .literal .notranslate} in a string that you do not
pass arguments for, you may not get an error, but you will see a weird
`undefined`{.docutils .literal .notranslate} value you probably did not
intend suddenly inserted into your string. You can see an example below.

For example,

::: {.runestone .explainer .ac_section}
::: {#ac8_8_11 component="activecode" question_label="9.10.8"}
::: {#ac8_8_11_question .ac_question}
:::
:::
:::

A technical point: Since braces have special meaning in a format string,
there must be a special rule if you want braces to actually be included
in the final *formatted* string. The rule is to double the braces:
`{​{`{.docutils .literal .notranslate} and `}​}`{.docutils .literal
.notranslate}. For example mathematical set notation uses braces. The
initial and final doubled braces in the format string below generate
literal braces in the formatted string:

::: {.highlight-default .notranslate}
::: {.highlight}
    a = 5
    b = 9
    setStr = 'The set is {​{​{}, {}​}​}.'.format(a, b)
    print(setStr).
:::
:::

Unfortunately, at the time of this writing, the ActiveCode format
implementation has a bug, printing doubled braces, but standard Python
prints `{5, 9}`{.docutils .literal .notranslate}.

::: {.runestone}
-   [Nothing - it causes an error]{#question8_8_3_opt_a}
-   It is legal format syntax: put the data in place of the braces.
-   [sum of {} and {} is {}; product: {}. 2 6 8
    12]{#question8_8_3_opt_b}
-   Put the data into the format string; not after it.
-   [sum of 2 and 6 is 8; product: 12.]{#question8_8_3_opt_c}
-   Yes, correct substitutions!
-   [sum of {2} and {6} is {8}; product: {12}.]{#question8_8_3_opt_d}
-   Close: REPLACE the braces.
:::

::: {.runestone}
-   [2.34567 2.34567 2.34567]{#question8_8_4_opt_a}
-   The numbers before the f in the braces give the number of digits to
    display after the decimal point.
-   [2.3 2.34 2.34567]{#question8_8_4_opt_b}
-   Close, but round to the number of digits and display the full number
    of digits specified.
-   [2.3 2.35 2.3456700]{#question8_8_4_opt_c}
-   Yes, correct number of digits with rounding!
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

-   [[](NonmutatingMethodsonStrings.html)]{#relations-prev}
-   [[](FStrings.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
