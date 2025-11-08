# Windows-EXE-corruptor
This is an easy to use Windows executable corruptor that randomly replaces specific instructions with NOP

You'll need to run the following in CMD to use this:

```
pip install iced_x86
pip install pefile
```

The first time you select a specific executable, it has to generate a list of the instructions in that executable. This can take a while, so be patient!

Instruction lists are named after the executable itself and stored in the same folder. They're formatted like this:

```
{offset} {length} {instruction name}
```

Here's a small example:

```
0x00000600 0x01 push 
0x00000601 0x04 sub 
0x00000605 0x05 mov 
0x0000060a 0x02 cpuid 
0x0000060c 0x03 mov 
0x0000060f 0x03 mov 
0x00000612 0x02 xor 
0x00000614 0x05 mov
```

Screenshot of the program itself:

<img width="635" height="388" alt="image" src="https://github.com/user-attachments/assets/40cd5d29-8ca3-4efc-b2fc-f0438eafd438" />
