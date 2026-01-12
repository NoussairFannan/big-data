from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, sum, count, col, when

class TrafficProcessor:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("TrafficAnalysis") \
            .getOrCreate()
    
    def process_traffic(self, input_path='/data/raw/traffic', 
                       output_path='/data/processed/traffic'):
        
        # Lire les données JSON
        df = self.spark.read.json(input_path)
        
        # 1. Trafic moyen par zone
        traffic_by_zone = df.groupBy('zone').agg(
            avg('vehicle_count').alias('avg_vehicles'),
            avg('average_speed').alias('avg_speed'),
            avg('occupancy_rate').alias('avg_occupancy'),
            count('*').alias('total_events')
        )
        
        # 2. Vitesse moyenne par route
        speed_by_road = df.groupBy('road_id', 'road_type').agg(
            avg('average_speed').alias('avg_speed'),
            avg('vehicle_count').alias('avg_vehicles')
        )
        
        # 3. Identifier zones congestionnées (occupancy > 70%)
        congestion = df.groupBy('zone').agg(
            avg('occupancy_rate').alias('avg_occupancy')
        ).withColumn(
            'congestion_level',
            when(col('avg_occupancy') > 80, 'Critique')
            .when(col('avg_occupancy') > 60, 'Élevé')
            .otherwise('Normal')
        )
        
        # Sauvegarder les résultats
        traffic_by_zone.write.mode('overwrite') \
            .parquet(f"{output_path}/by_zone")
        
        speed_by_road.write.mode('overwrite') \
            .parquet(f"{output_path}/by_road")
        
        congestion.write.mode('overwrite') \
            .parquet(f"{output_path}/congestion")
        
        print("✓ Traitement terminé")
        
        return traffic_by_zone, speed_by_road, congestion
    
    def show_results(self):
        """Afficher les résultats"""
        print("\n=== Trafic par Zone ===")
        self.spark.read.parquet('/data/processed/traffic/by_zone').show()
        
        print("\n=== Zones Congestionnées ===")
        self.spark.read.parquet('/data/processed/traffic/congestion').show()

if __name__ == '__main__':
    processor = TrafficProcessor()
    processor.process_traffic()
    processor.show_results()