#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';
my $logfile='downlog.txt';
our %in;
my ($siteurl,$rooturl,$menufile)=&get_vars;


&ReadParse(*in);
my $file=$in{'link'};
my $link="/files";
$link=$link.$file;

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
	
	print LOGFILE "$host\t\t$ip\t$time\t$link\n";
	
	close LOGFILE;



open MYFILE, "$rooturl$link"	or &error("cannot open $rooturl$link");
seek MYFILE,0,2;
my $size=tell MYFILE;
close MYFILE;
print   "Content-Length: $size\n";
print   "Connection: close\n";
print 	"Content-Type: application/zip\n\n";


open MYFILE, "$rooturl$link"	or &error("cannot open $rooturl$link");
binmode(MYFILE);
binmode(STDOUT); 
while(<MYFILE>)
{
print;
}

close MYFILE;


	
	