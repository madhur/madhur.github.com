module Jekyll
  class MarkdownConverter
    alias :old_convert :convert
    
    # This adds the gist #1 syntax.
    def convert(content)
      old_convert content.gsub(/gist #(\d+)/, '[gist #\1](https://gist.github.com/\1)')
    end
  end
end