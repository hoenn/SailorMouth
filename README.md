# SailorMouth
Profiles a reddit user's word choice against a target word list.

###Dependencies
[PRAW](https://github.com/praw-dev/praw), [ascii_graph](https://github.com/kakwa/py-ascii-graph)

Dependencies can easily be installed with pip by:
```
$ pip install praw
$ pip install ascii_graph
```

###Running the program
This program is launched from the command line and outputs to the command line

Using argparse run the program with a series of commands
```
$ python sailor_mouth.py --help
usage: sailor_mouth.py [-h] -u USER [-l LIMIT] [-d DICT] [-s SORT] [-v] [-c]
```
The only required argument is ```-u``` which must be immediately followed by a user

Example: ```$ python sailor_mouth.py -u i_am_hoenn```

Optional arguments include

```-l, --limit``` Number of comments to profile. Default value of 100. Upper limit of 999 imposed by Reddit API

```-d, --dict``` File path to target word definitions. Defaults to 'bad_words.txt'. Ensure that file is in 'lists' directory and include '.txt' in argument

```-s, --sort``` Sort graph data. Include 'inc' or 'dec' as an argument

```-v, --verbose``` Includes extra information: what words occured in what subreddits and how many times they occured

```-c, --color``` Enables a colored graph based, must have ANSI color enabled


Running using all settings
```
$ python sailor_mouth.py -u i_am_hoenn -l 1000 -d sat_300.txt -s dec -c -v
```

###Windows Command Prompt color not working
ANSI Escape codes may not be supported in your version of windows. 

See [ansicon](https://github.com/adoxa/ansicon) to work around the issue

###License
[GPLv3](

####Note
Due to artificial limitations imposed by the Reddit API, the runtime of the program is slowed
