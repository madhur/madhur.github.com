require_relative 'custom_page'

module Jekyll   
  class Tag < CustomPage
    def initialize(site, base, dir, tag)
      super site, base, dir, tag
	 
      self.data['tag'] = tag
      self.data['title'] = tag
      self.data['description'] = tag
    end
  end
  
  class Tags < CustomPage
    def initialize(site, base, dir)
      super site, base, dir, 'alltags'
      self.data['tags'] = site.categories.keys.sort
	 
    end
  end
  
  class Site
    # generate_tags_categories is called by the custom process function in site_process.rb
        
    def generate_tags_categories            
      dir = 'categories'
      #write_page Tags.new(self, self.source, dir) if self.layouts.key? 'tags'      	 	  
      self.categories.keys.each do |tag|	 
		
      write_page Tag.new(self, self.source, dir, tag)
      end
    end
  end
end