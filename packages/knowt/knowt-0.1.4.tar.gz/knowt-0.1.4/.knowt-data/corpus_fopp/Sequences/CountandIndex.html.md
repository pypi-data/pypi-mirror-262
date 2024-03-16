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
        Problem](/runestone/default/reportabug?course=fopp&page=CountandIndex)
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

::: {#count-and-index .section}
[6.8. ]{.section-number}Count and Index[¶](#count-and-index "Permalink to this heading"){.headerlink}
=====================================================================================================

As you create more complex programs, you will find that some tasks are
commonly done. Python has some built-in functions and methods to help
you with these tasks. This page will cover two helpful methods for both
strings and lists: count and index.

You've learned about methods before when drawing with the turtle module.
There, you used `.forward(50)`{.docutils .literal .notranslate} and
`.color("purple")`{.docutils .literal .notranslate} to complete actions.
We refer to forward and color as methods of the turtle class. Objects
like strings and lists also have methods that we can use.

::: {#count .section}
[6.8.1. ]{.section-number}Count[¶](#count "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------

The first method we'll talk about is called `count`{.docutils .literal
.notranslate}. It requires that you provide one argument, which is what
you would like to count. The method then returns the number of times
that the argument occured in the string/list the method was used on.
There are some differences between count for strings and count for
lists. When you use count on a string, the argument can only be a
string. You can't count how many times the integer 2 appears in a
string, though you can count how many times the string "2" appears in a
string. For lists, the argument is not restricted to just strings.

::: {.runestone .explainer .ac_section}
::: {#ac5_8_1 component="activecode" question_label="6.8.1.1"}
::: {#ac5_8_1_question .ac_question}
:::
:::
:::

The activecode window above demonstrates the use of count on a string.
Just like with the turtle module when we had to specify which turtle was
changing color or moving, we have to specify which string we are using
count on.

::: {.runestone .explainer .ac_section}
::: {#ac5_8_2 component="activecode" question_label="6.8.1.2"}
::: {#ac5_8_2_question .ac_question}
:::
:::
:::

When you run the activecode window above, you'll see how count with a
list works. Notice how "4" has a count of zero but 4 has a count of
three? This is because the list `z`{.docutils .literal .notranslate}
only contains the integer 4. There are never any strings that are 4.
Additionally, when we check the count of "a", we see that the program
returns zero. Though some of the words in the list contain the letter
"a", the program is looking for items in the list that are *just* the
letter "a".
:::

::: {#index .section}
[6.8.2. ]{.section-number}Index[¶](#index "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------

The other method that can be helpful for both strings and lists is the
`index`{.docutils .literal .notranslate} method. The `index`{.docutils
.literal .notranslate} method requires one argument, and, like the
`count`{.docutils .literal .notranslate} method, it takes only strings
when index is used on strings, and any type when it is used on lists.
For both strings and lists, `index`{.docutils .literal .notranslate}
returns the leftmost index where the argument is found. If it is unable
to find the argument in the string or list, then an error will occur.

::: {.runestone .explainer .ac_section}
::: {#ac5_8_3 component="activecode" question_label="6.8.2.1"}
::: {#ac5_8_3_question .ac_question}
:::
:::
:::

All of the above examples work, but were you surprised by any of the
return values? Remember that `index`{.docutils .literal .notranslate}
will return the left most index of the argument. Even though
"Metatarsal" occurs many times in `bio`{.docutils .literal
.notranslate}, the method will only return the location of one of them.

Here's another example.

::: {.runestone .explainer .ac_section}
::: {#ac5_8_4 component="activecode" question_label="6.8.2.2"}
::: {#ac5_8_4_question .ac_question}
:::
:::
:::

In the activecode window above, we're trying to see where "autumn" is in
the list seasons. However, there is no string called autumn (though
there is string called "fall" which is likely what the program is
looking for). Remember that an error occurs if the argument is not in
the string or list.

**Check your understanding**

::: {.runestone}
-   [5]{#question5_8_1_opt_a}
-   Yes, when we get the index of a string that is longer than one
    character, we get the index for the first character in the string.
-   [6]{#question5_8_1_opt_b}
-   When we get the index of a string that is longer than one character,
    we get the index for the first character in the string.
-   [13]{#question5_8_1_opt_c}
-   Remember that index returns the left most occurance of the argument.
-   [14]{#question5_8_1_opt_d}
-   Remember that index returns the left most occurance of the argument.
-   [There is an error.]{#question5_8_1_opt_e}
-   There is at least one \'we\' in the string assigned to qu.
:::

::: {.runestone}
-   [0]{#question5_8_2_opt_a}
-   No, there is at least one e in the string.
-   [2]{#question5_8_2_opt_b}
-   Yes, there is a difference between \"we\" and \"We\" which means
    there are only two in the string.
-   [3]{#question5_8_2_opt_c}
-   there is a difference between \"we\" and \"We\".
-   [There is an error.]{#question5_8_2_opt_d}
-   There is no error in the code.
:::

::: {.runestone}
-   [0]{#question5_8_3_opt_a}
-   No, the first element is \'bathroom\', not \'garden\'.
-   [-1]{#question5_8_3_opt_b}
-   Though there is no \'garden\' in the list, we do not get back -1
    when we use index. Instead, we get an error.
-   [There is an error.]{#question5_8_3_opt_c}
-   Yes, there is no \'garden\' in the list, so we get back an error.
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

-   [[](ConcatenationandRepetition.html)]{#relations-prev}
-   [[](SplitandJoin.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
