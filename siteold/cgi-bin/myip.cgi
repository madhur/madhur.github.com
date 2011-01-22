#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;
our %in;
my $name;


print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>Tools</title>
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


print <<EOF6

<h1 align=center>Tools</h1>
<h2>Your IP address is:</h2>

<table border=1 width=50% align=center>
<tr>
	<td align=center bgcolor=purple><font size=6 align=center>$ENV{'REMOTE_ADDR'}</font></td>
</tr>
</table>

EOF6
;

my $host=&get_host;

my $agent=$ENV{'HTTP_USER_AGENT'};
my $browser;
if ($agent =~ /Mozilla/i ) {
	($agent =~ /MSIE/i ) && ($browser="Microsoft Internet Explorer");
	($agent =~ /Opera/i ) && ($browser="Opera");
	($browser) || ($browser="Netscape");
}
($browser) ||  ($browser="Unknown");


print <<EOF6

<h2>Your host name is:</h2>
<table border=1 width=50% align=center>
<tr>
	<td align=center bgcolor=purple><font size=4 align=center>$host</font></td>
</tr>
</table>
<font size=4 align=center bgcolor=pruple >$host</font>

<h2>You are running:</h2>
<table border=1 width=50% align=center>
<tr>
	<td align=center bgcolor=purple><font size=3 align=center>$browser</font></td>
</tr>
</table>


</td>
</tr>
</table>


EOF6
;


my $data;
read  STDIN,$data,50;
print "$data";


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
	