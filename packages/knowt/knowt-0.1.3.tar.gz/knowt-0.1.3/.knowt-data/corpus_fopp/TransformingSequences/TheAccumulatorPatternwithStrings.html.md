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
        Problem](/runestone/default/reportabug?course=fopp&page=TheAccumulatorPatternwithStrings)
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

::: {#the-accumulator-pattern-with-strings .section}
[9.13. ]{.section-number}The Accumulator Pattern with Strings[¶](#the-accumulator-pattern-with-strings "Permalink to this heading"){.headerlink}
================================================================================================================================================

We can also accumulate strings rather than accumulating numbers, as
you've seen before. The following program isn't particularly useful for
data processing, but we will see more useful things later that
accumulate strings.

::: {.runestone .explainer .ac_section}
::: {#ac8_10_1 component="activecode" question_label="9.13.1"}
::: {#ac8_10_1_question .ac_question}
:::
:::
:::

Look carefully at line 4 in the above program
(`ac = ac + c + "-"`{.docutils .literal .notranslate}). In words, it
says that the new value of `ac`{.docutils .literal .notranslate} will be
the old value of `ac`{.docutils .literal .notranslate} concatenated with
the current character and a dash. We are building the result string
character by character.

Take a close look also at the initialization of `ac`{.docutils .literal
.notranslate}. We start with an empty string and then begin adding new
characters to the end. Also note that I have given it a different name
this time, `ac`{.docutils .literal .notranslate} instead of
`accum`{.docutils .literal .notranslate}. There's nothing magical about
these names. You could use any valid variable and it would work the same
(try substituting x for ac everywhere in the above code).

We can use the accumulator pattern to reverse a string, as in the
following code.

::: {.runestone .explainer .ac_section}
::: {#ac8_10_1_1 component="activecode" question_label="9.13.2"}
::: {#ac8_10_1_1_question .ac_question}
:::
:::
:::

The key thing here is that we have `ac = c + ac`{.docutils .literal
.notranslate}. The iterator variable comes first, before the
accumulator. We are pre-pending the new value onto the beginning of the
value that has been accumulated so far, and that leads to reversing the
whole string. Try it in codelens if you're having trouble envisioning
why this works.

::: {.admonition .note}
Note

A little humorous aside... You've probably heard of Murphy's Law, that
everything that can go wrong will go wrong.

In a [paper](https://doi.org/10.1007%2Fs10683-006-4309-2){.reference
.external} co-authored by one of this book's authors, we described
eBay's reputation system as an example of Yhprum's Law (Yhprum is Murphy
spelled backward, with a little change in capitalization): "Systems that
shouldn't work sometimes do, or at least work fairly well."
:::

**Check your understanding**

::: {.runestone}
-   [Ball]{#question8_10_1_opt_a}
-   Each item is converted to upper case before concatenation.
-   [BALL]{#question8_10_1_opt_b}
-   Each character is converted to upper case but the order is wrong.
-   [LLAB]{#question8_10_1_opt_c}
-   Yes, the order is reversed due to the order of the concatenation.
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_10_2 component="activecode" question_label="9.13.4"}
::: {#ac8_10_2_question .ac_question}
1.  Accumulate all the characters from the string in the variable
    `str1`{.docutils .literal .notranslate} into a list of characters
    called `chars`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac6_6_6 component="activecode" question_label="9.13.5"}
::: {#ac6_6_6_question .ac_question}
Assign an empty string to the variable `output`{.docutils .literal
.notranslate}. Using the `range`{.docutils .literal .notranslate}
function, write code to make it so that the variable `output`{.docutils
.literal .notranslate} has 35 `a`{.docutils .literal .notranslate} s
inside it (like `"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"`{.docutils
.literal .notranslate}). Hint: use the accumulation pattern!
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

-   [[](TheAccumulatorPatternwithLists.html)]{#relations-prev}
-   [[](WPAccumulatorPatternStrategies.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
