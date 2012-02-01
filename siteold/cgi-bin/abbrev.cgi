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
#my $menufile='menu.htm';
my $name;
my $abfile='abv.txt';
my $line;
my $temp1;

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

	print <<EOF1;
	
	<head>
	<script language=javascript1.2>
	function submit_onclick()
	{
		var a1=new String;
		a1=document.forms("abbrev").item("abb").value;
		if(a1=="")
		{
			alert("You must enter the search field");
			return false;	//return 0 will not work
		}
		delete a1;
		return true;
		
	}	
	</script>
	</head>
	
	<h1 align=center>Acronym Lookup</h1>
	<p><hr>
	
	<form method = get action=/cgi-bin/abbrev.cgi onsubmit="return submit_onclick();" name=abbrev>
	<table width=100% border=0>
	<tr>
		<td width=20%>Enter the acronym to search</td>
		<td width=30%><input type=text size=40 name=abb></td>
		<td width=30%><input type=submit value=Search></td>
	</tr>
	</table>
	</form>
	
EOF1
;
	
	
}
else
{
	&ReadParse(*in);
	print <<EOF1;
	<h1 align=center>Acronym Lookup</h1>
	<h3>Search results for  $in{'abb'}</h3>
	
EOF1
;
	my @matches;
	my @results;
	
	my @abv;
	my $i=0;
	my $pos;
	
	open MYFILE,"$rooturl/$abfile" or &error("cannot open file");
	my $query=uc($in{'abb'});
	while(<MYFILE>)
	{
		if(/$query/)
		{
			
			@abv=split(/[\t ]+/,$_);
			if($abv[0]=~/$query/)
			{
				push(@matches,$abv[0]);		#push the acronym
				shift(@abv);
				$results[$i]=join(" ",@abv);
				$pos=tell MYFILE;
				$line=<MYFILE>;
				while($line=~/^[\t ]+/)
				{
					@abv=split(/[\t ]+/,$line);
					$temp1=join(" ",@abv);
					$results[$i]=$results[$i]."<br>".$temp1;
					$line=<MYFILE>;
				}
				
				seek MYFILE,$pos,0;
				
				$i++;
			}
		}
	}
		
	close MYFILE;
	
	print "<table width=70% border=0 align =center cellspacing=0 cellpadding=10>";
	foreach my $i(0..$#matches)
	{
		
		print "<tr valign=top>";
			print "<td width=30%><font color=green>$matches[$i]</font></td>";
			print "<td width=70%><font color=yellow>$results[$i]</font></td>";
		print "</tr>";

	}
	print "</table>";
	print "<p><p><CENTER>Click <a href=$siteurl/cgi-bin/abbrev.cgi>here</a> to perform a new search</center>";
	
	
	
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
	


