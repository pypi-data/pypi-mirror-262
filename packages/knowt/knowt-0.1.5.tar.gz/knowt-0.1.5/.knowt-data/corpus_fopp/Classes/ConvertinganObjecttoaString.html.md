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
        Problem](/runestone/default/reportabug?course=fopp&page=ConvertinganObjecttoaString)
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
::: {#converting-an-object-to-a-string .section}
[20.7. ]{.section-number}Converting an Object to a String[¶](#converting-an-object-to-a-string "Permalink to this heading"){.headerlink}
========================================================================================================================================

When we're working with classes and objects, it is often necessary to
print an object (that is, to print the state of an object). Consider the
example below.

::: {.runestone .explainer .ac_section}
::: {#chp13_classesstr1 component="activecode" question_label="20.7.1"}
::: {#chp13_classesstr1_question .ac_question}
:::
:::
:::

The `print`{.docutils .literal .notranslate} function shown above
produces a string representation of the Point `p`{.docutils .literal
.notranslate}. The default functionality provided by Python tells you
that `p`{.docutils .literal .notranslate} is an object of type
`Point`{.docutils .literal .notranslate}. However, it does not tell you
anything about the specific state of the point.

We can improve on this representation if we include a special method
call `__str__`{.docutils .literal .notranslate}. Notice that this method
uses the same naming convention as the constructor, that is two
underscores before and after the name. It is common that Python uses
this naming technique for special methods.

The `__str__`{.docutils .literal .notranslate} method is responsible for
returning a string representation as defined by the class creator. In
other words, you as the programmer, get to choose what a
`Point`{.docutils .literal .notranslate} should look like when it gets
printed. In this case, we have decided that the string representation
will include the values of x and y as well as some identifying text. It
is required that the `__str__`{.docutils .literal .notranslate} method
create and *return* a string.

Whatever string the `__str__`{.docutils .literal .notranslate} method
for a class returns, that is the string that will print when you put any
instance of that class in a print statement. For that reason, the string
that a class's `__str__`{.docutils .literal .notranslate} method returns
should usually include values of instance variables. If a point has
`x`{.docutils .literal .notranslate} value 3 and `y`{.docutils .literal
.notranslate} value 4, but another point has `x`{.docutils .literal
.notranslate} value 5 and `y`{.docutils .literal .notranslate} value 9,
those two Point objects should probably look different when you print
them, right?

Take a look at the code below.

::: {.runestone .explainer .ac_section}
::: {#chp13_classesstr2 component="activecode" question_label="20.7.2"}
::: {#chp13_classesstr2_question .ac_question}
:::
:::
:::

When we run the program above you can see that the `print`{.docutils
.literal .notranslate} function now shows the string that we chose.

Now, you ask, don't we already have a `str`{.docutils .literal
.notranslate} type converter that can turn our object into a string? Yes
we do!

And doesn't `print`{.docutils .literal .notranslate} automatically use
this when printing things? Yes again!

However, as we saw earlier, these automatic mechanisms do not do exactly
what we want. Python provides many default implementations for methods
that we as programmers will probably want to change. When a programmer
changes the meaning of a method we say that we **override** the method.
Note also that the `str`{.docutils .literal .notranslate} type converter
function uses whatever `__str__`{.docutils .literal .notranslate} method
we provide.

**Check Your Understanding**

1.  Create a class called Cereal that accepts three inputs: 2 strings
    and 1 integer, and assigns them to 3 instance variables in the
    constructor: `name`{.docutils .literal .notranslate},
    `brand`{.docutils .literal .notranslate}, and `fiber`{.docutils
    .literal .notranslate}. When an instance of `Cereal`{.docutils
    .literal .notranslate} is printed, the user should see the
    following: "\[name\] cereal is produced by \[brand\] and has \[fiber
    integer\] grams of fiber in every serving!" To the variable name
    `c1`{.docutils .literal .notranslate}, assign an instance of
    `Cereal`{.docutils .literal .notranslate} whose name is
    `"Corn Flakes"`{.docutils .literal .notranslate}, brand is
    `"Kellogg's"`{.docutils .literal .notranslate}, and fiber is
    `2`{.docutils .literal .notranslate}. To the variable name
    `c2`{.docutils .literal .notranslate}, assign an instance of
    `Cereal`{.docutils .literal .notranslate} whose name is
    `"Honey Nut Cheerios"`{.docutils .literal .notranslate}, brand is
    `"General Mills"`{.docutils .literal .notranslate}, and fiber is
    `3`{.docutils .literal .notranslate}. Practice printing both!

::: {.runestone .explainer .ac_section}
::: {#ac_ch13_classstr_01 component="activecode" question_label="20.7.3"}
::: {#ac_ch13_classstr_01_question .ac_question}
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

-   [[](ObjectsasArgumentsandParameters.html)]{#relations-prev}
-   [[](InstancesasReturnValues.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
