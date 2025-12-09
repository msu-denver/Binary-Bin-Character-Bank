# Overview



This application is known as the Character Bank. It was developed to help new d&d players and DM's get ideas for characters. The character bank allows users to create a bare bones D&D 2024 edition, also sometimes referred to as D&D 5.5e, character for a quick speed up for final character creation. For players this might give them ideas for new characters while for DMs this is a good way to make template characters for people that are new to their table and to dungeons and dragons.

# Design

## User Stories

# User Story 1
As a user, I want to be able to make a D&D character so that I can be prepared for future campaigns.

# User Story 2
As a user, I want to be able to view other user's character creations so that I can be inspired for my personal characters

# User Story 3
As a user, I want to be able to view all of the characters I have made, private and public, so that I can have a list of characters to choose from for making a balanced party dynamic.

# User Story 4
As a user, I want to be able to edit my characters so that I can fix any mistakes I may have previously made.

# User Story 5
As a user, I want to be able to copy interesting character ideas from the community bank so that I can fine tune the character idea towards my playstyle

# User Story 6
As a user, I want to be able to delete a character so that my personal character bank doesn't get over crowded.



## Sequence Diagram
Below is a sequence diagram for character creation:

sequenceDiagram
    actor User
    participant UI as Web UI
    participant Server as Backend
    participant DB as Database

    User->>UI: Click "Create Character"
    UI->>Server: Request character creation page
    Server->>UI: Send HTML creation form
    UI-->>User: Display form

    User->>UI: Fill form and click Submit
    UI->>Server: POST character data
    Server->>DB: Insert new character record
    DB-->>Server: Insert success
    Server-->>UI: Redirect to dashboard
    UI-->>User: Show dashboard


## Model 

Include a **class diagram** that clearly describes the **model classes** used in the project and their associations. A **class diagram** is a UML diagram that represents the structure of the system by showing its classes, their attributes, methods, and the relationships between them (such as inheritance, aggregation, or composition). This helps visualize how the data and logic are organized within the application.
+----------------+
| User           |------------------>
+----------------+
|UserName        |
|Password        |
|Id              |
+----------------+
# Development Process 

This section should describe, in general terms, how Scrum was applied in the project. Include a table summarizing the division of the project into sprints, the **user story** goals planned for each sprint, the ones actually completed, and the start and end dates of each sprint. You may also add any relevant observations or reflections about the sprints as you see fit.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, ...|mm/dd/23|mm/dd/23|US#1|...|
|1|US#1: Planout, Create Login|11/18/25|11/22/25|US#1|User Login done|
|2|US#2,3,4:Ceate Characters, store, view others users characters|11/22/25|11/28/25|US#2,3,4|Work compelete code ran well|
|3|US#5.6,7:testing,fix usecase, finsish notes|12/02/25|12/08/25|US#5,6,7|Testing was done, notes were compelete ready to push|






As in Project 2, you should take notes on the major Scrum meetings: planning, daily scrums, review, and retrospective. These meetings are essential for tracking progress, identifying obstacles, and ensuring continuous improvement. Use the Scrum folder and the shared templates to record your notes in an organized and consistent manner.

Embed an image of the burndown chart here. <img width="1376" height="567" alt="Screenshot 2025-12-08 at 12 11 25 PM" src="https://github.com/user-attachments/assets/fb0f5c85-1fb8-492d-aaad-697a4195b494" />


# Testing 


To make sure that the Charcater data bank worked well and functioned well. Black box and white box testing were tools and methods we used to ensure our application worked corrctly.
Testing makes surethat user is fucntion and interal appilcation logic works well.
Black box testing was written using selenium webdriver so that it can simulate a user interaction in the web application. 

The registration test:
Open the register page
Enter username
Enter
Validate the registration

Duplicate username Test:
Attempted to put the same username 
The application gave a waring with .flash-danger to make sure that the user was informed about the username

Both test were passed

White box testing was written with python unittest to be able to test the internal register_user() function.

The following was tested:

Empty username,

Empty password,

Existing username,

Valid new user,

These test will help to make sure all of the logics for the registration is valid and works well. And will return to the user the issues there is.






