require_relative 'site_process'
require "Nokogiri"
require "Maruku"

module Jekyll
	
	class Projects < CustomPage
		def initialize(site, base, dir, projects)
			super site, base, dir,'index', 'projects.html'
			data = []
			projects.each { |v| data << v.data }
			self.data['projects'] = data
		end
	end
	
	class Project < CustomPage
		def initialize(site, base, dir, name, info, url)
			super site, base, dir,'index', 'project.html'
			puts "Building project: #{name}"
			
			self.data['name']      = name
			self.data['title']     = info['title'] || name
			self.data['nice_name'] = info['title']
			
			
			self.data['version']   = info['version_title'] || info['version']
			#self.data['repo']      = "https://github.com/#{site.config['github_user']}/#{name}"
			self.data['download']  = info['download'] || "#{self.data['repo']}/zipball/#{info['version'] || 'master'}"
			self.data['docs']      = info['docs'] == 'wiki' ? "#{self.data['repo']}/wiki" : info['docs'] if info['docs']
			
			self.data['changelog_url'] = 'changelog.html'  if info['changelog']
			self.data['apidocs_url']   = "/docs/#{name}"   if info['apidocs']
			self.data['support_url']   = info['support']   if info['support']
			self.data['icon']          = info['icon']      if info['icon']  
			
			if info['gallery'] then 
				self.data['gallery_url']  = 'gallery.html'    
				self.data['gallery']      = info['gallery']
			end
			
			self.data['apidocs_name']  = info['apidocs_name']   if info['apidocs_name']
			
			if info['features']  then
				self.data['features']     = info['features']
				self.data['readme_url']   = 'readme.html'
				self.data['features_url'] = url
			elsif self.data['changelog_url'] #TODO else?
				self.data['readme_url']   = url
			end
			
			readme =
			if info['readme'] then
				IO.read info['readme']
				puts("1")
			else
			#	check_cache(name,"Readme.md")
				#puts("2")
			end
			self.data['readme'] = Maruku.new(readme).to_html
			self.data['readme_name'] = info['readme_name'] if info['readme_name']
			
			doc = Nokogiri::HTML(self.data['readme'])
			self.data['description'] = info['description'] || doc.css('#description').text || ""
			
			self.data['changelog_location'] =     info['changelog_location']     || nil
			self.data['changelog_heading_hash'] = info['changelog_heading_hash'] || false
			
			if info['languages'] then
				self.data['languages'] = info['languages'].join(" &nbsp;&nbsp;")
			end 
			
			["iusethis", "macupdate", "alternativeto"].each do |e|
				self.data[e] = info[e]  if info[e]
			end
			
		end 
	end

	# Sets the commons vars for a project page
	class ProjectPage < CustomPage
		def initialize(site, base, dir, name, project,html_name)
			@project = project
			puts "Building project's #{name}"
			super site, base, dir, name, html_name
			['version','repo','download', 'icon', 'name'].each do |key|
				self.data[key] = project.data[key]
			end
			self.data['title'] = project.data['title'] + "'s #{name}"
			
			copy_keys 'features_url', 'apidocs_url', 'gallery_url', 'nice_name',
			'readme_name','changelog_url', 'readme_url', 'apidocs_name', "support_url", 
			"iusethis", "macupdate","alternativeto"
		end
		
		def copy_keys(*keys)
			keys.each do |key|
				self.data[key] = @project.data[key] if @project.data[key]
			end
		end
		
	end
	
	class Gallery < ProjectPage
		def initialize(site, base, dir, name, project)
			super site, base, dir, 'gallery', project, "gallery.html"
				copy_keys 'gallery'
		end
	end
	
	class Readme < ProjectPage
		def initialize(site, base, dir, name, project)
			super site, base, dir, 'readme', project, "readme.html"
			copy_keys 'readme', 'description'
		end 
	end
	
	class ChangeLog < ProjectPage
		def initialize(site, base, dir, name, project)
			super site, base, dir, 'changelog', project, "changelog.html"
			
			changelog='test'
			#changelog = check_cache(name,"Changelog.md",  project.data['changelog_location'])
			changelog.gsub!(/\`{3} ?(\w+)\n(.+?)\n\`{3}/m, "{% highlight \\1 %}\n\\2\n{% endhighlight %}")
			changelog = Liquid::Template.parse(changelog).render(
				{}, :filters => [Jekyll::Filters], :registers => { :site => site }
			)
			
			# if true check heading with  ## Heading ##
			regex = project.data['changelog_heading_hash'] ? /##\s+([\w.(): ]+)\s+##/m
																									   : /\n([\w :().+]+)\n-+/m
			
			builder = Nokogiri::XML::Builder.new do |xml|
				xml.table{
					# xml << "<tr>"
					# (changelog.scan(/##\s+([\w.() ]+)\s+##/m)).each_with_index do |e,i|
					arr=changelog.scan(regex)
					i=0
					while i < arr.length
						xml.tr{
							while i < arr.length
								xml.td{
									text = arr[i].flatten[0]
									name = text.gsub(/ \(.*\)/, '')
									id	 = text.strip.gsub(/\s/,'_')
									id.gsub!(/[:+.()]/,'')
									id.downcase!
									xml.a(:href => "##{id}"){
										xml << name
									}
								}	
								break if i % 5 == 4
								i+=1
							end
						}
						i+=1
					end
				}
			end
			
			toc = builder.to_xml
			
			toc.sub!(/<\?xml version="1.0"\?>/, '')
			changelog.sub! /([\w :().+]+\n=+)/m, "#ChangeLog\n#{toc}"
			self.data['changelog'] = changelog
			
		end
		
	end
	
	class ProjectGenerator < Generator
		def generate(site)
			return unless site.config.key? 'projects'
			throw "No 'project' layout found." unless site.layouts.key? 'project'
			dir = site.config['project_dir'] || 'projects'
			projects = []
			Dir.mkdir '_cache' unless	 File.directory?('_cache')
			
			site.config['projects'].each do |k, v|
				slug = v['slug'] || k.slugize
				p = Project.new(site, site.source, File.join(dir, slug), k, v,"/#{dir}/#{slug}")
				p.data['url'] = "/#{dir}/#{slug}"
				projects << p
				write_page site, p
				write_page site,ChangeLog.new(site, site.source, File.join(dir, slug),k, p) if v['changelog']
				write_page site, Readme.new(site, site.source, File.join(dir, slug),k, p)    if v['features']
				write_page site, Gallery.new(site, site.source, File.join(dir, slug),k, p)   if v['gallery']
				
			end
			
			write_page site, Projects.new(site, site.source, dir, projects) if site.layouts.key? 'projects'
		end
		
		def write_page(site, page)
			page.render(site.layouts, site.site_payload)
			page.write(site.dest)
			site.pages << page
		end
	end
	
end
 