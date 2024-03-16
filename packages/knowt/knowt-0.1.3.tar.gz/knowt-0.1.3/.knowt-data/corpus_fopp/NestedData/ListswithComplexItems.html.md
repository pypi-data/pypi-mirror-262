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
        Problem](/runestone/default/reportabug?course=fopp&page=ListswithComplexItems)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [17.1 Introduction: Nested Data and Nested
        Iteration](ListswithComplexItems.html){.reference .internal}
    -   [17.2 Nested Dictionaries](NestedDictionaries.html){.reference
        .internal}
    -   [17.3 Processing JSON results](jsonlib.html){.reference
        .internal}
    -   [17.4 Nested Iteration](NestedIteration.html){.reference
        .internal}
    -   [17.5 👩‍💻 Structuring Nested
        Data](WPStructuringNestedData.html){.reference .internal}
    -   [17.6 Deep and Shallow
        Copies](DeepandShallowCopies.html){.reference .internal}
    -   [17.7 👩‍💻 Extracting from Nested
        Data](WPExtractFromNestedData.html){.reference .internal}
    -   [17.8 Exercises](Exercises.html){.reference .internal}
    -   [17.9 Chapter Assessment](ChapterAssessment.html){.reference
        .internal}
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

::: {#introduction-nested-data-and-nested-iteration .section}
[]{#nested-chap}

[17.1. ]{.section-number}Introduction: Nested Data and Nested Iteration[¶](#introduction-nested-data-and-nested-iteration "Permalink to this heading"){.headerlink}
===================================================================================================================================================================

::: {#lists-with-complex-items .section}
[17.1.1. ]{.section-number}Lists with Complex Items[¶](#lists-with-complex-items "Permalink to this heading"){.headerlink}
--------------------------------------------------------------------------------------------------------------------------

The lists we have seen so far have had numbers or strings as items.
We've snuck in a few more complex items, but without ever explicitly
discussing what it meant to have more complex items.

In fact, the items in a list can be any type of python object. For
example, we can have a list of lists.

::: {.runestone .explainer .ac_section}
::: {#ac17_1_1 component="activecode" question_label="17.1.1.1"}
::: {#ac17_1_1_question .ac_question}
:::
:::
:::

Line 2 prints out the first item from the list that `nested1`{.docutils
.literal .notranslate} is bound to. That item is itself a list, so it
prints out with square brackets. It has length 3, which prints out on
line 3. Line 4 adds a new item to `nested1`{.docutils .literal
.notranslate}. It is a list with one element, 'i' (it a list with one
element, it's not just the string 'i').

Codelens gives a you a reference diagram, a visual display of the
contents of nested1.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="17.1.1.2"}
::: {#clens_1_1_question .ac_question}
:::

::: {#clens_1_1 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 17.1.1.2 (clens\_1\_1)]{.runestone_caption_text}
:::
:::

When you get to step 4 of the execution, take a look at the object that
variable nested1 points to. It is a list of three items, numbered 0, 1,
and 2. The item in slot 1 is small enough that it is shown right there
as a list containing items "d" and "e". The item in slot 0 didn't quite
fit, so it is shown in the figure as a pointer to another separate list;
same thing for the item in slot 2, the list `['f', 'g', 'h']`{.docutils
.literal .notranslate}.

There's no special meaning to whether the list is shown embedded or with
a pointer to it: that's just CodeLens making the best use of space that
it can. In fact, if you go on to step 5, you'll see that, with the
addition of a fourth item, the list \['i'\], CodeLens has chosen to show
all four lists embedded in the top-level list.

With a nested list, you can make complex expressions to get or set a
value in a sub-list.

::: {.runestone .explainer .ac_section}
::: {#ac17_1_2 component="activecode" question_label="17.1.1.3"}
::: {#ac17_1_2_question .ac_question}
:::
:::
:::

Lines 1-4 above probably look pretty natural to you. Line 5 illustrates
the left to right processing of expressions. `nested1[1]`{.docutils
.literal .notranslate} evaluates to the second inner list, so
`nested1[1][1]`{.docutils .literal .notranslate} evaluates to its second
element, `'e'`{.docutils .literal .notranslate}. Line 6 is just a
reminder that you index into a literal list, one that is written out,
the same way as you can index into a list referred to by a variable.
`[10, 20, 30]`{.docutils .literal .notranslate} creates a list.
`[1]`{.docutils .literal .notranslate} indexes into that list, pulling
out the second item, 20.

Just as with a function call where the return value can be thought of as
replacing the text of the function call in an expression, you can
evaluate an expression like that in line 7 from left to right. Because
the value of `nested1[1]`{.docutils .literal .notranslate} is the list
`['d', 'e']`{.docutils .literal .notranslate}, `nested1[1][0]`{.docutils
.literal .notranslate} is the same as `['d', 'e'][0]`{.docutils .literal
.notranslate}. So line 7 is equivalent to lines 2 and 4; it is a simpler
way of pulling out the first item from the second list.

At first, expressions like that on line 7 may look foreign. They will
soon feel more natural, and you will end up using them a lot. Once you
are comfortable with them, the only time you will write code like lines
2-4 is when you aren't quite sure what your data's structure is, and so
you need to incrementally write and debug your code. Often, you will
start by writing code like lines 2-4, then, once you're sure it's
working, replace it with something like line 7.

You can change values in such lists in the usual ways. You can even use
complex expressions to change values. Consider the following

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="17.1.1.4"}
::: {#clens_1_2_question .ac_question}
:::

::: {#clens_1_2 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 17.1.1.4 (clens\_1\_2)]{.runestone_caption_text}
:::
:::

The complex items in a list do not have to be lists. They can be tuples
or dictionaries. The items in a list do not all have to be the same
type, but you will drive yourself crazy if you have lists of objects of
varying types. Save yourself some headaches and don't do that. Here's a
list of dictionaries and some operations on them. Take a look at its
visual representation in codelens.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="17.1.1.5"}
::: {#clens_1_3_question .ac_question}
:::

::: {#clens_1_3 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 17.1.1.5 (clens\_1\_3)]{.runestone_caption_text}
:::
:::

Try practicing some operations to get or set values in a list of
dictionaries.

::: {.runestone .explainer .ac_section}
::: {#ac17_1_3 component="activecode" question_label="17.1.1.6"}
::: {#ac17_1_3_question .ac_question}
:::
:::
:::

You can even have a list of functions (!).

::: {.runestone .explainer .ac_section}
::: {#ac17_1_4 component="activecode" question_label="17.1.1.7"}
::: {#ac17_1_4_question .ac_question}
:::
:::
:::

Here, L is a list with three items. All those items are functions. The
first is the function square that is defined on lines 1 and 2. The
second is the built-in python function abs. The third is an anonymous
function that returns one more than its input.

In the first for loop, we do not call the functions, we just output
their printed representations. The output \<function square\> confirms
that square truly is a function object. For some reason, in our online
environment, it's not able to produce a nice printed representation of
the built-in function abs, so it just outputs \<unknown\>

In the second for loop, we call each of the functions, passing in the
value -2 each time and printing whatever value the function returns.

The last two lines just emphasize that there's nothing special about
lists of functions. They follow all the same rules for how python treats
any other list. Because L\[0\] picks out the function square, L\[0\](3)
calls the function square, passing it the parameter 3.

Step through it in Codelens if that's not all clear to you yet.

::: {.runestone .codelens}
::: {.cd_section component="codelens" question_label="17.1.1.8"}
::: {#clens_1_4_question .ac_question}
:::

::: {#clens_1_4 .pytutorVisualizer params="{\"embeddedMode\": true, \"lang\": \"python\", \"jumpToEnd\": false}"}
:::

[Activity: CodeLens 17.1.1.8 (clens\_1\_4)]{.runestone_caption_text}
:::
:::

**Check Your Understanding**

::: {.runestone .explainer .ac_section}
::: {#ac17_1_5 component="activecode" question_label="17.1.1.9"}
::: {#ac17_1_5_question .ac_question}
**1.** Below, we have provided a list of lists. Use indexing to assign
the element 'horse' to the variable name `idx1`{.docutils .literal
.notranslate}.
:::
:::
:::

::: {.runestone .explainer .ac_section}
::: {#ac17_1_6 component="activecode" question_label="17.1.1.10"}
::: {#ac17_1_6_question .ac_question}
**2.** Using indexing, retrieve the string 'willow' from the list and
assign that to the variable `plant`{.docutils .literal .notranslate}.
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

-   [[](toctree.html)]{#relations-prev}
-   [[](NestedDictionaries.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
