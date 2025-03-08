# Miracle Coding Challenge

## Getting Started

Run the command `docker-compose up --build` in the root directory of the project.
For some reason, occasionally the first time it is run it stalls at some point, but after
ctrl-c and rerunning, it works fine. From there if you want to look at the Airflow
UI, you can go to http://localhost:8080/ and use "admin" for both the username and password.
**If you don't want to wait for the Airflow scheduler to run the web scraper automatically,
you can trigger the DAG manually in the UI. This will run the web scraper and populate the database.**

For the Flask backend to access port 5000 on Mac, you may need to disable AirPlay and Handoff.
You can test the API by sending requests to http://localhost:5000/

To view the frontend, go to http://localhost:3000/ in your browser. Note, instead of showing a simple
comparison between the current total clinical trials vs one week ago, I thought it would be nicer to
show the change over time in the last week with a line graph :)

## Architecture
I am using Airflow to run and schedule the web scraper pipeline, and MySQL as the database.
currently, the webpage and API server are hosted locally.

## Future Work
Aside from completing the requirements, improvements include but are not limited to:
 * instead of putting all the web scraper code in the dags folder, create a python packaage and import it
 * the web-scrapers could be made more resilient to changes in the web pages using more edge case handling
 * separate Airflow metadata and the trial tables into separate databases
 * move secret values in the docker-compose file to a secure location
 * improve memory handling in pipeline
 * scrub user facing error messages for potentially sensitive information (such as SQL requests)
 * restrict cors
 * maybe make database updates atomic to avoid concurrency issues with queries
 * iterate over the rest of the pages of EudraCT instead of just the first 3
 * move SQL queries in `mysql_manager.py` to their own file
 * add tests

## How I would approach some of the incomplete requirements
* the database rollback design could be achieved by taking snapshots of the database and archiving them in AWS S3.
* I forgot to exclusively use the combined_trials table for the visualizations, but the SQL queries wouldn't need much changing.
