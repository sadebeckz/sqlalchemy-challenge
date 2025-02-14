Project Overview
This project analyzes Hawaii’s climate data using SQLAlchemy and Flask. The data analysis is conducted in Jupyter Notebook, and a Flask API is built to serve climate information.

Data Analysis Steps
Connected to SQLite database.
Analyzed precipitation and temperature data.
Identified the most active weather stations.
Created visualizations using Pandas and Matplotlib.
Flask API Endpoints
Endpoint	Description
/	Lists available API routes.
/api/v1.0/precipitation	Returns last 12 months of precipitation data.
/api/v1.0/stations	Returns a list of weather stations.
/api/v1.0/tobs	Returns temperature observations for the most active station.
/api/v1.0/<start>	Returns min, avg, and max temperatures from the start date onward.
/api/v1.0/<start>/<end>	Returns min, avg, and max temperatures for a date range.
Technologies Used
Python
SQLAlchemy
Flask
Pandas
Matplotlib
