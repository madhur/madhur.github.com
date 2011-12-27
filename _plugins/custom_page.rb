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
  
  class Site
    def write_page(page)
      
      page.render(self.layouts, site_payload)
      page.write(self.dest)
      self.pages << page
    end
  end
end
