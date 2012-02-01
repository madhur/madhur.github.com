#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';

#my $siteurl="http://$ENV{SERVER_NAME}";
my ($siteurl,$rooturl,$menufile)=&get_vars;
our %in;
#my $rooturl="$ENV{'DOCUMENT_ROOT'}";
my $baseurl="$rooturl/gbook";
my $countfile='count.txt';
my $guestfile='guests.txt';
my $menufile='menu.htm';
my $name;
	

if(! -e "$rooturl/gbook/$guestfile")
{
	open (MYFILE,">$rooturl/gbook/$guestfile") ||  &error("\n$rooturl/gbook/$guestfile Cannot open file1","fatal");
	open (MYFILE1,">$rooturl/gbook/$countfile") ||  &error("\n$rooturl/gbook/$countfile Cannot open file1","fatal");
	close MYFILE;
	close MYFILE1;
}	

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>GuestBook</title>
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

print <<EOF1;

<h1 align="center">GuestBook</font></h1>

EOF1

if($ENV{'QUERY_STRING'} eq "")
{
	print <<EOF1;
	
	<head>
	<script language="javascript">
	<!--
	function submit_onclick()
	{
	var a1=new String;
	a1=document.forms("guest").item("name").value;
	if(a1=="")
	{
		alert("You must enter the name");
		return false;	//return 0 will not work
	}
	delete a1;
	return true;
	-->
	}
	
	</script>
	</head>
	
	<p>Fill out the blanks below to sign the guestbook.
	<br>After you submit your entry, you will be returned to the guestbook.
	<br>The blanks with * represent required fields.
	<p><a href=/cgi-bin/guest.cgi>Back to GuestBook</a>
	<p>
	
	<table border=0 cellpadding=2 cellspacing=1 width=70% style="height:20">
	<tr bgcolor=purple>
		<td colspan=2 height=20><b>Sign the Guestbook :</td></b>
	</tr>
	
	<form method=get action="/cgi-bin/guestadd.cgi" name=guest onsubmit="return submit_onclick();">
	<!-- see if return value is true, it is submitted, if it is false, it is not submitted -->
	
	<tr bgcolor=green>
		<td width=30%>Name* :</td>
		<td align=left><input type=text name=name size=50 title=name1></td>
	</tr>
	
	<tr bgcolor=green>
		<td>E-mail :</td>
		<td align=left><input type=text name=email size=50></td>
	</tr>
	
	
	<tr bgcolor=green>
		<td >Homepage :</td>
		<td align=left><input type=text name=add size=50 value=http://></td>
	</tr>
	
	<tr bgcolor=green>
		<td valign=center>Comments :</td>
		<td align=left valign=top><textarea name=comm cols=38 rows=8 title=comments></textarea></td>
	</tr>

	<tr valign=bottom bgcolor=green>
		<td></td>
		<td cellspacing=1 valign=bottom><input type=submit value="Sign GuestBook" id=addguest><input type=reset  ></td>
		
	</tr>
	</form>
	
	</table>
	
	<br>
	</td>
	</tr>
	
	</table>
	
	
	</body>
	</html>

EOF1
}


else
{
	
	&ReadParse(*in);
	
	my $retval=&dowork;
	if($retval==1)
	{
		print <<EOF2;
		
		<head>
		<meta http-equiv="refresh" content="3;URL=/cgi-bin/guest.cgi">
		</head>
		
		<p>Thank you <b><i>$name</i></b> for signing the guestbook.	
		<p>Your entry was added successfully
		<br>You should be transferred to the guestbook in 3 seconds.
		<br>Click <a href=/cgi-bin/guest.cgi>here</a> if you browswer doesn't support automatic reloading.
		
EOF2
	}
	if($retval==0)
	{
		print <<EOF3
		<p>There was an error signing the guestbook.	

EOF3
;
	}
	if($retval==2)
	{
		print <<EOF3
		<p>There was an error in the homepage you entered.
		<p>Please enter the correct homepage or leave the field blank
		
EOF3
;
	}
	if($retval==3)
	{
		print <<EOF3
		<p>There was an error in the email address you entered.
		<p>Please enter the correct email or leave the field blank
		<p>Please correct the error and resubmit
		
		
EOF3
;
	}


}

print <<EOF3
		</td>
		</tr>
	
		</table>
EOF3
;
	
		open(MYFILE1,"$rooturl/footer.html") || &error("\n$rooturl/$menufile Cannot open file1","fatal");
		while(<MYFILE1>)
		{
			print $_;
		}
		close MYFILE1;
		
		
		print <<EOF3
		</body>
		</html>
		
		
EOF3
;





sub dowork
 {

	open COUNTFILE,"$baseurl/$countfile" or &error("\nCannot open file $baseurl/$countfile");
	my $count=<COUNTFILE>;
	chomp($count);
	$count++;
	close COUNTFILE;
	open COUNTFILE,">$baseurl/$countfile" or &error("\nCannot open file");
	print COUNTFILE $count;
	close COUNTFILE;
	
	
	open MYFILE,">>$baseurl/$guestfile" or &error("\nCannot open file");
	#$flag=1;
	
	my $ret=&checkstr;
	return $ret if($ret!=1);
	
	foreach my $temp(sort(keys(%in)))
	{
			print MYFILE "$temp:\n";
			print MYFILE "$in{$temp}\n";
			#print "$temp\n";
	}
	
	$name=$in{'name'};
	print MYFILE "time:\n";
	my $time=&get_time;
	print MYFILE "$time\n";
	my $host=&get_host;
	print MYFILE "host:\n";
	print MYFILE "$host\n\n";
	close MYFILE;
	

  return 1; # just for fun
}
##############################################################################################
sub checkstr
{
	foreach my $temp(sort(keys(%in)))
	{
		if($temp eq "add")
		{
			if($in{$temp} eq "http://")
			{
				$in{$temp}="";
				next;
			}
			 
			#print $in{$temp};
			my $i=$in{$temp}=~/^http/;
			return 2 if($i==0);
		}
		if($temp eq "email")
		{
			next if ($in{$temp} eq "");
			my $i=$in{$temp}=~/[a-zA-Z0-9_]+@[a-zA-Z0-9_]/;
			return 3 if($i==0);
		}
		if($temp eq "name")
		{
			$in{$temp}="anonymous" if ($in{$temp} eq "");
		}
		if($temp eq "comm")
		{
			$in{$temp}="no comments" if ($in{$temp} eq "");
		}
	}
	return 1;
}

