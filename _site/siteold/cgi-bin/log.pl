#!e:/perl/bin/perl.exe

use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;
my $temp;
my $logfile='log.txt';
my $file = "$rooturl/images/pixel.gif";

if($ENV{'QUERY_STRING'} eq "")
{
		
	if(-e "$rooturl/log/$logfile")
	{
		open LOGFILE,">>$rooturl/log/$logfile" ;
	}
	else
	{
		open LOGFILE,">$rooturl/log/$logfile" ;
	}
	
	my $host=&get_host;
	my $ip=$ENV{'REMOTE_ADDR'};
	my $time=&get_time;
	
	print LOGFILE "$host\t\t$ip\t$time\t$ENV{'HTTP_REFERER'}\n";
	
	close LOGFILE;
	
	print "Content-type: image/gif\n"; 
	print "Pragma: no-cache\r\n";
	print "Expires: Saturday, August 14, 1999 02:00:00 GMT\r\n"; 
	print "\n";
	open(IMAGE, "<$file");
	binmode(IMAGE);
	binmode(STDOUT); 
	while (<IMAGE>) { 
	  print $_; 
	} 
	close(IMAGE);
}
else
{
		print "content-type:text/html\n\n";
		print <<EOF6
		<html>
		<body bgcolor=black text=white>
		<table width=100% border=1>
EOF6
;

		open LOGFILE,"$rooturl/log/$logfile" ;
		while(<LOGFILE>)
		{
			my @fields=split(/[\t]+/);
			print <<EOF6
			<tr>
				<td width=10%>$fields[0]</td>
				<td width=20%>$fields[1]</td>
				<td width=60%>$fields[2]</td>
				<td width=10%>$fields[3]</td>
			</tr>
EOF6
;
				
		}
		print "</table>";
		close LOGFILE;
		
		print <<EOF6
		</body>
		</html>
EOF6
;


}
		
	
	
	
	
	
	
	
	
	
	
	
	
	
