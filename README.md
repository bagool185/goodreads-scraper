# Goodreads Scraper [WIP]

_Description incoming_

## Pre-requisites 

Python >=3.8.x  
pip >=21.1.x

## Project setup

* [Create and activate a python virtual environment](https://docs.python.org/3/tutorial/venv.html)
* Clone the repo ```git clone git@github.com:bagool185/goodreads-scraper.git```
* Install dependencies ```pip install -r requirements.txt```

## Remote debugging azure functions

**Note** if you're using PyCharm you'll need the Professional edition to set up Remote Debugging:

Toolbar -> Run -> Edit configurations... -> Click on the '+' to add a new configuration -> Choose 'Python Debug Server'

Set whichever host name and port you want and click 'OK'.

Make sure this snippet is added at the top of a function's Python file:

```py
import pydevd_pycharm
pydevd_pycharm.settrace(<your_host>, port=<your_port>, stdoutToServer=True, stderrToServer=True)
```

Start the debugger and set a breakpoint as you normally would, then run `func start` in the terminal.


## Scraping

Scraping is done using BeautifulSoup with the lxml parser. The scraping scripts follow somewhat of a 
[Page Object Model](https://www.browserstack.com/guide/page-object-model-in-selenium) - see the `pages` directory

## How to contribute

Feel free to raise a GitHub issue with any suggestions you might have. If you want to contribute directly, please try to  
keep your pull requests consistent with the rest of the project, within reasonable limits.