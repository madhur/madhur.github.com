#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'func.pl';

#my $siteurl="http://$ENV{SERVER_NAME}";
#my $rooturl="$ENV{'DOCUMENT_ROOT'}";
#my $baseurl="$ENV{'DOCUMENT_ROOT'}/gbook";
my ($siteurl,$rooturl,$menufile)=&get_vars;
my $bookurl='/gbook';
my $countfile='count.txt';
my $guestfile='guests.txt';
#my $menufile='menu.htm';
my (@add,@email,@names,@comm,@time,@ip);

if(! -e "$rooturl/gbook/$guestfile")
{
	open (MYFILE,">$rooturl/gbook/$guestfile") ||  &error("\n$rooturl/gbook/$guestfile Cannot open file1","fatal");
	open (MYFILE1,">$rooturl/gbook/$countfile") ||  &error("\n$rooturl/gbook/$countfile Cannot open file1","fatal");
	close MYFILE;
	close MYFILE1;
	
}

open(MYFILE,"$rooturl/gbook/$guestfile") || &error("\n$rooturl/gbook/$guestfile Cannot open file1","fatal");

while(<MYFILE>)
{
	chomp;
	if($_ eq "add:")
	{
		my $temp=<MYFILE>;
		push(@add,$temp);

	}
	elsif($_ eq "comm:")
	{
		my $comments;
		while(<MYFILE>)
		{
			chomp;
			last if($_ eq "email:" || $_ eq "name:");
			$comments=$comments."<br>".$_;	
		}
		if($_ eq "email:")
		{
			push(@comm,$comments);
			my $temp=<MYFILE>;
			push(@email,$temp);
		}
		if($_ eq "name:")
		{
			push(@comm,$comments);
			my $name=<MYFILE>;
			push(@names,$name);
		}
	}
	elsif($_ eq "name:")
	{
		my $temp=<MYFILE>;
		push(@names,$temp);
	}
	elsif($_ eq "time:")
	{
		my $temp=<MYFILE>;
		push(@time,$temp);
	}
	elsif($_ eq "host:")
	{
		my $temp=<MYFILE>;
		push(@ip,$temp);
	}
}

print "content-type:text/html\n\n";

print <<EOF1
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

print <<EOF1
<h1 align="center">GuestBook</h1>

<p>Thank you for stopping by my site. Here you can leave your mark.
<br>Fill out the blanks to sign the guestbook.
<p>After you submit your entry, you will be returned to the guestbook.
<a href=/cgi-bin/guestadd.cgi>Sign the GuestBook</a>
<p>
<pre>


</pre>

<p>


<table width=95% cellpadding=1 cellspacing=1 border=0 >
	<tr bgcolor=#BCBCDE valign=baseline bordercolor=yellow >
		<th width=32% >Name</th>
		<th width=48%>Comments</th>
	</tr>

EOF1
;


for(my $i=0;$i<=$#names;++$i)
{
	print <<EOF3
	<tr bgcolor=green>
		<td width=32%>
			<table border=0 cellspacing=3 cellpadding=1 valign=baseline>
				<tr  >
					<td >$i)</td>
					<td >$names[$i]</td>
				</tr>
EOF3
;
	if($email[$i] ne "\n")
	{
	print <<EOF3
				<tr>
					<td ><img src=images/mail.gif></td>
					<td ><font face=verdana size=1><a href="mailto:$email[$i]">$email[$i]</a></td>
				</tr>
EOF3
;
	}
	
	if($add[$i] ne "\n")	#if blank dont print
	{
	print <<EOF3
				<tr>
					<td ><img src="images/url.gif" width=20 height=20></td>
					<td><a href="$add[$i]">$add[$i]</a></font></td>
				</tr>
		
			
EOF3
;
	}
print <<EOF3
				</table>
		</td>
	
		
		<td width="68%">
			<table border=0 cellspacing=0 cellpadding=0 width=100%>
				<tr>
					<td>$comm[$i]</td>	<!--comment as  first row-->
				</tr>
				<tr>
					 <td>  <hr></td>	<!--hor line as second row-->
				</tr>
				<tr>
					<td><img src="images/point.gif" width=9 height=9>	<!--image as third -->
					<font face=verdana size=1>$time[$i] from $ip[$i]</font></td>
				</tr>
			</table>
		</td>
	</tr>

EOF3
;

}


print <<EOF6	
</table>

<br>
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
