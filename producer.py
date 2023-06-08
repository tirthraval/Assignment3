import spacy
import pyspark
from pyspark.sql import SparkSession
import praw

import socket

# 4Yhh7u0NaPqZ7J7UZJrbcmHo elastic password

from confluent_kafka import Producer
import json


reddit = praw.Reddit(
    client_id=" ",#please insert your client Id
    client_secret=" ",#please insert your client secret key
    user_agent="my user agent",
)


configuration = {
    'bootstrap.servers': "localhost:9092",
    'client.id':socket.gethostname()
}
producer = Producer(configuration)

topic_name ='mytopic'

def call_back(error,message):
    if error is not None:
        print("Failed to deliver message: %s: %s" % (str(message), str(error)))
    else:
        print("Message produced: %s" % (str(message)))


pos_tag = []
for comment in reddit.subreddit("politics").comments(limit =10):
    sentence = comment.body
    # doc = nlp(sentence)
    # for ent in doc.ents:
    #     pos_tag.append(ent.label_)

    # listRDD = spark.sparkContext.parallelize(pos_tag)
    # data = listRDD.countByValue()
    payload = {}
    payload['data'] = sentence
    json_data = json.dumps(payload)
    producer.produce(topic_name, key="data", value=json_data, callback=call_back)
    producer.poll(1)
    print(json_data)