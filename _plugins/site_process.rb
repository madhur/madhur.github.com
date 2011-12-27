module Jekyll
  class Madhur < Generator
    def generate(s)
	
	
	puts "Build complete"
      s.generate_tags_categories
    end
  end
end