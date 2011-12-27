#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';


our %in;
my ($siteurl,$rooturl,$menufile)=&get_vars;
my $downfile='files.txt';

&ReadParse(*in);

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>$in{title}</title>
<base href=$siteurl>

<link rel="stylesheet" type="text/css" href="programs.css" />
<script language=javascript src=scripts/jsp.js> </script>
EOF1
;

open(MYFILE1,"$rooturl/$menufile") || &error("\n$rooturl/$menufile Cannot open file1");
while(<MYFILE1>)
{
	print $_;
}

close MYFILE1;
	
if($ENV{'QUERY_STRING'} ne "")
{	
	print "<br><h1 align=center>$in{title}</h1>";
	
	open MYFILE,"$rooturl/$downfile" or &error("\ncannot open file");
	my $i=0;
	while(<MYFILE>)
	{
		my %words=split(/\|/);
		if($words{'CAT'} eq $in{'cat'})
		{
			
			print "<h4>$words{TITLE}</h4>\n";
			print "<p>\n";
			my $desfile=$words{'DESC'};
			
			open MYFILE1,"$rooturl/$desfile" or &error("\ncannot open file");
			while(<MYFILE1>)
			{
				my $line=$_;
				print $line;
				print "<br>";
			}
			close MYFILE1;
			
			my $file=$words{'URL'};
			my $key=substr($file,6);
			print "<p><a href=/cgi-bin/download.cgi?link=$key>Download</a>\n";
			print "<p><a href=javascript:openwin($words{IMAGE})>View Screenshot</a>" if($words{'IMAGE'});;
			print "<hr>";
		}
		
		++$i;
	}
	
	close MYFILE;


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
	