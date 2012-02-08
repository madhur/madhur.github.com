---
layout: blog-post
title: "Using MakeFile with Assembly Programming"
excerpt: "Using MakeFile with Assembly Programming"
disqus_id: /2012/02/08/makefileassembly/
location: New Delhi, India
time: 8:00 PM
tags:
- Assembly
- MASM
---


I have been a big fan of assembly programming since my old school days. The raw power of CPU which you get is just pure awesome.
But, with that power, you also get much headache of non-availablity of standard IDE's for using Assembly language.

* Visual Studio is one of the options, but it restricts you to the installed version of Microsoft Macro Assembler (ml.exe)

* Some prefer using QEditor.exe which ships with [MASM32 SDK](http://masm32.com)

* Some like me, just cannot stay away from there favourite editors such as Notepad++, Ultraedit etc.

The benefit of using editors such as Notepad++, Ultraedit is that you get fully customizable syntax highlighting and command line tools
to be used while assembling and linking their programs. However, with these tools you have to add commands to both assemble and link your programs. And if you are like me,
who fiddles with 16bit, 32bit and 64 bit assembly programs, you have to add seperate commands for them. And not to forget, seperate commands for outputting debug and release binaries as well.

To simplify the above process, I have been exploring the use of makefiles to assemble and link my programs and this has worked wonderfully well. I just maintain my each assembly project in seperate directory with the makefile
and use that as a command to assembly and link the program from [Notepad++], using [NppExec plugin]. Apart from Notepad++, I am using following tools as my development environment. You might be using different, but they can be applied in same concept.

1. NMAKE(nmake.exe) v10.00.30319.01 which ships with Visual Studio 2010 available [here](http://www.microsoft.com/visualstudio/en-in)
2. Borland Resource compiler (brcc32.exe) v4.50 which ships with Borland compiler tools available somewhere on the net
3. Microsoft Macro Assembler(ml.exe) v6.14 and Linker (link.exe) v5.12 which ships with Masm 32 SDK available [here](http://www.masm32.com/)

Note that all the above tools should be put preferable in the PATH variable for easy access. I do this by creating a simple command script as follows:

{% highlight text %}
setx PATH "f:\common tools\git\bin;f:\common tools\python\app;f:\common tools\python\app\scripts;f:\common tools\ruby\bin;f:\masm32\bin;F:\Borland\BCC55\Bin;"
{% endhighlight %}	

I am going to show you some scenarios here on how I am using Makefiles to assemble and link my programs. Note that this is not a tutorial for using makefiles. I assume you have some basic familiarity with it. If not, you can 
browse some excellent tutorials [here](http://web.sau.edu/lilliskevinm/csci240/masmdocs/envtools/26LMAETC16.pdf) and [here](http://webster.cs.ucr.edu/AoA/DOS/ch08/CH08-10.html#HEADING10-131).

* A Win32 Assembly program without the use of resources:

{% highlight makefile %}
MASMPATH=F:\MASM32
ML=ml
DEBUG = 1
!IF $(DEBUG)==1
CFLAGS=/c /coff /Zd /Zi /Fl /Sn /nologo /I
!ELSE
CFLAGS=/c /coff /Fl /Sn /nologo /I
!ENDIF
LDFLAGS=
SOURCES=trans.asm
OBJECTS=$(SOURCES:.asm=.obj)
PROJ=trans.exe


$(PROJ): $(OBJECTS)
	link /NOLOGO /SUBSYSTEM:WINDOWS /LIBPATH:$(MASMPATH)\LIB $(OBJECTS)
	
$(OBJECTS): $(SOURCES)
	$(ML) $(CFLAGS) $(MASMPATH)\include $(SOURCES) 
	
clean:
	del *.exe
	del *.obj
	del *.lst
{% endhighlight %}		


* A win32 Assembly program with the use of resources:

{% highlight makefile %}
MASMPATH=F:\MASM32
ML=ml
DEBUG = 1
!IF $(DEBUG)==1
CFLAGS=/c /coff /Zd /Zi /Fl /Sn /nologo /I
!ELSE
CFLAGS=/c /coff /Fl /Sn /nologo /I
!ENDIF
LDFLAGS=
SOURCES=vaoffset.asm
RESOURCES=vaoffset.rc
OBJECTS=$(SOURCES:.asm=.obj) vaoffset.res
PROJ=vaoffset.exe


$(PROJ): $(OBJECTS)
	link /NOLOGO /SUBSYSTEM:WINDOWS /LIBPATH:$(MASMPATH)\LIB /LIBPATH:f:\projects\programs\winsock\netsend $(OBJECTS)
	
$(OBJECTS): $(SOURCES)
	$(ML) $(CFLAGS) $(MASMPATH)\include $(SOURCES) 
	C:\Borland\BCC55\Bin\brcc32.exe vaoffset.rc
	
	
clean:
	del *.exe
	del *.obj
	del *.lst
	
{% endhighlight %}			



Now, Provided **NMAKE** is in your path variable, you can simply set a command in Notepad++ or in your favourite text editor to invoke nmake in current directory.

{% highlight text %}
F:\projects\programs\WIN32ASM\transparent>nmake /U

Microsoft (R) Program Maintenance Utility Version 10.00.30319.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        ml /c /coff /Zd /Zi /Fl /Sn /nologo /I F:\MASM32\include trans.asm
 Assembling: trans.asm
        link /NOLOGO /SUBSYSTEM:WINDOWS /LIBPATH:F:\MASM32\LIB trans.obj
{% endhighlight %}	

And to clean the output,

{% highlight text %}
F:\projects\programs\WIN32ASM\transparent>nmake clean

Microsoft (R) Program Maintenance Utility Version 10.00.30319.01
Copyright (C) Microsoft Corporation.  All rights reserved.

        del *.exe
        del *.obj
        del *.lst		
{% endhighlight %}			