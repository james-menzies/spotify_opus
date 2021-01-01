Recently, I published a case study on Spotify's technological infrastructure. Within, I raised the notion of altering the underlying data structure so that it could cater better for consumers of classical music. This repository is a rudimentary full stack prototype of the data model proposed in that case study, as well as a small demonstration of the front end features that it could enable.

I would highly recommend reading the [case study](docs/A%20Case%20Study%20on%20Spotify.pdf) before browsing the rest of this project, in particular sections R7 - R9.

## Installation for Local Development

In order to use this repository locally, you will need a .env file with the relevant client secrets in order to use this code base. Please email me for a copy, unfortunately I cannot store this information publically for security reasons.

Similarly, a populated database can be added on request, however note that **_the user must be using a Postgres database_**.

1. Clone the repository locally.
2. Install a database on your local system if not present. I would recommend PostgresQL if wanting to pre-populate the database.
3. Place the provided .env file in the root of the directory.
4. Set the DB_URI in the .env file so that the application can link to the database. For example:
```
DB_URI='postgres+psycopg2://user:password@localhost/dbname'
```
5. (If prepopulating) Prepopulate the database with the provided .sql file by executing:
```
psql {dbname} < path/to/sqlfile
```
If not prepopulating, run the following command instead:
```
flask manage reset
```

6. Run the app by executing:
```
flask run
```

7. The local server should be available at `http://localhost:5000/`

## The Data Structure

When implementing the new data model, there were some necessary compromises and alterations from the original vision, either due to keeping the scope of the project manageable or practical considerations during implementation. The revised scheme is below:

![Opus ERD](docs/spotify_opus_erd.png)

### Notes

- The super type entity `ContextObject` has been abandoned due to complications with implementing inheritance in a database.
- As the front end application will support browing by composer, the `Composer` entity has been added to assist creating the initial `GET` request as the entry point of the application.
- Similar to `Composer`, the `Performance` entity has been added to facilitate the selection of performances of the same work.
- Subsections have been abandoned. Works will be displayed instead via the `sanitized_name` attribute of the `Track` entity.

## Features

### Searching

Typically a user listening to classical music will want to search for a specific piece of music, which can be cumbersome to achieve with the existing Spotify model. This application supports searching for music via the following progression: 

![User flow of application](docs/user_flow.png)

This application enables that progression via the new data model and its endpoints.

### Listening

When on a page where playback occurs, the track listings are aggregated by work and section, rather than simply track-by-track.

## Pages

### Login Screen

To use Spotify Opus, the user needs to sign in through Spotify's official authorization flow. Once completed, the user will be able to use the application for an hour in order to browse the demonstration before requiring another log in. 

This is to mitigate any potential security concerns as a result of refresh tokens being stored server side.

`/login`

![login screen](docs/screenshots/login.png)

### Composers

If the signed on user is an administrator, there will also be controls to add or edit composer entities.

`/composers`

![composer screen](docs/screenshots/composers.png)

### Composer Edit

A simple form to create or alter a `Composer` entity. When adding a composer, the name must exactly match an existing record in the Spotify database or the create operation will fail.

`/composers/create`

`/composers/edit`
![composer screen](docs/screenshots/composer_edit.png)

### Works

`/composers/{id}/works`
![composer screen](docs/screenshots/works.png)

### Performance

`/works/{id}/performances`

![composer screen](docs/screenshots/performances.png)

### Playback

`/performances/{id}`

![composer screen](docs/screenshots/play.png)

## Migration Techniques

### Data Extraction

Since all data being used is stored natively by the application, there is a need to pull the data from the Spotify API to populate the `Album`, `Artist` and `Track` entities. This is done as a batch operation by the program, where all of the `Album` entities which feature a track by a desired composer, along with their related `Artist` and `Track` entities.

In order to extract data for a single composer, the following steps need to take place.

1. Create a `Composer` entity via the front end of the application as an administrator.
2. Obtain the ID of the `Composer` entity.
3. Then on the back end server running the application, run the following command:

```
flask manage pull {composer_id} 
```

This operation can take some time, due to the nature of how Spotify paginates its requests. However the CLI will inform the administrator about the progress as the import takes place.

### Data Parsing

To expedite the process of parsing data, the CLI also offers the ability to run custom Python scripts to interact with the database. By placing a Python script in the `spotify_opus/services/scripts` directory, and running the command `flask manage run {script.py}`, a developer is able to run arbitrary Python code whilst also having the application context available to interact with the data layer.

In this repo, I've used the `beethoven.py` script to migrate all of the pulled tracks featuring Beethoven, and safely create `Work` and `Performance` entities, as well as sanitize the names of the `Track` entities.

## Tech Stack

**Python:** The core language of the project.

**Flask:** The web framework which handles all the web requests of the application.

**Jinja:** The templating language used to render HTML content to the user.

**WTForms:** A framework which allows for easy form creation and user validation, whilst also providing CSRF protection across the application.

**SQL Alchemy:** An ORM framework that allows Python objects to be mapped to an underlying relational database.

**PostgreSQL:** The database which serves the main application.

## Professional Obligations

To read about legal, ethical, and professional matters relating to this project, [please click here](docs/professional_obligations.md).

## Security

For a detailed discussion on risk mitigation strategies, such as OAuth handling and CSRF protection, please read the [security report for this project](docs/security_report.md).

## CI / CD

Currently, this application supports a rudimentary workflow which tests for correct uses of type hinting, PEP 8 formatting and runs all of the automated testing suites upon any push to this repository.