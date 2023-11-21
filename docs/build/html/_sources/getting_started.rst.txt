Getting Started
===============

Introduction
------------

Welcome to **Stream Tool**, a Python package for creating a customizable website
for with custom macros. With Stream Tool, you can easily build a website, create
pages, and add buttons with various functionalities, including integration with
OBS using websockets.

Before getting started make sure you have Stream Tool :doc:`installed <installing>`.

Although all the commands are written for the console in this tutorial,
I recommend following along in a script. You can put ``build_and_run`` at
the end of your script and run at any point to see your progress. You
can also use ``print()`` commands to see what the attributes return. This
is because of an issue with running ``build_and_run`` in the console
multiple times which is explained in the footnote to the :ref:`Running
the Website <running the website>` section.

Importing
---------

Make sure Stream Tool is imported. You can import the whole library
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

Running the Website
--------------------
When you want to see the current state of the site or are ready to use it you
should run the method ``build_and_run`` from your Website.

.. code-block:: python

    >>> my_site.build_and_run()
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

Running this starts the server on your local machine on port 5000. This site
can be accessed on that machine at http://127.0.0.1:5000.

The console will tell you this as well. It will also provide a warning about this
being a development server. That is just fine for this use which is intended to only
be used within your local network.

You can press CTRL + C to stop the server.

You may get an error when running this saying that the port is already in use. In that
case you'll have to use the following code to specify a different port than
the default ``5000``.

The server can also be made available to other machines on the local network
and on a different port using arguments or keyword arguments. Host is the first
argument and ``'0.0.0.0'`` is the host to set to to have this available on the
local network. The port is the second argument and can be any valid integer port.

.. code-block:: python

    # Using arguments
    >>> my_site.build_and_run('0.0.0.0', 6050)
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:6050
     * Running on http://192.168.86.124:6050
    Press CTRL+C to quit

    # Using keyword arguments
    >>> my_site.build_and_run(port=6050, host='0.0.0.0')
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:6050
     * Running on http://192.168.86.124:6050
    Press CTRL+C to quit

You can do this at any time during the tutorial to see what it currently looks
like or at the end of a script [1]_ .

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

The page ``name`` is what will be used as the url for the page. Since page names cannot have a space in them
it will replace it with a dash when it's set. We can check this by looking at the pages url or name.

.. code-block:: python

    >>> volume_page.url
    '/Volume-Page'
    >>> volume_page.name
    'Volume-Page'

Adding Buttons
--------------

Buttons can be added to pages to perform various actions. Now, let's
add a new button to our page. It has one required argument of a name
for the button. Adding a button returns an instance of the
``Button`` class:

.. code-block:: python

    >>> my_button = volume_page.add_button("My Button")

Customizing Buttons
-------------------

We can change the attributes of our already created button to change its text
or functionality.

We can change the text the button says by assigning to the ``text`` parameter.
If no text is provided in the initializing of the button the ``text`` is set to the
``name``.

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

    >>> def print_hello():
    ...     print("Hello, world!")

    >>> my_print_button = volume_page.add_button("Print Hello")
    >>> my_print_button.button_function = print_hello

Adding Buttons With Functionality or Links
-------------------------------------------

All the attributes discussed above are also keyword arguments of the ``add_button``
function: ``text``, ``button_link``, ``button_function``.

Using the arguments we can add a button with specific text and a link to
our other Volume page. Let's put this on the index page so we have a way to
get there:

.. code-block:: python

    >>> link = volume_page.url
    >>> my_index_page.add_button("btn1",
    ...                          text="volume",
    ...                          button_link=link)

We can also add another button to use our previous function, but this time
on the index page (it's important that every page can say 'Hello, Word!'):

.. code-block:: python

    >>> my_index_page.add_button("Print Hello Again",
    ...                          button_function=print_hello)

Adding OBS Websockets Integration
---------------------------------

If you want to integrate with OBS using websockets, you first need to setup
the connection and authentication information. There are 3 variables in
``Websockets_Auth`` for this: ``websocket_host``, ``websocket_port``,
``websocket_password``.

These need to be configured with what you have setup in OBS.

If you are running the webserver from the same machine as OBS than the
host will be the ``'localhost'`` or ``'127.0.0.1'``. If it is running on a different
machine then the one running the web server that machines IP address will
be used. This is a string.

If it is running on the same machine the port will be the one that OBS says
websockets is using. If it is not the same machine it will also be the same
port unless there is port forwarding on that computer. (The firewall may
need to be opened up if using a different machine for the web server
and OBS)

The port is an integer.

The password is the one set in OBS. It is a string.

.. code-block:: python

    >>> Websockets_Auth.websocket_host = "your_host"
    >>> Websockets_Auth.websocket_port = "your_port"
    >>> Websockets_Auth.websocket_password = "your_password"


You will also need to enable the use of OBS websockets when creating your
website. Make sure the authentication is setup before you create the website because
this is when the connection will be made.

.. code-block:: python

    >>> obs_site = create_website(use_obs_websockets=True)

Buttons can then be linked to OBS actions. For example, let's create a button to increase the volume of
an audio input by 6 dB:

.. code-block:: python

    >>> my_obs_button = volume_page.add_button(
    ...     "Change Volume",
    ...     button_function=builtin_obs_actions.change_volume,
    ...     button_function_args=('your_input_name', 6))

We pass the function we want to run into ``button_function`` and if there are any arguments for that
function it goes in order as a list into ``button_function_args``.

``change_volume`` takes 2 arguments, the audio input to change and the amount of dB to change
it by.

Remember to replace ``'your_input_name'`` with the actual name of the input in your OBS configuration.

There are other functions in ``builtin_obs_actions`` that can be used in the same fashion. There's
a list in the API documentation :ref:`here<obs functions>`.

What Have We Got?
--------------------
If you've followed along through the whole tutorial you have a lot of
buttons now and 2 pages. Let's run it and see what we've got!

.. code-block:: python

    >>> my_site.build_and_run("0.0.0.0")
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on all addresses (0.0.0.0)
     * Running on http://127.0.0.1:5000
     * Running on http://xxx.xxx.xxx.xxx:5000
    Press CTRL+C to quit

If we visit the site (either one) that shows up in the console, we can see our index
page with wonderful links to Google and our Volume page as well as a button
to say 'Hello, world!'

If we go to the volume page we have a button to go
back to the index, one that does nothing, one to adjust the volume of a source
in obs, and one to say 'Hello, world!'

You can even try checking it out on another device. Take out your phone
and if its on the same network try going to the second address shown in
the console. You should be able to control all the same things from your phone
or any other device on the network!

------------------------------------------

Congrats! You made it through the tutorial... or skimmed it...
or skipped to the end.

No matter how you got here, for more information on everything,
refer to the official Stream Tool :doc:`API <api>` documentation.

But we don't have to stop the learning yet, we can also do some
more advanced macros, :doc:`let's try that<advanced_use>`!

------------------------------------------

.. [1] It is known that running ``build_and_run`` more than once in the console
   causes an error. If you intend on running it more than once, you should work
   through this tutorial in a script and have the ``build_and_run`` command at the end:

   .. code-block:: python

       from stream_tool import create_website

       my_site = create_website()
       my_page = my_site.add_page("page")
       my_button = my_page.add_button("button")

       my_site.build_and_run()


