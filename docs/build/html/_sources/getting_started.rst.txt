Getting Started
===============

Introduction
------------

Welcome to **Stream Tool**, a Python package that simplifies the
process of creating a customizable website for creating macros.
With Stream Tool, you can easily build a website, create pages, and
add buttons with various functionalities, including integration with
OBS using websockets.

Before getting started make sure you have Stream Tool :doc:`installed <installing>`.

Importing
---------

Make sure Stream Tool is imported into the script. You can import the whole library
or just specific modules and functions.

.. code-block:: python

    >>> from stream_tool import *

For this tutorial we'll only need the ``create_website`` function, ``builtin_obs_actions``, and
``Websockets_Auth`` so we can just import those to keep the namespace clean.

.. code-block:: python

    >>> from stream_tool import create_website, builtin_obs_actions, Websockets_Auth

Creating a Basic Website
------------------------

With Stream Tool imported, to get started, use the ``create_website`` function to create a basic website:

.. code-block:: python

    >>> my_site = create_website()

This returns an instance of the class ``Website`` and assigns it to the variable my_site.

That instance will have an empty website with a blank index page.

Using The Index Page
--------------------

We can access and store the saved index page by pulling it from the attribute ``Website.index_page``.

.. code-block:: python

    >>> my_index_page = my_site.index_page

Adding Pages
------------

Now, let's create a new page for our website. Creating a page requires
a name to be specified as the first argument. The name will be used in the
link to the page. Creating a page returns an instance of the ``Page`` class.

.. code-block:: python

    >>> volume_page = my_site.add_page("My Page")

Customizing Pages
-----------------

Oh wait! That's not a very cool page name, let's pick a new one. We can change the name at any time
with the ``Page.name`` attribute.

.. code-block:: python

    >>> volume_page.name = "Volume Page"

The page name is what will be used as the url for the page. Since page names cannot have a space in them
it will replace it with a dash when it's set. We can check this by looking at the pages url or name.

.. code-block:: python

    >>> volume_page.url
    '/Volume-Page'
    >>> volume_page.name
    'Volume-Page'

Adding Buttons
--------------

Buttons can be added to pages to perform various actions. Now, let's
add a new page to our website. It has one required argument of a name
for the button. Adding a button returns an instance of the
``Button`` class:

.. code-block:: python

    >>> my_button = volume_page.add_button("My Button")

Customizing Buttons
-------------------

We can change the attributes of our already created button to change its text
or functionality.

We can change the text the button says by assigning the text parameter.
If no text is provided in the initializing of the button the text is set to the
name.

.. code-block:: python

    >>> my_button.text
    'My Button'


Let's change the button to say "Volume Up". We can change the name while we are at it,
but that isn't really used for anything we'll see.

.. code-block:: python

    >>> my_button.text = "Volume Up"
    >>> my_button.name = "better name"

The name is formatted similarly to the page names, except it removes spaces
and adjusts cases.

    >>> my_button.name
    'BetterName'

Making Buttons Functional
-------------------------

Let's add a button with a link to another page. We can edit the ``button_link``
attribute of the button. This can be a link to another page or a relative
link to this site.

Here's how we'll add a button and have it link to the index page:

.. code-block:: python

    >>> index_link_button = volume_page.add_button("Index")
    >>> index_link_button.button_link = my_index_page.url

This is how we could add a button to link to an external site. Let's try
adding it to the index page.

.. code-block::

    >>> ext_link_button = my_index_page.add_button("Google")
    >>> ext_link_button.button_link = "https://www.google.com"

We can also have the button press execute a python function. Here's one that
would print text on the button press. We have to define a function and then
set the attribute ``button_function`` to that function.

.. code-block:: python

    # Add a button on "My Page" with a Python print function
    >>> def print_hello():
    ...     print("Hello, world!")
    ...
    >>> my_print_button = my_page.add_button("Print Hello")
    >>> my_print_button.button_function = print_hello

Adding Buttons With Functionality or Links
-------------------------------------------

All the attributes discussed above are also keyword arguments of the add_button
function: ``text``, ``button_link``, ``button_function``.

Using the arguments we can add a button with specific text and a link to
github.com

.. code-block:: python

    >>> link = "https://www.github.com"
    >>> my_index_page.add_button("btn1",
    ...                          text="github",
    ...                          button_link=link)

We can also add another button to use our previous function. We'll put this one
on the index page.

.. code-block:: python

    >>> my_index_page.add_button("Go to index",
    ...                          button_function=print_hello)

Adding OBS Websockets Integration
---------------------------------

If you want to integrate with OBS using websockets, you can enable it when creating the website:

.. code-block:: python

    # Create a website with OBS websockets integration
    obs_site = create_website(use_obs_websockets=True)

Buttons can then be linked to OBS actions. For example, let's create a button to change the volume:

.. code-block:: python

    # Add a button on "My Page" to change the volume in OBS
    my_obs_button = my_page.create_button("Change Volume",
    ...                                   button_function=builtin_obs_actions.change_volume,
    ...                                   input_name="your_input_name",
    ...                                   amount=6)

Remember to replace ``"your_input_name"`` with the actual name of the input in your OBS configuration.

There are other functions in ``builtin_obs_actions`` that can be used in the same fashion. There's
a list in the API documentation :ref:`here<obs_functions_section>`.

------------------------------------------

For more information on everything, refer to the official Stream Tool :doc:`API <api>` documentation.


We can also do some more advanced OBS Websocket macros, :doc:`let's try that<advanced_use>`!

