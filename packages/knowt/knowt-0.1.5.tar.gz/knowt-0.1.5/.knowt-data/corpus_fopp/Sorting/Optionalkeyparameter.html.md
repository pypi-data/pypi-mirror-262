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
        Problem](/runestone/default/reportabug?course=fopp&page=Optionalkeyparameter)
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
::: {#optional-key-parameter .section}
[16.3. ]{.section-number}Optional key parameter[¶](#optional-key-parameter "Permalink to this heading"){.headerlink}
====================================================================================================================

If you want to sort things in some order other than the "natural" or its
reverse, you can provide an additional parameter, the key parameter. For
example, suppose you want to sort a list of numbers based on their
absolute value, so that -4 comes after 3? Or suppose you have a
dictionary with strings as the keys and numbers as the values. Instead
of sorting them in alphabetic order based on the keys, you might like to
sort them in order based on their values.

First, let's see an example, and then we'll dive into how it works.

First, let's define a function absolute that takes a number and returns
its absolute value. (Actually, python provides a built-in function
`abs`{.docutils .literal .notranslate} that does this, but we are going
to define our own, for reasons that will be explained in a minute.)

::: {.runestone .explainer .ac_section}
::: {#ac18_3_1 component="activecode" question_label="16.3.1"}
::: {#ac18_3_1_question .ac_question}
:::
:::
:::

Now, we can pass the absolute function to sorted in order to specify
that we want the items sorted in order of their absolute value, rather
than in order of their actual value.

::: {.runestone .explainer .ac_section}
::: {#ac18_3_2 component="activecode" question_label="16.3.2"}
::: {#ac18_3_2_question .ac_question}
:::
:::
:::

What's really going on there? We've done something pretty strange.
Before, all the values we have passed as parameters have been pretty
easy to understand: numbers, strings, lists, Booleans, dictionaries.
Here we have passed a function object: absolute is a variable name whose
value is the function. When we pass that function object, it is *not*
automatically invoked. Instead, it is just bound to the formal parameter
key of the function sorted.

We are not going to look at the source code for the built-in function
sorted. But if we did, we would find somewhere in its code a parameter
named key with a default value of None. When a value is provided for
that parameter in an invocation of the function sorted, it has to be a
function. What the sorted function does is call that key function once
for each item in the list that's getting sorted. It associates the
result returned by that function (the absolute function in our case)
with the original value. Think of those associated values as being
little post-it notes that decorate the original values. The value 4 has
a post-it note that says 4 on it, but the value -2 has a post-it note
that says 2 on it. Then the sorted function rearranges the original
items in order of the values written on their associated post-it notes.

To illustrate that the absolute function is invoked once on each item,
during the execution of sorted, I have added some print statements into
the code.

::: {.runestone .explainer .ac_section}
::: {#ac18_3_3 component="activecode" question_label="16.3.3"}
::: {#ac18_3_3_question .ac_question}
:::
:::
:::

Note that this code never explicitly calls the absolute function at all.
It passes the absolute function as a parameter value to the sorted
function. Inside the sorted function, whose code we haven't seen, that
function gets invoked.

::: {.admonition .note}
Note

It is a little confusing that we are reusing the word *key* so many
times. The name of the optional parameter is `key`{.docutils .literal
.notranslate}. We will usually pass a parameter value using the keyword
parameter passing mechanism. When we write `key=some_function`{.docutils
.literal .notranslate} in the function invocation, the word key is there
because it is the name of the parameter, specified in the definition of
the sort function, not because we are using keyword-based parameter
passing.
:::

**Check Your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac18_3_4 component="activecode" question_label="16.3.4"}
::: {#ac18_3_4_question .ac_question}
**1.** You will be sorting the following list by each element's second
letter, a to z. Create a function to use when sorting, called
`second_let`{.docutils .literal .notranslate}. It will take a string as
input and return the second letter of that string. Then sort the list,
create a variable called `sorted_by_second_let`{.docutils .literal
.notranslate} and assign the sorted list to it. Do not use lambda.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac18_3_5 component="activecode" question_label="16.3.5"}
::: {#ac18_3_5_question .ac_question}
**2.** Below, we have provided a list of strings called `nums`{.docutils
.literal .notranslate}. Write a function called `last_char`{.docutils
.literal .notranslate} that takes a string as input, and returns only
its last character. Use this function to sort the list `nums`{.docutils
.literal .notranslate} by the last digit of each number, from highest to
lowest, and save this as a new list called `nums_sorted`{.docutils
.literal .notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac18_3_6 component="activecode" question_label="16.3.6"}
::: {#ac18_3_6_question .ac_question}
**3.** Once again, sort the list `nums`{.docutils .literal .notranslate}
based on the last digit of each number from highest to lowest. However,
now you should do so by writing a lambda function. Save the new list as
`nums_sorted_lambda`{.docutils .literal .notranslate}.
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

-   [[](Optionalreverseparameter.html)]{#relations-prev}
-   [[](SortingaDictionary.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
