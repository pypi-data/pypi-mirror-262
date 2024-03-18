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
        Problem](/runestone/default/reportabug?course=fopp&page=ThinkingAboutClasses)
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
::: {#thinking-about-classes-and-instances .section}
[]{#thinking-about-classes}

[20.12. ]{.section-number}Thinking About Classes and Instances[¶](#thinking-about-classes-and-instances "Permalink to this heading"){.headerlink}
=================================================================================================================================================

You can now imagine some reasons you may want to define a class. You
have seen examples of creating types that are more complicated or
specific than the ones built in to Python (like lists or strings).
`Turtle`{.docutils .literal .notranslate}, with all the instance
variables and methods you learned about using earlier in the semester,
is a class that programmers defined which is now included in the Python
language. In this chapter, we defined `Point`{.docutils .literal
.notranslate} with some functionality that can make it easier to write
programs that involve `x,y`{.docutils .literal .notranslate} coordinate
`Point`{.docutils .literal .notranslate} instances. And shortly, you'll
see how you can define classes to represent objects in a game.

You can also use self-defined classes to hold data -- for example, data
you get from making a request to a REST API.

Before you decide to define a new class, there are a few things to keep
in mind, and questions you should ask yourself:

-   **What is the data that you want to deal with?** (Data about a bunch
    of songs from iTunes? Data about a bunch of tweets from Twitter?
    Data about a bunch of hashtag searches on Twitter? Two numbers that
    represent coordinates of a point on a 2-dimensional plane?)

-   **What will one instance of your class represent?** In other words,
    which sort of new *thing* in your program should have fancy
    functionality? One song? One hashtag? One tweet? One point? The
    answer to this question should help you decide what to call the
    class you define.

-   **What information should each instance have as instance
    variables?** This is related to what an instance represents. See if
    you can make it into a sentence. *"Each instance represents one \<
    song \> and each \< song \> has an \< artist \> and a \< title \> as
    instance variables."* Or, *"Each instance represents a \< Tweet \>
    and each \< Tweet \> has a \< user (who posted it) \> and \< a
    message content string \> as instance variables."*

-   **What instance methods should each instance have?** What should
    each instance be able to *do*? To continue using the same examples:
    Maybe each song has a method that uses a lyrics API to get a long
    string of its lyrics. Maybe each song has a method that returns a
    string of its artist's name. Or for a tweet, maybe each tweet has a
    method that returns the length of the tweet's message. (Go wild!)

-   **What should the printed version of an instance look like?** (This
    question will help you determine how to write the
    `__str__`{.docutils .literal .notranslate} method.) Maybe, "Each
    song printed out will show the song title and the artist's name." or
    "Each Tweet printed out will show the username of the person who
    posted it and the message content of the tweet."

After considering those questions and making decisions about how you're
going to get started with a class definition, you can begin to define
your class.

Remember that a class definition, like a function definition, is a
general description of what *every instance of the class should have*.
(Every Point has an `x`{.docutils .literal .notranslate} and a
`y`{.docutils .literal .notranslate}.) The class instances are specific:
e.g. the Point with *a specific x and y \>.* You might have a Point with
an `x`{.docutils .literal .notranslate} value of 3 and a `y`{.docutils
.literal .notranslate} value of 2, so for that particular *instance* of
the *class* `Point`{.docutils .literal .notranslate}, you'd pass in
`3`{.docutils .literal .notranslate} and `2`{.docutils .literal
.notranslate} to the constructor, the `__init__`{.docutils .literal
.notranslate} method, like so: `new_point = Point(3,2)`{.docutils
.literal .notranslate}, as you saw in the last sections.
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

-   [[](PrivateInstanceVariables.html)]{#relations-prev}
-   [[](TestingClasses.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
