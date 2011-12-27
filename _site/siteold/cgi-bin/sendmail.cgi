#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';
my ($siteurl,$rooturl,$menufile)=&get_vars;
$| = 1; 
open(STDERR, ">&STDOUT"); 

#my $siteurl="http://$ENV{SERVER_NAME}";

our %in;
#my $rooturl="$ENV{'DOCUMENT_ROOT'}";
#my $menufile='menu.htm';
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

if($ENV{'QUERY_STRING'} eq "")
{
	print <<EOF6
	<head>
	
	<h1 align=center>Tools</h1>
	<h2>send Mail</h2>
	
	Here you can send mail by directly talking with the SMTP server.
	
	<form method=get name=sendmail action=/cgi-bin/sendmail.cgi onclick="return onsubmit_click();">
	<table width=70% border=0 cellspacing=1 cellpadding=7 align=left>
	<tr bgcolor=green>
		<td width=30%>Server Address</td>
		<td bgcolor><input type=text size=25 name=server></td>
	</tr>
	
	<tr bgcolor=green>
		<td>From:</td>
		<td><input type=text size=20 name=from></td>
	</tr>
	
	<tr bgcolor=green>
		<td>To:</td>
		<td><input type=text size=20 name=to></td>
	</tr>
	
	<tr bgcolor=green>
		<td>Body:</td>
		<td><input type=textarea size=20 name=to></td>
	</tr>
	
	<tr bgcolor=green>
		<td><input type=submit value=send></td>
		<td><input type=reset value=reset></td>
	</tr>
	</table>


EOF6
;

}
else
{

	my $ServerName = "smtp.your_isp.com";
	
	# Connect to the server
	$smtp = Net::SMTP->new($ServerName,Debug => 1);
	die "Couldn't connect to server" unless $smtp
	
	my $MailFrom = "someone\@sender.com";
	my $MailTo = "someone_else\@recipient.com";

	$smtp->mail( $MailFrom );
	$smtp->to( $MailTo );
	$smtp->data("Hello World!");

	$smtp->datasend("To: mailing-list\@mydomain.com");
	$smtp->datasend("From: MyMailList\@mydomain.comt\n");
	$smtp->datasend("Subject: Updates To My Home Page\n");
	$smtp->datasend("\n");

	# Send the message
	$smtp->datasend("Here are all the cool new links...\n\n");

	# Send the termination string
	$smtp->dataend();
	
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
	