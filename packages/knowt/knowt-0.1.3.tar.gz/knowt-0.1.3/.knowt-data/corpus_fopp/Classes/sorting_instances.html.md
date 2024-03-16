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
        Problem](/runestone/default/reportabug?course=fopp&page=sorting_instances)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [20.1 Introduction: Classes and Objects - the
        Basics](intro-ClassesandObjectstheBasics.html){.reference
        .internal}
    -   [20.2 Objects Revisited](ObjectsRevisited.html){.reference
        .internal}
    -   [20.3 User Defined Classes](UserDefinedClasses.html){.reference
        .internal}
    -   [20.4 Adding Parameters to the
        Constructor](ImprovingourConstructor.html){.reference .internal}
    -   [20.5 Adding Other Methods to a
        Class](AddingOtherMethodstoourClass.html){.reference .internal}
    -   [20.6 Objects as Arguments and
        Parameters](ObjectsasArgumentsandParameters.html){.reference
        .internal}
    -   [20.7 Converting an Object to a
        String](ConvertinganObjecttoaString.html){.reference .internal}
    -   [20.8 Instances as Return
        Values](InstancesasReturnValues.html){.reference .internal}
    -   [20.9 Sorting Lists of
        Instances](sorting_instances.html){.reference .internal}
    -   [20.10 Class Variables and Instance
        Variables](ClassVariablesInstanceVariables.html){.reference
        .internal}
    -   [20.11 Public and Private Instance
        Variables](PrivateInstanceVariables.html){.reference .internal}
    -   [20.12 Thinking About Classes and
        Instances](ThinkingAboutClasses.html){.reference .internal}
    -   [20.13 Testing classes](TestingClasses.html){.reference
        .internal}
    -   [20.14 A Tamagotchi Game](Tamagotchi.html){.reference .internal}
    -   [20.15 Class Decorators](ClassDecorators.html){.reference
        .internal}
    -   [20.16 Glossary](Glossary.html){.reference .internal}
    -   [20.17 Exercises](Exercises.html){.reference .internal}
    -   [20.18 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#sorting-lists-of-instances .section}
[]{#sort-instances-chap}

[20.9. ]{.section-number}Sorting Lists of Instances[¶](#sorting-lists-of-instances "Permalink to this heading"){.headerlink}
============================================================================================================================

You previously learned [[how to sort lists]{.std
.std-ref}](../Sorting/intro-SortingwithSortandSorted.html#sort-chap){.reference
.internal}. Sorting lists of instances of a class is fundamentally the
same as sorting lists of objects of any other type. There are two main
ways to sort lists of instances: (1) by providing a `key`{.docutils
.literal .notranslate} function as a parameter to `sorted()`{.docutils
.literal .notranslate} (or `.sort()`{.docutils .literal .notranslate})
or by (2) defining a "comparison operator" that determines how two
instances should be compared (specifically, given two instances, which
one should come first). We will describe both ways here.

::: {#approach-1-sorting-lists-of-instances-with-key .section}
[20.9.1. ]{.section-number}Approach 1: Sorting Lists of Instances with `key`{.docutils .literal .notranslate}[¶](#approach-1-sorting-lists-of-instances-with-key "Permalink to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Previously, you have seen how to provide such a function as input when
sorting lists of other kinds of objects. For example, given a list of
strings, you can sort them in ascending order of their lengths by
passing `len`{.docutils .literal .notranslate} as the key parameter.
Note that if you refer to a function by name, you give the name of the
function without parentheses after it, because you want the function
object itself. The sorted function will take care of calling the
function, passing the current item in the list. Thus, in the example
below, we write `key=len`{.docutils .literal .notranslate} and not
`key=len()`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#sort_instances_1 component="activecode" question_label="20.9.1.1"}
::: {#sort_instances_1_question .ac_question}
:::
:::
:::

When each of the items in a list is an instance of a class, the function
you pass for the key parameter takes one instance as an input and
returns a number. The instances will be sorted by their returned
numbers.

::: {.runestone .explainer .ac_section}
::: {#sort_instances_2 component="activecode" question_label="20.9.1.2"}
::: {#sort_instances_2_question .ac_question}
:::
:::
:::

Sometimes you will find it convenient to define a method for the class
that does some computation on the data in an instance. In this case, our
class is too simple to really illustrate that. But to simulate it, I've
defined a method `sort_priority`{.docutils .literal .notranslate} that
just returns the price that's stored in the instance. Now, that method,
sort\_priority takes one instance as input and returns a number. So it
is exactly the kind of function we need to provide as the key parameter
for sorted. Here it can get a little confusing: to refer to that method,
without actually invoking it, you can refer to
`Fruit.sort_priority`{.docutils .literal .notranslate}. This is
analogous to the code above that referred to `len`{.docutils .literal
.notranslate} rather than invoking `len()`{.docutils .literal
.notranslate}.

::: {.runestone .explainer .ac_section}
::: {#sort_instances_3 component="activecode" question_label="20.9.1.3"}
::: {#sort_instances_3_question .ac_question}
:::
:::
:::
:::

::: {#approach-2-defining-sort-orders-with-comparison-operators .section}
[20.9.2. ]{.section-number}Approach 2: Defining Sort Orders with Comparison Operators[¶](#approach-2-defining-sort-orders-with-comparison-operators "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Another approach to sorting lists of instances is to specify a
"comparison operator" for the class---a method that takes two instances
as arguments and "decides" which should come first. One advantage of
this approach is that you can call `sorted`{.docutils .literal
.notranslate} on a list of instances **without** specifying a value for
`key`{.docutils .literal .notranslate} and it will sort in the order you
defined.

To do this, we can define a method named `__lt__`{.docutils .literal
.notranslate} which stands for "less than". Note that this method starts
and ends with two underscores. This signifies that it is a special
method, just like `__init__`{.docutils .literal .notranslate} and
`__str__`{.docutils .literal .notranslate}. Our method,
`__lt__`{.docutils .literal .notranslate}, takes two instances as
arguments: `self`{.docutils .literal .notranslate} and an argument for
another instance. It returns `True`{.docutils .literal .notranslate} if
the `self`{.docutils .literal .notranslate} instance should come before
the other instance, and `False`{.docutils .literal .notranslate}
otherwise. Normally, `__lt__`{.docutils .literal .notranslate} is called
when we try to use the less than operator (`<`{.docutils .literal
.notranslate}) on class instances; Python translates the expression
`a < b`{.docutils .literal .notranslate} into `a.__lt__(b)`{.docutils
.literal .notranslate}. However, we can also use `__lt__`{.docutils
.literal .notranslate} to decide which of two instances should come
first in a sorted list. For example, if we wanted to sort instances of
`Fruit`{.docutils .literal .notranslate} by prices by default, we could
define `__lt__`{.docutils .literal .notranslate} as follows:

::: {.runestone .explainer .ac_section}
::: {#sort_instances_4 component="activecode" question_label="20.9.2.1"}
::: {#sort_instances_4_question .ac_question}
:::
:::
:::

When we call `sorted(L)`{.docutils .literal .notranslate} without
specifying a value for the `key`{.docutils .literal .notranslate}
parameter, it will sort the items in the list using the
`__lt__`{.docutils .literal .notranslate} method defined for the class
of items. `sorted()`{.docutils .literal .notranslate} will automatically
call the `__lt__`{.docutils .literal .notranslate} method, passing in
two instances from the list. Calling `__lt__`{.docutils .literal
.notranslate} when `self`{.docutils .literal .notranslate} is
`Fruit("Apple", 10)`{.docutils .literal .notranslate} and
`other`{.docutils .literal .notranslate} is
`Fruit("Cherry", 5)`{.docutils .literal .notranslate} returns
`False`{.docutils .literal .notranslate} (because the `price`{.docutils
.literal .notranslate} of the apple is not less than the price of the
cherry) so this means `Cherry`{.docutils .literal .notranslate} should
come before `Apple`{.docutils .literal .notranslate} in the sorted list.

If we wanted to sort by names, we could define `__lt__`{.docutils
.literal .notranslate} differently. *Note that when we call \`\`\<\`\`
on strings, it does an alphabetical comparison; \`\`"Apple" \<
"Cherry"\`\` is \`\`True\`\`. We can take advantage of this in our
\`\`\_\_lt\_\_\`\` method*:

::: {.runestone .explainer .ac_section}
::: {#sort_instances_5 component="activecode" question_label="20.9.2.2"}
::: {#sort_instances_5_question .ac_question}
:::
:::
:::

Finally, note that if we pass in a function for the `key`{.docutils
.literal .notranslate} parameter when we call `sorted()`{.docutils
.literal .notranslate} (approach 1), it will use that key function
instead of calling the `__lt__`{.docutils .literal .notranslate} method.
You can try putting a print statement inside the `__lt__`{.docutils
.literal .notranslate} method to see this for yourself: \_\_lt\_\_ will
not be called when you provide a key function but it will be called when
you don't provide a key function.
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

-   [[](InstancesasReturnValues.html)]{#relations-prev}
-   [[](ClassVariablesInstanceVariables.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
