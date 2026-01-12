import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data-generator'))

from kafka import KafkaProducer
import json
from traffic_generator import TrafficDataGenerator
import time

class TrafficProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.generator = TrafficDataGenerator()
    
    def send_events(self, topic='traffic-events'):
        while True:
            event = self.generator.generate_event()
            self.producer.send(topic, value=event)
            print(f"Envoyé: {event['sensor_id']} - Zone: {event['zone']}")
            time.sleep(0.5)

if __name__ == '__main__':
    producer = TrafficProducer()
    producer.send_events()