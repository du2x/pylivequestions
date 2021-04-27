PyLiveQuestions
==========

Let your questions be answered in sync with your desire.

Inside the room you create, you can pick the question you want to be answered by the other in the room, and you can give the feedback whenever you want.

There will be always only one CURRENT question in a room. FOCUS guys!

Create room
----
The UI lacks functionality for creating room. You can create with:

```
curl 'https://b5i7oe5cjg.execute-api.us-east-1.amazonaws.com/dev/rooms' --request POST --data '{"name":"Cool room name"}' -H "Authorization: Bearer $TOKEN"
```

The room created can be managed only by you. And the attempts made in your room will be only available to you.


Pick Question
----
When you enter in a room which you are creator, you will be able to Pick Questions. When you click the Pick Question button, the choosen question will be automatically be shown to the other users in the room.

When a question is answered by someone, you get his information instataniously in the room screen.


Show feedback
----
When you think there were time enougth to the others answer the current question, you can pick another question, or show feedback to the others by clicking "Show feedback" button. (Feedback is a text that comes along with the options of the question data)


Close Room
------

When you end your use of the room, it is appropriate that you close it.

The UI lacks functionality for closing room. You can create with:
```
curl 'https://b5i7oe5cjg.execute-api.us-east-1.amazonaws.com/dev/rooms' --request POST --data '{"name":"Cool room name"}' -H "Authorization: Bearer $TOKEN"
```

System design notes
=========

This app was made aiming learning goals, so I tried to use interesting serverless system components, like websockets and dynamodb streams, and not necessarily I think those decision are the best to this kind of app.

First, let's talk about persistence. 

Dynamodb Design
-----

This app has 4 strong entities: user; room; question and attempts. The user entity is not a concern, because its management was delegated to the **Cognito** User Pool service.

So, there are rooms, questions and attempts to be stored. We are using dynamodb, a NoSQL database. So we have to design it's Keys (PARTITION KEY and SORT KEY) by analising data access patterns. By doing, I got the following data queries:

- query all rooms
- query all questions
- query room by room id.
- query active question on room. 
- query attempts for a question in a room.
- query attempts for a question.  (this case is not explored yet)


So I came up with the following key design:

Room: (PK=Room, SK=Room#[roomid]).
Thus, I can query all rooms using only PK, and query room by room id.

Question: (PK=Question, SK=Question#[questionuiid]). Same as Room.
But about question, there is a gotcha.  The same question can be in many rooms. So, I created the concept of QuestionInRoom: When a Question is picket for a Room, it will be copied into a QuentionInRoom concept, which will be stored with the following Keys: 

QuestionInRoom: (PK=QUESTION#ROOM#[roomName], SK=pickedAt) So, I can query the active question on a room by using the roomName of PK and getting the higher "pickedAt" QuestionInRoom - the active question will be always the last picked.

Attempts: (PK: Attempt#Question#[questionuuid], SK:Room#[roomid]) Thus, I can query by room and questionuuid, or just by questionuuid.

WebSockets
---------

The live part of pylivequestion is provided by WebSockets connections. 
When someone enters on a room a websocket connection is stabilished and when events occur, that connection receives messages and the UI responds accordingly.

When the user connects, it will stabilish a connection with the AWS Apigateway on the wss endpoint. Follows the trigger a lambda on the $connect route. This lambda will persist the connection on dynamodb.
When a connection ends, a trigger to $disconnect will fire another lambda, that will delete the connection by connection_id.
And yes, one more "entity" to be stored.


Dynamodb Stream
-----------

The connections will receive messages as the events occurs on the app.
The events are: 
- new attempt - triggers message to room owner.
- new question picked on room - triggers message to users on room.
- room action to show feedback - triggers message to users on room.

So, I need to query the connection in two ways:
- by room
- by connection_id (when disconnect)_

Here is its key design:

WSConnection: (PK: Connection#Room#[roomid], SK: Connection#[connectionid]) and GSI on connectionid


Tracing
--------------
The tracing was enabled by using aws-xray-sdk python package on dynamodb stream triggered lambda (the most "complex" one).

Layered architecture
------
I tried to separate the layers of business and domain, of the persistense logic and other presentation. I also organized the many lambda by the event that triggers them.

Issues
----------
There are many frontend issues, as I am a hookie on react and a noob on UI. The most worse one is when token expires and the app can't handle it. So you need to go back to the root and refresh. 

There are issues on deleting connections also, I am working on it.

Future
----
I'll make this my pet project. :)