# Professional Obligations

## Delivery

Launching code into production, whether it be a new feature or an entire application is a multi-faceted, coordinated effort which is inherently time-critical. This application merely represents the prototyping stage of development, however other phases of development include (amongst others):

- Front-end development.
- Proper testing and load-balancing.
- Marketing activities and launch related events.

As such, failure to deliver on time can adversely affect other phases of development, and even lead to launch delays. The consequences of this can be a host of issues including loss of consumer and investor confidence in the product and in the case of 3rd party development leave the developers vulnerable to litigation.

To ensure delivery, a [kanban board](kanban_screenshots/kanban.md) was used to keep track of the project, which enabled efficiency as well as the dynamic scaling of the scope of the project as necessary.

## Maintenance

Given this is merely a prototype, maintenance could be considered irrelevant, as if the change were to be properly implemented in Spotify's architecture, there would already be robust support for data migration. However should the idea of the prototype be expanded in the future, a migration strategy in place will prevent the need to purge any existing data already present within the system.

To that end, the Flask-Migrate library has been used to migrate existing data into any alterations that may be made to the database schema in the future. Flask-Migrate functions by using a migrate command, which automatically detects differences between the current database schema and the state of the database when the command was previously executed. The database can then be upgraded to reflect the current schema.

Whilst many of the changes will be automatically detected, it is often required to manually tweak the upgrade functions, which are written in pure Python and stored in the designated migrations directory.

## Ethical Obligations

All data extracted by the prototype makes use of the Spotify API. Therefore in order for the application to conform to the same ethical guidelines that Spotify enforces, the user merely needs to be authorized by an official Spotify authorization method. This application ensures that any user operating the application be authorized by an Authorization Code Flow, through the use of an endpoint decorator. More information can be found in the security report for this application.

Additionally, this authorization process asks for the minimum scope possible, where only basic information like ID and name are actually obtained in the process. This helps keep more sensitive information such as contact details from being accessed by the application or worse, malicious 3rd-party actors.

As far as storing user data is concerned, the application only stores the unique identifier of administrator users in the persistence layer. Regular user's data is never stored at all, and is only used in the application layer to communicate that the correct user is logged in.

## Legal Obligations

Music copyright and distribution laws are both incredibly nuanced and dense topics, which have a wide variance from country-to-country. Thankfully, since this prototype is not actually producing playback, there is no concern for laws being broken in this area. However, even in the event that *it were* to support playback in the future, legal compliance could still be assured. This is due to the fact that playback would be obtained via the [Playback SDK](https://developer.spotify.com/documentation/web-playback-sdk/) offered by Spotify, which would enforce any relevant laws.

However, there is one additional consideration that needs to be made as a result of the proposed change to the underlying data structure. As part of the new `Composer` entity, there is an optional field that can contain biographical information. This prose would ideally be written by an esteemed academic, and its ownership would need to be clarified as part of a legal agreement.