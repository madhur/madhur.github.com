---
layout: blog-post
title: "Protections against buffer overflow exploits in Linux"
excerpt: Protections against buffer overflow exploits in Linux
disqus_id: /2011/08/06/protbufferoverflow/
location: New Delhi, India
time: 11:00 AM
tags:
- Security
- Exploits
---



Linux has several inbuilt protection mechanisms to deal with malicious buffer overflow attacks. Some of them are built into kernel
while some of them are part of compiler tools such as gcc, g++. 
* Address space Layout Randomization (Kernel)
* Executable Stack Protection (Compiler)
* Stack smashing protection (Compiler)
* Position Independent Executables (Compiler)
* Fortify Source (Compiler)
* Stack Protector (Compiler)   

**[Address Space Randomization](http://en.wikipedia.org/wiki/Address_space_layout_randomization)** is a technique in which various parts of executable such as data, stack and code are randomly given start addresses whenever a program starts. This makes difficult for an attacker to guess let's stay the base of stack in order for him to successfully launch the buffer overflow attack. ASLR can be disabled in linux with the following command

{% highlight text %}
madhur@bt:~/buffer$ sudo echo 0 > /proc/sys/kernel/randomize_va_space
{% endhighlight %}

To reneable just echo it with a positive integer, for ex

{% highlight text %}
madhur@bt:~/buffer$ sudo echo 2 > /proc/sys/kernel/randomize_va_space
{% endhighlight %}

**[Executable Stack Protection ](http://en.wikipedia.org/wiki/Executable_space_protection)** is another technique of preventing buffer overflow attacks. As a result of this protection, the stack portion of the memory is marked non executable. To check if the stack is executable or not, run the following command

{% highlight text %}
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
{% highlight text %}
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW 0x4
{% endhighlight %}

In order to make the stack executable, the program needs to be compiled with ***-z execstack*** option
{% highlight text %}
madhur@bt:~/buffer$ gcc -ggdb -m32 -z execstack -o buffer1 buffer1.c
{% endhighlight %}

In that case, the output of ***readelf*** program would be 

{% highlight text %}
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RWE 0x4
{% endhighlight %}

**[Stack smashing protection](http://en.wikipedia.org/wiki/Stack-smashing_protection)** refers to compiler generated protection techniques of smash stacking. Refer to wikipedia link to get more details about the techniques involved in this protection. This can be disabled in gcc as follows:

{% highlight text %}
madhur@bt:~/buffer$ gcc -ggdb -m32 -o buffer1 -fno-stack-protector -mpreferred-stack-boundary=4 buffer1.c
{% endhighlight %}

**Windows Implementation**
The /GS switch is a compiler option that will add some code to functionâ€™s prologue and epilogue code in order to prevent successful abuse of typical stack based (string buffer) overflows.

When an application starts, a program-wide master cookie (4 bytes (dword), unsigned int) is calculated (pseudo-random number) and saved in the .data section of the loaded module. In the function prologue, this program-wide master cookie is copied to the stack, right before the saved EBP and EIP. (between the local variables and the return addresses)

\[buffer\]\[cookie\]\[saved EBP\]\[saved EIP\]
During the epilogue, this cookie is compared again with the program-wide master cookie. If it is different, it concludes that corruption has occurred, and the program is terminated.

In order to minimize the performance impact of the extra lines of code, the compiler will only add the stack cookie if the function contains string buffers or allocates memory on the stack using ***alloca***. Furthermore, the protection is only active when the buffer contains 5 bytes or more.

In a typical buffer overflow, the stack is attacked with your own data in an attempt to overwrite the saved EIP. But before your data overwrites the saved EIP, the cookie is overwritten as well, rendering the exploit useless (but it may still lead to a DoS). The function epilogue would notice that the cookie has been changed, and the application dies.

<pre>
|buffer||cookie||saved EBP||saved EIP|
|AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA|
         ^
         |
</pre>
The second important protection mechanism of /GS is variable reordering. In order to prevent attackers from overwriting local variables or arguments used by the function, the compiler will rearrange the layout of the stack frame, and will put string buffers at a higher address than all other variables. So when a string buffer overflow occurs, it cannot overwrite any other local variables.

**Position Independent Executables (PIE)** In order to take advantage of Address Space Layout Randomization (ASLR), programs need to be built as Position Independent Executables (PIE) with -fPIE â€“pie flag. PIE has a 5-10% performance penalty on architectures with small numbers of general registers (e.g. x86). 

**Fortify Source** enables several compile-time and run-time protections including protections against overflows. In order to use Fortify Source which provides run-time checks of buffer lengths and memory regions, programs need to be built with -D_FORTIFY_SOURCE=2 flag. 

**Stack Protector** is enabled at compile-time with -fstack-protector flag. It enables run-time stack overflow verification protecting against stack overflows, and reducing the chances of arbitrary code execution via controlling return address destinations.


