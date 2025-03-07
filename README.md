# Miracle Coding Challenge

## Getting Started

Run the command `docker-compose up --build` in the root directory of the project.
For some reason, usually the first time it is run it stalls at some point, but after
ctrl-c and rerunning, it works fine. From there if you want to look at the Airflow
UI, you can go to http://localhost:8080/ and use "admin" for both the username and password.

## Future Work
Aside from completing the requirements, improvements include but are not limited to:
 * instead of putting all the web scraper code in the dags folder, create a python packaage and import it
 * the web-scrapers could be made more resilient to changes in the web pages using more edge case handling
 * separate Airflow metadata and the trial tables into separate databases
 * move secret values in the docker-compose file to a secure location
 * improve the pipeline to stream data into the database (or at least use better batches than just downloading a giant CSV locally and then dumping it)

## How I would approach some of the incomplete requirements
* the database rollback design could be achieved by taking snapshots of the database and archiving them in AWS S3.
* I forgot to exclusively use the combined_trials table for the visualizations, but the SQL queries wouldn't need much changing.