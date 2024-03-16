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
        Problem](/runestone/default/reportabug?course=fopp&page=listenerLoop)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [14.1 Introduction](intro-indefiniteiteration.html){.reference
        .internal}
    -   [14.2 The while Statement](ThewhileStatement.html){.reference
        .internal}
    -   [14.3 The Listener Loop](listenerLoop.html){.reference
        .internal}
    -   [14.4 Randomly Walking
        Turtles](RandomlyWalkingTurtles.html){.reference .internal}
    -   [14.5 Break and Continue](BreakandContinue.html){.reference
        .internal}
    -   [14.6 👩‍💻 Infinite Loops](WPInfiniteLoops.html){.reference
        .internal}
    -   [14.7 Exercises](Exercises.html){.reference .internal}
    -   [14.8 Chapter Assessment](ChapterAssessment.html){.reference
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

::: {#the-listener-loop .section}
[]{#listener-loop}[]{#index-0}

[14.3. ]{.section-number}The Listener Loop[¶](#the-listener-loop "Permalink to this heading"){.headerlink}
==========================================================================================================

At the end of the previous section, we advised using a for loop whenever
it will be known at the beginning of the iteration process how many
times the block of code needs to be executed. Usually, in python, you
will use a for loop rather than a while loop. When is it *not* known at
the beginning of the iteration how many times the code block needs to be
executed? The answer is, when it depends on something that happens
during the execution.

One very common pattern is called a **listener loop**. Inside the while
loop there is a function call to get user input. The loop repeats
indefinitely, until a particular input is received.

::: {.runestone .explainer .ac_section}
::: {#ac14_3_1 component="activecode" question_label="14.3.1"}
::: {#ac14_3_1_question .ac_question}
:::
:::
:::

This is just our old friend, the accumulation pattern, adding each
additional output to the sum-so-far, which is stored in a variable
called theSum and reassigned to that variable on each iteration. Notice
that theSum is initialized to 0. Also notice that we had to initialize
x, our variable that stores each input that the user types, before the
while loop. This is typical with while loops, and makes them a little
tricky to read and write. We had to initialize it because the condition
`x != 0`{.docutils .literal .notranslate} is checked at the very
beginning, before the code block is ever executed. In this case, we
picked an initial value that we knew would make the condition true, to
ensure that the while loop's code block would execute at least once.

If you're at all unsure about how that code works, try adding print
statements inside the while loop that print out the values of x and
theSum.

::: {#other-uses-of-while .section}
[14.3.1. ]{.section-number}Other uses of `while`{.docutils .literal .notranslate}[¶](#other-uses-of-while "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------------------------------------

::: {#sentinel-values .section}
### [14.3.1.1. ]{.section-number}Sentinel Values[¶](#sentinel-values "Permalink to this heading"){.headerlink}

Indefinite loops are much more common in the real world than definite
loops.

-   If you are selling tickets to an event, you don't know in advance
    how many tickets you will sell. You keep selling tickets as long as
    people come to the door and there's room in the hall.

-   When the baggage crew unloads a plane, they don't know in advance
    how many suitcases there are. They just keep unloading while there
    are bags left in the cargo hold. (Why *your* suitcase is always the
    last one is an entirely different problem.)

-   When you go through the checkout line at the grocery, the clerks
    don't know in advance how many items there are. They just keep
    ringing up items as long as there are more on the conveyor belt.

Let's implement the last of these in Python, by asking the user for
prices and keeping a running total and count of items. When the last
item is entered, the program gives the grand total, number of items, and
average price. We'll need these variables:

-   `total`{.docutils .literal .notranslate} - this will start at zero

-   `count`{.docutils .literal .notranslate} - the number of items,
    which also starts at zero

-   `moreItems`{.docutils .literal .notranslate} - a boolean that tells
    us whether more items are waiting; this starts as True

The pseudocode (code written half in English, half in Python) for the
body of the loop looks something like this:

::: {.highlight-default .notranslate}
::: {.highlight}
    while moreItems
        ask for price
        add price to total
        add one to count
:::
:::

This pseudocode has no option to set `moreItems`{.docutils .literal
.notranslate} to `False`{.docutils .literal .notranslate}, so it would
run forever. In a grocery store, there's a little plastic bar that you
put after your last item to separate your groceries from those of the
person behind you; that's how the clerk knows you have no more items. We
don't have a "little plastic bar" data type in Python, so we'll do the
next best thing: we will use a `price`{.docutils .literal .notranslate}
of zero to mean "this is my last item." In this program, zero is a
**sentinel value**, a value used to signal the end of the loop. Here's
the code:

::: {.runestone .explainer .ac_section}
::: {#ac14_3_2 component="activecode" question_label="14.3.1.1.1"}
::: {#ac14_3_2_question .ac_question}
:::
:::
:::

There are still a few problems with this program.

-   If you enter a negative number, it will be added to the total and
    count. Modify the code so that negative numbers give an error
    message instead (but don't end the loop) Hint: `elif`{.docutils
    .literal .notranslate} is your friend.

-   If you enter zero the first time you are asked for a price, the loop
    will end, and the program will try to divide by zero. Use an
    `if`{.docutils .literal .notranslate}/`else`{.docutils .literal
    .notranslate} statement outside the loop to avoid the division by
    zero and tell the user that you can't compute an average without
    data.

-   This program doesn't display the amounts to two decimal places.
    You'll be introduced to that in another chapter.
:::

::: {#validating-input .section}
### [14.3.1.2. ]{.section-number}Validating Input[¶](#validating-input "Permalink to this heading"){.headerlink}

You can also use a `while`{.docutils .literal .notranslate} loop when
you want to **validate** input; when you want to make sure the user has
entered valid input for a prompt. Let's say you want a function that
asks a yes-or-no question. In this case, you want to make sure that the
person using your program enters either a Y for yes or N for no (in
either upper or lower case). Here is a program that uses a
`while`{.docutils .literal .notranslate} loop to keep asking until it
receives a valid answer. As a preview of coming attractions, it uses the
`upper()`{.docutils .literal .notranslate} method which is described in
String Methods to convert a string to upper case. When you run the
following code, try typing something other than Y or N to see how the
code reacts:

::: {.runestone .explainer .ac_section}
::: {#ac14_3_3 component="activecode" question_label="14.3.1.2.1"}
::: {#ac14_3_3_question .ac_question}
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

-   [[](ThewhileStatement.html)]{#relations-prev}
-   [[](RandomlyWalkingTurtles.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
