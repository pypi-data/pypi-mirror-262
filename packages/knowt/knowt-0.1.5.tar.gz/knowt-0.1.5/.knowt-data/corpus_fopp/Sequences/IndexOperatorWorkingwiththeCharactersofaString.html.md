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
        Problem](/runestone/default/reportabug?course=fopp&page=IndexOperatorWorkingwiththeCharactersofaString)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [6.1 Introduction: Sequences](intro-Sequences.html){.reference
        .internal}
    -   [6.2 Strings, Lists, and
        Tuples](StringsandLists.html){.reference .internal}
    -   [6.3 Index Operator: Working with the Characters of a
        String](IndexOperatorWorkingwiththeCharactersofaString.html){.reference
        .internal}
    -   [6.4 Disambiguating \[\]: creation vs
        indexing](DisabmiguatingSquareBrackets.html){.reference
        .internal}
    -   [6.5 Length](Length.html){.reference .internal}
    -   [6.6 The Slice Operator](TheSliceOperator.html){.reference
        .internal}
    -   [6.7 Concatenation and
        Repetition](ConcatenationandRepetition.html){.reference
        .internal}
    -   [6.8 Count and Index](CountandIndex.html){.reference .internal}
    -   [6.9 Splitting and Joining
        Strings](SplitandJoin.html){.reference .internal}
    -   [6.10 Exercises](Exercises.html){.reference .internal}
    -   [6.11 Chapter Assessment](week2a1.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#index-operator-working-with-the-characters-of-a-string .section}
[]{#index-0}

[6.3. ]{.section-number}Index Operator: Working with the Characters of a String[¶](#index-operator-working-with-the-characters-of-a-string "Permalink to this heading"){.headerlink}
====================================================================================================================================================================================

The **indexing operator** (Python uses square brackets to enclose the
index) selects a single character from a string. The characters are
accessed by their position or index value. For example, in the string
shown below, the 14 characters are indexed left to right from postion 0
to position 13.

![index values](../_images/indexvalues.png)

It is also the case that the positions are named from right to left
using negative numbers where -1 is the rightmost index and so on. Note
that the character at index 6 (or -8) is the blank character.

::: {.runestone .explainer .ac_section}
::: {#ac5_3_1 component="activecode" question_label="6.3.1"}
::: {#ac5_3_1_question .ac_question}
:::
:::
:::

The expression `school[2]`{.docutils .literal .notranslate} selects the
character at index 2 from `school`{.docutils .literal .notranslate}, and
creates a new string containing just this one character. The variable
`m`{.docutils .literal .notranslate} refers to the result.

The letter at index zero of `"Luther College"`{.docutils .literal
.notranslate} is `L`{.docutils .literal .notranslate}. So at position
`[2]`{.docutils .literal .notranslate} we have the letter `t`{.docutils
.literal .notranslate}.

If you want the zero-eth letter of a string, you just put 0, or any
expression with the value 0, in the brackets. Give it a try.

The expression in brackets is called an **index**. An index specifies a
member of an ordered collection. In this case the collection of
characters in the string. The index *indicates* which character you
want. It can be any integer expression so long as it evaluates to a
valid index value.

Note that indexing returns a *string* --- Python has no special type for
a single character. It is just a string of length 1.

::: {#index-operator-accessing-elements-of-a-list-or-tuple .section}
[6.3.1. ]{.section-number}Index Operator: Accessing Elements of a List or Tuple[¶](#index-operator-accessing-elements-of-a-list-or-tuple "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The syntax for accessing the elements of a list or tuple is the same as
the syntax for accessing the characters of a string. We use the index
operator ( `[]`{.docutils .literal .notranslate} -- not to be confused
with an empty list). The expression inside the brackets specifies the
index. Remember that the indices start at 0. Any integer expression can
be used as an index and as with strings, negative index values will
locate items from the right instead of from the left.

When we say the first, third or nth character of a sequence, we
generally mean counting the usual way, starting with 1. The nth
character and the character AT INDEX n are different then: The nth
character is at index n-1. Make sure you are clear on what you mean!

Try to predict what will be printed out by the following code, and then
run it to check your prediction. (Actually, it's a good idea to always
do that with the code examples. You will learn much more if you force
yourself to make a prediction before you see the output.)

::: {.runestone .explainer .ac_section}
::: {#ac5_3_2 component="activecode" question_label="6.3.1.1"}
::: {#ac5_3_2_question .ac_question}
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_3_3 component="activecode" question_label="6.3.1.2"}
::: {#ac5_3_3_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [t]{#question5_3_1_opt_a}
-   Index locations do not start with 1, they start with 0.
-   [h]{#question5_3_1_opt_b}
-   Yes, index locations start with 0.
-   [c]{#question5_3_1_opt_c}
-   s\[-3\] would return c, counting from right to left.
-   [Error, you cannot use the \[ \] operator with a
    string.]{#question5_3_1_opt_d}
-   \[ \] is the index operator.
:::

::: {.runestone}
-   [tr]{#question5_3_2_opt_a}
-   Almost, t is at postion 2, counting left to right starting from 0;
    but r is at -5, counting right to left starting from -1.
-   [to]{#question5_3_2_opt_b}
-   For -4 you count from right to left, starting with -1.
-   [ps]{#question5_3_2_opt_c}
-   p is at location 0, not 2.
-   [nn]{#question5_3_2_opt_d}
-   n is at location 5, not 2.
-   [Error, you cannot use the \[ \] operator with the +
    operator.]{#question5_3_2_opt_e}
-   \[ \] operator returns a string that can be concatenated with
    another string.
:::

::: {.runestone}
-   [\[ \]]{#question5_3_3_opt_a}
-   The empty list is at index 4.
-   [3.14]{#question5_3_3_opt_b}
-   Yes, 3.14 is at index 5 since we start counting at 0 and sublists
    count as one item.
-   [False]{#question5_3_3_opt_c}
-   False is at index 6.
-   [\"dog\"]{#question5_3_3_opt_d}
-   Look again, the element at index 3 is a list. This list only counts
    as one element.
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_3_4 component="activecode" question_label="6.3.1.6"}
::: {#ac5_3_4_question .ac_question}
Assign the value of the 34th element of `lst`{.docutils .literal
.notranslate} to the variable `output`{.docutils .literal .notranslate}.
Note that the l in lst is a letter, not a number; variable names can't
start with a number.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_3_5 component="activecode" question_label="6.3.1.7"}
::: {#ac5_3_5_question .ac_question}
Assign the value of the 23rd element of `l`{.docutils .literal
.notranslate} to the variable `checking`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac5_3_6 component="activecode" question_label="6.3.1.8"}
::: {#ac5_3_6_question .ac_question}
Assign the value of the last chacter of `lst`{.docutils .literal
.notranslate} to the variable `output`{.docutils .literal .notranslate}.
Do this so that the length of lst doesn't matter.
:::
:::
:::

::: {.admonition .note}
Note

Why does counting start at 0 going from left to right, but at -1 going
from right to left? Well, indexing starting at 0 has a long history in
computer science having to do with some low-level implementation details
that we won't go into. For indexing from right to left, it might seem
natural to do the analgous thing and start at -0. Unfortunately, -0 is
the same as 0, so s\[-0\] can't be the last item. Remember we said that
programming languages are formal languages where details matter and
everything is taken literally?
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

-   [[](StringsandLists.html)]{#relations-prev}
-   [[](DisabmiguatingSquareBrackets.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
