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
        Problem](/runestone/default/reportabug?course=fopp&page=SortingaDictionary)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [16.1 Introduction: Sorting with Sort and
        Sorted](intro-SortingwithSortandSorted.html){.reference
        .internal}
    -   [16.2 Optional reverse
        parameter](Optionalreverseparameter.html){.reference .internal}
    -   [16.3 Optional key
        parameter](Optionalkeyparameter.html){.reference .internal}
    -   [16.4 Sorting a Dictionary](SortingaDictionary.html){.reference
        .internal}
    -   [16.5 Breaking Ties: Second
        Sorting](SecondarySortOrder.html){.reference .internal}
    -   [16.6 👩‍💻 When to use a Lambda
        Expression](WPWhenToUseLambdaVsFunction.html){.reference
        .internal}
    -   [16.7 Glossary](Glossary.html){.reference .internal}
    -   [16.8 Exercises](Exercises.html){.reference .internal}
    -   [16.9 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#sorting-a-dictionary .section}
[]{#sort-dictionaries}

[16.4. ]{.section-number}Sorting a Dictionary[¶](#sorting-a-dictionary "Permalink to this heading"){.headerlink}
================================================================================================================

Previously, you have used a dictionary to accumulate counts, such as the
frequencies of letters or words in a text. For example, the following
code counts the frequencies of different numbers in the list.

::: {.runestone .explainer .ac_section}
::: {#ac18_4_1 component="activecode" question_label="16.4.1"}
::: {#ac18_4_1_question .ac_question}
:::
:::
:::

The dictionary's keys are not sorted in any particular order. In fact,
you may get a different order of output than someone else running the
same code. We can force the results to be displayed in some fixed
ordering, by sorting the keys.

::: {.runestone .explainer .ac_section}
::: {#ac18_4_2 component="activecode" question_label="16.4.2"}
::: {#ac18_4_2_question .ac_question}
:::
:::
:::

With a dictionary that's maintaining counts or some other kind of score,
we might prefer to get the outputs sorted based on the count rather than
based on the items. The standard way to do that in python is to sort
based on a property of the key, in particular its value in the
dictionary.

Here things get a little confusing because we have two different meaning
of the word "key". One meaning is a key in a dictionary. The other
meaning is the parameter name for the function that you pass into the
sorted function.

Remember that the key function always takes as input one item from the
sequence and returns a property of the item. In our case, the items to
be sorted are the dictionary's keys, so each item is one key from the
dictionary. To remind ourselves of that, we've named the parameter in
tha lambda expression *k*. The property of key k that is supposed to be
returned is its associated value in the dictionary. Hence, we have the
lambda expression `lambda k: d[k]`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#ac18_4_5 component="activecode" question_label="16.4.3"}
::: {#ac18_4_5_question .ac_question}
:::
:::
:::

Here's a version of that using a named function.

::: {.runestone .explainer .ac_section}
::: {#ac18_4_6 component="activecode" question_label="16.4.4"}
::: {#ac18_4_6_question .ac_question}
:::
:::
:::

::: {.admonition .note}
Note

When we sort the keys, passing a function with
`key=lambda x: d[x]`{.docutils .literal .notranslate} does not specify
to sort the keys of a dictionary. The lists of keys are passed as the
first parameter value in the invocation of sort. The key parameter
provides a function that says *how* to sort them.
:::

An experienced programmer would probably not even separate out the
sorting step. And they might take advantage of the fact that when you
pass a dictionary to something that is expecting a list, its the same as
passing the list of keys.

::: {.runestone .explainer .ac_section}
::: {#ac18_4_7 component="activecode" question_label="16.4.5"}
::: {#ac18_4_7_question .ac_question}
:::
:::
:::

Eventually, you will be able to read code like that and immediately know
what it's doing. For now, when you come across something confusing, like
line 11, try breaking it down. The function `sorted`{.docutils .literal
.notranslate} is invoked. Its first parameter value is a dictionary,
which really means the keys of the dictionary. The second parameter, the
key function, decorates the dictionary key with a post-it note
containing that key's value in dictionary d. The last parameter, True,
says to sort in reverse order.

There is another way to sort dictionaries, by calling .items() to
extract a sequence of (key, value) tuples, and then sorting that
sequence of tuples. But it's better to learn the pythonic way of doing
it, sorting the dictionary keys using a key function that takes one key
as input and looks up the value in the dictionary.

**Check Your Understanding**

::: {.runestone}
-   [sorted(ks, key=g)]{#question18_4_1_opt_a}
-   g is a function that takes two parameters. The key function passed
    to sorted must always take just one parameter.
-   [sorted(ks, key=lambda x: g(x, d))]{#question18_4_1_opt_b}
-   The lambda function takes just one parameter, and calls g with two
    parameters.
-   [sorted(ks, key=lambda x: d\[x\])]{#question18_4_1_opt_c}
-   The lambda function looks up the value of x in d.
:::

::: {.runestone .explainer .ac_section}
::: {#ac18_4_8 component="activecode" question_label="16.4.7"}
::: {#ac18_4_8_question .ac_question}
**2.** Sort the following dictionary based on the keys so that they are
sorted a to z. Assign the resulting value to the variable
`sorted_keys`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac18_4_9 component="activecode" question_label="16.4.8"}
::: {#ac18_4_9_question .ac_question}
**3.** Below, we have provided the dictionary `groceries`{.docutils
.literal .notranslate}, whose keys are grocery items, and values are the
number of each item that you need to buy at the store. Sort the
dictionary's keys into alphabetical order, and save them as a list
called `grocery_keys_sorted`{.docutils .literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac18_4_10 component="activecode" question_label="16.4.9"}
::: {#ac18_4_10_question .ac_question}
**4.** Sort the following dictionary's keys based on the value from
highest to lowest. Assign the resulting value to the variable
`sorted_values`{.docutils .literal .notranslate}.
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

-   [[](Optionalkeyparameter.html)]{#relations-prev}
-   [[](SecondarySortOrder.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
