---
layout: blog-post
title: "Removing the Default Editor Parts from SharePoint Web Parts"
excerpt: Removing the Default Editor Parts from SharePoint Web Parts
disqus_id: /2011/09/06/hidingproppane/
location: Delhi, India
time: 8:00 PM
categories:
- SharePoint
- WebParts
---

#{{ page.title }}

I was recently asked how to remove the Editor Parts (Appearance, Layout, Advanced, etc) from custom Web Parts.

{% highlight csharp %}
class MyEditorPart : EditorPart
{
    protected override void CreateChildControls()
    {        // this line hides the default EditorParts
        Parent.Controls[2].Visible = false;
        base.CreateChildControls();
    }

    public override bool ApplyChanges()
    {
        // do stuff here
        return true;
    }

    public override void SyncChanges()
    {
        // do stuff here
    }
}
{% endhighlight %}	


{% highlight csharp %}
public class MyWebPart : WebPart
{
    public override EditorPartCollection CreateEditorParts()
    {
        ArrayList aryParts = new ArrayList();

        MyEditorPart myEditor = new MyEditorPart();
        myEditor.ID = this.ID + "_myEditorPart";
        aryParts.Add(myEditor);

        return new EditorPartCollection(aryParts);
    }
    // do more stuff here...
}
{% endhighlight %}	