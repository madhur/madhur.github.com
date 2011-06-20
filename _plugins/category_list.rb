module Jekyll
  class CategoryList < Liquid::Tag
    safe = true
    
    def render(context)
      result = ""
      categories = context.registers[:site].categories
      
      categories.keys.each do |category|
        result << %(<a href="/categories/#{category.slugize}"><strong>#{category}</strong></a> (#{categories[category].length})<br />)
      end
      
      result
    end
  end
end

Liquid::Template.register_tag('category_list', Jekyll::CategoryList)
