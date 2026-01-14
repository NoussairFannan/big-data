#  Smart City Traffic Analysis - Big Data Pipeline

##  Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Pipeline Components](#pipeline-components)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [KPIs & Analytics](#kpis--analytics)

---

##  Overview

This project implements an **end-to-end Big Data pipeline** for real-time urban traffic analysis in the context of Smart Cities. The system collects, processes, and analyzes traffic data from simulated urban sensors to provide actionable insights for intelligent mobility management.

### Business Objectives
- Monitor real-time traffic conditions
- Identify congested zones
- Analyze traffic patterns by zone, time period, and road type
- Support data-driven urban planning decisions

### Key Features
-  Real-time data generation from simulated IoT sensors
-  Stream processing with Apache Kafka
-  Data Lake architecture using HDFS
-  Distributed processing with Apache Spark
-  Analytics-ready data in Parquet format
-  Orchestration with Apache Airflow
-  Visualization dashboards with Grafana

---

##  Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SMART CITY PLATFORM                         │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Urban Sensors   │────▶│  Data Ingestion │────▶│   Data Lake      │
│  (Simulated)     │     │  Apache Kafka    │     │   HDFS Raw       │
│                  │     │                  │     │                  │
│ - Cameras        │     │ Topic:           │     │ /data/raw/       │
│ - IoT Devices    │     │ traffic-events   │     │   traffic/       │
│ - Loop Detectors │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                           │
                                                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Visualization   │◀────│  Analytics Zone  │◀───│  Processing      │
│  Grafana         │     │  Parquet Format  │     │  Apache Spark    │
│                  │     │                  │     │                  │
│ - Dashboards     │     │ /data/analytics/ │     │ - Aggregations   │
│ - KPIs           │     │   traffic/       │     │ - Transformations│
│ - Alerts         │     │                  │     │ - Congestion AI  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                           │
                                                           ▼
                         ┌──────────────────────────────────┐
                         │   Orchestration & Monitoring     │
                         │   Apache Airflow                 │
                         │                                  │
                         │   DAG: traffic_analysis_pipeline │
                         └──────────────────────────────────┘
```

### Data Flow Architecture

```

   STEP 1              STEP 2              STEP 3              STEP 4
┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
│  Data   │──────▶│  Kafka   │──────▶│   HDFS   │─────▶│  Spark   │
│Generator │       │ Producer │       │Consumer  │       │Processing│
│          │       │          │       │          │       │          │
│ JSON     │       │ Stream   │       │Raw Zone  │       │Analytics │
│Events    │       │Pipeline  │       │Storage   │       │Jobs      │
└──────────┘       └──────────┘       └──────────┘       └──────────┘
     │                   │                   │                   │
     │                   │                   │                   │
     ▼                   ▼                   ▼                   ▼
 Sensors            Topic:             /data/raw/        /data/processed/
 - sensor_id        traffic-events     traffic/          traffic/
 - road_id                             - Partitioned     - Aggregated
 - zone                                  by date/zone    - Enriched
 - metrics                                                 
                                                             │
                                                             ▼
                                                      ┌──────────┐
                                                      │Analytics │
                                                      │  Zone    │
                                                      │          │
                                                      │ Parquet  │
                                                      │ Format   │
                                                      └──────────┘
```

### Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                         INGESTION LAYER                                │
├────────────────────────────────────────────────────────────────────────┤
│  data-generator/          │  kafka-producer/                           │
│  ├── traffic_generator.py │  ├── producer.py                           │
│  └── config.json          │  └── requirements.txt                      │
└────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         STREAMING LAYER                                │
├────────────────────────────────────────────────────────────────────────┤
│  Apache Kafka                                                          │
│  ├── Broker: localhost:9092                                            │
│  ├── Topic: traffic-events                                             │
│  ├── Partitions: 3                                                     │
│  └── Replication Factor: 1                                             │
└────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          STORAGE LAYER                                 │
├────────────────────────────────────────────────────────────────────────┤
│  kafka-consumer/          │  HDFS Data Lake                            │
│  ├── consumer.py          │  ├── /data/raw/traffic/                    │
│  └── hdfs_writer.py       │  ├── /data/processed/traffic/              │
│                           │  └── /data/analytics/traffic/              │
└────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        PROCESSING LAYER                                │
├────────────────────────────────────────────────────────────────────────┤
│  spark-jobs/                                                           │
│  ├── traffic_analytics.py                                              │
│  ├── congestion_detection.py                                           │
│  └── zone_aggregation.py                                               │
└────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                               │
├────────────────────────────────────────────────────────────────────────┤
│  Apache Airflow                                                        │
│  └── DAG: traffic_pipeline                                             │
│      ├── Task 1: Generate Data                                         │
│      ├── Task 2: Ingest to Kafka                                       │
│      ├── Task 3: Process with Spark                                    │
│      └── Task 4: Validate Results                                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

##  Project Structure

```
big-data/
│
├── data-generator/              # Traffic data simulation
│   ├── traffic_generator.py     # Main generator script
│   ├── config.json              # Sensor configurations
│   └── requirements.txt         # Python dependencies
│
├── kafka-producer/              # Kafka data ingestion
│   ├── producer.py              # Kafka producer implementation
│   ├── config.py                # Producer configurations
│   └── requirements.txt         # Python dependencies
│
├── kafka-consumer/              # HDFS writer
│   ├── consumer.py              # Kafka consumer
│   ├── hdfs_writer.py           # HDFS integration
│   └── requirements.txt         # Python dependencies
│
├── spark-jobs/                  # Data processing jobs
│   ├── traffic_analytics.py     # Main analytics job
│   ├── congestion_detection.py  # Congestion analysis
│   ├── zone_aggregation.py      # Zone-based aggregation
│   └── requirements.txt         # Python dependencies
│
├── airflow/                     # Orchestration (to be added)
│   └── dags/
│       └── traffic_pipeline.py  # Airflow DAG
│
├── grafana/                     # Visualization (to be added)
│   └── dashboards/
│       └── traffic_dashboard.json
│
├── docker-compose.yml           # Container orchestration
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

---

##  Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Data Generation** | Python | 3.9+ | Simulate IoT sensors |
| **Message Broker** | Apache Kafka | 3.x | Real-time streaming |
| **Storage** | Apache Hadoop (HDFS) | 3.x | Distributed data lake |
| **Processing** | Apache Spark | 3.x | Distributed computing |
| **Orchestration** | Apache Airflow | 2.x | Workflow management |
| **Visualization** | Grafana | 9.x | Dashboards & KPIs |
| **Containerization** | Docker | 20.x | Environment isolation |
| **Language** | Python | 3.9+ | Primary development |

---

##  Prerequisites

- Docker & Docker Compose (v20.10+)
- Python 3.9+
- Java 8 or 11 (for Spark & Kafka)
- Minimum 8GB RAM
- 20GB free disk space

---

##  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/NoussairFannan/big-data.git
cd big-data
```

### 2. Start Docker Infrastructure

```bash
# Start all services
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 3. Install Python Dependencies

```bash
# Data Generator
cd data-generator
pip install -r requirements.txt
cd ..

# Kafka Producer
cd kafka-producer
pip install -r requirements.txt
cd ..

# Kafka Consumer
cd kafka-consumer
pip install -r requirements.txt
cd ..

# Spark Jobs
cd spark-jobs
pip install -r requirements.txt
cd ..
```

### 4. Create HDFS Directories

```bash
# Access Hadoop NameNode container
docker exec -it namenode bash

# Create directory structure
hdfs dfs -mkdir -p /data/raw/traffic
hdfs dfs -mkdir -p /data/processed/traffic
hdfs dfs -mkdir -p /data/analytics/traffic

# Verify creation
hdfs dfs -ls /data/
exit
```

### 5. Create Kafka Topic

```bash
# Access Kafka container
docker exec -it kafka bash

# Create topic
kafka-topics.sh --create \
  --topic traffic-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# Verify topic
kafka-topics.sh --list --bootstrap-server localhost:9092
exit
```

---

## Pipeline Components

### Step 1: Data Generation

Simulates urban traffic sensors generating real-time events.

```bash
cd data-generator
python traffic_generator.py
```

**Event Structure:**
```json
{
  "sensor_id": "SENSOR_001",
  "road_id": "ROAD_A1",
  "road_type": "autoroute",
  "zone": "Centre-Ville",
  "vehicle_count": 45,
  "average_speed": 65.5,
  "occupancy_rate": 72.3,
  "event_time": "2025-01-14T10:30:00Z"
}
```

### Step 2: Kafka Ingestion

Streams data to Kafka for real-time processing.

```bash
cd kafka-producer
python producer.py
```

### Step 3: HDFS Storage

Consumes Kafka messages and writes to HDFS raw zone.

```bash
cd kafka-consumer
python consumer.py
```

### Step 4: Spark Processing

Processes raw data and generates analytics.

```bash
cd spark-jobs
spark-submit --master local[*] traffic_analytics.py
```

### Step 5: Visualization

Access Grafana dashboards at `http://localhost:3000`

---

##  Data Flow

### Raw Zone → Processed Zone → Analytics Zone

```
RAW DATA (JSON)
└─▶ Partitioned by date and zone
    └─▶ /data/raw/traffic/2025-01-14/Centre-Ville/

PROCESSED DATA (Parquet)
└─▶ Aggregated metrics
    └─▶ /data/processed/traffic/

ANALYTICS DATA (Parquet)
└─▶ KPIs and insights
    └─▶ /data/analytics/traffic/
```

---

##  KPIs & Analytics

### Key Performance Indicators

1. **Average Traffic by Zone**
   - Vehicles per hour per zone
   - Peak vs off-peak comparison

2. **Average Speed by Road Type**
   - Highway vs avenue vs street
   - Speed degradation analysis

3. **Congestion Rate**
   - Threshold: occupancy_rate > 70%
   - Time-based congestion patterns

4. **Critical Zones Detection**
   - Zones with consistent congestion
   - Alert generation

---

