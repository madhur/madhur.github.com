class String
  def slugize
    self.gsub(/[^\w\d\-]/, ' ')
  end
end