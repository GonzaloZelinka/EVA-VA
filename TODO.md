# Next Steps:

- [x] Set the bases for langchain.
- [ ] Set the different roles and templates for GPT-4/3.5:
  - [x] Request Enhanced role (improve the text generated from Whisper) --> GPT-3.5.
  - [ ] Question and answer role ([search in google the question if we need](https://python.langchain.com/docs/modules/agents/agent_types/chat_conversation_agent)) --> GPT-4.
    - Tools:
      - [ ] [Google Search API](https://developers.google.com/custom-search/v1/overview).
      - [ ] [Wikipedia API](https://pypi.org/project/wikipedia/).
      - [ ] [Wolfram Alpha API](https://pypi.org/project/wolframalpha/).
  - [ ] Reminder/Todo/Meeting role --> GPT-3.5.
    - Tools:
      - [ ] [Google Calendar API](https://developers.google.com/calendar/overview).
  - [ ] Add DataBase Manager Role.
    - Tools:
      - [ ] [Redis](https://redis.io/).
      - [ ] [MongoDB](https://www.mongodb.com/).
  - [ ] Code generation role --> GPT-4.
- [x] Set OpenAI API.
- [ ] Add a talker logic.
- [ ] Add a database to store the user request and responses (memory langchain and Database Role).

## Notes:

- We need to add a agent that can handle a search in a database to find for example the "team" and give the emails and after create the meeting. # Maybe we can use a chain and first we can return a response with a specific format like the persons, the date, the hour, etc. (we can have like a conversation) # and after we can use the response to create the meeting in the calendar that we have in the db.
- The modelResponse should create a instance of the langChain role and create the str final response to the executionController. If it's needed, the modelResponse can use the database to find the information that the user request or google search API, etc.
