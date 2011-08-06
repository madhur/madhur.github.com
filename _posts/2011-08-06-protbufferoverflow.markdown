---
layout: blog-post
title: "Protections against buffer overflow exploits in Linux"
excerpt: Protections against buffer overflow exploits in Linux
disqus_id: /2011/08/06/protbufferoverflow/
location: New Delhi, India
time: 11:00 AM
categories:
- Security
- Exploits
---

#{{ page.title }}

Linux has several inbuilt protection mechanisms to deal with malicious buffer overflow attacks. Some of them are built into kernel
while some of them are part of compiler tools such as gcc, g++. 
* Address space Layout Randomization (Kernel)
* Executable Stack Protection (Compiler)
* Stack smashing protection (Compiler)

**[Address Space Randomization](http://en.wikipedia.org/wiki/Address_space_layout_randomization)** is a technique in which various parts of executable such as data, stack and code are randomly given start addresses whenever a program starts. This makes difficult for an attacker to guess let's stay the base of stack in order for him to successfully launch the buffer overflow attack. ASLR can be disabled in linux with the following command

{% highlight bash %}
madhur@bt:~/buffer$ sudo echo 0 > /proc/sys/kernel/randomize_va_space
{% endhighlight %}

To reneable just echo it with a positive integer, for ex

{% highlight bash %}
madhur@bt:~/buffer$ sudo echo 2 > /proc/sys/kernel/randomize_va_space
{% endhighlight %}

**[Executable Stack Protection ](http://en.wikipedia.org/wiki/Executable_space_protection)** is another technique of preventing buffer overflow attacks. As a result of this protection, the stack portion of the memory is marked non executable. To check if the stack is executable or not, run the following command

{% highlight bash %}
madhur@bt:~/buffer$ readelf -l <filename>

Elf file type is EXEC (Executable file)
Entry point 0x8048330
There are 8 program headers, starting at offset 52

Program Headers:
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  PHDR           0x000034 0x08048034 0x08048034 0x00100 0x00100 R E 0x4
  INTERP         0x000134 0x08048134 0x08048134 0x00013 0x00013 R   0x1
      [Requesting program interpreter: /lib/ld-linux.so.2]
  LOAD           0x000000 0x08048000 0x08048000 0x004e4 0x004e4 R E 0x1000
  LOAD           0x000f0c 0x08049f0c 0x08049f0c 0x00108 0x00110 RW  0x1000
  DYNAMIC        0x000f20 0x08049f20 0x08049f20 0x000d0 0x000d0 RW  0x4
  NOTE           0x000148 0x08048148 0x08048148 0x00044 0x00044 R   0x4
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x4
  GNU_RELRO      0x000f0c 0x08049f0c 0x08049f0c 0x000f4 0x000f4 R   0x1

 Section to Segment mapping:
  Segment Sections...
   00     
   01     .interp 
   02     .interp .note.ABI-tag .note.gnu.build-id .hash .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rel.dyn .rel.plt .init .plt .text .fini .rodata .eh_frame 
   03     .ctors .dtors .jcr .dynamic .got .got.plt .data .bss 
   04     .dynamic 
   05     .note.ABI-tag .note.gnu.build-id 
   06     
   07     .ctors .dtors .jcr .dynamic .got 
{% endhighlight %}

The following line , shows that stack is Read Write but not executable
{% highlight bash %}
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW 0x4
{% endhighlight %}

In order to make the stack executable, the program needs to be compiled with ***-z execstack*** option
{% highlight bash %}
madhur@bt:~/buffer$ gcc -ggdb -m32 -z execstack -o buffer1 buffer1.c
{% endhighlight %}

In that case, the output of ***readelf*** program would be 

{% highlight bash %}
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
{% endhighlight %}

**[Stack smashing protection](http://en.wikipedia.org/wiki/Stack-smashing_protection)** refers to compiler generated protection techniques of smash stacking. Refer to wikipedia link to get more details about the techniques involved in this protection. This can be disabled in gcc as follows:

{% highlight bash %}
madhur@bt:~/buffer$ gcc -ggdb -m32 -o buffer1 -fno-stack-protector -mpreferred-stack-boundary=4 buffer1.c
{% endhighlight %}


