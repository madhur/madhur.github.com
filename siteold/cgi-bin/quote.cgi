#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;

our %in;
my $name;
my $qfile='quotes.txt';

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>Quotes</title>
<base href=$siteurl>

<link rel="stylesheet" type="text/css" href="programming.css" />

EOF1
;

open(MYFILE1,"$rooturl/$menufile") || &error("$rooturl/$menufile Cannot open file1","fatal");
while(<MYFILE1>)
{
	print $_;
}

close MYFILE1;

print "<h1 align=center>Quotes</h1>\n";

open MYFILE,"$rooturl/$qfile" or &error("\nCannot open file","fatal");
while(<MYFILE>)
{
	if(/^-/)
	{
		print "<h5 align=right>$_</h5>";
		next;
	}
		
	
	print "<strong><i>$_</strong></i>";
}
	
		
print <<EOF6



</td>
</tr>

</table>

EOF6
;


open(MYFILE1,"$rooturl/footer.html") || &error("\n$rooturl/$menufile Cannot open file1","fatal");
while(<MYFILE1>)
{
	print $_;
}
close MYFILE1;

print <<EOF6

</body>
</html>


EOF6
;
	