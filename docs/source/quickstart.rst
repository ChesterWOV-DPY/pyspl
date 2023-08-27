Quickstart
==========

.. note::

   This is a quick guide for beginners to start using **PySPL**. For the full API documentation, see the section :doc:`api`.

Installation
------------
To use **PySPL**, first install it using ``pip``:

.. code-block:: console

   (.venv) $ pip install pyspl


Getting Started
---------------
.. code-block:: python

   import pyspl

First enter this piece of code shown above. You import the module using this.

If you wish, you can shorten more of the module name by using ``import pyspl as spl``. Well, don't complain "the name is too long".
I could've named it "python_shakespeare_programming_langauge". ;)

Then enter:

.. code-block:: python

   hamlet = pyspl.Character('Hamlet', 'a male.')
   juliet = pyspl.Character('Juliet', 'a female.')

   play = pyspl.Play()
   play.add_characters(hamlet, juliet)

   class ActI(rspl.Act):
      @rspl.scene('I', 'The Only Scene.')
      def sceneI(self):
         play.enter(hamlet, juliet)
         play.set(juliet, pyspl.sum(64, 8))
         play.print(juliet, str)
         play.set(hamlet, pyspl.sum(juliet.value, pyspl.sum(32, 1)))
         play.print(hamlet, str)

   play.add_act(ActI(), 'I', 'The Only Act.')
         
We added two characters to the program, then written a program to print Hi.

Then add:

.. code-block:: python

   play.save('./play.spl')

You should then run the following command in your terminal/command prompt (if you haven't yet):

.. tabs::

   .. group-tab:: Unix (Mac/Linux)

      .. code-block:: console

         $ git clone https://github.com/zmbc/shakespearelang && pip install ./shakespearelang

   .. group-tab:: Windows

      .. code-block:: console

         > git clone https://github.com/zmbc/shakespearelang && pip install .\shakespearelang

That should install the latest version of `zmbc's SPL interpreter <https://github.com/zmbc/shakespearelang>`_, which is written 
in Python. 

You can then run your SPL play by using the following command in your console:

.. tabs::

   .. group-tab:: Unix (Mac/Linux)

      .. code-block:: console

         $ shakespeare run ./play.spl

   .. group-tab:: Windows

      .. code-block:: console

         > shakespeare run .\play.spl


If it doesn't work, using the following command might work:

.. tabs::

   .. group-tab:: Unix (Mac/Linux)

      .. code-block:: console

         $ python -m shakespeare run ./play.spl

   .. group-tab:: Windows

      .. code-block:: console

         > py -m shakespeare run .\play.spl

