
# Free Delivery

Mr. Krabs has decided to make a new food delivery app for the Krusty Krab but Plankton decided to make his own patched version. Loyal Krusty Krab customers are saying weird network traffic and shell commands are coming from the app! Can you figure out what's going on?

---

FLAG: UMASS{0ur_d3l1v3ry_squ1d_w1ll_br1ng_1t_r1ght_0ver_!}

---

Basically it's suppose to do some malware-like things and contains two parts for the flag. The Main Activity does HTTP data exfiltration of the MAC Address, Device Name, and the first-half flag which are all base64 encoded and XORed before being exfiltrated. The second flag is in Native code and in the "system" call which can be obtained by unzipping the APK, going into the lib folder and analyzing what is sent to the system call in libfreedelivery.so. For the second part, dynamic analysis is needed and Frida is used to hook anti-debugging/emulation functions that cause the app to crash and see the flag string that is sent to the system call. Some elements in the challenge include proguard obfuscation and anti-debugger/emulation checks.
