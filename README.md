# Deep Metal

[TDI](http://www.thedataincubator.com) capstone project for the Winter 2019 cohort.

### Business Objective

Despite the fact that music reviews are entirely subjective, there is still a lot of value in being able to gauge their sentiment. For example, a band may want to know how fans are reacting to their latest single or a label may want to know how their roster is perceived by the general music community at large on social media.

Opinion mining, or more formally sentiment analysis, is a branch of natural language processing that processes unstructured text to gauge the sentiment behind it. In this capstone, I scraped hundreds of thousands of album reviews off the [Metal-Archives](http://www.metal-archives.com) website and built a custom sentiment classifier using the latest NLP technologies.

### Data Ingestion

The dataset was built by web scraping the Metal-Archives website using the **maq** command-line tool I wrote and [open sourced on Github](https://github.com/pisymbol/maq). Please see this project's page on usage and architecture for more details.

### Visualizations

Visualizations were mainly performed using [bokeh](https://bokeh.pydata.org/en/latest). 

### Machine Learning

* For unsupervised learning, I used sklearn to build a bag-of-words model and [pyLDAvis](https://github.com/bmabey/pyLDAvis) to visualize the most common topics per review.
* For all tokenization and text processing I used [spaCy](https://spacy.io)
* For building my word embedding matrix (word2vec) and final RNN I used [Tensorflow/Keras](https://www.tensorflow.org/)

### Distributed Computing

Because spaCy's neural model is very computationally intensive, I processed all reviews in batches and distributed them over several cores using Python's native [multiprocessing](https://docs.python.org/3.6/library/multiprocessing.html) module. I have recently switched to using [Apache Spark](https://spark.apache.org) and [mlib](https://spark.apache.org/mllib) for my initial modeling work.

### Interactive Website

Please visit [https://deepmetal.herokuapp.com](https://deepmetal.herokuapp.com) to see my final deliverable which was written in [Flask](http://flask.pocoo.org) and [Bootstrap](https://getbootstrap.com).

### Authors

* **Alexander Sack**

### Acknowledgments

* Don Fox for mentoring me throughout the project.
* My classmates for making it fun.

