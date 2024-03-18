Glossary
--------

member function:
   A function that operates on an object that is passed as an implicit
   parameter named ``this``.

nonmember function:
   A function that is not a member of any structure definition. Also
   called a “free-standing” function.

invoke:
   To call a function “on” an object, in order to pass the object as an
   implicit parameter.

current object:
   The object on which a member function is invoked. Inside the member
   function, we can refer to the current object implicitly, or by using
   the keyword ``this``.

this:
   A keyword that refers to the current object. ``this`` is a pointer,
   which makes it difficult to use, since we do not cover pointers in
   this book.

interface:
   A description of how a function is used, including the number and
   types of the parameters and the type of the return value.

function declaration:
   A statement that declares the interface to a function without
   providing the body. Declarations of member functions appear inside
   structure definitions even if the definitions appear outside.

implementation:
   The body of a function, or the details of how a function works.

constructor:
   A special function that initializes the instance variables of a
   newly-created object.

.. dragndrop:: glossary11_1
    :feedback: Try again!
    :match_1: member function|||A function that operates on an object that is passed as an implicit parameter named "this".
    :match_2: nonmember function|||A free-standing function that is not part of any structure definition.
    :match_3: current object|||The object on which a member function is invoked.

    Match the vocabulary word with its definition.

.. dragndrop:: glossary11_2
    :feedback: Try again!
    :match_1: invoke|||To call a function “on” an object.
    :match_2: this|||A keyword that refers to the current object.
    :match_3: interface|||A description of how a function is used.

    Match the vocabulary word with its definition.

.. dragndrop:: glossary11_3
    :feedback: Try again!
    :match_1: function declaration|||A statement that declares the interface to a function without providing the body.
    :match_2: implementation|||The body of a function, or the details of how a function works.
    :match_3: constructor|||A special function that initializes the instance variables of a newly-created object.

    Match the vocabulary word with its definition.