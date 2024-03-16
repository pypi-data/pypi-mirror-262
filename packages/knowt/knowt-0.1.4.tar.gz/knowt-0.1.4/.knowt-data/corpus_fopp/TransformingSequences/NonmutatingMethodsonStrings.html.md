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
        Problem](/runestone/default/reportabug?course=fopp&page=NonmutatingMethodsonStrings)
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
::: {#non-mutating-methods-on-strings .section}
[9.9. ]{.section-number}Non-mutating Methods on Strings[¶](#non-mutating-methods-on-strings "Permalink to this heading"){.headerlink}
=====================================================================================================================================

There are a wide variety of methods for string objects. Try the
following program.

::: {.runestone .explainer .ac_section}
::: {#ac8_8_1 component="activecode" question_label="9.9.1"}
::: {#ac8_8_1_question .ac_question}
:::
:::
:::

In this example, `upper`{.docutils .literal .notranslate} is a method
that can be invoked on any string object to create a new string in which
all the characters are in uppercase. `lower`{.docutils .literal
.notranslate} works in a similar fashion changing all characters in the
string to lowercase. (The original string `ss`{.docutils .literal
.notranslate} remains unchanged. A new string `tt`{.docutils .literal
.notranslate} is created.)

You've already seen a few methods, such as `count`{.docutils .literal
.notranslate} and `index`{.docutils .literal .notranslate}, that work
with strings and are non-mutating. In addition to those and
`upper`{.docutils .literal .notranslate} and `lower`{.docutils .literal
.notranslate}, the following table provides a summary of some other
useful string methods. There are a few activecode examples that follow
so that you can try them out.

  Method    Parameters      Description
  --------- --------------- --------------------------------------------------------------------------------------------------------------------------
  upper     none            Returns a string in all uppercase
  lower     none            Returns a string in all lowercase
  count     item            Returns the number of occurrences of item
  index     item            Returns the leftmost index where the substring item is found and causes a runtime error if item is not found
  strip     none            Returns a string with the leading and trailing whitespace removed
  replace   old, new        Replaces all occurrences of old substring with new
  format    substitutions   Involved! See [[String Format Method]{.std .std-ref}](StringFormatting.html#format-strings){.reference .internal}, below

You should experiment with these methods so that you understand what
they do. Note once again that the methods that return strings do not
change the original. You can also consult the [Python documentation for
strings](http://docs.python.org/3/library/stdtypes.html#string-methods){.reference
.external}.

::: {.runestone .explainer .ac_section}
::: {#ac8_8_2 component="activecode" question_label="9.9.2"}
::: {#ac8_8_2_question .ac_question}
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac8_8_3 component="activecode" question_label="9.9.3"}
::: {#ac8_8_3_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [0]{#question8_8_1_opt_a}
-   There are definitely o and p characters.
-   [2]{#question8_8_1_opt_b}
-   There are 2 o characters but what about p?
-   [3]{#question8_8_1_opt_c}
-   Yes, add the number of o characters and the number of p characters.
:::

::: {.runestone}
-   [yyyyy]{#question8_8_2_opt_a}
-   Yes, s\[1\] is y and the index of n is 5, so 5 y characters. It is
    important to realize that the index method has precedence over the
    repetition operator. Repetition is done last.
-   [55555]{#question8_8_2_opt_b}
-   Close. 5 is not repeated, it is the number of times to repeat.
-   [n]{#question8_8_2_opt_c}
-   This expression uses the index of n
-   [Error, you cannot combine all those things
    together.]{#question8_8_2_opt_d}
-   This is fine, the repetition operator used the result of indexing
    and the index method.
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

-   [[](AppendversusConcatenate.html)]{#relations-prev}
-   [[](StringFormatting.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
