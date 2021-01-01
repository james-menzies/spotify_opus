#Security Report
The following document provides a summary of the potential attacks the application could face, as well as the mitigation techniques that have been applied throughout the code base. 

## Authentication

This application makes use of the official Spotify API in order to populate the prototype's database, which in turn serves as the basis for its search and display functionality. As such, it's important to ensure that any user interfacing with the application be the valid owner of an authentic Spotify account. 

To ensure this, the application verifies the user by using Spotify's [Authorization Code Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow). Once obtained the user is then free to use the application. The following steps have additionally been taken to reduce potential exploits:

- Refresh tokens are completely ignored by application and are not stored. While this requires the user to re-login every hour, it prevents any attacker from indefinitely being able to access a user's Spotify account.
- Access tokens are stored server-side in a Flask session. This prevents an attacker from stealing a token stored as a cookie from cross-site scripting (XSS) or cross-site request forgery (CSRF).
- There are no additional scopes requested in the OAuth process. This means that only basic user information can be obtained via the access token and more sensitive information will be protected. Actions such as playlist manipulation are also not be possible.

## Authorization

As part of the application's requirements, there is full CRUD functionality for the `Composer` entity in the application layer. As this operation should only be performed by an administrator, there needs to be a mechanism to ensure that a regular user cannot access this endpoint.

Therefore, the IDs of an administrator's Spotify's account are stored in a `User` table, and cross referenced when a user tries to access a protected endpoint. This is achieved via a helper decorator, called `VerifyUser`. This decorator is intended to be used in combination with a flask endpoint function and accepts an optional boolean argument for whether the endpoint should be admin-only.

The decorator works the following way:

- Checks to see if there is a token in the current session, if not, redirects to the login page.
- Obtains the user information via the Spotify API.
- If admin is required, checks the obtained ID against the `User` table and obtains the user object if present, otherwise returns a redirect.
- If no admin is required, generates a new User object.
- The endpoint is wrapped, passing both the `User` object and the authorization header dictionary for convenience onto the endpoint.
- The `User` object can also be passed to the templating engine, to enable the display to be dynamically altered based on the privilege level of the user.

There also needs to be the ability to manipulate the underlying database outside of the request context, such as when data is being manually extracted and manipulated. The [`VerifyUser`](../spotify_opus/services/oauth_service.py) decorator has been enhanced such that when the code being run is outside of this context, administrator access is implicitly granted. This is achieved by manually storing an administrator refresh token as an environment variable. By utilizing this strategy, data manipulation can still occur outside of the application, but with the protection of interfacing with the database via an ORM, rather than through raw SQL.

Given that it is impossible for an outside user to access the application outside of Flask's request context, there is no security vulnerability as a result.

## Form Safety

Even though creating and editing a Composer is an admin-only operation, there are still measures being taken to ensure data-integrity and security:

**Data Layer:**  Unique and Not Null constraints are applied to `Composer` fields to ensure entities are not partially instantiated.

**Business Layer:** The application make use of SQL Alchemy's ORM capability as a higher-level abstraction when interfacing with the database layer. A python object `Composer` is created, which is an extended class of the Flask-Alchemy library, which is subsequently committed to the database. This will sanitize user input, preventing attacks such as SQL injection.

**Application Layer**: The WTForms library is used to generate the application's forms, where HTML form data is automatically generated based off the `Composer` entity model. While this affords a redundant layer of protection against SQL injection attacks, it also improves the front-end experience for the user by providing real-time validation of input.

**CSRF protection:** Cross-site request forgery occurs when an attacker intercepts an HTTP request and attempts to inject their own form data in place of the user's data. Flask-WTF provides a utility called CSRFProtect, which will automatically generate 401 errors for any form using a POST submit that does not have valid CSRF protection. This application makes use of that module, and manually includes an invisible CSRF token in all of its forms.

## Database Backup

As part of the application's assignment brief, it is a requirement that the entire database be able to be exported, via raw SQL, and exposed as front-end facing endpoint. Whilst this functionality is largely against the philosophy of the application's security counter-measures, the following steps have been taken to keep this potentially dangerous mechanism as safe as possible:

- The endpoint can only be accessed by an administrator.
- The endpoint does not accept any input, the SQL is generated only from the server side of the application.
- The endpoint generates the backup and stores it on the server, rather than sending it over the wire. This means that the data can only be accessed by one with server access. The application will merely communicate that the data has been successfully backed up to the user.