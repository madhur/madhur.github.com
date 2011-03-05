---
layout: name
section: Code
title: Code
---


Code
====
This page  contain links to most of the research and non-research
related programming I've done.

<div class="section" markdown="1">
C/C++
=====
Beller
:	Beller is a winsock Application which plays a sound bell on a remote computer on a LAN. 
The aim is to wake up the person sitting there. 
The lists of connected hosts can be configured by the user. 


Error
:	The program shows the error description corresponding to error number using FormatMessage API. 

</div>

<div class="section" markdown="1">
Assembly (DOS)
=====
Buffer
:	The TSR displays the contents of keyboard buffer. Useful for MS-DOS system programmers. 

##Interrupt List Viewer (IView)##
ImpExp displays all the functions imported and exported by the PE file. 
Similar to DUMPBIN /EXPORTS :) 

##TSR Clock##
This is a TSR written in Assembly language to display the clock on the DOS Screen. 

##TSR Screen##
This is a screen saver for DOS. 
</div>

<div class="section" markdown="1">
Assembly (Windows)
=====
##LanTalk##
LANChat is a chatting client which works over the LAN. 
The program uses the Windows Messenger Service 
Works only on Win2000/XP 

Written in: Win32 Assembly 


##FileHeader##
File Header is an explorer shell extension which displays the complete information about the Portable Executable (PE ) file and header for DOS MZ files.. Current version only supports .exe extension. The program is useful for those involved in programming of packers, unpackers as it displays all header fields at a click of button.

##ImpExp##
ImpExp displays all the functions imported and exported by the PE file. 
Similar to DUMPBIN /EXPORTS :) 



##VA2Offset##
	VA2Offset is a nifty utility to convert the virtual address seen under debuggers likesoftice,ollydbg etc to offsets of the file. Virtual address supplied can reside in any of the section or in header of the Portable Executable File. 

Currently the program supports only Portable Executable Files. 
I have tested this program on Win98/2000. 

##Windows Password Revelation##
Demonstrates the use of Hooks in windows. This one shows a simple Mouse Hook to reveal asterisk passwords. 
Although the program runs on all Windows versions, the revelation will occur on only win9x systems 

##Port Scanner##
Port Scanner scans the system's ports and shows the open TCP and UDP ports. 

Written in: Win32(VC++)

##Transparent##
Turn your Desktop Icon's background color to transparent using this cool utility. 
The program remains in memory and consumes very little resources  

</div>

<div class="section" markdown="1">
Perl
=====================
h2inc
:	This is a Perl script to convert c style equates to asm style equates.
	Its an experimental program.
	Comments and suggestions will be appreciated. 

	Written in: Perl 
</div>


<div class="section" markdown="1">
Java
=====================
##Mail##
A mail sender written in Java

##Proxy Server##
A multithreaded proxy server written in Java

</div>



