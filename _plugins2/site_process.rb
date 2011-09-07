require 'growl'

module Jekyll
  class Madhur < Generator
    def generate(s)
	
	
	puts "Build complete"
      #s.reset
      #s.read
      #s.generate
      #s.render
      
      # these must come after render
      s.generate_tags_categories
      #s.generate_archives
      #s.generate_projects
      
      #s.cleanup
      #s.write
      
      # Growl
	  #puts "Build complete"
      #Growl.notify "Build complete.", :title => "Jekyll"
    end
  end
end