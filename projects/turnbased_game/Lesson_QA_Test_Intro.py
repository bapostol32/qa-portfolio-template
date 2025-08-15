

"""What is a Test?"""

# Software under test means a part of subset of a program is copmleted
# Where we can exercise some bheavior. 
# Usually a method, a function, subroutine, prcedure, etc.
# A small defined set of steps or tasks that we can expect how it behaves 
# once we run the code
# Test data is the information on which to act
# Can be factored based on predicted user input, probability etc.

# watch the behavior of a program given the output

# Oracle: Is the deeloper or tester that runs the test
# They run the tests, and determine whether a test or not gave the esult 
# as expected.
# many are now automated with pre given oputput data
# Many frameworks have this 
# They provide a visual report of whether or not tests pass or fail
# Allows hundreds or even thousands of test to run very quickly 
# We analyze the rupport ot see which tests didn't pass and why

# These are all wrapped in what are called test cases

"""Dissecting the anatomy of a test"""

# Setup:
# how you put the software under test
# For example:
#  if you are testing a function that 
# deletes an item from your inventory,
# The condition must be firsdt met that you have an item
# in your inventory

# Invocation:
# The execution of a single tes cases given input values

# Assessment:
# The active observing of the software under test and compare
#  with expected results

# Teardown:
# Opposite side of the setup
# May be instances where what was done in the test 
# ends after the tests are over
# For example:
# closing database connections, file handles, deleting data 
# restored or even restoring data deleted

# Oracle is what decides whether the test was a success or not