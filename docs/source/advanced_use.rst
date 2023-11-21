Advanced Uses
==============

More advanced customized OBS integrations can be
created as well as other more advanced Macros.

We'll look at three examples in this tutorial. (1) Using
``obs-websocket-py`` to create OBS macros that aren't available
in ``builtin-obs-functions``. (2) Creating reusable functions to
assign to a button and supplying arguments and keyword arguments
for those. (3) Creating an advanced macro using other python
libraries.

Other OBS Functions
--------------------

For this tutorial let's make a button that will either fade or cut
to a scene depending on which scene it's currently on. Let's also
make sure it sets the transition back to whatever it was when the
button was pressed.

To follow along you'll want to have OBS running in studio mode with
a scene collection with three scenes and OBS WebSocket running. It's
helpful to have a color source in each to tell them apart. I'll name
mine ``scene 1``, ``scene 2``, and ``scene 3`` and use those names
in the tutorial.

You can use any module of your choice to interface with OBS
websockets, but I'll walk through using ``obs-websocket-py`` because
its the one used by this library and so it is already installed and an object
for interfacing will already be created.

First make sure we import the necessary module from ``obs-websocket-py``

.. code-block:: python

    >>> from obswebsocket import requests

Then after we've created a website that is using OBS websockets let's
save the web socket manager object ``ws`` for interfacing with the websocket. Make sure you set
the :ref:`connection and authentication info<adding obs websockets integration>` if you need to.

.. code-block:: python

    >>> from stream_tool import create_website
    >>> my_site = create_website(use_obs_websockets=True)
    >>> ws = my_site.ws


We'll define a function for making the macro.

Following the `documentation`__ for ``obs-websocket-py`` we can use the
call method on our web socket manager ``ws`` to send a method from the requests class, like this:

__ https://github.com/Elektordi/obs-websocket-py/blob/master/README.md

.. code-block:: python

    >>> def switch_to_scene1():
    >>>      ws.call(requests.SetCurrentPreviewScene(
    ...         sceneName="scene 1"))

The name of the method to run on requests and the keyword arguments for
that method are taken from the ``obs-websocket`` `documentation`__.

__ https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#requests

You can see how setCurrentPreviewScene has one field named "sceneName" that
takes a string in that request's `documentation`__.

__ https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#setcurrentpreviewscene

We can set the scene and run the transition in the same fashion using the requests
from ``obs-websocket`` SetCurrentSceneTransition_ and TriggerStudioModeTransition_:

.. _SetCurrentSceneTransition: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#setcurrentscenetransition

.. _TriggerStudioModeTransition: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#triggerstudiomodetransition

.. code-block:: python

    >>> def switch_to_scene1():
    >>>     transition = "Fade"
    >>>     ws.call(requests.SetCurrentPreviewScene(
    ...         sceneName="scene 1"))
    >>>     ws.call(requests.SetCurrentSceneTransition(
    ...         transitionName=transition))
    >>>     ws.call(requests.TriggerStudioModeTransition())

In order to make it so we do a different transition based on what
scene is currently active we have to get data from the OBS
and save it. We'll use GetCurrentProgramScene_ and we'll assign what
it returns to ``response``:

.. _GetCurrentProgramScene: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#getcurrentprogramscene

.. code-block:: python

    >>> response = ws.call(requests.GetCurrentProgramScene())

From the ``response`` object we'll read its dictionary ``datain``.
This dictionary will have the names of the response fields as keys
and the values will be the associated response data. In this case the key is
``'currentProgramSceneName'`` and it will hold a string with the name
of the current scene in program. We'll save it like this:

.. code-block:: python

    >>> current_scene_name = response.datain['currentProgramSceneName']

I currently have ``'scene 2'`` in program so if I check it's value we'll
see it says that:

.. code-block:: python

    >>> current_scene_name
    scene 2

Let's add that into our function with some logic to fade if we are
currently on scene 2 and cut if we are currently on scene 3:

.. code-block:: python

    >>> def switch_to_scene1():
    >>>     response = ws.call(requests.GetCurrentProgramScene())
    >>>     current_scene_name = response.datain['currentProgramSceneName']
    >>>     if current_scene_name == "scene 2":
    >>>         transition = "Fade"
    >>>     elif current_scene_name == "scene 3":
    >>>         transition = "Cut"
    >>>     ws.call(requests.SetCurrentPreviewScene(
    ...         sceneName="scene 1"))
    >>>     ws.call(requests.SetCurrentSceneTransition(
    ...         transitionName=transition))
    >>>     ws.call(requests.TriggerStudioModeTransition())

Let's make sure that whatever the transition was set to when
the button was pressed it is set to again. We don't want to mess
anyone up by suddenly changing the scene transition. We'll do this similarly to how we
got the current scene, using GetCurrentSceneTransition_ and
SetCurrentSceneTransition_.

.. _GetCurrentSceneTransition: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#getcurrentscenetransition

.. _SetCurrentSceneTransition: https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#setcurrentscenetransition

Let's also add in handling for the case where a different scene is in
program, like scene 1. There also needs to be a bit of time between running
the transition and setting it back if the transition takes time (like a fade).
This is because if we change the transition instantly, it'll stop running the
current transition.

.. code-block:: python

    >>> import time
    >>> def switch_to_scene1():
    >>>     response = ws.call(requests.GetCurrentSceneTransition())
    >>>     start_transition = response.datain['transitionName']
    >>>     response = ws.call(requests.GetCurrentProgramScene())
    >>>     current_scene_name = response.datain['currentProgramSceneName']
    >>>     if current_scene_name == "scene 2":
    >>>         transition = "Fade"
    >>>     elif current_scene_name == "scene 3":
    >>>         transition = "Cut"
    >>>     else:
    >>>         return
    >>>     ws.call(requests.SetCurrentPreviewScene(
    ...         sceneName="scene 1"))
    >>>     ws.call(requests.SetCurrentSceneTransition(
    ...         transitionName=transition))
    >>>     ws.call(requests.TriggerStudioModeTransition())
    >>>     if transition == "Fade":
    >>>         time.sleep(.5)
    >>>     ws.call(requests.SetCurrentSceneTransition(
    ...         transitionName=start_transition))

Now if we create a button on the index page to do this, attach
this function to it and run the site we can see what happens:

.. code-block:: python

    >>> my_site.index_page.add_button(
    ...     "Scene 1",
    ...     button_function=switch_to_scene1)
    >>> my_site.build_and_run()
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

If we set the scene to scene 2 in obs and press the button
we should now see it fade to scene 1. If we set the scene
to scene 3 in obs we should now see it cut to scene 1. Whatever
transition was set as the scene transition when the button was
should be set again as well.

Functions With Arguments
------------------------

Let's say you want to have buttons to transform your sources in
some way. It would be quite inefficient to create a function for
each type of transformation and different source, so we can create
one function to fill our transforming needs and pass arguments to it.

To follow along you'll want to have OBS running in studio mode with a
scene and a source and OBS WebSocket running. I'll name my scene ``'scene 1'``
and my source ``'Color Source'`` and use those names in the tutorial.

We can create this function using the functions from ``builtin_obs_actions``
``get_source_transform`` and ``set_source_transform``:

.. code-block:: python

    >>> from stream_tool import builtin_obs_actions
    >>> def transform_source(scene_name, source_name, move_x=0, move_y=0, scale=1):
    >>>     current_transform = builtin_obs_actions.get_source_transform(
    ...         scene_name,
    ...         source_name)
    >>>     new_transform = current_transform
    >>>     new_transform['positionX'] += move_x
    >>>     new_transform['positionY'] += move_y
    >>>     new_transform['scaleX'] *= scale
    >>>     new_transform['scaleY'] *= scale
    >>>     builtin_obs_actions.set_source_transform(
    ...         scene_name,
    ...         source_name,
    ...         new_transform)

Let's create some buttons on an index page to transform
this source. Make sure to set any :ref:`authentication and connection
<adding obs websockets integration>` information before creating
your website. First we need a site with OBS websocket integration
and to save our index page:

.. code-block:: python

    >>> from stream_tool import create_website
    >>> my_site = create_website(use_obs_websockets=True)
    >>> index = my_site.index_page

Next, we will create our first button for shrinking the source by
half. To do this use the ``button_function_args`` parameter of add
button to add the arguments and ``button_function_kwargs`` to
add the keyword arguments.

``button_function_args`` takes a list of arguments or a single argument
and ``button_function_kwargs`` takes a dictionary of keyword
arguments with keywords as keys and the arguments as the values.

To use this to create our button, we'll send our
``scene_name`` and ``source_name`` arguments and the value for the
``scale`` keyword argument:

.. code-block:: python

>>> index.add_button(
...     "Shrink",
...     button_function=transform_source,
...     button_function_args=(
...         "scene 1",
...         "Color Source"),
...     button_function_kwargs=
...         {'scale': 0.5})

We can add another button but instead of using the parameters of
``add_button`` we can assign values to the button's attributes after
creating it. This one will move the source down and to the right a bit:

.. code-block:: python

    >>> btn2 = index.add_button("Down Right")
    >>> btn2.button_function = transform_source
    >>> btn2.button_function_args = (
    ...     "scene 1", "Color Source")
    >>> btn2.button_function_kwargs = {
    ...     'moveX': 50
    ...     'moveY': -50 }


This function can be used to create buttons with other
combinations of the move and scale and for other sources.

When you're ready to see what you've got run it and try it out:

.. code-block:: python

    >>> my_site.build_and_run()
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

That's how you build custom functions with arguments and keyword
arguments!

Macros With Other Libraries
---------------------------

Functions are useful for making macros because they can run any code
you want to. Just import the necessary libraries and incorporate them
in your function.

To follow along you'll want to have OBS running with
two scenes and OBS WebSocket running. I'll name
mine ``'scene 1'``, and ``'scene 2'`` and use those names
in the tutorial.

Here's an example using ``random`` to pick a random scene to go to,
``obs-websocket-py`` to go to it and ``pyclip`` to put something in the clipboard.

Pyclip documentation_ can be consulted for installation.

.. _documentation: https://github.com/spyoungtech/pyclip

First we'll import the modules:

.. code-block:: python

    >>> from stream_tool import create_website
    >>> from obswebsocket import requests
    >>> import random
    >>> import pyclip

Next, we'll create our site with OBS websocket integration and
save the index page and the websocket manager. Make sure
to set any :ref:`authentication and connection <adding obs
websockets integration>` information before creating your website.

.. code-block:: python

    >>> my_site = create_website(use_obs_websockets=True)
    >>> index = my_site.index_page
    >>> ws = my_site.ws

We need to make the actual function to perform all our actions:

.. code-block:: python

    >>> def btn1_function():
    ...     random_number = random.randint(1, 2)
    ...     if random_number == 1:
    ...         ws.call(requests.SetCurrentProgramScene(sceneName="scene 1"))
    ...     else:
    ...         ws.call(requests.SetCurrentProgramScene(sceneName="scene 2"))
    ...     pyclip.copy("hello clipboard")

Let's add a button and connect the function to it:

.. code-block:: python

    >>> index.add_button(
    ...     "stuff",
    ...     button_function=btn1_function)

Now if we run the site we'll have a button to
control the scenes randomly. The button will also
add new text to the clipboard that can be pasted.

.. code-block:: python

    >>> my_site.build_and_run()
     * Serving Flask app 'stream_tool._website'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit

--------------------

That's all I wrote.

For my information on anything check out the :doc:`API documenation<api>`.