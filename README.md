## Purpose
* Owler grubber.

## Development
### Project local configuration
* python3 bootstrap-buildout.py (add flag --allow-site-packages for windows machine)
* bin/buildout

### Buildout Windows installation issues
To properly compile depended C libraries (during bildout run) the following changes in environment are required:

> SET VS90COMNTOOLS=%VS100COMNTOOLS%  # with Visual Studio 2010 installed (Visual Studio Version 10)
>
> or
>
> SET VS90COMNTOOLS=%VS110COMNTOOLS%  # with Visual Studio 2012 installed (Visual Studio Version 11)
>
> or
>
> SET VS90COMNTOOLS=%VS120COMNTOOLS%  # with Visual Studio 2013 installed (Visual Studio Version 12)

The list of precompiled libraries for windows you can find here http://www.lfd.uci.edu/~gohlke/pythonlibs/
