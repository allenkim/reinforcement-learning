# Resources

Below is a list of resources and a brief description of each one.

### Reinforcement Learning: An Introdcution by Sutton and Barto
The first version of this book came out in the 1990's, but recently, they have been working on the 2nd editon and is available as a draft online. As the name suggests, it is an introduction to reinforcement learning and is probably **the** book to learn. It covers all of the classic introductory material as well as some modern topics.

### Deep Learning Book
The deep learning book is not directly related to reinforcement learning, but has become a hot topic nowadays. Classic reinforcement learning algorithms such as Q-learning has been "deepenized" into deep Q-learning, which was shown to work in practice as displayed by DeepMind's Atari game playing bots. The concept of convolutional neural networks is also important in dealing with large input sizes and has been the way many recent researchers have been tackling problems.

### Trust Region Policy Optimization (TRPO)
This is a more specialized paper that shows a technique that works better in practice than vanilla policy gradient methods traditionally used in training agents. I include this as a modern method that has worked out well and would be nice to implement into practice, but this is more of a reach goal.

### AlphaGo Paper
Ah, this is the paper that brought me into the field as it was a revolutionary moment in Go history to have a computer beat a professional player in an even game. I've read through this paper several times and while not everything is clear to me (due to my lack of background knowledge in some areas like convolutional neural networks), I have been gaining a better understanding of what they did. Implementing an AlphaGo-algorithm for other problems would be another reach goal.

### Survey of Monte Carlo Tree Search Methods
This paper talks in depth about all the ways Monte Carlo Tree Search methods have been used and extended. MCTS is not really related to learning since it's more of a technique to tree search in very large search spaces, but it provides a means to do search where it is required. It was found in AlphaGo for example that using just neural networks did not do as well as combining neural networks with MCTS, which shows the importance of balancing intuition (having good feel for the game) as well as reflection (really thinking about the moves to come).

### CS231n - Stanford CS Class on Convolutional Neural Networks
This is a class from Stanford that was made public and contains all the information one can need to know about neural networks (well, much of it anyway). It starts off fairly introductory and quickly moves into a lot of the important details anyone working neural networks should know. It is an amazing supplement to the other material.

