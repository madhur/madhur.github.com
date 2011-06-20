module Jekyll
  class TagCloud < Liquid::Tag
    @@max_size = 280
    @@min_size = 75
    safe = true
    
    def render(context)
      @@cloud ||= generate_cloud(context)
    end
    
    private
    
      def generate_cloud(context)
        tags = context.registers[:site].tags.map do |tag| 
          { 
            :title => tag[0], 
            :slug => tag[0].slugize,
            :posts => tag[1]
          } 
        end

        tags.sort! { |a, b| a[:title] <=> b[:title] }
        min_count = tags.min { |a, b| a[:posts].length <=> b[:posts].length }[:posts].length
        max_count = tags.max { |a, b| a[:posts].length <=> b[:posts].length }[:posts].length

        weights = tags.inject({}) do |result, tag|
          result[tag[:title]] = (tag[:posts].length - min_count) * (@@max_size - @@min_size) / (max_count - min_count) + @@min_size
          result
        end

        tags.inject("") do |html, tag|
          length = tag[:posts].length

          html << %(
            <span style="font-size: #{weights[tag[:title]].to_i}%">
              <a href="/tags/#{tag[:slug]}/" title="#{length} post#{"s" if length != 1}">#{tag[:title]}</a>
            </span>
          )

          html
        end
      end
  end
end

Liquid::Template.register_tag('tag_cloud', Jekyll::TagCloud)
