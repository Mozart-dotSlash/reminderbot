# reminderbot
This is a server side application that runs the telegram bot and responds to requests from vsc clients.

An endpoint that reponds to scheduled tasks from vscode and schedules telegram reminders with the help of cron.
The endpoint has been created with the help of python flask web-framework.
A MongoDB database has been used to store the mappings of user telegram chat IDs to their hashes.
Hashes have been calculated using the SHA-256 cryptographic hash function to enable the security of users.
