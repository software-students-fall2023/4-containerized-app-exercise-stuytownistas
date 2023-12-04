	# in Docker, it is common to base a new image on a previously-created image
	FROM python:3.8-slim
	
	# Set the working directory in the image
	WORKDIR /machine-learning-client
	

	RUN apt-get update && \
    apt-get install -y ffmpeg

	# Copy the current directory contents into the container at /app
	COPY . /machine-learning-client


	# Install any needed packages specified in requirements.txt
	RUN pip install --no-cache-dir -r requirements.txt

	# Make port 5002 available to the world outside this container
	EXPOSE 5002

	# Run app.py when the container launches
	CMD ["python", "whisper_model.py"]
