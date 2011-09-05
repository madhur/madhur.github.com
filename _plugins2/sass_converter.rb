require 'sass'
require 'growl'

module Jekyll
  class SassConverter < Converter
    safe true
    priority :low
    
    def matches(ext)
      ext =~ /scss/i
    end
    
    def output_ext(ext)
      ".css"
    end
    
    def convert(content)
      begin
        Sass::Engine.new(content, :syntax => :scss, :style => :compressed).render
      rescue StandardError => e
        Growl.notify "Sass Error: #{e.message}", :title => "Jekyll"
        puts "[Sass Error] #{e.message}"
      end
    end
  end
end