---
layout: blog-post
title: "Migrating 3rd party blogs to Jekyll"
excerpt: Migrating 3rd party blogs to Jekyll
disqus_id: /2011/09/01/migratingthirdjekyll/
location: Delhi, India
time: 10:00 PM
tags:
- Jekyll
---



There are 3rd party migrators avilable to migrate from Wordpress blog to Jekyll based blogs. In this post, I am going to outline simple process of migrating most 3rd 
party blogs to Jekyll based blogs. Most of the blog web sites support a common interface called ***MetaWeblog***.

For example, on telligent based blogs, this can be accessed as follows:

[http://blogs.msdn.com/b/mahuja/metablog.ashx](http://blogs.msdn.com/b/mahuja/metablog.ashx)

The RFC of this interface is given [here](http://www.xmlrpc.com/metaWeblogApi)

The metablog interface exposts a common set of methods to retrieve the blog data using XML-RPC communication.

Since this API is exposed from the Weblogs providers, programmer have to use a client-side programming model to communicate with it according to the XML-RPC protocol.

I have created and published this C# programming wrapper which allows us to easily develop C# client applications that consumes this API via a service.

1. Download my sample wrapper from the github repository [here](https://github.com/madhur/Telligent2Jekyll).
2. Create a .Net application and reference the ***CookComputing.XmlRpc*** that come in the above repository
3. Create a class for the API provided.

Notice that the above post contains an implemention of IBlogger interface, which is decorated with \[XmlRpcUrl\("http://blogs.msdn.com/metablog.ashx"\)\] attribute. 

Don't forget to change the URL of your Community Server Blogs metaBlog.

Now you can easily use the proxy in your code.

{% highlight csharp %}
class Program
{
        static void Main(string[] args)
        {

            IBlogger proxy = MetaBlogAPIFactory.Create();
            PostInfo[] posts = proxy.getRecentPosts("mahuja", "mahuja@microsoft.com ", "sdfsdf", 1000);

            IJekyllFiles jekyllFiles = new JekyllFiles();

            foreach (PostInfo post in posts)
            {
                List<MappingEntry> sampleYaml=jekyllFiles.GetSampleYaml();

                List<MappingEntry> newYaml = jekyllFiles.SetYaml(post, sampleYaml);

                string filename = jekyllFiles.GenerateFileName(post);

                jekyllFiles.GenerateFileOutput(post, filename, newYaml, "description");

                Console.WriteLine("{0} written successfully", filename);
            }

            Console.ReadLine();


        }
}
{% endhighlight %}	

To generate the YAML header for the files, I have re-used publically available YAML parser. We can choose from several available YAML parsers:
* [http://www.codeproject.com/KB/recipes/yamlparser.aspx](http://www.codeproject.com/KB/recipes/yamlparser.aspx)
* [http://yaml.codeplex.com/](http://yaml.codeplex.com/)
* [http://yaml-net-parser.sourceforge.net/](http://yaml-net-parser.sourceforge.net/)

