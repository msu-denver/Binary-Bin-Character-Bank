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

# Development Process 

This section should describe, in general terms, how Scrum was applied in the project. Include a table summarizing the division of the project into sprints, the **user story** goals planned for each sprint, the ones actually completed, and the start and end dates of each sprint. You may also add any relevant observations or reflections about the sprints as you see fit.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, ...|mm/dd/23|mm/dd/23|US#1|...|


|Sprint1|Plan out|11/18|11/21|Done|We were trying to decide what do for our project Steve Wanted to do a weather app Malachi wanted to do a character data bank. We decided the data bank would be better |
|Sprint2|Implament/Documentation|11/22|11/28|Done|---|
|Sprint3|Runing code/Uml|12/02|12/04|Done|---|
|Retrospective|Pushing most pf the work |12/06|12/07|Done|---|

As in Project 2, you should take notes on the major Scrum meetings: planning, daily scrums, review, and retrospective. These meetings are essential for tracking progress, identifying obstacles, and ensuring continuous improvement. Use the Scrum folder and the shared templates to record your notes in an organized and consistent manner.

Embed an image of the burndown chart here. 

# Testing 


In this section, share the results of the tests performed to verify the quality of the developed product, including the test coverage relative to the written code. Test coverage indicates how much of your code is exercised by tests, helping assess reliability. There is no minimum coverage requirement, but ensure there is at least some coverage through one white-box test (which examines internal logic and structure) and one black-box test (which validates functionality from the user’s perspective).
