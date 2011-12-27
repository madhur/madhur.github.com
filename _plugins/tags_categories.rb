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
end
