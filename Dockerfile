FROM python:3.11.2

WORKDIR /app
# Copy requirements.txt into the image
COPY requirements.txt requirements.txt
COPY DrawingColour.py DrawingColour.py
COPY DrawingOverlay.py DrawingOverlay.py
COPY FileNameMatcher.py FileNameMatcher.py
COPY frontend.py frontend.py

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

# docker build -t streamlit .
# docker run -p 8501:8501 streamlit


## if stuck - upload to google cloud run
# gcloud init
# gcloud auth configure-docker eu.gcr.io
# gcloud auth login
# docker build -t eu.gcr.io/drawingoverlay/drawingoverlay:v1 .
# docker push eu.gcr.io/drawingoverlay/drawingoverlay:v1
