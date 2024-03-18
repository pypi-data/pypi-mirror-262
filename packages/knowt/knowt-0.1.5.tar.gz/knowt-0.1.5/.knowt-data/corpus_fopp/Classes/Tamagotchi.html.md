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
        Problem](/runestone/default/reportabug?course=fopp&page=Tamagotchi)
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
[]{#tamagotchi-chap .target}

::: {#a-tamagotchi-game .section}
[]{#index-0}

[20.14. ]{.section-number}A Tamagotchi Game[¶](#a-tamagotchi-game "Permalink to this heading"){.headerlink}
===========================================================================================================

There are also a lot of interesting ways to put user-defined classes to
use that don't involve data from the internet. Let's pull all these
mechanics together in a slightly more interesting way than we got with
the Point class. Remember
[Tamagotchis](https://en.wikipedia.org/wiki/Tamagotchi){.reference
.external}, the little electronic pets? As time passed, they would get
hungry or bored. You had to clean up after them or they would get sick.
And you did it all with a few buttons on the device.

We are going to make a simplified, text-based version of that. In your
problem set and in the chapter on [[Inheritance]{.std
.std-ref}](../Inheritance/intro.html#inheritance-chap){.reference
.internal} we will extend this further.

First, let's start with a class `Pet`{.docutils .literal .notranslate}. Each instance of the class will be one electronic pet for the user to take care of. Each instance will have a current state, consisting of three instance variables:

:   -   hunger, an integer

    -   boredom, an integer

    -   sounds, a list of strings, each a word that the pet has been
        taught to say

In the `__init__`{.docutils .literal .notranslate} method, hunger and
boredom are initialized to random values between 0 and the threshold for
being hungry or bored. The `sounds`{.docutils .literal .notranslate}
instance variable is initialized to be a copy of the class variable with
the same name. The reason we make a copy of the list is that we will
perform destructive operations (appending new sounds to the list). If we
didn't make a copy, then those destructive operations would affect the
list that the class variable points to, and thus teaching a sound to any
of the pets would teach it to all instances of the class!

There is a `clock_tick`{.docutils .literal .notranslate} method which
just increments the boredom and hunger instance variables, simulating
the idea that as time passes, the pet gets more bored and hungry.

The `__str__`{.docutils .literal .notranslate} method produces a string
representation of the pet's current state, notably whether it is bored
or hungry or whether it is happy. It's bored if the boredom instance
variable is larger than the threshold, which is set as a class variable.

To relieve boredom, the pet owner can either teach the pet a new word,
using the `teach()`{.docutils .literal .notranslate} method, or interact
with the pet, using the `hi()`{.docutils .literal .notranslate} method.
In response to `teach()`{.docutils .literal .notranslate}, the pet adds
the new word to its list of words. In response to the `hi()`{.docutils
.literal .notranslate} method, it prints out one of the words it knows,
randomly picking one from its list of known words. Both `hi()`{.docutils
.literal .notranslate} and `teach()`{.docutils .literal .notranslate}
cause an invocation of the `reduce_boredom()`{.docutils .literal
.notranslate} method. It decrements the boredom state by an amount that
it reads from the class variable `boredom_decrement`{.docutils .literal
.notranslate}. The boredom state can never go below `0`{.docutils
.literal .notranslate}.

To relieve hunger, we call the `feed()`{.docutils .literal .notranslate}
method.

::: {.runestone .explainer .ac_section}
::: {#tamagotchi_1 component="activecode" question_label="20.14.1"}
::: {#tamagotchi_1_question .ac_question}
:::
:::
:::

Let's try making a pet and playing with it a little. Add some of your
own commands, too, and keep printing `p1`{.docutils .literal
.notranslate} to see what the effects are. If you want to directly
inspect the state, try printing `p1.boredom`{.docutils .literal
.notranslate} or `p1.hunger`{.docutils .literal .notranslate}.

::: {.runestone .explainer .ac_section}
::: {#tamagotchi_2_copy component="activecode" question_label="20.14.2"}
::: {#tamagotchi_2_copy_question .ac_question}
:::
:::
:::

That's all great if you want to interact with the pet by writing python
code. Let's make a game that non-programmers can play.

We will use the [[Listener Loop]{.std
.std-ref}](../MoreAboutIteration/listenerLoop.html#listener-loop){.reference
.internal} pattern. At each iteration, we will display a text prompt
reminding the user of what commands are available.

The user will have a list of pets, each with a name. The user can issue
a command to adopt a new pet, which will create a new instance of Pet.
Or the user can interact with an existing pet, with a Greet, Teach, or
Feed command.

No matter what the user does, with each command entered, the clock ticks
for all their pets. Watch out, if you have too many pets, you won't be
able to keep them all satisfied!

::: {.runestone .explainer .ac_section}
::: {#tamogotchi_3 component="activecode" question_label="20.14.3"}
::: {#tamogotchi_3_question .ac_question}
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

-   [[](TestingClasses.html)]{#relations-prev}
-   [[](ClassDecorators.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
