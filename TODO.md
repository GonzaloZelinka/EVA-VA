# Next Steps:

- [x] Set the bases for langchain.
- [x] Request Enhanced role (improve the text generated from Whisper) --> GPT-4.
- [x] Create a API format, to receive and audio, decodify, sent to the model, and return the response in text, initially. After we can create a response in audio.
- [ ] Create a ChainCreator for analize the monthly income, expenditure and investments
- [ ] ToDoChainCreator.
  - [ ] Add create, edit, delete, search [custom Tools](https://python.langchain.com/docs/modules/agents/tools/custom_tools).
- [ ] Q_AChainCreator.
  - [x] Implement LLMMathChain (math questions).
  - [ ] Specific questions about concepts ([use wikipedia API](https://pypi.org/project/wikipedia/)).
  - [ ] Use Memory/Retrivers to store and reuse the results ([Redis](https://redis.io/)).
- [ ] Create MeetingChainCreator.
  - [ ] [Add a calendar API](https://developers.google.com/calendar/overview).
  - [ ] Add create, edit, delete, search [custom Tools](https://python.langchain.com/docs/modules/agents/tools/custom_tools).
  - [ ] Use vector database to search for the team members to add in the meeting.
- [x] ErrorChainCreator.
  - [x] handle error Schema.
- [x] Set OpenAI API.
- [x] Add a talker logic.
- [ ] Add a database to store the user request and responses (memory langchain and Database Role).

## Notes:

- We need to add a agent that can handle a search in a database to find for example the "team" and give the emails and after create the meeting. # Maybe we can use a chain and first we can return a response with a specific format like the persons, the date, the hour, etc. (we can have like a conversation) # and after we can use the response to create the meeting in the calendar that we have in the db.
