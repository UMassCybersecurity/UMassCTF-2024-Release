# Brutalmogging

---

### User Description

I've been securitymaxxing lately so I increased the key size on my new encryption system. Only securitychads like me can crack it now. Good luck. ;)

---

### Flag

UMASS{1_h4ve_b33n_m3w1ng_f0r_my_l1f3_733061741}

---

### Description

The challenge pads and then encrypts the flag with a feistel cipher based symmetric key block cipher. The cipher's key length is only 16 bits, but it encrypts twice with two different keys for a total of 32 bits. The key is 4 bytes from `os.urandom` The user is then presented with the encrypted flag and allowed to give three queries to an oracle.

### Solution

The intended solution is to realize that although the key appears to be 32 bits long, an un reasonable length, the effective length is only 17 bits, because the cipher is vulnerable to a meet in the middle attack, due to it using the same cipher twice. 17 bits is a reasonable amount of work and with a 3-query oracle, it is possible to conduct use the meet in the middle attack to uncover the key and then decrypt the flag.
