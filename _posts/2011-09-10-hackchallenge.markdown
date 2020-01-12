---
layout: blog-post
title: "HackingLab Challenge: Disassemble .NET Clients"
excerpt: "HackingLab Challenge: Disassemble .NET Clients"
disqus_id: /2011/09/10/hackchallenge/
location: Delhi, India
time: 11:00 PM
tags:
- Hacking
- Disassembling
- .NET
---


Compass Security has come up with a hacking challenge on their [site](https://www.hacking-lab.com/sh/LAE04Jf). The challenge consist of an .NET client having some hidden functionality which needs to be uncovered by the user. I decided to give it a try.

## Requirements ##
* Download  [Application: DotNetFatClientHacking.exe](http://media.hacking-lab.com/largefiles/7205/DotNetFatClientHacking.exe)

## Tools used in the trade ##
* [Reflector](http://www.reflector.net/) or now better [DotPeek](http://www.jetbrains.com/decompiler/)
* ILDasm
* Hex Editor
* MSDN

## Solution ##

Let's run our .NET assembly and see what it looks like. Its a normal Windows Form application with just one button which does nothing. I could not figure out anything else from the application.

![](/images/netapp.png)

Let's open the assembly in Reflector and see what it's doing. 

![](/images/reflector.png)

From the reflector, I could figure out the following
* The form has got actually 3 buttons, 2 are hidden
* There is a *BusinessClass* class in the assembly which is invoked by the hidden buttons
* The visible button checks if the user is *Admin* and hides or shows the other two buttons

Now, our job is to become the Admin :) . That's the code which is called by the Visible button **Identify me**
{% highlight csharp %}
 private void identifyUser()
    {
      if (this.IsAdmin())
      {
        this.labUser.Text = "Welcome Admin!";
        this.butAdminHTTP.Visible = true;
        this.butAdminHTTPS.Visible = true;
      }
      else
      {
        this.labUser.Text = "Welcome User!";
        this.butAdminHTTP.Visible = false;
        this.butAdminHTTPS.Visible = false;
      }
    }
{% endhighlight %}

Clearly, our main interest is in *IsAdmin()* function which is defined as follows:

{% highlight csharp %}
private bool IsAdmin()
    {
      foreach (object obj in Dns.GetHostEntry(Dns.GetHostName()).AddressList)
      {
        if (obj.ToString().Equals("258.54.54.699"))
          return true;
      }
      return false;
    }	
{% endhighlight %}

Hmmm. Very Interesting !!!	Do you understand what is it doing ?

It basically retrieving the host name of our computer and based on that hostname getting all the IP addresses assigned to the network interfaces present in the system.
If any of its IP address matches *258.54.54.699*, I am the Admin :).

Now the interesting part here is that *258.54.54.699* is actually an invalid IP address otherwise I could have fooled the program by temporarily assigning this IP address to either one of my interfaces or even write that in *hosts* file.

But since its invalid IP, it will never be returned by system API. So, we must patch the program.

Let's open the function in *ILDASM* and look at its disassembly.
{% highlight text %}
  IL_001c:  ldloc.1
  IL_001d:  callvirt   instance string [mscorlib]System.Object::ToString()
  IL_0022:  ldstr      "258.54.54.699"
  IL_0027:  callvirt   instance bool [mscorlib]System.String::Equals(string)
  IL_002c:  brfalse.s  IL_0032
  IL_002e:  ldc.i4.1
{% endhighlight %}  


There are several ways to do it. I will write down from tedious to easiest
* Export the classes from Reflector to Visual Studio solution and change the IP address to our actual IP address. But then Why not just NOP out the call itself :). This requires boring effort
* Use the ILASM or any other utility to change the instruction at *ldstr      "258.54.54.699"* to *ldstr actual ip*. Even this requires some effort
* Easiest Way: Actually we can just take advantage of if-else branch reversal.

Let's take a look at disassembly of *identifyuser()* function

![](/images/ildasm-output.png)

If you closely look at the disassembly above,  the instruction at IL_0006 is doing all the magic which is 
{% highlight text %}
  IL_0006:  /* 2C   | 29               */ brfalse.s  IL_0031
{% endhighlight %}  

What this instruction means is that if output of *IsAdmin()* is false, branch to instruction at IL_0031, the instruction which hides the buttons.
Now, we can just change this instruction to reverse, i.e. make it **brtrue.s**. A quick look at MSDN tells me that its opcode is 2D as opposed to 2C which stands for **brfalse.s**.

Now, we just need to fire up the favourite hex editor and **change just one byte.** from 2C to 2D.

{% highlight text %}
Offset(h) 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

000005A0  02 28 02 00 00 06 02 28 05 00 00 06 2A 1E 02 28  
000005B0  05 00 00 06 2A 00 00 00 03 30 02 00 5A 00 00 00  
000005C0  00 00 00 00 02 28 06 00 00 06 2D 29 02 7B 02 00  
000005D0  00 04 72 F5 00 00 70 6F 1E 00 00 0A 02 7B 04 00  
{% endhighlight %}  

Our target lies at offset 5CA which I have already flipped from 2C to 2D as shown above. Let's save the file and run it again.

![](/images/cracked.png)

Voilla !!! The Administrative buttons are visible and clicking them invokes the Business functions which fetch some HTML output over the internet :)
