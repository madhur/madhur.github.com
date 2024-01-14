---
layout: blog-post
title: "Enable code highlighting with Pygments/Jekyll"
excerpt: "Enable code highlighting with Pygments/Jekyll"
disqus_id: /2012/03/05/codehighlightjekyll/
location: New Delhi, India
time: 9:00 PM
tags:
- Jekyll
categories:
- Web Development
---

If you have been using Jekyll, you must be aware of code highlighting feature using highlight blocks. This highlighting is accomplished by
a neat python script called [Pygments](http://pygments.org/)

Pygments is a very powerful code syntax highlighter. It allows you to pass various options such as weather to display line no.s or which lines to be highlighted.
When Jekyll was released, there was no way to use these options since Jekyll encapsulated the execution of Python internally through [Albino gem](https://github.com/github/albino)

There has been some progress over this, a [pull request](https://github.com/mojombo/jekyll/issues/31) was submitted in Jekyll which allowed various options to be passed to Pygments.

However, when I tried to use **hl_lines** option to highlight the lines of code, I faced several issues. Following is the syntax I used

{% highlight text %}
 highlight html hl_lines=2 4
{% endhighlight %}

Running the above piece of code reults in only line 2 being highlighted and not both. So I decided to enclose it with quotation marks


{% highlight text %}
 highlight html hl_lines="2 4"  
{% endhighlight %}

The above piece of code gives the error. 

{% highlight text %}
Invalid flag value -O
{% endhighlight %}

Certainly, there are some things which needs to be fixed. First of all in albino, the validation function has a bug. The value regular express should be allowed quotation marks character so that hl_lines list can be provided enclosed in quotation marks. This is the first problem in **albino.rb** file.

{% highlight ruby %}
  def validate_shell_args(flag, value)
    if flag !~ /^[a-z]+$/i
      raise ShellArgumentError, "Flag is invalid: #{flag.inspect}"
    end
    if value !~ /^[a-z0-9\-\_\+\=\#\,\s]+$/i
      raise ShellArgumentError, "Flag value is invalid: -#{flag} #{value.inspect}"
    end
  end
{% endhighlight %}

The second problem is that we can seperate the hl_lines list with spaces since Jekyll uses the space as a delimeter to parse these options. To solve this problem, I pass in the list seperated by commas and then modified the 
**highlight.rb** file in Jekyll to recombine them into the list. See the updated function below:

{% highlight ruby %}
 def initialize(tag_name, markup, tokens)
      super	 
      if markup =~ SYNTAX	
        @lang = $1
        if defined? $2
		# puts $2
          tmp_options = {}
          $2.split.each do |opt|		    
            key, value = opt.split('=')						
			if key == 'hl_lines'
				puts value
				value = value.gsub(","," ")
			end			
            if value.nil?
              if key == 'linenos'			
                value = 'inline'
			  else
                value = true
              end
            end
            tmp_options[key] = value
          end
          tmp_options = tmp_options.to_a.collect { |opt| opt.join('=') }
		  
          # additional options to pass to Albino
          @options = { 'O' => tmp_options.join(',') }		  		  		  
        else
          @options = {}
        end
      else
        raise SyntaxError.new("Syntax Error in 'highlight' - Valid syntax: highlight <lang> [linenos]")
      end
    end
{% endhighlight %}

I cannot submit it as patch in Jekyll since this fix involves fixing two components: Jekyll and Albino. May be someone can come with better approach to fix this. This works for me as of now.	
