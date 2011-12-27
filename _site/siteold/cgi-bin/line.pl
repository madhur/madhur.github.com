#!e:/perl/bin/perl.exe
use strict;
use warnings;


open (CURDIR,"-|","cd") or die("\ncommand failed");

my $df=<CURDIR>;
print $df;
#$df =~ s/\\/\\\\/g;
print $df;

opendir MYDIR,"e:\\impdata\\site\\cgi-bin" or die("\nerror in program");

my $filename;
my $path;

print "\nEnter the shebang line without #!";
$path=<STDIN>;
$path="#!".$path;
while($filename=readdir(MYDIR))
{	
	#print $filename;
	if($filename=~/\.pl|\.cgi/)
	{
		open MYFILE,"+<$filename" or die ("cannot open $filename");
		my $loc=tell MYFILE;
		print $loc;
		my $old=<MYFILE>;
		chop $old;
		print MYFILE $path;
		print "$old changed to $path";
		close MYFILE;
		
		print "\n$filename";
		exit;
		
	}
}
	


