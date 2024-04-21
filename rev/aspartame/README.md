# Aspartame

## Description:

Just because you can, doesn't mean you should.

## Hint 1:

```
There are two ways to run the challenge.

1. Boot the game by having a FAT32-formatted USB, then at the root of the storage add the file to `efi/boot/bootx64.efi`.

2. Run using [QEMU](https://www.qemu.org/download/).
First, download [OVMF prebuilt](https://www.kraxel.org/repos/jenkins/edk2/edk2.git-ovmf-x64-0-20220719.209.gf0064ac3af.EOL.no.nore.updates.noarch.rpm) and extract `OVMF-pure-efi.fd` from the archive in path `.\usr\share\edk2.git\ovmf-x64\`.
You can then start the game by executing `qemu-system-x86_64 -m 256M -bios OVMF-pure-efi.fd -kernel bootx64.efi`.
```

## Hint 2:

```
You should try winning the game.
```

## Flag:

```
UMASS{H3y,as_10ng_as_it_vv0rks}
```

## Internal Description:

A tetris game running in UEFI.

## Solve:

First, reverse the binary to find out the winning condition.
Looking at the strings, we can find "You win" text in the game.
Locating the text references is quite annoying since the text is in UTF16LE
and it is addressed as part of a struct.

Here we should see the condition before the text is printed:
Drop at least 69 pieces and the game area does not have any line that contains
tetrominos (basically, PC or Perfect Clear).

After knowing the fact, we either play the game or reverse the code after the "You win".

If we reverse the code after "You win", we should see a while loop that read an array,
bitshfiting and printing out `#`, ` `, and `\n`. Concatnating the output, we should see
the QR code.

It is possible to play the game, since by observation, the random seed is always the
same so the tetromino sequences is deterministic. The QR-encoded flag should be printed out on the screen.
