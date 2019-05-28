# Camlytics

Camlytics is a project that uses computer vision to analyze the movement of people in a video.

# Getting Started

We assume you have `yarn v1.13` and `python v3.6` installed on your machine.

## Install Dependencies 

* We assume you start at the root directory for all directions below. To install the dependencies for the frontend:
```
# Go to frontend directory
cd frontend
yarn install
```
 
* To install the dependencies for the backend in a virtual environment:
```
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Running Camlytics

1. To launch the detector model:
```
cd backend/detector
python3 detector.py
```

2. To launch the backend server:
```
cd backend
FLASK_APP=api.py flask run
```

3. To launch the frontend server:
```
cd frontend
yarn start
```

You should then have a local Camlytics server running at `http://localhost:3000`.

