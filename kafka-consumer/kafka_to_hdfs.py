from kafka import KafkaConsumer
import json
from datetime import datetime
from hdfs import InsecureClient
import time

class KafkaToHDFS:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'traffic-events',
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='hdfs-writer'
        )
        self.hdfs_client = InsecureClient('http://localhost:9870', user='hadoop')
        self.buffer = []
        self.buffer_size = 100  # Écrire par batch de 100
    
    def consume_and_write(self):
        for message in self.consumer:
            event = message.value
            self.buffer.append(event)
            
            if len(self.buffer) >= self.buffer_size:
                self.write_to_hdfs()
    
    def write_to_hdfs(self):
        if not self.buffer:
            return
        
        # Organiser par date et zone
        now = datetime.now()
        date_path = now.strftime('%Y/%m/%d')
        zone = self.buffer[0]['zone']
        
        hdfs_path = f"/data/raw/traffic/{date_path}/{zone}_{int(time.time())}.json"
        
        # Écrire dans HDFS
        data = '\n'.join([json.dumps(event) for event in self.buffer])
        self.hdfs_client.write(hdfs_path, data, encoding='utf-8')
        
        print(f"✓ Écrit {len(self.buffer)} événements dans {hdfs_path}")
        self.buffer = []

if __name__ == '__main__':
    writer = KafkaToHDFS()
    writer.consume_and_write()