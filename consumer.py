from confluent_kafka import Consumer
import socket
import json
import spacy
from pyspark.sql import SparkSession
from confluent_kafka import Producer

configuration = {
    'bootstrap.servers': "localhost:9092",
    'client.id':socket.gethostname(),
    'group.id':'python_consumer'
}

# concf = {
#     'bootstrap.servers': "localhost:9092",
#     'client.id':socket.gethostname(),
    
# }

consumer = Consumer(configuration)


producer = Producer(configuration)

consumer_topic = 'mytopic'
producer_topic = 'topic2'


consumer.subscribe([consumer_topic])

pos_tag = []
spark = SparkSession.builder.getOrCreate()
nlp = spacy.load('en_core_web_sm')

def call_back(error,message):
    if error is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(error)))
    else:
        print("Message produced: %s" % (str(message)))

while True:
    msg = consumer.poll(1)
    if msg is None:
        continue
    val = json.loads(msg.value())
    doc = nlp(val['data'])
    for ent in doc.ents:
        pos_tag.append(ent.label_)
    listRDD = spark.sparkContext.parallelize(pos_tag)
    data = listRDD.countByValue()
    json_data = json.dumps(data)
    producer.produce(producer_topic, key="data", value=json_data, callback=call_back)
    print(data)
    producer.poll(1)

    
consumer.close()