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
        Problem](/runestone/default/reportabug?course=fopp&page=intro-HowtobeaSuccessfulProgrammer)
-   

```{=html}
<!-- -->
```
-   
-   [This Chapter](../index.html){.dropdown-toggle}
    -   [3.1 Introduction to
        Debugging](intro-DebuggingGeneral.html){.reference .internal}
    -   [3.2 👩‍💻 Programming in the Real
        World](intro-HowtobeaSuccessfulProgrammer.html){.reference
        .internal}
    -   [3.4 👩‍💻 Beginning tips for
        Debugging](BeginningtipsforDebugging.html){.reference .internal}
    -   [3.5 Syntax errors](Syntaxerrors.html){.reference .internal}
    -   [3.6 Runtime Errors](RuntimeErrors.html){.reference .internal}
    -   [3.7 Semantic Errors](SemanticErrors.html){.reference .internal}
    -   [3.8 👩‍💻 Know Your Error
        Messages](KnowyourerrorMessages.html){.reference .internal}
    -   [3.9 Exercises](Exercises.html){.reference .internal}
-   
-   
:::
:::
:::

::: {#continue-reading .container}
:::

::: {#main-content .container role="main"}
::: {#programming-in-the-real-world .section}
[]{#index-0}

[3.2. ]{.section-number}👩‍💻 Programming in the Real World[¶](#programming-in-the-real-world "Permalink to this heading"){.headerlink}
=====================================================================================================================================

Before we dive into the nitty gritty details of debugging, here is a
video to give you a flavor for what its like to be a programmer in the
real world.

::: {.runestone style="margin-left: auto; margin-right:auto"}
::: {#goog_waymo_swes .align-left .youtube-video component="youtube" video-height="315" question_label="3.2.1" video-width="560" video-videoid="Os5YyfTjM20" video-divid="goog_waymo_swes" video-start="0" video-end="-1"}
:::
:::
:::

::: {#debugging .section}
[3.3. ]{.section-number}👩‍💻 Debugging[¶](#debugging "Permalink to this heading"){.headerlink}
=============================================================================================

Programming is a complex process. Since it is done by human beings,
errors may often occur. Programming errors are called **bugs** and the
process of tracking them down and correcting them is called
**debugging**. Some claim that in 1945, a dead moth caused a problem on
relay number 70, panel F, of one of the first computers at Harvard, and
the term **bug** has remained in use since. For more about this historic
event, see [first
bug](http://en.wikipedia.org/wiki/File:H96566k.jpg){.reference
.external}.

One of the most important skills you need to acquire to complete this
book successfully is the ability to debug your programs. Debugging might
be the most under-appreciated, and under-taught, skill in introductory
computer science. For that reason we are introducing a series of
"debugging interludes." Debugging is a skill that you need to master
over time, and some of the tips and tricks are specific to different
aspects of Python programming. So look for additional Way of the
Programmer interludes throughout the rest of this book.

Programming is an odd thing in a way. Here is why. As programmers we
spend 99% of our time trying to get our program to work. We struggle, we
stress, we spend hours deep in frustration trying to get our program to
execute correctly. Then when we do get it going we celebrate, hand it
in, and move on to the next homework assignment or programming task. But
here is the secret, when you are successful, you are happy, your brain
releases a bit of chemical that makes you feel good. You need to
organize your programming so that you have lots of little successess. It
turns out your brain doesn't care all that much if you have successfully
written hello world, or a fast fourier transform (trust me its hard) you
still get that little release that makes you happy. When you are happy
you want to go on and solve the next little problem. Essentially I'm
telling you once again, start small, get something small working, and
then add to it.

::: {#how-to-avoid-debugging .section}
[3.3.1. ]{.section-number}How to Avoid Debugging[¶](#how-to-avoid-debugging "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------------------------------

Perhaps the most important lesson in debugging is that it is **largely
avoidable** -- if you work carefully.

1.  **Understand the Problem** You must have a firm grasp on **what**
    you are trying to accomplish but not necessarily **how** to do it.
    You do not need to understand the entire problem. But you must
    understand at least a portion of it and what the program should do
    in a specific circumstance -- what output should be produced for
    some given input. This will allow you to test your progress. You can
    then identify if a solution is correct or whether there remains work
    to do or bugs to fix. This is probably the single biggest piece of
    advice for programmers at every level.

2.  **Start Small** It is tempting to sit down and crank out an entire
    program at once. But, when the program -- inevitably -- does not
    work, you have a myriad of options for things that might be wrong.
    Where to start? Where to look first? How to figure out what went
    wrong? I'll get to that in the next section. So, start with
    something really small. Maybe just two lines and then make sure that
    runs. Hitting the run button is quick and easy. It gives you
    immediate feedback about whether what you have just done works or
    not. Another immediate benefit of having something small working is
    that you have something to turn in. Turning in a small, incomplete
    program, is almost always better than nothing.

3.  **Keep Improving It** Once you have a small part of your program
    working, the next step is to figure out something small to add to it
    -- how can you move closer to a correct solution. As you add to your
    program, you gain greater insight into the underlying problem you
    are trying to solve.

    If you keep adding small pieces of the program one at a time, it is
    much easier to figure out what went wrong. (This of course means you
    must be able to recognize if there is an error. And that is done
    through testing.)

    As long as you always test each new bit of code, it is most likely
    that any error is in the new code you have just added. Less new code
    means its easier to figure out where the problem is.

This notion of **Get something working and keep improving it** is a
mantra that you can repeat throughout your career as a programmer. It's
a great way to avoid the frustrations mentioned above. Think of it this
way. Every time you have a little success, your brain releases a tiny
bit of chemical that makes you happy. So, you can keep yourself happy
and make programming more enjoyable by creating lots of small victories
for yourself.

::: {.admonition .note}
Note

The technique of start small and keep improving is the basis of
**Agile** software development. This practice is used widely in the
industry.
:::

Ok, lets look at an example. Lets solve the problem posed in question 3
at the end of the Simple Python Data chapter. Ask the user for the time
now (in hours 0 -- 23), and ask for the number of hours to wait. Your
program should output what the time will be on the clock when the alarm
goes off.

So, where to start? The problem requires two pieces of input from the
user, so lets start there and make sure we can get the data we need.

::: {.runestone .explainer .ac_section}
::: {#db_ex3_1 component="activecode" question_label="3.3.1.1"}
::: {#db_ex3_1_question .ac_question}
:::
:::
:::

If you haven't yet, click Run: get in the habit of checking whether
small things are working before you go on.

So far so good. Now lets take the next step. We need to figure out what
the time will be after waiting `wait_time`{.docutils .literal
.notranslate} number of hours. A good first approximation to that is to
simply add `wait_time`{.docutils .literal .notranslate} to
`current_time`{.docutils .literal .notranslate} and print out the
result. So lets try that.

::: {.runestone .explainer .ac_section}
::: {#db_ex3_2 component="activecode" question_label="3.3.1.2"}
::: {#db_ex3_2_question .ac_question}
:::
:::
:::

Hmm, when you run that example you see that something funny has
happened.

::: {.runestone}
-   [Python is stupid and does not know how to add
    properly.]{#db_q_ex3_1_opt_a}
-   No, Python is probabaly not broken.
-   [There is nothing wrong here.]{#db_q_ex3_1_opt_b}
-   No, try adding the two numbers together yourself, you will
    definitely get a different result.
-   [Python is doing string concatenation, not integer
    addition.]{#db_q_ex3_1_opt_c}
-   Yes! Remember that input returns a string. Now we will need to
    convert the string to an integer
:::

This error was probably pretty simple to spot, because we printed out
the value of `final_time`{.docutils .literal .notranslate} and it is
easy to see that the numbers were just concatenated together rather than
added. So what do we do about the problem? We will need to convert both
`current_time`{.docutils .literal .notranslate} and
`wait_time`{.docutils .literal .notranslate} to `int`{.docutils .literal
.notranslate}. At this stage of your programming development, it can be
a good idea to include the type of the variable in the variable name
itself. So lets look at another iteration of the program that does that,
and the conversion to integer.

::: {.runestone .explainer .ac_section}
::: {#db_ex3_3 component="activecode" question_label="3.3.1.4"}
::: {#db_ex3_3_question .ac_question}
:::
:::
:::

Now, that's a lot better, and in fact depending on the hours you chose,
it may be exactly right. If you entered 8 for the current time and 5 for
the wait time then 13 is correct. But if you entered 17 (5pm) for the
hours and 9 for the wait time then the result of 26 is not correct. This
illustrates an important aspect of **testing**, which is that it is
important to test your code on a range of inputs. It is especially
important to test your code on **boundary conditions**. In this case you
would want to test your program for hours including 0, 23, and some in
between. You would want to test your wait times for 0, and some really
large numbers. What about negative numbers? Negative numbers don't make
sense, but since we don't really have the tools to deal with telling the
user when something is wrong we will not worry about that just yet.

So finally we need to account for those numbers that are bigger than 23.
For this we will need one final step, using the modulo operator.

::: {.runestone .explainer .ac_section}
::: {#db_ex3_4 component="activecode" question_label="3.3.1.5"}
::: {#db_ex3_4_question .ac_question}
:::
:::
:::

Of course even in this simple progression, there are other ways you
could have gone astray. We'll look at some of those and how you track
them down in the next section.

**Check your understanding**

::: {.runestone}
-   [tracking down programming errors and correcting
    them.]{#question4_1_1_opt_a}
-   Programming errors are called bugs and the process of finding and
    removing them from a program is called debugging.
-   [removing all the bugs from your house.]{#question4_1_1_opt_b}
-   Maybe, but that is not what we are talking about in this context.
-   [finding all the bugs in the program.]{#question4_1_1_opt_c}
-   This is partially correct. But, debugging is more than just finding
    the bugs. What do you need to do once you find them?
-   [fixing the bugs in the program.]{#question4_1_1_opt_d}
-   This is partially correct. But, debugging is more than just fixing
    the bugs. What do you need to do before you can fix them?
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

-   [[](intro-DebuggingGeneral.html)]{#relations-prev}
-   [[](BeginningtipsforDebugging.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
