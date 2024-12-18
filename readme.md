
# Event Management System -----


Project Overview:-

The Event Management System is a feature-rich web application created to make event planning, registration, and administration easier.

## Features: User Features

Authentication and User Registration
Event Search and Filtering Event Browsing
Registration for the Event

## Features for the Administrator

Organizing Events
Editing Events
Deletion of Events
Opening and closing an event for registration

## Utilized Backend Technologies


Python as the language and Flask as the web framework
Authentication: Bcrypt Flask
Database: PyODBC Database Connector: Microsoft SQL Server

### Front-end

JavaScript, CSS3, HTML5,Bootstrap
### Safety

Hashing of the Bcrypt Password for Session-based Authentication
CSRF Defense



###### DIFFERENT IMPORTANT ROUTES


# 1. User Registration Route (/sign_up_user) :- 
Important attributes:

takes user registration information
uses Bcrypt to securely hash passwords and stores user data in a database.
returns a message indicating success or failure.

# 2. User Login Route (/userLogin)

verifies the user's credentials
uses Bcrypt to verify the password.
establishes a user session
Addresses login issues
takes you to the relevant page.

# 3. Event Search Route (/search_events)
Look up events by date or name.
Adaptable filtering
returns events that match

# 4. Event Registration Route (/register_event)
Verified registration
Avoids duplicate registrations
keeps track of the registration time.
Addresses issues with registration

# 5.Admin Event Management Route (/admin/events)
Administrator-only access
Make new occasions
Get the current events
All-inclusive event coordination

# 6. Event Status Update Route (/update_event_status)
Change whether an event is open or closed.
Admin-only change
Rapid control of event status


