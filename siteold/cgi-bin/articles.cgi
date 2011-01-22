#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;

our %in;
my $artfile='index.txt';

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
	print "<br><h2 align=center>Articles</h2>";
	
	print"<ul>";

	open MYFILE,"$rooturl/articles/$artfile" or &error("\ncannot open file","fatal");
	while(<MYFILE>)
	{
		my %words=split(/\|/);
		print "<li> $words{CATEGORY}: <a href=\"$ENV{REQUEST_URI}?file=$words{FILE}&category=$words{CATEGORY}&topic=$words{TOPIC}\">$words{TOPIC}</a></li>";
	}
	close MYFILE;

	print "</ul>"	
}
	
				
else
{	
	open MYFILE,"$rooturl/articles/$in{'file'}.txt" or &error("\ncannot open file","fatal");
	print <<EOF1
	<table width=80% border=0 align=center>
	<tr>
	<td valign=bottom><h1>$in{'topic'}</h1></td>
	</tr>
	<tr>
	<td colspan=3>
EOF1
;

	while(<MYFILE>)
	{
		print "<br>$_";
	}
	
	close MYFILE;
print <<EOF6	

	</td>
	</tr>
	<tr height=20%>
	<td ><a href=$ENV{SCRIPT_NAME}>Back to index</a></td>
	</tr>
	</table>
EOF6
;
	

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
	