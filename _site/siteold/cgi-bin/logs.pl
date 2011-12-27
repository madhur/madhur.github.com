#!e:/perl/bin/perl.exe

# Copyright 2001 David J Spelts  All Rights Reserved.
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;

$logs = "$rooturl/log/logs.txt";
$file = "$rooturl/images/pixel.gif";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = localtime(time);
$ip=$ENV{'REMOTE_ADDR'};
$page=$ENV{'HTTP_REFERER'};
$agent = $ENV{'HTTP_USER_AGENT'};
$year =~ s/^.//;
$mon = sprintf("%.2d",$mon);
$mday = sprintf("%.2d",$mday);
$page =~ tr/A-Z/a-z/;
$page =~ s/\?.*//;
$page =~ s/http:\/\///;

if ($agent =~ /Mozilla/i ) {
	($agent =~ /MSIE/i ) && ($browser="IE");
	($agent =~ /Opera/i ) && ($browser="Opera");
	($browser) || ($browser="Netscape");
}
($browser) ||  ($browser="Unknown");

$hit= "$year$mon$mday|$ip|$page|$browser\n";

open(OUTF,">>$logs");
print OUTF $hit;
close(OUTF);

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