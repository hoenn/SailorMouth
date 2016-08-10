#! python3
"""
Scrapes a reddit users comment history to collect
statistics about certain words they've used
Author: github.com/Hoenn
"""

import sys, praw, argparse, re
import operator
from collections import OrderedDict
# Graphing imports
import ascii_graph.colors
from ascii_graph import Pyasciigraph
from ascii_graph.colordata import vcolor

# Container for statistics on a particular subreddit
class SubredditData:
  def __init__(self, name):
    self.name = name
    self.word_dict = {}
    self.total_count = 0
  def add_word(self, word):
    # If word exists, increment value
    if word in self.word_dict:
      self.word_dict[word] += 1
    # Otherwise set the value and type
    else: 
      self.word_dict[word] = 1

    self.total_count +=1

# Creates list of colors for each row of graph
def create_color_pattern(data):

  # Initialize list of colors
  pattern=[]
  # Set color of row depending on how many total hits in each subreddit
  for k,v in data.items():
    if   v.total_count >= 100:
      pattern.append(ascii_graph.colors.Red)
    elif v.total_count >= 75:
      pattern.append(ascii_graph.colors.Yel)
    elif v.total_count >= 50:
      pattern.append(ascii_graph.colors.Cya)
    elif v.total_count >= 25:
      pattern.append(ascii_graph.colors.Blu)
    elif v.total_count >= 10:
      pattern.append(ascii_graph.colors.Pur)
    elif v.total_count >= 5:
      pattern.append(ascii_graph.colors.Gre)
    else:
      pattern.append(ascii_graph.colors.Whi)
  return pattern

def main():
  parser = argparse.ArgumentParser(
          description='Profiling a Reddit user\'s word usage',
          epilog="The data was there all along.")
  
  required = parser.add_argument_group('required arguments')
  required.add_argument('-u', '--user', type=str, help="Reddit username to analyze", required=True)
  parser.add_argument('-l', '--limit', type=int, help="Number of comments to profile, defaults to 100 (upper limit of 999 imposed by Reddit)", default=100)
  parser.add_argument('-d', '--dict', type = str, help="Path to target word definitions. Make sure file is in 'lists' directory and include .txt. Each word must be on separate line", default='bad_words.txt')
  parser.add_argument('-s', '--sort', help = "Sort graph. Include 'inc' for increasing or 'dec' for decreasing", dest = 'sort')
  parser.add_argument('-v', '--verbose', help="Include verbose breakdown for each Subreddit", dest = 'verbose', action = 'store_true')
  parser.set_defaults(verbose = False)
  parser.add_argument('-c', '--color', help="Included intensity colored graph, must have ANSI color enabled", dest ='color', action = 'store_true')
  parser.set_defaults(color = False)


  # Gather arguments 
  args = parser.parse_args()
  username = args.user
  limit = args.limit
  dict_path = args.dict
  verbose_output = args.verbose
  color_output = args.color
  sort = args.sort

  # Identifies our script and allows more requests
  user_agent = "Word Profiler v0.2 by i_am_hoenn"
  r = praw.Reddit(user_agent = user_agent)

  # Reddit object
  user = r.get_redditor(username)
  # Load list of targetted words
  with open("lists/"+dict_path) as f:
    targetwords = f.read().splitlines()


  # Dictionary of data objects
  data = {}

  # Main loop to iterate comments
  comments_affected = 0
  found_in_comment= False
  num_comments = 0
  for comment in user.get_comments(limit = limit):
    # Keep track of actual number of comments
    num_comments += 1
    # Convert to lower case to mitigate case sensitivity
    c_body = comment.body.lower()
    for t_word in targetwords:
      # Check each target word against the comment
      while re.search(r"\b" + re.escape(t_word) + r"\b", c_body):

        found_in_comment = True
        # Remove found match until no matches remain
        c_body = c_body.replace(t_word, '', 1)
        # Convert subreddit name to string
        sr_str = str(comment.subreddit)
        
        # Check if subreddit has been catalogued and add word
        if sr_str in data:
          data[sr_str].add_word(word = t_word)
        # If not, create Subreddit object and add word
        else:
          data[sr_str] = SubredditData(sr_str)
          data[sr_str].add_word(word = t_word)
    if found_in_comment:
      # Reset flag
      found_in_comment = False
      comments_affected += 1

  # Sort verbose output if desired
  if sort != None:
    #Sort subreddits by total count, then sort each word list by num occurances
    sort = sort.lower()
    if sort == 'inc':
      data = OrderedDict(sorted(data.items(), key=lambda x: x[1].total_count, reverse=False))
      for k, v in data.items():
        v.word_dict = OrderedDict(sorted(v.word_dict.items(), key= operator.itemgetter(1), reverse=False))
    elif sort == 'dec':
      data = OrderedDict(sorted(data.items(), key=lambda x: x[1].total_count, reverse=True))
      for k, v in data.items():
        v.word_dict = OrderedDict(sorted(v.word_dict.items(), key= operator.itemgetter(1), reverse=True))
  else:
      #Sort subreddits and word lists alphabetically
      data = OrderedDict(sorted(data.items(), key=lambda x: x[1].name.lower(), reverse=False))
      for k, v in data.items():
        v.word_dict = OrderedDict(sorted(v.word_dict.items(), key= operator.itemgetter(0), reverse=False))



  
  if verbose_output:
    print("\nBreakdown by individual subreddit\n")
    # Iterate through key, value pairs for results
    for k,v in data.items():
      print("/r/"+k)
      for word in v.word_dict:
        print("  '"+word+"' appears: "+ str(v.word_dict[word])+" time(s).")
 
  print("\nTotal comments analyzed: "+ str(num_comments))
  print("Number of comments containing target words: " + str(comments_affected))
  if num_comments > 0:
    ratio = round((comments_affected/num_comments) * 100, 3)
    print("Percentage of comments containing target words: "+str(ratio) +"%")   



  # Initialize graph
  bar_graph= []

  # Add data to graph
  for k,v in data.items():    
    bar_graph.append((k, v.total_count))

  # Determine each rows color if desired
  if color_output:
    pattern = create_color_pattern(data)        
    bar_graph = vcolor(bar_graph, pattern)

  # Sort graph if desired
  if sort != None:
    sort = sort.lower()
    if sort == 'inc':
      bar_graph = sorted(bar_graph, key=lambda value: value[1], reverse = False)
    elif sort == 'dec':
      bar_graph = sorted(bar_graph, key=lambda value: value[1], reverse = True)

  #Create graph
  graph = Pyasciigraph(
    graphsymbol='|',
    human_readable='si',
    multivalue = False,
    min_graph_length = 1
    )

  # Title of graph
  print("\n"+username+"'s Graph")
  #Display graph
  for line in graph.graph(label=None, data=bar_graph):
    print(line)

  #Display message if graph was empty
  if len(data) <= 0:
    print("Hmm. Nothing found")

# Launch main
if __name__ == "__main__":
  main()




