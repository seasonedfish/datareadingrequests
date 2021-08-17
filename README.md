# Data Reading Requests
A new client for Energize Andover's Building Energy API, with a focus on clarity and usability.

## Differences from building_data_requests
For compatibility, datareadingrequests' function definitions are similar to those of building_data_requests.
However, there are a few key differences between the two modules:
- datareadingrequests has a more intuitive `get_value()`. 
Instead of a tuple, its `get_value()` returns a DataReading namedtuple with fields `value` and `units`.
- datareadingrequests has a predictable, single return type for `get_value()`.
With building_data_requests, `get_value()` could return a valid result or `None`.
Here, it can only return a valid result; an exception will be thrown if the server returns no data.
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
- datareadingrequests is packaged!
You can install datareadingrequests with pip instead of manually copying a file.
- datareadingrequests has no way (currently) to change hostname or port.

# Improvements
- datareadingrequests has unit tests!
- datareadingrequests is open source: it uses the MIT License.
  
## Setup
Use your favorite Python package manager, and do as you would with pandas, matplotlib, etc.
The only difference is that since the package is not published on PyPI,
you must use the repository URL instead of just its name.

Pip:
```
pip install git+https://github.com/tactlessfish/datareadingrequests
echo "git+https://github.com/tactlessfish/datareadingrequests@master" >> requirements.txt
```

Poetry:
```
poetry add git:https://github.com/tactlessfish/datareadingrequests.git
```

