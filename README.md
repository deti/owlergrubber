Owler grubber
=============
Once I was curious: "How startups funded?" 
There are several resouces like https://www.crunchbase.com/, http://mattermark.com/, https://www.owler.com/ 
where you can put some filters onto their database and make key-words search. However it didn't answer my needs.

But I wanted whole picture. In Shpreadsheet format.
I knew Python basics and Selenium framework.


Configuration
-------
### Project local configuration
```
python3 bootstrap-buildout.py (add flag --allow-site-packages for windows machine)
bin/buildout
```

### Buildout Windows installation issues
To properly compile depended C libraries (during bildout run) the following changes in environment are required:

```
SET VS90COMNTOOLS=%VS100COMNTOOLS%  # with Visual Studio 2010 installed (Visual Studio Version 10)
```
or
```
SET VS90COMNTOOLS=%VS110COMNTOOLS%  # with Visual Studio 2012 installed (Visual Studio Version 11)
```
or

```
SET VS90COMNTOOLS=%VS120COMNTOOLS%  # with Visual Studio 2013 installed (Visual Studio Version 12)
```
The list of precompiled libraries for windows you can find here http://www.lfd.uci.edu/~gohlke/pythonlibs/


Run
-------

### Configuration file
For proper execution you have to provide yaml-config in environment variable OG_CONFIG
```yaml
owler: #account info
  login: "accoung@examle.com"
  password: "password"

funds: # Funds in millions
  start:
  finish:

year: # founded
  start: 0
  finish: 5

requests: #requests for key-words in companies description
  kids: # Name for CSV file
    - kids
    - children
```


###Run commands

Scan, collect profiles in local DB, search for key words and produce CSV file
```
./bin/owlergrubber.py
```

Only scan and collect profiles only
```
./bin/collect_profiles.py
```

Search for key wordds and produce CSV file only 
```
./bin/search_for_words.py
```