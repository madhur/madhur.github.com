# Thanks to http://recursive-design.com/projects/jekyll-plugins/ for the code off which this is based
require_relative 'custom_page'

module Jekyll
  class Category < CustomPage
    def initialize(site, base, dir, category)
      super site, base, dir, 'category'
      self.data['category'] = category
      self.data['title'] = "#{site.config['category_title_prefix'] || 'Category: '}#{category}"
      self.data['description'] = "#{site.config['category_meta_description_prefix'] || 'Category: '}#{category}"
    end
  end
  
  class Categories < CustomPage
    def initialize(site, base, dir)
      super site, base, dir, 'categories'
      self.data['categories'] = site.categories.keys.sort
    end
  end
  
  class Tag < CustomPage
    def initialize(site, base, dir, tag)
      super site, base, dir, 'tag'
      self.data['tag'] = tag
      self.data['title'] = "#{site.config['tag_title_prefix'] || 'Tag: '}#{tag}"
      self.data['description'] = "#{site.config['tag_meta_description_prefix'] || 'Tag: '}#{tag}"
    end
  end
  
  class Tags < CustomPage
    def initialize(site, base, dir)
      super site, base, dir, 'tags'
      self.data['tags'] = site.categories.keys.sort
	  
    end
  end
  
  class Site
    # generate_tags_categories is called by the custom process function in site_process.rb
        
    def generate_tags_categories
      
      # Tags
      dir = self.config['tag_dir'] || 'tags'
      write_page Tags.new(self, self.source, dir) if self.layouts.key? 'tags'
      puts dir
	  
	  
      self.categories.keys.each do |tag|
	  puts tag
	  puts File.join(dir, tag.slugize)
        write_page Tag.new(self, self.source, File.join(dir, tag.slugize), tag)
      end
    end
  end
end