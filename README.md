## Goals and Non-Goals

- Spotify Opus is a prototype demonstration of my formal written proposal for the Spotify Platform.
- It will simulate the search functionality for the end user.
- It will allow admin users to perform CRUD operations on composer entities.
- It will provide a means to go about migrating the data to the new model.
- It is not a complete implementation of the Spotify UI. There will not be any actual playback or many of the usual pages such as library, explore etc.
- Not everything will be implemented on the application layer. Data migration will be a data access layer function only via Python scripting.

## Application Views

- Media: The home page. Will display generic results, and search results
- Login: This will be if there's no token present. A simple login button for OAuth
- Album View: This will display a single album
- Composers: This will display the user created composer entities.
- Composer Edit: This will allow a user to add, edit or remove a composer.


## Roadmap

- [x] Create underlying models
- [x] Create a view for logging in
- [x] Create a view for viewing media
- [x] Establish Oauth
- [x] Implement controllers for handling logging in and out, including redirection
- [x] Develop adapter for raw Spotify search data and display results.
- [x] Develop feature for restricting media type.
- [ ] Create template for view of specific album
- [ ] Implement routing to specific album 
