module Jekyll


  class CustomPage < Page
    def initialize(site, base, dir, tag)
      @site = site
      @base = base
      @dir  = dir
      @name = tag+'.html'
      
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'tags.html')
	  
    end
	
	 
	
  end
  
  
  class Tag < CustomPage
    def initialize(site, base, dir, tag)
      super site, base, dir, tag
	 
      self.data['tag'] = tag
      self.data['title'] = tag
      self.data['description'] = tag
    end
  end



  class Madhur < Generator
    def generate(site)
	
	 dir = 'categories'
      #write_page Tags.new(self, self.source, dir) if self.layouts.key? 'tags'      	 	  
      site.categories.keys.each do |tag|	 
		
		
		write_page(site, dir, tag)
	 
	  end
	  #puts "build complete"
	
    end
	
	def write_page(site, dir, tag)
      tagpage=Tag.new(site, site.source, dir, tag)
      tagpage.render(site.layouts, site.site_payload)
      tagpage.write(site.dest)
      site.pages << tagpage
    end
	
	
  end
end