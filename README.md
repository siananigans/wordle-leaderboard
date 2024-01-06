# wordle-leaderboard
A python web app to keep track of scores on the New York Times "Wordle" game. 

```mermaid
sequenceDiagram
  participant server
  participant wordleResultsEmail
  participant AaronEmail
  server->>wordleResultsEmail: do you have any emails from x, y, z?
  wordleResultsEmail-->>server: Emails
  server->>wordleResultsEmail: Can I have yesterdays results?
  wordleResultsEmail-->>: Yesterdays results email.
  server->>wordleResultsEmail: Here are todays results
  wordleResultsEmail->>AaronEmail: Results
```
