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
        Problem](/runestone/default/reportabug?course=fopp&page=Dictionarymethods)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [11.1 Introduction:
        Dictionaries](intro-DictionaryGoals.html){.reference .internal}
    -   [11.2 Getting Started with
        Dictionaries](intro-Dictionaries.html){.reference .internal}
    -   [11.3 Dictionary
        operations](Dictionaryoperations.html){.reference .internal}
    -   [11.4 Dictionary methods](Dictionarymethods.html){.reference
        .internal}
    -   [11.5 Aliasing and copying](Aliasingandcopying.html){.reference
        .internal}
    -   [11.6 Introduction: Accumulating Multiple Results In a
        Dictionary](intro-AccumulatingMultipleResultsInaDictionary.html){.reference
        .internal}
    -   [11.7 Accumulating Results From a
        Dictionary](AccumulatingResultsFromaDictionary.html){.reference
        .internal}
    -   [11.8 Accumulating the Best
        Key](AccumulatingtheBestKey.html){.reference .internal}
    -   [11.9 👩‍💻 When to use a
        dictionary](WPChoosingDictionaries.html){.reference .internal}
    -   [11.10 Glossary](Glossary.html){.reference .internal}
    -   [11.11 Exercises](Exercises.html){.reference .internal}
    -   [11.12 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#dictionary-methods .section}
[11.4. ]{.section-number}Dictionary methods[¶](#dictionary-methods "Permalink to this heading"){.headerlink}
============================================================================================================

Dictionaries have a number of useful built-in methods. The following
table provides a summary and more details can be found in the [Python
Documentation](http://docs.python.org/3/library/stdtypes.html#mapping-types-dict){.reference
.external}.

  Method   Parameters   Description
  -------- ------------ ---------------------------------------------------------
  keys     none         Returns a view of the keys in the dictionary
  values   none         Returns a view of the values in the dictionary
  items    none         Returns a view of the key-value pairs in the dictionary
  get      key          Returns the value associated with key; None otherwise
  get      key,alt      Returns the value associated with key; alt otherwise

As we saw earlier with strings and lists, dictionary methods use dot
notation, which specifies the name of the method to the right of the dot
and the name of the object on which to apply the method immediately to
the left of the dot. For example, if `x`{.docutils .literal
.notranslate} is a variable whose value is a dictionary,
`x.keys`{.docutils .literal .notranslate} is the method object, and
`x.keys()`{.docutils .literal .notranslate} invokes the method,
returning a view of the value.

::: {#iterating-over-dictionaries .section}
[11.4.1. ]{.section-number}Iterating over Dictionaries[¶](#iterating-over-dictionaries "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------------

There are three ways to iterate over the contents of a dictionary. Let's
take a moment to examine them.

The first technique involves iterating over the keys of the dictionary
using the `keys`{.docutils .literal .notranslate} method. The
`keys`{.docutils .literal .notranslate} method returns a collection of
the keys in the dictionary.

::: {.runestone .explainer .ac_section}
::: {#ac10_3_1 component="activecode" question_label="11.4.1.1"}
::: {#ac10_3_1_question .ac_question}
:::
:::
:::

Note the first line of the for loop:

::: {.highlight-default .notranslate}
::: {.highlight}
    for akey in inventory.keys():
:::
:::

Each time through the loop, the loop variable `akey`{.docutils .literal
.notranslate} is assigned a different key in the dictionary. In the loop
body, the value associated with the key is accessed by indexing the
dictionary with `akey`{.docutils .literal .notranslate} using the
expression `inventory[akey]`{.docutils .literal .notranslate}. Note that
the order in which the keys are assigned in the loop is not predictable.
If you want to visit the keys in alphabetic order, you must use the
`sorted`{.docutils .literal .notranslate} function to produce a sorted
collection of keys, like this:

::: {.highlight-default .notranslate}
::: {.highlight}
    for akey in sorted(inventory.keys()):
:::
:::

It's so common to iterate over the keys in a dictionary that you can
omit the `keys`{.docutils .literal .notranslate} method call in the
`for`{.docutils .literal .notranslate} loop --- iterating over a
dictionary implicitly iterates over its keys.

::: {.runestone .explainer .ac_section}
::: {#ac10_3_2 component="activecode" question_label="11.4.1.2"}
::: {#ac10_3_2_question .ac_question}
:::
:::
:::

The `values`{.docutils .literal .notranslate} method returns a
collection of the values in the dictionary. Here's an example that
displays a list of the values:

::: {.runestone .explainer .ac_section}
::: {#ac10_3_3a component="activecode" question_label="11.4.1.3"}
::: {#ac10_3_3a_question .ac_question}
:::
:::
:::

The `items`{.docutils .literal .notranslate} method returns a collection
of tuples containing each key and its associated value. Take a look at
this example that iterates over the dictionary using the
`items`{.docutils .literal .notranslate} method:

::: {.runestone .explainer .ac_section}
::: {#ac10_3_3b component="activecode" question_label="11.4.1.4"}
::: {#ac10_3_3b_question .ac_question}
:::
:::
:::

Take a close look at the first line of the for loop:

::: {.highlight-default .notranslate}
::: {.highlight}
    for k, v in inventory.items():
:::
:::

Each time through the loop, `k`{.docutils .literal .notranslate}
receives a key from the dictionary, and `v`{.docutils .literal
.notranslate} receives its associated value. That avoids the need to
index the dictionary inside the loop body to access the value associated
with the key.

::: {.admonition .note}
Note

You may have noticed in the examples above that, to print the result of
the `keys()`{.docutils .literal .notranslate}, `values()`{.docutils
.literal .notranslate}, and `items()`{.docutils .literal .notranslate}
methods, we used lines like this:

::: {.highlight-default .notranslate}
::: {.highlight}
    print(list(inventory.keys())
:::
:::

instead of this:

::: {.highlight-default .notranslate}
::: {.highlight}
    print(inventory.keys())
:::
:::

Technically, `keys()`{.docutils .literal .notranslate},
`values()`{.docutils .literal .notranslate}, and `items()`{.docutils
.literal .notranslate} don't return actual lists. Like the
`range`{.docutils .literal .notranslate} function described previously,
they return objects that produce the items one at a time, rather than
producing and storing all of them in advance as a list. If you need to
perform an operation on the result of one of these methods such as
extracting the first item, you must convert the result to a list using
the `list`{.docutils .literal .notranslate} conversion function. For
example, if you want to get the first key, this won't work:
`inventory.keys()[0]`{.docutils .literal .notranslate}. You need to make
the collection of keys into a real list before using `[0]`{.docutils
.literal .notranslate} to index into it:
`list(inventory.keys())[0]`{.docutils .literal .notranslate}.
:::
:::

::: {#safely-retrieving-values .section}
[11.4.2. ]{.section-number}Safely Retrieving Values[¶](#safely-retrieving-values "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------

Looking up a value in a dictionary is a potentially dangerous operation.
When using the `[]`{.docutils .literal .notranslate} operator to access
a key, if the key is not present, a runtime error occurs. There are two
ways to deal with this problem.

The first approach is to use the `in`{.docutils .literal .notranslate}
and `not in`{.docutils .literal .notranslate} operators, which can test
if a key is in the dictionary:

::: {.runestone .explainer .ac_section}
::: {#ac10_3_4 component="activecode" question_label="11.4.2.1"}
::: {#ac10_3_4_question .ac_question}
:::
:::
:::

The second approach is to use the `get`{.docutils .literal .notranslate}
method. `get`{.docutils .literal .notranslate} retrieves the value
associated with a key, similar to the `[]`{.docutils .literal
.notranslate} operator. The important difference is that `get`{.docutils
.literal .notranslate} will not cause a runtime error if the key is not
present. It will instead return the value `None`{.docutils .literal
.notranslate}. There exists a variation of `get`{.docutils .literal
.notranslate} that allows a second parameter that serves as an
alternative return value in the case where the key is not present. This
can be seen in the final example below. In this case, since "cherries"
is not a key, `get`{.docutils .literal .notranslate} returns 0 (instead
of None).

::: {.runestone .explainer .ac_section}
::: {#ac10_3_5 component="activecode" question_label="11.4.2.2"}
::: {#ac10_3_5_question .ac_question}
:::
:::
:::

**Check your understanding**

::: {.runestone}
-   [2]{#question10_3_1_opt_a}
-   get returns the value associated with a given key so this divides 12
    by 6.
-   [0.5]{#question10_3_1_opt_b}
-   12 is divided by 6, not the other way around.
-   [bear]{#question10_3_1_opt_c}
-   Take another look at the example for get above. get returns the
    value associated with a given key.
-   [Error, divide is not a valid operation on
    dictionaries.]{#question10_3_1_opt_d}
-   The integer division operator is being used on the values returned
    from the get method, not on the dictionary.
:::

::: {.runestone}
-   [True]{#question10_3_2_opt_a}
-   Yes, dog is a key in the dictionary.
-   [False]{#question10_3_2_opt_b}
-   The in operator returns True if a key is in the dictionary, False
    otherwise.
:::

::: {.runestone}
-   [True]{#question10_3_3_opt_a}
-   23 is a value in the dictionary, not a key.
-   [False]{#question10_3_3_opt_b}
-   Yes, the in operator returns True if a key is in the dictionary,
    False otherwise.
:::

::: {.runestone}
-   [18]{#question10_3_4_opt_a}
-   Add the values that have keys longer than 3 characters, not those
    with exactly 3 characters.
-   [43]{#question10_3_4_opt_b}
-   Yes, the for statement iterates over the keys. It adds the values of
    the keys that have length greater than 3.
-   [0]{#question10_3_4_opt_c}
-   This is the accumulator pattern. Total starts at 0 but then changes
    as the iteration proceeds.
-   [61]{#question10_3_4_opt_d}
-   Not all the values are added together. The if statement only chooses
    some of them.
:::

::: {#tabbed_ac10_3_7 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac10_3_7 component="activecode" question_label="11.4.2.7"}
::: {#ac10_3_7_question .ac_question}
**5.** We have a dictionary of the specific events that Italy has won
medals in and the number of medals they have won for each event. Assign
to the variable `events`{.docutils .literal .notranslate} a list of the
keys from the dictionary `medal_events`{.docutils .literal
.notranslate}. Use a dictionary method and cast to a list; do not hard
code or accumulate a list via iteration.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
Add the following line:

::: {.highlight-default .notranslate}
::: {.highlight}
    events = list(medal_events.keys())
:::
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

-   [[](Dictionaryoperations.html)]{#relations-prev}
-   [[](Aliasingandcopying.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
