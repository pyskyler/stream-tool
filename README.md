# Stream Tool
**Stream Tool** is a simple tool for making macros!

Use Stream Tool to create macros to control OBS or other programs on your computer. Or literally to run any python code you want to on a button press.

There is currently built-in functionality to run control some basic parts of OBS and to send your own OBS websocket requests. Other functionality may be added in the future but the main feature is that a function can be created and attached to a button to run it.

Project documentation is hosted at Read the Docs [here](https://stream-tool.readthedocs.io).


## Installing Stream Tool

Stream Tool is available on PyPI:

```console
$ python -m pip install stream-tool
```

Stream Tool officially supports Python 3.10+.

## Documentation

Full public API documentation as well as several tutorial to get started are available at [Read the Docs](https://stream-tool.readthedocs.io). A quick start is available below to show you the jist of it.

## Quick Start

Import Stream Tool and necessary modules and functions:

```python
>>> from stream_tool import create_website, builtin_obs_actions, Websockets_Auth
```

Configure OBS websocket password, create a site, and add a page:

```python
>>> Websockets_Auth.websockets_password = "password"
>>> my_site = create_website(use_obs_websockets=True)
>>> my_page = my_site.add_page("page 1")
```

Add a button with a link to the index page:

```python
>>> btn_1 = my_page.add_button("index")
>>> btn_1.button_link =m y_site.index.url)
```

Add a button to increase a OBS input's volume: 

```python
>>> btn_2 = my_page.add_button("sound up")
>>> btn2.button_function = 
...     obs_websockets_actions.change_volume("input")
```

Run the webiste and visit it at the link:

```python
>>> my_site.build_and_run()
* Serving Flask app 'stream_tool._website'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
