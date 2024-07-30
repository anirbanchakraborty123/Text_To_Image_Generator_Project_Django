# Django Text To Image Generator with Celery using Stability AI API

## Setup Instructions

### Prerequisites

- Python 3.x
- Django
- Celery
- Redis
- requests

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd image_generator


2. Install dependencies:

   pip install -r requirements.txt

3. Configure your Stability AI API key in .env file:
  
   STABILITY_API_KEY = "your stability api"

4. Run Redis server

   redis-server

5. Run Celery workers:

   celery -A text_to_image_generator worker -l info --concurrency=3 -P solo

6. Start Django server:
  
   python makemigrations
   python migrate
   python manage.py runserver

7. http://localhost:8000/v1/api/generate/image/  to trigger image generation.


**NOTE** 

API Configuration
Ensure you have a Stability AI account and API key.
Use the Stable Diffusion XL API endpoint.
Running the Application
Ensure Redis server is running.
Start Celery workers.
Start Django server and access the generate endpoint.