module Jekyll


  class CustomPage < Page
    def initialize(site, base, dir, filename, layout)
      @site = site
      @base = base
      @dir  = dir
      @name = filename+'.html'
      
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), layout)
	  
    end		 	

	def check_cache(name, filename, custom_url=nil)
			cache = "_cache/#{name}-#{filename}.cache"
			# cache = "_cache/#{name}#{filename}.cache"
			data = ""
			if !File.exists?(cache) then
				# this stuff is bit hackish, but it works
				# this will fail if the file isn't present
				#puts "https://raw.github.com/#{site.config['github_user']}/#{name}/master/#{filename}"
				url = custom_url ? custom_url : "https://raw.github.com/#{site.config['github_user']}/#{name}/master/#{filename}"
				
				data = `curl #{url}` 
				data.gsub!(/\`{3} ?(\w+)\n(.+?)\n\`{3}/m, "{% highlight \\1 %}\n\\2\n{% endhighlight %}")
				data = Liquid::Template.parse(data).render(
					{}, :filters => [Jekyll::Filters], :registers => { :site => site }
				)
				File.open(cache, "w") { |f| f.puts data } 
			else 
				data = IO.read cache
			end
			return data
	end	
  end
  
  
  class Tag < CustomPage
    def initialize(site, base, dir, tag)
      super site, base, dir, tag, 'tags.html'
	 
      self.data['tag'] = tag
      self.data['title'] = tag
      self.data['description'] = tag
    end
  end



  class Madhur < Generator
  def generate(site)
	
	dir = 'categories'      
    site.tags.keys.each do |tag|	 
		
		write_page(site, dir, tag)	 	 
	end		
	

  end
	
	def write_page(site, dir, tag)
      tagpage=Tag.new(site, site.source, dir, tag)
      tagpage.render(site.layouts, site.site_payload)
      tagpage.write(site.dest)
      site.pages << tagpage
    end
	
	
  end
end