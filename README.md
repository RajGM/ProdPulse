# ProdPulse: FastAPI-based Monitoring & Alerting Service

ProdPulse is a production-grade monitoring and alerting web service built with FastAPI. This service continuously collects system metrics, exposes them for Prometheus scraping, and triggers alerts when defined thresholds are breached. The project is designed to showcase best practices in production engineering and site reliability engineering (SRE).

## Project Overview

**Goal:**  
To build a deployable web service that monitors system metrics (CPU, memory, disk usage, etc.) and sends alerts (via email or Slack) when anomalies are detected.

**Key Features:**
- Real-time metrics collection using `psutil`
- Metrics exposure via Prometheus client
- Alerting mechanisms using email and Slack integrations
- Configurable thresholds and settings loaded from YAML/JSON files
- Structured logging for audit and debugging purposes

## Module Design

### 1. API Server (`api/`)
- **Purpose:** Hosts the FastAPI application and defines RESTful endpoints.
- **Endpoints:**
  - `GET /metrics/live`: Returns the latest collected metrics.
  - `GET /health`: Provides a health check for the service.
  - `GET /metrics`: Exposes Prometheus metrics for scraping.
- **Details:**  
  Utilizes Prometheus’ ASGI middleware to seamlessly expose metrics.

### 2. Metrics Collector (`metrics/`)
- **Purpose:** Gathers system metrics (CPU, memory, disk usage) using `psutil`.
- **Functionality:**
  - Runs on a schedule (using an `asyncio` loop or background thread).
  - Updates both an in-memory store and Prometheus exporter metrics.
- **Usage:**  
  Essential for providing up-to-date system statistics to both the API and the alerting service.

### 3. Alerting Service (`alerts/`)
- **Purpose:** Monitors collected metrics against pre-defined thresholds and sends alerts.
- **Alert Methods:**
  - **Email Alerts:** Utilizes Python’s `smtplib` for sending email notifications.
  - **Slack Alerts:** Uses `slack_sdk` to send messages to Slack channels.
- **Additional Features:**
  - Implements retry logic using `tenacity` for robust alert delivery.

### 4. Configuration Loader (`config/`)
- **Purpose:** Loads configuration settings such as alert thresholds, collection intervals, and API keys.
- **File Formats:**  
  Supports YAML or JSON for easy configuration.
- **Usage:**  
  Centralizes configuration management to keep the system flexible and maintainable.

### 5. Logging (`core/logging.py`)
- **Purpose:** Provides structured logging across the entire application.
- **Libraries:**  
  Uses `loguru` (or Python’s built-in logging module) to capture detailed logs.
- **Benefits:**  
  Enables effective debugging and operational insights by logging key events (metrics collection, API requests, alerts).

## Data Flow Architecture

Below is a simplified overview of how data flows through the system:

```plaintext
+-------------------+       +--------------------+       +-------------------+
|  Config Loader    |-----> |  Metrics Collector |-----> |  In-Memory Store  |
+-------------------+       +--------------------+       +-------------------+
                                |       |                          |
                                v       v                          |
                       Prometheus Exporter (ASGI)                 |
                                |                                  |
                                v                                  v
+-------------------+       +-------------------+       +------------------+
| FastAPI API Layer |<----->| Alerting Service  |-----> |  Email/Slack API |
+-------------------+       +-------------------+       +------------------+
                                (uses thresholds)

```

```
git clone https://github.com/your-username/prodpulse.git
cd prodpulse
```

```
pipenv --python 3.8
pipenv install
pipenv install --dev pytest coverage
pipenv shell
```

```
uvicorn api.main:app --reload
```

```
Health Check: http://localhost:8000/health

Live Metrics: http://localhost:8000/metrics/live

Prometheus Metrics: http://localhost:8000/metrics
```


This `README.md` provides a clear outline of the project's architecture, module design, and data flow, making it easy for others to understand the structure and purpose of your application.
