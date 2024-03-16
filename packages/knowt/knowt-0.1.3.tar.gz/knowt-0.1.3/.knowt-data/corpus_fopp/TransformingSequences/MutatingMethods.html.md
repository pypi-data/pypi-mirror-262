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
        Problem](/runestone/default/reportabug?course=fopp&page=MutatingMethods)
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
::: {#mutating-methods .section}
[9.7. ]{.section-number}Mutating Methods[¶](#mutating-methods "Permalink to this heading"){.headerlink}
=======================================================================================================

You've seen some methods already, like the `count`{.docutils .literal
.notranslate} and `index`{.docutils .literal .notranslate} methods.
Methods are either mutating or non-mutating. Mutating methods are ones
that change the object after the method has been used. Non-mutating
methods do not change the object after the method has been used.

The `count`{.docutils .literal .notranslate} and `index`{.docutils
.literal .notranslate} methods are both non-mutating. Count returns the
number of occurrences of the argument given but does not change the
original string or list. Similarly, index returns the leftmost
occurrence of the argument but does not change the original string or
list. Below we'll talk about list methods in general. Keep an eye out
for methods that are mutating!

::: {#list-methods .section}
[9.7.1. ]{.section-number}List Methods[¶](#list-methods "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------------

The dot operator can also be used to access built-in methods of list
objects. `append`{.docutils .literal .notranslate} is a list method
which adds the argument passed to it to the end of the list. Continuing
with this example, we show several other list methods. Many of them are
easy to understand.

::: {.runestone .explainer .ac_section}
::: {#ac8_6_1 component="activecode" question_label="9.7.1.1"}
::: {#ac8_6_1_question .ac_question}
:::
:::
:::

There are two ways to use the `pop`{.docutils .literal .notranslate}
method. The first, with no parameter, will remove and return the last
item of the list. If you provide a parameter for the position,
`pop`{.docutils .literal .notranslate} will remove and return the item
at that position. Either way the list is changed.

The following table provides a summary of the list methods shown above.
The column labeled `result`{.docutils .literal .notranslate} gives an
explanation as to what the return value is as it relates to the new
value of the list. The word **mutator** means that the list is changed
by the method but nothing is returned (actually `None`{.docutils
.literal .notranslate} is returned). A **hybrid** method is one that not
only changes the list but also returns a value as its result. Finally,
if the result is simply a return, then the list is unchanged by the
method.

Be sure to experiment with these methods to gain a better understanding
of what they do.

  Method    Parameters       Result       Description
  --------- ---------------- ------------ --------------------------------------------------
  append    item             mutator      Adds a new item to the end of a list
  insert    position, item   mutator      Inserts a new item at the position given
  pop       none             hybrid       Removes and returns the last item
  pop       position         hybrid       Removes and returns the item at position
  sort      none             mutator      Modifies a list to be sorted
  reverse   none             mutator      Modifies a list to be in reverse order
  index     item             return idx   Returns the position of first occurrence of item
  count     item             return ct    Returns the number of occurrences of item
  remove    item             mutator      Removes the first occurrence of item

Details for these and others can be found in the [Python
Documentation](http://docs.python.org/py3k/library/stdtypes.html#sequence-types-str-bytes-bytearray-list-tuple-range){.reference
.external}.

It is important to remember that methods like `append`{.docutils
.literal .notranslate}, `sort`{.docutils .literal .notranslate}, and
`reverse`{.docutils .literal .notranslate} all return `None`{.docutils
.literal .notranslate}. They change the list; they don't produce a new
list. So, while we did reassignment to increment a number, as in
`x = x + 1`{.docutils .literal .notranslate}, doing the analogous thing
with these operations will lose the entire list contents (see line 8
below).

::: {.runestone .explainer .ac_section}
::: {#ac8_6_2 component="activecode" question_label="9.7.1.2"}
::: {#ac8_6_2_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [\[4,2,8,6,5,False,True\]]{#question8_6_1_opt_a}
-   True was added first, then False was added last.
-   [\[4,2,8,6,5,True,False\]]{#question8_6_1_opt_b}
-   Yes, each item is added to the end of the list.
-   [\[True,False,4,2,8,6,5\]]{#question8_6_1_opt_c}
-   append adds at the end, not the beginning.
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

-   [[](CloningLists.html)]{#relations-prev}
-   [[](AppendversusConcatenate.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
