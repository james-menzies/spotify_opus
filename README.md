## Goals and Non-Goals

- Spotify Opus is a prototype demonstration of my formal written proposal for the Spotify Platform.
- It will simulate the search functionality for the end user.
- It will allow users to create and modify their own work entities.
- It will provide an example of how to migrate the existing Spotify data
- It is not a complete implementation of the Spotify UI. There will not be any actual playback or many of the usual pages such as library, explore etc.
- Not everything will be implemented on the application layer. Data migration will be a data access layer function only via Python scripting.

## Application Views

- Media: The home page. Will display generic results, and search results
- Login: This will be if there's no token present. A simple login button for OAuth
- Album View: This will display a single album
- Work View: This will display authored works to the user
- Work Edit: This will contain a form to edit a work.

## Roadmap

- [x]  Create underlying models
- [ ]  Create the media view
- [ ]  Create the main display view
- [ ]  Implement OAuth
- [ ]  Integrate the search funtion to integrate
- [ ]  Write a script that migrates the Beethoven repertoire
