#!/usr/bin/env ruby19
class String
  def slugize
    self.downcase.gsub(/[\s\.]/, '-').gsub(/[^\w\d\-]/, '').downcase
  end
end
 