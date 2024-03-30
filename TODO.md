# Next Steps:

- [ ] Create a API format, to receive and audio, decodify, sent to the model, and return the response in text, initially. After we can create a response in audio.

- [x] Set the bases for langchain.
- [ ] Set the different roles and templates for GPT-4/3.5:
  - [x] Request Enhanced role (improve the text generated from Whisper) --> GPT-4.
  - [ ] Question and answer role.
    - [x] General response from GPT-4.
    - [x] [Search in google the question if we need](https://serper.dev/dashboard).
    - [x] Implement LLMMathChain (math questions).
    - [ ] Specific questions about concepts ([use wikipedia API](https://pypi.org/project/wikipedia/)).
    - [ ] Use Memory/Retrivers to store and reuse the results ([Redis](https://redis.io/)).
  - [ ] Reminder/Todo/Meeting role --> GPT-3.5.
    - [ ] [Add a calendar API](https://developers.google.com/calendar/overview).
    - [ ] Add create, edit, delete, search [custom Tools](https://python.langchain.com/docs/modules/agents/tools/custom_tools).
    - Tools:
      - [ ] [Redis](https://redis.io/).
      - [ ] [MongoDB](https://www.mongodb.com/).
  - [ ] Code generation role --> GPT-4.
  - [ ] Send messages role --> GPT-3.5.
- [x] Set OpenAI API.
- [x] Add a talker logic.
- [ ] Add a database to store the user request and responses (memory langchain and Database Role).

## Notes:

- We need to add a agent that can handle a search in a database to find for example the "team" and give the emails and after create the meeting. # Maybe we can use a chain and first we can return a response with a specific format like the persons, the date, the hour, etc. (we can have like a conversation) # and after we can use the response to create the meeting in the calendar that we have in the db.
- The modelResponse should create a instance of the langChain role and create the str final response to the executionController. If it's needed, the modelResponse can use the database to find the information that the user request or google search API, etc.
- https://python.langchain.com/docs/guides/expression_language/cookbook#router check this to create a router to identify the subtasks.
