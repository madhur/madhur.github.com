require_relative 'site_process'

module Jekyll
  class Archive < CustomPage
    def self.archives(site)
	 
      years = Hash.new { |h, k| h[k] = Array.new }
      
      months = Hash.new do |h, k|
        h[k] = Hash.new { |h, k| h[k] = Array.new }
      end
      
      days = Hash.new do |h, k|
        h[k] = Hash.new do |h, k|
          h[k] = Hash.new { |h, k| h[k] = Array.new }
        end
      end
      
      site.posts.docs.each do |post|   
		d = post.date	  
        years[d.year] << post
        months[d.year][d.month] << post 
        days[d.year][d.month][d.day] << post
      end
      
      [years, months, days]
    end
    
    def initialize(site, base, posts, year, month = nil, day = nil)
      time = Time.new(year, month, day)
      
      if day
        dir = time.strftime('%Y/%m/%d')
      elsif month
        dir = time.strftime('%Y/%m')
      else
        dir = time.strftime('%Y')
      end
      
      destdir="blog/" + dir

      super site, base, destdir, 'index', 'archive.html'
      title = "Archives for "
      
      if day
        title += "#{time.strftime('%B %d, %Y')}"
      elsif month
        title += "#{time.strftime('%B %Y')}"
      else
        title += year.to_s
      end
      
      self.data["title"] = title
      self.data["posts"] = posts.reverse
    end
  end
  
  class ArchiveGenerator < Generator
    def generate(site)
	  	  
      years, months, days = Archive.archives(site)
      
	  
      days.each do |year, m|	  
        write_page site, Archive.new(site, site.source, years[year], year)
        
        m.each do |month, d|
          write_page site, Archive.new(site, site.source, months[year][month], year, month)
          d.each { |day, posts| write_page site, Archive.new(site, site.source, posts, year, month, day) }
        end
      end
    end
	
		
	 def write_page(site, page)
      page.render(site.layouts, site.site_payload)
    
      page.write(site.dest)
      site.pages << page
    end
	
	
  end
  
  class MonthlyArchives < Liquid::Tag
    safe = true
    
    def render(context)
      @@list ||= generate_list(context)
    end
    
    private
    
      def generate_list(context)
        years, months, days = Archive.archives(context.registers[:site])
        result = ""
        
        months.each do |year, m|
          m.each do |month, posts|
            time = Time.new(year, month)
            result.insert(0, %(<div class='archivemonth'><a href="/blog/#{time.strftime('/%Y/%m')}">#{time.strftime('%B %Y')}</a> (#{posts.length})<br /></div>)) # for reverse order
          end
        end
        
        result
      end
  end
end

Liquid::Template.register_tag('monthly_archives', Jekyll::MonthlyArchives)
