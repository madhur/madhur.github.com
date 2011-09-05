# encoding: utf-8
require_relative 'custom_page'

module Jekyll
  class Project < CustomPage
    def initialize(site, base, dir, name, info)
      super site, base, dir, 'project'
      puts "Building project: #{name}"
      
      self.data['title'] = info['title'] || name
      self.data['version'] = info['version_title'] || info['version']
      self.data['repo'] = "https://github.com/#{site.config['github_user']}/#{name}"
      self.data['download'] = "#{self.data['repo']}/zipball/#{info['version'] || 'master'}"
      self.data['docs'] = info['docs'] == 'wiki' ? "#{self.data['repo']}/wiki" : info['docs'] if info['docs']
      self.data['description'] = info['description']
      
      # this stuff is bit hackish, but it works
      readme = `curl https://raw.github.com/#{site.config['github_user']}/#{name}/master/README.md` # this will fail if README.md isn't present
      readme.gsub!(/\`{3} ?(\w+)\n(.+?)\n\`{3}/m, "{% highlight \\1 %}\n\\2\n{% endhighlight %}")
      #readme.gsub!(/Ö/, '&#214;') # so that I can use LÖVE in my READMEs
      readme = Liquid::Template.parse(readme).render({}, :filters => [Jekyll::Filters], :registers => { :site => site })
      self.data['readme'] = RDiscount.new(readme).to_html
    end
  end
  
  class Projects < CustomPage
    def initialize(site, base, dir, projects)
      super site, base, dir, 'projects'
      data = []
      projects.each { |v| data << v.data }
      self.data['projects'] = data
    end
  end
  
  class Site
    def generate_projects
      return unless self.config.key? 'projects'
      throw "No 'project' layout found." unless self.layouts.key? 'project'
      dir = self.config['project_dir'] || 'projects'
      projects = []
      
      self.config['projects'].each do |k, v|
        slug = v['slug'] || k.slugize
        p = Project.new(self, self.source, File.join(dir, slug), k, v)
        p.data['url'] = "/#{dir}/#{slug}"
        projects << p
        write_page p
      end
      
      write_page Projects.new(self, self.source, dir, projects) if self.layouts.key? 'projects'
    end
  end
end