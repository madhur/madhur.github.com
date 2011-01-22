#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

#my $siteurl="http://$ENV{SERVER_NAME}";

our %in;
#my $rooturl="$ENV{'DOCUMENT_ROOT'}";
#my $menufile='menu.htm';
my ($siteurl,$rooturl,$menufile)=&get_vars;
my $downfile='downloads.txt';

&ReadParse(*in);

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>Articles</title>
<base href=$siteurl>

<link rel="stylesheet" type="text/css" href="programming.css" />

EOF1
;

open(MYFILE1,"$rooturl/$menufile") || &error("\n$rooturl/$menufile Cannot open file1","fatal");
while(<MYFILE1>)
{
	print $_;
}

close MYFILE1;
	
if($ENV{'QUERY_STRING'} eq "")
{	
	print "<br><h1 align=center>Downloads</h1>";
	
	print"<ul>";

	open MYFILE,"$rooturl/$downfile" or &error("\ncannot open file","fatal");
	while(<MYFILE>)
	{
		my %words=split(/\|/);
		print "<li><a href=\"$words{FILE}\">$words{DESC}</a></li>";
	}
	close MYFILE;

	print "</ul>"	
}
	
				
	print <<EOF6	

	</ul>
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
	