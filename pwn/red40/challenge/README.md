# Build instructions

```
docker build -t red40 .
docker run --privileged -p1337:1337 red40
```

# Name

red40

# Description

I heard you like RED40

# Flag

`UMASS{r0j0_4d_k33p!n6_y0u_r1ch_4$_h3ck!}`

# Solve

Gamble to leak ppid. Steal to read /proc/ppid/maps to get heap leak of parent. Call `warn` to get printf leak and gets overflow. Then rop to open /proc/ppid/mem, lseek, read, write.
