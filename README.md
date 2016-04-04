# Insight-Coding-Challenge
## Program Summary
This program calculates the average degree of a vertex in a Twitter graph for the last 60s. The source code is writtern in Python and uses mostly the basic functions. 
It contains a class to handle tweet messages including extracting hashtags, collecting hashtags in a sliding time window, creating twitter graph from hashtags and calculating average degree of a vertex for the graph.
It can run on its own or be used as an indipendent module.

## Libraries Used
Three libraries are used in the source code.
1, json :  this library is used to parses a tweet message written in JSON into a Python dictionary.
2, sys : this library is used to catch the command line arguments, which specify the input and output file dictionaries.
3, datetime : this librariy is used to compare time stamps for different tweets.

## Test
This program passed two indipendent tests using the provided insight testsuite. The test files are included in the insight_testsuite folder.

## Example:
<<<<<<< HEAD
To run the program:      python average_degree.py  tweet_input_file_path  tweet_output_file_path
=======
To run the program:   python average_degree.py  tweet_input_file_ path  tweet_output_file_path
>>>>>>> origin/master

Use as a module: 
 
import average_degree

<<<<<<< HEAD
twitter = average_degree.twitter_graph()      # create an twitter_graph object and use all the methods included

## Author:  
This program is written by Jiansh Zhao. Any questions about this program can be sent to jszhaopsu at gmail.com

 
=======
twitter = average_degree.twitter_graph()  # create an twitter_graph object and use all the methods included

## Author:  
This program is written by Jiansh Zhao. Any questions about this program can be sent to jszhaopsu at gmail.com
>>>>>>> origin/master
