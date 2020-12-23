Recently, I published an case study on Spotify's technological infrastructure. Within it I raised the notion of altering the underlying data structure so that it could cater better for consumers of classical music. This repository is a rudimentary full stack prototype of the data model proposed in that case study, as well as a small demonstration of the front end features that it could enable.

I would highly recommend reading the case study before browsing the rest of this project, in particular sections R7 - R9.

## The Data Structure

When implementing the new data model, there were some necessary compromises and alterations from the original vision, either due to keeping the scope of the project manageable or practical considerations during implementation. The revised scheme is below:

### Notes

- The super type entity `ContextObject` has been abandoned due to complications with implementing inheritance in a database.
- As the front end application will support browing by composer, the `Composer` entity has been added to assist creating the initial `GET` request as the entry point of the application.
- Similar to `Composer`, the `Performance` entity has been added to facilitate the selection of performances of the same work.
- Infinite nesting of `SubSection` entities within works has been abandoned.

## Features

### Searching

Typically a user listening to classical music will want to search for a specific piece of music, which can be cumbersome to achieve with the existing Spotify model. This application supports searching for music via the following progression: 

This application enables that progression via the new data model and its endpoints.

### Listening

When on a page where playback occurs, the track listings are aggregated by work and section, rather than simply track-by-track.

## Pages

### Login Screen

To use Spotify Opus, the user needs to sign in through Spotify's official authorization flow. Once completed, the user will be able to use the application for an hour in order to browse the demonstration before requiring another log in. 

This is to mitigate any potential security concerns as a result of refresh tokens being stored server side.

`/login`

### Composers

If the signed on user is an administrator, there will also be controls to add or edit composer entities.

`/composers`

### Composer Edit

A simple form to create or alter a `Composer` entity. When adding a composer, the name must exactly match an existing record in the Spotify database or the create operation will fail.

`/composers/create`

`/composers/edit`

### Works

`/composers/{id}/works`

### Performance

`/works/{id}/performances`

### Playback

`/performances/{id}`

## Migration Techniques

### Data Extraction

Since all data being used is stored natively by the application, there is a need to pull the data from the Spotify API to populate the `Album`, `Artist` and `Track` entities. This is done as a batch operation by the program, where all of the `Album` entities which feature a track by a desired composer, along with their related `Artist` and `Track` entities.

In order to extract data for a single composer, the following steps need to take place.

1. Create a `Composer` entity via the front end of the application as an administrator.
2. Obtain the ID of the `Composer` entity.
3. Then on the back end server running the application, run the following command:

```jsx
flask manage pull {composer_id} 
```

This operation can take some time, due to the nature of how Spotify paginates its requests. However the CLI will inform the administrator about the progress as the import takes place.

### Data Parsing

(to be completed) 

## Tech Stack

**Python:** The core language of the project.

**Flask:** The web framework which handles all the web requests of the application.

**Jinja:** The templating language used to render HTML content to the user.

**WTForms:** A framework which allows for easy form creation and user validation, whilst also providing CSRF protection across the application.

**SQL Alchemy:** An ORM framework that allows Python objects to be mapped to an underlying relational database.

**PostgreSQL:** The database which serves the main application.

## Professional Obligations

To read about legal, ethical, and professional matters relating to this project, please click here.

## Security

For a detailed discussion on risk mitigation strategies, such as OAuth handling and CSRF protection, please read the security report for this project.

## CI / CD

Currently, this application supports a rudimentary workflow which tests for correct uses of type hinting, PEP 8 formatting and runs all of the automated testing suites upon any push to this repository.