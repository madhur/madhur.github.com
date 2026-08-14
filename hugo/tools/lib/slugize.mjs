// Replicates _plugins/core_ext.rb's String#slugize exactly:
//   self.downcase.gsub(/[\s\.]/, '-').gsub(/[^\w\d\-]/, '').downcase
export function slugize(text) {
  return text
    .toLowerCase()
    .replace(/[\s.]/g, '-')
    .replace(/[^\w\d-]/g, '')
    .toLowerCase();
}
