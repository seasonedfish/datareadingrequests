# Data Reading Requests
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datareadingrequests)](https://pypi.org/project/datareadingrequests/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/tactlessfish/datareadingrequests/main)](https://github.com/tactlessfish/datareadingrequests/actions)
[![Coveralls](https://img.shields.io/coveralls/github/tactlessfish/datareadingrequests)](https://coveralls.io/github/tactlessfish/datareadingrequests)

A new client for Energize Andover's Building Energy Gateway, with a focus on clarity and usability.

## Differences from building_data_requests
For compatibility, datareadingrequests' function definitions are similar to those of building_data_requests.
However, there are a few key differences between the two modules:
- Instead of a tuple, datareadingrequests' `get_value()` returns a DataReading namedtuple.
This allows you to use the original tuple notation or the cleaner dot notation.
Read more about namedtuples [here](https://realpython.com/python-namedtuple/).
- datareadingrequests has a predictable, single return type for `get_value()`.
With building_data_requests, `get_value()` could return a valid result or `None`.
Here, it can only return a valid result; it raises an exception if the server returns no data.
The reasoning for this is well-explained by williballenthin:
> I've learned that *returning more than one type of data from a function is a recipe for trouble*.
> For example, when a function can return a string *or* a list,
> then every place that the function is called must check "is it a string or a list?".
> If the programmer forgets this, then inevitably,
> the program breaks at an inconvenient time.
> By extension, if a function returns a string or `None`,
> then every invocation must check "is the result `None`?".
> This is easy to forget, and leads to latent bugs.
> With the existing style, forgetting a `try/except` block is also a bug,
> but when the exception is generated,
> the programmer gets a very explicit stack trace with easy-to-find line number.
- In the same way, datareadingrequests' `get_bulk()` raises an exception
if the server returns no data for any specific instance.
- datareadingrequests has no way (currently) to change hostname or port.
- datareadingrequests does not retry requests without SSL.

## Improvements
- datareadingrequests is packaged!
You can install datareadingrequests with pip instead of manually copying a file.
- datareadingrequests has unit tests.
- datareadingrequests is open source:
it uses the MIT License.
  
## Setup
Use your favorite Python package manager, and do as you would with pandas, matplotlib, etc.

Pip:
```
pip install datareadingrequests
echo datareadingrequests >> requirements.txt
```

Poetry:
```
poetry add datareadingrequests
```
