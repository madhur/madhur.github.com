#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

my ($siteurl,$rooturl,$menufile)=&get_vars;
our %in;
my $name;
my $postfile='posts.txt';
my $line;
my $temp1;

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>Post a Message</title>
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

if($ENV{'REQUEST_METHOD'} eq "GET")
{
	if($ENV{'QUERY_STRING'} eq "")
	{
		print <<EOF1;
		
		<head>
		<script language=javascript1.2>
		function submit_onclick()
		{
			var a1=new String;
			
			a1=document.forms("abbrev").item("name").value;
			if(a1=="")
			{
				alert("You must enter the Name field");
				return false;	//return 0 will not work
			}
			a2=document.forms("abbrev").item("email").value;
			if(a2=="")
			{
				alert("You must enter the Email field");
				return false;	//return 0 will not work
			}
			a3=document.forms("abbrev").item("message").value;
			if(a3=="")
			{
				alert("You must enter the message field");
				return false;	//return 0 will not work
			}

			delete a1;
			return true;
			
		}	
		</script>
		</head>
		
		<h1 align=center>Post a Message</h1>
		<p>
		At this page, you can post a private message to me.
		<hr>
		<form method = post action=$ENV{'SCRIPT_NAME'} onsubmit="return submit_onclick();" name=abbrev>
		<table width=80% border=0>
		<tr>
			<td>Name</td>
			<td><input type=text size=30 name=name></td>
		</tr>
		<tr >
			<td>Email</td>
			<td><input type=text size=30 name=email></td>
		</tr>
		<tr>
			<td>Message</td>
			<!--<td><input type=textarea size=40 name=message></td>-->
			<td><textarea cols=50 rows=10 name=message></textarea></td>
		</tr>
		<tr></tr>
		<tr>
			<td></td>
			<td cellspacing=1 valign=bottom><input type=submit value="Post Message" id=addguest><input type=reset></td>
		</tr>


		</table>
		</form>
			
EOF1
;
	
	}

	
}
else
{
	&ReadParse(*in);
	
	$in{'message'}=~s/"\r\n"/~/;
	open MYFILE,">>$rooturl/$postfile" or &error("cannot open file");
	print MYFILE "$in{name}|$in{email}|$in{message}";
	close MYFILE;
	
	print <<EOF1;

	<h1 align=center>Message Posted</h1>
	<p>Thank you <b><i>$in{name}</i></b> for signing the guestbook.	
	<p>Your Message has been successfully sent to me.
	

EOF1
;	
	
}
	print <<EOF6	

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
	


