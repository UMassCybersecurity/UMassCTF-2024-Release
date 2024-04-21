# Holesome Birthday Party
### You just got invited to Spongebob's birthday! But he's decided to test your friendship with a series of challenges before granting you with the ticket of entrance. Can you prove that you're truly his friend and earn your entrance to this holesome birthday party?

### FLAG: UMASS{B3k3nIwH3rLP0oL~}

### Solve: 
curl http://holesomebirthdayparty.ctf.umasscybersec.org -A "Bikini Bottom" -H "Date: Wed, 14 Jul 2024 07:28:00 GMT" -H "Accept-Language: fr-FR" -H "Cookie: Cookie=chocolate chip cookies; Login=eyJsb2dnZWRpbiI6IHRydWV9"

Change User-Agent to "Bikini Bottom". Add in a header "Date" in the format `"<day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT"` and change day month year to "Jul 14 2024". Set Language to "fr-FR". Add a cookie header pair "Cookie=chocolate chip cookies". Lastly, change the cookie value of "Login" to "{"loggedin": true}" base64 encoded.
