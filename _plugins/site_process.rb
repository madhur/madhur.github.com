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
    site.categories.keys.each do |tag|	 
		
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