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
        Problem](/runestone/default/reportabug?course=fopp&page=KnowyourerrorMessages)
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
::: {#know-your-error-messages .section}
[3.8. ]{.section-number}👩‍💻 Know Your Error Messages[¶](#know-your-error-messages "Permalink to this heading"){.headerlink}
===========================================================================================================================

Many problems in your program will lead to an error message. For example
as I was writing and testing this chapter of the book I wrote the
following version of the example program in the previous section.

::: {.highlight-python .notranslate}
::: {.highlight}
    current_time_str = input("What is the current time (in hours 0-23)?")
    wait_time_str = input("How many hours do you want to wait")

    current_time_int = int(current_time_str)
    wait_time_int = int(wait_time_int)

    final_time_int = current_time_int + wait_time_int
    print(final_time_int)
:::
:::

Can you see what is wrong, just by looking at the code? Maybe, maybe
not. Our brain tends to see what we think is there, so sometimes it is
very hard to find the problem just by looking at the code. Especially
when it is our own code and we are sure that we have done everything
right!

Let's try the program again, but this time in an activecode:

::: {.runestone .explainer .ac_section}
::: {#ac4_7_1 component="activecode" question_label="3.8.1"}
::: {#ac4_7_1_question .ac_question}
:::
:::
:::

Aha! Now we have an error message that might be useful. The name error
tells us that `wait_time_int`{.docutils .literal .notranslate} is not
defined. It also tells us that the error is on line 5. That's **really**
useful information. Now look at line five and you will see that
`wait_time_int`{.docutils .literal .notranslate} is used on both the
left and the right hand side of the assignment statement.

::: {.admonition .note}
Note

The error descriptions you see in activecode may be different (and more
understandable!) than in a regular Python interpreter. The interpreter
in activecode is limited in many ways, but it is intended for beginners,
including the wording chosen to describe errors.
:::

::: {.runestone}
-   [You cannot use a variable on both the left and right hand sides of
    an assignment statement.]{#question4_7_1_opt_a}
-   No, You can, as long as all the variables on the right hand side
    already have values.
-   [wait\_time\_int does not have a value so it cannot be used on the
    right hand side.]{#question4_7_1_opt_b}
-   Yes. Variables must already have values in order to be used on the
    right hand side.
-   [This is not really an error, Python is
    broken.]{#question4_7_1_opt_c}
-   No, No, No!
:::

In writing and using this book over the last few years we have collected
a lot of statistics about the programs in this book. Here are some
statistics about error messages for the exercises in this book.

[![](../_images/error_dist.png){.align-center}](../_images/error_dist.png){.reference
.internal .image-reference}

Most of the error messages encountered are SyntaxError, TypeError,
NameError, or ValueError. We will look at these errors in three stages:

-   First we will define what these four error messages mean.

-   Then, we will look at some examples that cause these errors to
    occur.

-   Finally we will look at ways to help uncover the root cause of these
    messages.

::: {#syntaxerror .section}
[3.8.1. ]{.section-number}SyntaxError[¶](#syntaxerror "Permalink to this heading"){.headerlink}
-----------------------------------------------------------------------------------------------

Syntax errors happen when you make an error in the syntax of your
program. Syntax errors are like making grammatical errors in writing. If
you don't use periods and commas in your writing then you are making it
hard for other readers to figure out what you are trying to say.
Similarly Python has certain grammatical rules that must be followed or
else Python can't figure out what you are trying to say.

Usually SyntaxErrors can be traced back to missing punctuation
characters, such as parentheses, quotation marks, or commas. Remember
that in Python commas are used to separate parameters to functions.
Paretheses must be balanced, or else Python thinks that you are trying
to include everything that follows as a parameter to some function.

Here are a couple examples of Syntax errors in the example program we
have been using. See if you can figure out what caused them.

::: {#db_tabs1 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac4_7_2 component="activecode" question_label="3.8.1.1"}
::: {#ac4_7_2_question .ac_question}
Find and fix the error in the following code.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.highlight-python .notranslate}
::: {.highlight}
    current_time_str = input("What is the current time (in hours 0-23)?")
    wait_time_str = input("How many hours do you want to wait"

    current_time_int = int(current_time_str)
    wait_time_int = int(wait_time_str)

    final_time_int = current_time_int + wait_time_int
    print(final_time_int)
:::
:::

Since the error message points us to line 4 this might be a bit
confusing. If you look at line four carefully you will see that there is
no problem with the syntax. So, in this case the next step should be to
back up and look at the previous line. In this case if you look at line
2 carefully you will see that there is a missing right parenthesis at
the end of the line. Remember that parentheses must be balanced. Since
Python allows statements to continue over multiple lines inside
parentheses python will continue to scan subsequent lines looking for
the balancing right parenthesis. However in this case it finds the name
`current_time_int`{.docutils .literal .notranslate} and it will want to
interpret that as another parameter to the input function. But, there is
not a comma to separate the previous string from the variable so as far
as Python is concerned the error here is a missing comma. From your
perspective its a missing parenthesis.
:::
:::

**Finding Clues** How can you help yourself find these problems? One
trick that can be very valuable in this situation is to simply start by
commenting out the line number that is flagged as having the error. If
you comment out line four, the error message now changes to point to
line 5. Now you ask yourself, am I really that bad that I have two lines
in a row that have errors on them? Maybe, so taken to the extreme, you
could comment out all of the remaining lines in the program. Now the
error message changes to
`TokenError: EOF in multi-line statement`{.docutils .literal
.notranslate} This is a very technical way of saying that Python got to
the end of file (EOF) while it was still looking for something. In this
case a right parenthesis.

::: {#db_tabs2 .alert .alert-warning component="tabbedStuff"}
::: {component="tab" tabname="Question"}
::: {.runestone .explainer .ac_section}
::: {#ac4_7_3 component="activecode" question_label="3.8.1.2"}
::: {#ac4_7_3_question .ac_question}
Find and fix the error in the following code.
:::
:::
:::
:::

::: {component="tab" tabname="Answer"}
::: {.highlight-python .notranslate}
::: {.highlight}
    current_time_str = input("What is the "current time" (in hours 0-23)?")
    wait_time_str = input("How many hours do you want to wait")

    current_time_int = int(current_time_str)
    wait_time_int = int(wait_time_str)

    final_time_int = current_time_int + wait_time_int
    print(final_time_int)
:::
:::

The error message points you to line 1 and in this case that is exactly
where the error occurs. In this case your biggest clue is to notice the
difference in highlighting on the line. Notice that the words "current
time" are a different color than those around them. Why is this? Because
"current time" is in double quotes inside another pair of double quotes
Python thinks that you are finishing off one string, then you have some
other names and finally another string. But you haven't separated these
names or strings by commas, and you haven't added them together with the
concatenation operator (+). So, there are several corrections you could
make. First you could make the argument to input be as follows:
`"What is the 'current time' (in hours 0-23) "`{.docutils .literal
.notranslate} Notice that here we have correctly used single quotes
inside double quotes . Another option is to simply remove the extra
double quotes. Why were you quoting "current time" anyway?
`"What is the current time (in hours 0-23)"`{.docutils .literal
.notranslate}
:::
:::

**Finding Clues** If you follow the same advice as for the last problem,
comment out line one, you will immediately get a different error
message. Here's where you need to be very careful and not panic. The
error message you get now is:
`NameError: name 'current_time_str' is not defined on line 4`{.docutils
.literal .notranslate}. You might be very tempted to think that this is
somehow related to the earlier problem and immediately conclude that
there is something wrong with the variable name
`current_time_str`{.docutils .literal .notranslate} but if you reflect
for a minute you will see that by commenting out line one you have
caused a new and unrelated error. That is you have commented out the
creation of the name `current_time_str`{.docutils .literal
.notranslate}. So of course when you want to convert it to an
`int`{.docutils .literal .notranslate} you will get the NameError. Yes,
this can be confusing, but it will become much easier with experience.
It's also important to keep calm, and evaluate each new clue carefully
so you don't waste time chasing problems that are not really there.

Uncomment line 1 and you are back to the SyntaxError. Another track is
to eliminate a possible source of error. Rather than commenting out the
entire line you might just try to assign `current_time_str`{.docutils
.literal .notranslate} to a constant value. For example you might make
line one look like this:
`current_time_str = "10"  #input("What is the "current time" (in hours 0-23)?")`{.docutils
.literal .notranslate}. Now you have assigned
`current_time_str`{.docutils .literal .notranslate} to the string 10,
and commented out the input statement. And now the program works! So you
conclude that the problem must have something to do with the input
function.
:::

::: {#typeerror .section}
[3.8.2. ]{.section-number}TypeError[¶](#typeerror "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------

TypeErrors occur when you try to combine two objects that are not
compatible. For example you try to add together an integer and a string.
Usually type errors can be isolated to lines that are using mathematical
operators, and usually the line number given by the error message is an
accurate indication of the line.

Here's an example of a type error created by a Polish learner. See if
you can find and fix the error.

::: {.runestone .explainer .ac_section}
::: {#ac4_7_4 component="activecode" question_label="3.8.2.1"}
::: {#ac4_7_4_question .ac_question}
:::
:::
:::

::: {#dbex4_rev .runestone component="reveal" showtitle="Show me the Solution" hidetitle="Hide" style="visibility: hidden;"}
::: {.admonition-solution .admonition}
Solution

In finding this error there are few lessons to think about. First, you
may find it very disconcerting that you cannot understand the whole
program. Unless you speak Polish then this won't be an issue. But,
learning what you can ignore, and what you need to focus on is a very
important part of the debugging process. Second, types and good variable
names are important and can be very helpful. In this case a and x are
not particularly helpful names, and in particular they do not help you
think about the types of your variables, which as the error message
implies is the root of the problem here. The rest of the lessons we will
get back to in a minute.

The error message provided to you gives you a pretty big hint.
`TypeError: unsupported operand type(s) for FloorDiv: 'str' and 'number' on line: 5`{.docutils
.literal .notranslate} On line five we are trying to use integer
division on x and 24. The error message tells you that you are tyring to
divide a string by a number. In this case you know that 24 is a number
so x must be a string. But how? You can see the function call on line 3
where you are converting x to an integer. `int(x)`{.docutils .literal
.notranslate} or so you think. This is lesson three and is one of the
most common errors we see in introductory programming. What is the
difference between `int(x)`{.docutils .literal .notranslate} and
`x = int(x)`{.docutils .literal .notranslate}

-   The expression `int(x)`{.docutils .literal .notranslate} converts
    the string referenced by x to an integer but it does not store it
    anywhere. It is very common to assume that `int(x)`{.docutils
    .literal .notranslate} somehow changes x itself, as that is what you
    are intending! The thing that makes this very tricky is that
    `int(x)`{.docutils .literal .notranslate} is a valid expression, so
    it doesn't cause any kind of error, but rather the error happens
    later on in the program.

-   The assignment statement `x = int(x)`{.docutils .literal
    .notranslate} is very different. Again, the `int(x)`{.docutils
    .literal .notranslate} expression converts the string referenced by
    x to an integer, but this time it also changes what x references so
    that x now refers to the integer value returned by the
    `int`{.docutils .literal .notranslate} function.

So, the solution to this problem is to change lines 3 and 4 so they are
assignment statements.
:::
:::

**Finding Clues** One thing that can help you in this situation is to
print out the values and the types of the variables involved in the
statement that is causing the error. You might try adding a print
statement after line 4 `print(x, type(x))`{.docutils .literal
.notranslate} You will see that at least we have confirmed that x is of
type string. Now you need to start to work backward through the program.
You need to ask yourself, where is x used in the program? x is used on
lines 2, 3, and of course 5 and 6 (where we are getting an error). So
maybe you move the print statement to be after line 2 and again after 3.
Line 3 is where you expect the value of x to be changed to an integer.
Could line 4 be mysteriously changing x back to a string? Not very
likely. So the value and type of x is just what you would expect it to
be after line 2, but not after line 3. This helps you isolate the
problem to line 3. In fact if you employ one of our earlier techniques
of commenting out line 3 you will see that this has no impact on the
error, and is a big clue that line 3 as it is currently written is
useless.
:::

::: {#nameerror .section}
[3.8.3. ]{.section-number}NameError[¶](#nameerror "Permalink to this heading"){.headerlink}
-------------------------------------------------------------------------------------------

Name errors almost always mean that you have used a variable before it
has a value. Often NameErrors are simply caused by typos in your code.
They can be hard to spot if you don't have a good eye for catching
spelling mistakes. Other times you may simply mis-remember the name of a
variable or even a function you want to call. You have seen one example
of a NameError at the beginning of this section. Here is another one.
See if you can get this program to run successfully:

::: {.runestone .explainer .ac_section}
::: {#ac4_7_5 component="activecode" question_label="3.8.3.1"}
::: {#ac4_7_5_question .ac_question}
:::
:::
:::

::: {#db_ex5_reveal .runestone component="reveal" showtitle="Show me the Solution" hidetitle="Hide" style="visibility: hidden;"}
::: {.admonition-solution .admonition}
Solution

In this example, the student seems to be a fairly bad speller, as there
are a number of typos to fix. The first one is identified as wait\_time
is not defined on line 6. Now in this example you can see that there is
`str_wait_time`{.docutils .literal .notranslate} on line 2, and
`wai_time`{.docutils .literal .notranslate} on line 4 and
`wait_time`{.docutils .literal .notranslate} on line 6. If you do not
have very sharp eyes its easy to miss that there is a typo on line 4.
:::
:::

**Finding Clues** With name errors one of the best things you can do is
use the editor, or browser search function. Quite often if you search
for the exact word in the error message one of two things will happen:

1\. The word you are searching for will appear only once in your code,
it's also likely that it will be on the right hand side of an assignment
statement, or as a parameter to a function. That should confirm for you
that you have a typo somewhere. If the name in question **is** what you
thought it should be then you probably have a typo on the left hand side
of an assignment statement on a line before your error message occurs.
Start looking backward at your assignment statements. In some cases it's
really nice to leave all the highlighted strings from the search
function visible as they will help you very quickly find a line where
you might have expected your variable to be highlighted.

2\. The second thing that may happen is that you will be looking
directly at a line where you expected the search to find the string in
question, but it will not be highlighted. Most often that will be the
typo right there.

Here is another one for you to try:

::: {.runestone .explainer .ac_section}
::: {#ac4_7_6 component="activecode" question_label="3.8.3.2"}
::: {#ac4_7_6_question .ac_question}
:::
:::
:::

::: {#db_ex6_reveal .runestone component="reveal" showtitle="Show me the Solution" hidetitle="Hide" style="visibility: hidden;"}
::: {.admonition-solution .admonition}
Solution

This one is once again a typo, but the typo is not in a variable name,
but rather, the name of a function. The search strategy would help you
with this one easily, but there is another clue for you as well. The
editor in the textbook, as well as almost all Python editors in the
world provide you with color clues. Notice that on line 2 the function
`imt`{.docutils .literal .notranslate} is not highlighted blue like the
word `int`{.docutils .literal .notranslate} on line 4.
:::
:::

And one last bit of code to fix.

::: {.runestone .explainer .ac_section}
::: {#ac4_7_7 component="activecode" question_label="3.8.3.3"}
::: {#ac4_7_7_question .ac_question}
:::
:::
:::

::: {#db_ex7_reveal .runestone component="reveal" showtitle="Show me the Solution" hidetitle="Hide" style="visibility: hidden;"}
::: {.admonition-solution .admonition}
Solution

In this example the error message is about `set_time`{.docutils .literal
.notranslate} not defined on line 3. In this case the undefined name is
not used in an assignment statement, but is used as a parameter
(incorrectly) to a function call. A search on `set_time`{.docutils
.literal .notranslate} reveals that in fact it is only used once in the
program. Did the author mean `set_alarm`{.docutils .literal
.notranslate}? If we make that assumption we immediately get another
error `NameError: name 'alarm_time' is not defined on line: 3`{.docutils
.literal .notranslate}. The variable `alarm_time`{.docutils .literal
.notranslate} is defined on line 4, but that does not help us on line 3.
Furthermore we now have to ask the question is this function call
`int(present_time, set_alarm, alarm_time)`{.docutils .literal
.notranslate} even the correct use of the `int`{.docutils .literal
.notranslate} function? The answer to that is a resounding no. Let's
list all of the things wrong with line 3:

1.  `set_time`{.docutils .literal .notranslate} is not defined and never
    used, the author probably meant `set_alarm`{.docutils .literal
    .notranslate}.

2.  `alarm_time`{.docutils .literal .notranslate} cannot be used as a
    parameter before it is defined, even on the next line!

3.  `int`{.docutils .literal .notranslate} can only convert one string
    to an integer at a time.

4.  Finally, `int`{.docutils .literal .notranslate} should be used in an
    assignment statement. Even if `int`{.docutils .literal .notranslate}
    was called with the correct number of parameters it would have no
    real effect.
:::
:::
:::

::: {#valueerror .section}
[3.8.4. ]{.section-number}ValueError[¶](#valueerror "Permalink to this heading"){.headerlink}
---------------------------------------------------------------------------------------------

Value errors occur when you pass a parameter to a function and the
function is expecting a certain limitations on the values, and the value
passed is not compatible. We can illustrate that with this particular
program in two different ways.

::: {.runestone .explainer .ac_section}
::: {#ac4_7_8 component="activecode" question_label="3.8.4.1"}
::: {#ac4_7_8_question .ac_question}
:::
:::
:::

Run the program but instead of typing in anything to the dialog box just
click OK. You should see the following error message:
`ValueError: invalid literal for int() with base 10: '' on line: 4`{.docutils
.literal .notranslate} This error is not because you have made a mistake
in your program. Although sometimes we do want to check the user input
to make sure its valid, but we don't have all the tools we need for that
yet. The error happens because the user did not give us something we can
convert to an integer, instead we gave it an empty string. Try running
the program again. Now this time enter "ten" instead of the number 10.
You will get a similar error message.

ValueErrors are not always caused by user input error, but in this
program that is the case. We'll look again at ValueErrors again when we
get to more complicated programs. For now it is worth repeating that you
need to keep track of the restrictions needed for your variables, and
understand what your function is expecting. You can do this by writing
comments in your code, or by naming your variables in a way that reminds
you of their proper form.
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

-   [[](SemanticErrors.html)]{#relations-prev}
-   [[](Exercises.html)]{#relations-next}
:::

::: {.container}
[]{#numuserspan}[]{.loggedinuser} \| [Back to top](#)

© Copyright 2017 bradleymiller. Created using
[Runestone](http://runestoneinteractive.org/) 7.2.10.
:::
