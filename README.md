Vendor Qualification API

A simple API that helps rank and qualify software vendors based on their category, capabilities, and overall rating.
Built using Flask, Machine Learning, and Docker!

**Technologies Used

Python 3.10
Flask
Sentence Transformers (SBERT) / TF-IDF
Scikit-learn
Pandas, NumPy
Docker
Jupyter Notebook (for experimentation and development)

Features

Match vendors by software category and capabilities
Rank vendors based on feature similarity and ratings
Expose everything through a clean REST API (/vendor_qualification)
Health check endpoint (/health)
Unit tests provided
Dockerized for easy sharing and deployment


 How to Run Locally

1. Clone the repository
 git clone https://github.com/nithishkaranam/vendor-qualification-api.git
cd vendor-qualification-api

2. Install requirements
pip install -r requirements.txt

3. Run the Flask app
python app.py


The app will start running at: http://localhost:8000

Running with Docker (Highly Recommended)

1. Build the Docker Image
 docker build -t vendor-qualification-api .

2. Run the Docker Container
docker run -p 8000:8000 vendor-qualification-api
The app will be available at: http://localhost:8000

API Usage

Endpoint:
POST /vendor_qualification

Example CURL:

curl --request POST \
  --url http://localhost:8000/vendor_qualification \
  --header 'Content-Type: application/json' \
  --data '{
    "software_category": "CRM Software",
    "capabilities": ["workflow automation", "lead management", "sales tracking"]
}'
Response:

Top 10 vendors matching your input
Sorted by feature similarity and rating

Run Tests

python -m unittest test_app.py
All unit tests will run and validate your API.

Docker Image

You can pull the Docker image from my public Docker Hub:

👉 Docker Hub:  https://hub.docker.com/u/nithishkaranam



Author

Made with ❤️ by Nithish Karanam

GitHub: https://github.com/nithishkaranam
Docker Hub: https://hub.docker.com/u/nithishkaranam


Thank youy !



