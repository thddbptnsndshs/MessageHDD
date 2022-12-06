# MessageHDD for intertextual lexical diversity of short texts

MessageHDD is a metric for calculating lexical diversity for short texts (<100 tokens) in relation to the vocabulary of a larger corpus. Regular lexical diversity metrics do not make sense for such short texts, whereas MessageHDD is working better (see `usage.ipynb`).

## The maths behind it

The idea behind the metric is averaging the probability of each word in a text of occuring at least once in a sample of the size of the text (hypergeometric variable). 

- Say, the sentence 'I love trains' contains three tokens: 'I', 'love' and 'train'. 
- We calculate the probability of 'I' occuring at least once in a sample of 3 words while sampling form the entire corpus, same for 'love' and 'train'.
- Average the probabilities, the result is MHDD for the sentence.

## The naming

The metric is named after the dataset of text messages that I was working with when I thought of this metric on accident.