# Connection-Analyser

## How to use:

1) Fill in your email address and password in the script.
2) Run the script on a system (Pi/Server/PC) which should maintain a constant 
internet connection.
3) Check your email and the log file for connection drops :)

### Background:

This small script came about when I was experiencing connection drops with my
 ISP PlusNet. After contacting them through live chat I was told that they 
 only saw my connection drop once in the past 4 days.
 I was SURE this was not the case, so I informed them I would analyse the 
 connection myself and report back to them how many drops I experienced.
 
### What it does:

Ping's Google and/or BBC every 2 seconds to ensure you have a working internet
 connection. If the script fails to get a response, this is logged as a 
 connection drop. If the script fails to get a response for > 30 seconds, then 
 an email is sent to the provided email address with the log as an attachment 
 informing the user of all the drops that have taken place since the script has 
 been running.


 