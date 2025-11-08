# Windows-EXE-corruptor
This is an easy to use Windows executable+dll corruptor that randomly replaces specific instructions with NOP

This was written with Python 3.14.0

## Please read these first few sections before proceeding to the later ones.

Back up your game/program's save data and any important files before using this (maybe even use it in a VM for extra safety)

# DO NOT USE THIS ON ONLINE GAME EXECUTABLES! 
This is the most important warning. 

- You could send garbage data to the servers
- You could damage someone else's hardware depending on what the corruptor hits
- You could get yourself banned
- You could get others banned
- You could set a bad example and get either you or me into legal trouble if others copy you

If a game or program has online functionality (such as error reporting, leaderboards, collection of user info), be sure to block it from accessing the internet in the Windows firewall.

# Setup
You'll need to run the following in CMD to use this (be sure to enable the PATH option while installing Python!):

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

# Additional info
If you get a permission error, that's either because the file you're corrupting is in a folder that's read only, the script is in a location that's read only and it can't generate backups, or the file you're trying to corrupt is open and a program needs to be closed.

This is highly unlikely to work on Unity games unless they use IL2CPP.

Games are still highly likely to crash when corrupting them with this. Keep lowering the intensity until you start getting stable results.

16-Bit games aren't supported... Yet. I might add support for them at some point in the future, but don't expect them to work any time soon.

The default targets (the instructions we replace) are all floating point-related and very unlikely to damage your system. Only change them if you know what you're doing!
