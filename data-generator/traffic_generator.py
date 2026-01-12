import json
import random
from datetime import datetime
import time

class TrafficDataGenerator:
    def __init__(self):
        self.zones = ['Centre-Ville', 'Zone-Nord', 'Zone-Sud', 'Zone-Est', 'Zone-Ouest']
        self.road_types = ['autoroute', 'avenue', 'rue']
        self.roads = [f'R{i:03d}' for i in range(1, 51)]  # 50 routes
        self.sensors = [f'S{i:04d}' for i in range(1, 101)]  # 100 capteurs
    
    def generate_event(self):
        hour = datetime.now().hour
        
        # Simulation trafic selon l'heure (rush hours)
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            vehicle_count = random.randint(50, 200)
            average_speed = random.randint(20, 60)
            occupancy_rate = random.randint(60, 95)
        else:
            vehicle_count = random.randint(10, 80)
            average_speed = random.randint(40, 90)
            occupancy_rate = random.randint(20, 60)
        
        event = {
            'sensor_id': random.choice(self.sensors),
            'road_id': random.choice(self.roads),
            'road_type': random.choice(self.road_types),
            'zone': random.choice(self.zones),
            'vehicle_count': vehicle_count,
            'average_speed': average_speed,
            'occupancy_rate': occupancy_rate,
            'event_time': datetime.now().isoformat()
        }
        return event
    
    def generate_continuous(self, interval=1):
        """Génère des événements en continu"""
        while True:
            event = self.generate_event()
            print(json.dumps(event))
            time.sleep(interval)

if __name__ == '__main__':
    generator = TrafficDataGenerator()
    generator.generate_continuous(interval=0.5)  # 2 événements/seconde