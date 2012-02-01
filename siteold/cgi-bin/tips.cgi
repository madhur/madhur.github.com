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

&ReadParse(*in);
	
my $tipfile="$in{'file'}.txt";

print "content-type:text/html\n\n";

print <<EOF1;

<html>
<head>
<title>Tips & Troubleshooting</title>
<base href=$siteurl>
<style>
A:visited {text-decoration: none;} A:link {text-decoration: none;} A:active {text-decoration: none;} A:hover {text-decoration: underline; color:red;}
</style>

<link rel="stylesheet" type="text/css" href="programming.css" />

EOF1
;

open(MYFILE1,"$rooturl/$menufile") || &error("\n$rooturl/$menufile Cannot open file1","fatal");
while(<MYFILE1>)
{
	print $_;
}

close MYFILE1;


print "<h1 align=center>$in{'title'}</font></h1>";

	
print "	<hr>\n<ul>\n";
	
	
	my $index=1;
	open MYFILE,"$rooturl/$tipfile" or &error("\ncannot open file","fatal");
	while(<MYFILE>)
	{
		my @words=split(/ /,$_);
		my $line;
		
	
		if($words[0] eq "Q")
		{
			$line=$words[0];
			#@line=split(/[Q-R] /$_);
			while($line ne "")
			{
				
				shift(@words);
				
				print "<li>";
				print "<a href=$ENV{'REQUEST_URI'}#$index>@words</a>";
				print "</li>\n";
				$index++;
				$line=<MYFILE>;
				chomp($line);
				@words=split(/ /,$_);
			}
		}
	}
	
	close MYFILE;
				
	print	"\n</ul><hr>\n<ul>";

	
	$index=1;
	open MYFILE,"$rooturl/$tipfile" or &error("\ncannot open file","fatal");
	while(<MYFILE>)
	{
		my @words=split(/ /,$_);
		my $line;
		if($words[0] eq "Q" )
		{
			while($words[0] ne "")
			{
				
				shift(@words) if ($words[0] eq "Q");
				
				print "<p><li><b><i>";
				print "<a name=$index></a>@words";
				print "</li></b></i>\n";
				$index++;
				$words[0]=<MYFILE>;
				chomp($words[0]);
				@words=split(/ /,$words[0]);
			}
			
		}
		if($words[0] eq "A")
		{
			while($words[0] ne "-")
			{
				shift(@words) if ($words[0] eq "A");
				print "<br>@words\n";
				$line=<MYFILE>;
				chomp($line);
				@words=split(/ /,$line);
			
			}
			
		}
		
	}
	
	close MYFILE;
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
	