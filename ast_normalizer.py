"""
This file will normalize an AST into a uniformally sized
object so we can fead each token into a RNN later.

It's sort of similar in theme to the way that NLP people
always use just one feature: the text. We want to see
if just feeding in the raw code is the right thing to do.
"""