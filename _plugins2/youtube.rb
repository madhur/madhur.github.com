module Jekyll
  class Youtube < Liquid::Tag
    @@width = 640
    @@height = 510
    
    def initialize(name, id, tokens)
      super
      @id = id
    end
    
    def render(context)
      %(<iframe width="#{@@width}" height="#{@@height}" src="http://www.youtube.com/embed/#{@id}" frameborder="0" allowfullscreen></iframe>)
    end
  end
end

Liquid::Template.register_tag('youtube', Jekyll::Youtube)