#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 


print "content-type: text/html\n\n";

my $type;
my $len;

if($ENV{'REQUEST_METHOD'} eq "GET")
{
	
	if($ENV{'QUERY_STRING'} eq "")
	{
		
		print <<EOF6
		<html>
		<body>
		
		<h1>get form for debug.cgi</h1>
		<hr>
		<form method=get action=/cgi-bin/debug.cgi>
		Name:<input type=text name=name size=10></input>
		<br><input type=submit>
		</form>
		
		<p>
		<hr>
		<form method=post action=/cgi-bin/debug.cgi>
		Name:<input type=text name=name size=10></input>
		<br><input type=submit>
		</form>
		
		</body>
		</html>
EOF6
;
	
	}
	else
	{
		print "<table width=100% border =1>";
		foreach my $temp(keys(%ENV))
		{
			print "<tr>";
		
			print "<td>$temp</td>";
			print "<td>$ENV{$temp}</td>";
			print "</tr>";
		}
		
		print "</table>";
	}
}

else
{
	if($ENV{'REQUEST_METHOD'} eq "POST")
	{
		my $in;
		$type = $ENV{'CONTENT_TYPE'};
	  	$len  = $ENV{'CONTENT_LENGTH'};
		read(STDIN,$in,$len);
		print "<h1>$in</h1>";
		print "<table width=100% border =1>";
		foreach my $temp(keys(%ENV))
		{
			print "<tr>";
		
			print "<td>$temp</td>";
			print "<td>$ENV{$temp}</td>";
			print "</tr>";
		}
		print "</table>";
		
	}
	
}





	


