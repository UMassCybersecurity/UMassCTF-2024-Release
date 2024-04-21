# Krusty Katering

Krusty Katering is hemorrhaging money, and Mr. Krabs has brought you in to fix it.
You have 10 line cooks, and while they're okay at making Krabby patties, they can't agree on who cooks what and when.
To make matters worse, Squidward (trying to keep his job) refuses to give you the list of orders, and will only tell you them one by one.
Each time Squidward tells you a job, you get to add it to a cook's schedule for the day.
Cooks cannot trade jobs, once it's on the schedule, it stays there.
You want to ensure the last order finishes as soon as possible so that Mr. Krabs can close and count his profits.

The competing Plankton's Provisions assigns their jobs randomly.
So long as your crew is 20% more efficient than Team Chum Bucket every day this week, you're hired.
Can you save Mr. Krabs' business?

---

First, players `nc` to an address. The player is given a series of 1000 orders in the following format:

```plaintext
Order
├── Price
└── Estimated time to cook
```

Once the player receives the order, they respond with a number 1-10, representing which cook should be given the job.
This process runs 1000 times, giving each of the 10 cooks a queue of orders.
After all 1000 orders are assigned, each cook's total `Estimated time to cook` is computed (including any downtime).
If the resulting solution is 20% better than the random solution, the player advances to the next day.
If not, the user is told "You're fired.", and the connection is dropped.
This continues for 5 days, and if the player survives the fifth day they are served the flag.

This is a classic online algorithms problem, commonly called the "online job scheduling problem".
Just using greedy algorithms (giving each job to the cook with the smallest queue) is sufficient.
The player just needs the estimated times to cook, the rest of the information can be thrown away.

FLAG: UMASS{subst@nd@rd_c00k}
