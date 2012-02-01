#!e:/perl/bin/perl.exe
use CGI::Carp qw(fatalsToBrowser); 
require 'func.pl';

#
#     Traffic Log 
#
#     by  David J Spelts
#     http://www.spelts.com/
#     david@spelts.com
#                                       
# COPYRIGHT NOTICE:
#
# Copyright 2002 David J Spelts  All Rights Reserved.
#
# Selling the code for this program without prior written consent is 
# expressly forbidden.  You may not redistribute this program
# over the Internet or in any other medium.  In all cases copyright
# and header must remain intact.
#
# This program is distributed "as is" and without warranty of any
# kind, either express or implied.  (Some states do not allow the
# limitation or exclusion of liability for incidental or consequential
# damages, so this notice may not apply to you.)  In no event shall
# the liability of David J Spelts for any damages, losses and/or causes 
# of action exceed the total amount paid by the user for this software.

my ($siteurl,$rooturl,$menufile)=&get_vars;
#   Enter the path of the LOG file (the path, not the URL).
$logs = "$rooturl/log/logs.txt";

#   Enter the password required to access your statistics.
#   Leave this null if you don't want to have to enter passwords.
$password="goldi";


#   Do not edit below this line
#   ---------------------------------------------------------------

print "Content-type: text/html\n\n";

MAIN:
{
&ReadParse;

if (($in{'password'} eq $password) || !$password) {
	if ($in{'page'} eq "byDay") {
		&byDay;
	} elsif ($in{'page'} eq "byPage") {
		&byPage;
	} elsif ($in{'page'} eq "byEntry") {
		&byEntry;
	} elsif ($in{'page'} eq "byBrowser") {
		&byBrowser;
	} elsif ($in{'page'} eq "Purge") {
		&Purge;
	} elsif ($in{'cleanup'} eq "Purge Stats") {
		&Clean_Stats;
	} else {
		&Summary;
	}
} else {
	&NeedPassword;
	}
}

#######  NeedPassword   ##########
sub NeedPassword {
print <<EOT;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<HTML><HEAD><TITLE>Traffic Log</TITLE></HEAD>
<BODY bgcolor="336699" LINK="000066" VLINK="660088">
<BR><BR><H1 align="center">Traffic Log</H1>
<BR><BR><center>
<form method=get>
<table border="0" width="40%">
<tr><td align=left>Password:</td>
<td align=left><input type="password" name="password" length="15"></td>
<td align=left><input type="submit" value="Submit"></td></tr>
</table></form>
</center></BODY></HTML>
EOT
}

##########  Summary  ##########
sub Summary {

%unique_ips=();
%dates=();
%daily_hits=();
%page_hits=();
%visits=();
%entry_pages=();
%browsers=();
%months = ("00","Jan","01","Feb","02","Mar","03","Apr","04","May","05","Jun","06","Jul","07","Aug","08","Sep","09","Oct","10","Nov","11","Dec");

print "$logs";
open(INF,"$logs") || print "Cannot open logs file\n";
@hits= <INF>;
close(INF);

$number_hits=@hits;
($fdate,$fip,$fpage,$fbrowser)= split(/\|/,@hits[0]);  
($ldate,$lip,$lpage,$lbrowser)= split(/\|/,@hits[$#hits]);
$fyear = substr($fdate,0,2);
$fmonth = substr($fdate,2,2);
$fday = substr($fdate,4,2);
$lyear = substr($ldate,0,2);
$lmonth = substr($ldate,2,2);
$lday = substr($ldate,4,2);

foreach $i (@hits) {
	($date,$ip,$page,$browser)= split(/\|/,$i);
	$unique_ips{$ip}++;
	$dates{$date}++;
	$daily_hits{$date}++;
	$browsers{$browser}++;
	if ($page) {
		$page_hits{$page}++;
		$string="$visits{$ip}$page|";
		$visits{$ip}=$string;
	}
}

@u_ips=%unique_ips;
$ips=(@u_ips/2);
@u_dates = %dates;
($number_days = (@u_dates/2)) || ($number_days=1); #prevent division by zero
$avg_hits = sprintf("%0d",$number_hits/$number_days);
$avg_u_ips = sprintf("%0d",$ips/$number_days);

#  Calculate Top Date
foreach $key (sort DaySort (keys(%daily_hits))) { 
	@top_day = (@top_day,$key);
}
$topyear = substr($top_day[0],0,2);
$topmonth = substr($top_day[0],2,2);
$topdate = substr($top_day[0],4,2);

#  Calculate Top Page
foreach $key (sort PageSort (keys(%page_hits))) { 
	@top_page = (@top_page,$key);
}

#  Find Entry Pages
foreach $i (%visits) {
  ($page,$rest)= split(/\|/,$visits{$i});  
  ($page gt "a") && ($entry_pages{$page}++);
}

#  Calculate Top Entry Page
foreach $key (sort EntrySort (keys(%entry_pages))) { 
	@top_entry = (@top_entry,$key);
}


#  Calculate Top Browser
foreach $key (sort BrowserSort (keys(%browsers))) { 
	@top_browser = (@top_browser,$key);
}

&PrintHeader;

print <<EOT;
<font color="000066"><B>Summary</B></font><BR>
<table width="70%" border=0 bgcolor="F3F3F3" cellspacing=1 cellpadding=1>
<tr><td align=left>Total Hits</td><td align=right>$number_hits</td></tr>
<tr><td align=left>Average Hits</td><td align=right>$avg_hits</td></tr>
<tr><td align=left>Unique Visitors</td><td align=right>$ips</td></tr>
<tr><td align=left>Average Unique Visitors</td><td align=right>$avg_u_ips</td></tr>
<tr><td align=left>Starting</td><td align=right>$months{$fmonth} $fday, 20$fyear</td></tr>
<tr><td align=left>Ending</td><td align=right>$months{$lmonth} $lday, 20$lyear</td></tr>
<tr><td align=left>Top Day</td><td align=right>$months{$topmonth} $topdate, 20$topyear</td></tr>
<tr><td align=left>Top Page</td><td align=right>http://$top_page[0]</td></tr>
<tr><td align=left>Top Entry Page</td><td align=right>http://$top_entry[0]<td align=left></tr>
<tr><td align=left>Top Browser</td><td align=right>$top_browser[0]</td></tr>
</table>
EOT
&PrintFooter;
}

##########  byDay  ##########
sub byDay { 
%daily_hits=();
%months = ("00","Jan","01","Feb","02","Mar","03","Apr","04","May","05","Jun","06","Jul","07","Aug","08","Sep","09","Oct","10","Nov","11","Dec");
open(INF,"$logs") || print "Cannot open logs.txt file\n";
@hits= <INF>;
close(INF);
foreach $i (@hits) {
	($date,$ip,$page,$browser)= split(/\|/,$i);
	$daily_hits{$date}++;
}
&PrintHeader;
print "<font color=000066><B>Hits by Day</B></font><BR>\n";
print "<table width=\"70\%\" border=0 bgcolor=F3F3F3 cellspacing=4 cellpadding=4>\n";
foreach $key (sort DaySort (keys(%daily_hits))) { 
	@top_day = (@top_day,$key,$daily_hits{$key});
}
($max = $top_day[1]) || ($max = 1);
($max >= 300) && ($divisor = $max/300);
($max < 300) && ($multiplier = 300/$max);
foreach $key (sort keys %daily_hits) { 
	($divisor) && ($width = sprintf("%0d",$daily_hits{$key}/$divisor));
	($multiplier) && ($width = sprintf("%0d",$daily_hits{$key} * $multiplier));
	$year = substr($key,0,2);
	$month = substr($key,2,2);
	$day = substr($key,4,2);
	print "<tr><td align=left>$months{$month} $day, 20$year <hr align=left width=$width size=5 color=000066></td><td align=right valign=top>$daily_hits{$key}</td></tr>\n";
}
print "</table>\n";
&PrintFooter;
} 

##########  byPage  ##########
sub byPage { 

%page_hits=();
open(INF,"$logs") || print "Cannot open logs.txt file\n";
@hits= <INF>;
close(INF);
foreach $i (@hits) {
	($date,$ip,$page,$browser)= split(/\|/,$i);
	if ($page) {
		$page_hits{$page}++;
	}
}
&PrintHeader;
print "<font color=000066><B>Hits by Page</B></font><BR>\n";
print "<table width=\"70\%\" border=0 bgcolor=F3F3F3 cellspacing=4 cellpadding=4>\n";
$max = 1;
foreach $key (sort PageSort (keys(%page_hits))) { 
	($max > $page_hits{$key}) || ($max = $page_hits{$key});
	($max >= 300) && ($divisor = $max/300);
	($max < 300) && ($multiplier = 300/$max);
	($divisor) && ($width = sprintf("%0d",$page_hits{$key}/$divisor));
	($multiplier) && ($width = sprintf("%0d",$page_hits{$key} * $multiplier));
	print "<tr><td align=left>http://$key<hr align=left width=$width size=5 color=000066></td><td align=right valign=top>$page_hits{$key}</td></tr>\n";
}
print "</table>\n";
&PrintFooter;
} 

##########  byEntry  ##########
sub byEntry { 
%visits=();
%entry_pages=();
open(INF,"$logs") || print "Cannot open logs.txt file\n";
@hits= <INF>;
close(INF);
foreach $i (@hits) {
	($date,$ip,$page,$browser)= split(/\|/,$i);
	if ($page) {
		$string="$visits{$ip}$page|";
		$visits{$ip}=$string;
	}
}
foreach $i (%visits) {
  ($page,$rest)= split(/\|/,$visits{$i});  
  ($page gt "a") && ($entry_pages{$page}++);
}
&PrintHeader;
print "<font color=000066><B>Entry Pages</B></font><BR>\n";
print "<table width=\"70\%\" border=0 bgcolor=F3F3F3 cellspacing=4 cellpadding=4>\n";
$max = 1;
foreach $key (sort EntrySort (keys(%entry_pages))) { 
	($max > $entry_pages{$key}) || ($max = $entry_pages{$key});
	($max >= 300) && ($divisor = $max/300);
	($max < 300) && ($multiplier = 300/$max);
	($divisor) && ($width = sprintf("%0d",$entry_pages{$key}/$divisor));
	($multiplier) && ($width = sprintf("%0d",$entry_pages{$key} * $multiplier));
	print "<tr><td align=left>http://$key<hr align=left width=$width size=5 color=000066></td><td align=right valign=top>$entry_pages{$key}</td></tr>\n";
}

print "</table>\n";
&PrintFooter;
} 

##########  byBrowser  ##########
sub byBrowser { 
%browsers=();
open(INF,"$logs") || print "Cannot open logs.txt file\n";
@hits= <INF>;
close(INF);
foreach $i (@hits) {
	($date,$ip,$page,$browser)= split(/\|/,$i);
	$browsers{$browser}++;
}
&PrintHeader;
print "<font color=000066><B>Browsers</B></font><BR>\n";
print "<table width=\"70\%\" border=0 bgcolor=F3F3F3 cellspacing=4 cellpadding=4>\n"; 
$max = 1;
foreach $key (sort BrowserSort (keys(%browsers))) { 
	($max > $browsers{$key}) || ($max = $browsers{$key});
	($max >= 300) && ($divisor = $max/300);
	($max < 300) && ($multiplier = 300/$max);
	($divisor) && ($width = sprintf("%0d",$browsers{$key}/$divisor));
	($multiplier) && ($width = sprintf("%0d",$browsers{$key} * $multiplier));
	print "<tr><td align=left>$key<hr align=left width=$width size=5 color=000066></td><td align=right valign=top>$browsers{$key}</td></tr>\n";
}
print "</table>\n";
&PrintFooter;
} 

##########  Purge  ##########
sub Purge { 
@month_list = ("January","February","March","April","May","June","July","August","September","October","November","December");
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = localtime(time);
$year =~ s/^.//;
$year = "20" . $year;
$lastyear = ($year -1);
&PrintHeader;

print <<EOT;
<font color=000066><B>Purge Stats Prior To:</B></font><BR>
<form method="get">
<input type="hidden" name="password" value="$in{'password'}">
<table width="70%" border=0 bgcolor=F3F3F3 cellspacing=4 cellpadding=4>
<tr><td align=left><select name="Month" size=1>
EOT

foreach $i (@month_list) {
	if ($i eq $month_list[$mon]) {
		print "<option selected>$i\n";
	} else {
		print "<option>$i\n";
	}
}
print "</select></td><td align=left><select name=Date size=1>\n";
$x=1;
until ($x > 31) {
	print "<option>$x\n";
	$x++;
}
print "</select></td><td align=left><select name=Year size=1><option>$lastyear<option selected>$year</select></td>\n";
print "<td align=left><input type=submit value=\"Purge Stats\" name=cleanup></td></tr></table></form>\n";
&PrintFooter;
} 

##########  Clean_Stats  ##########
sub Clean_Stats { 

@clean_hits = ();
%months = ("January","00","February","01","March","02","April","03","May","04","June","05","July","06","August","07","September","08","October","09","November","10","December","11");
$year = substr($in{'Year'},2,2);
$month = $months{$in{'Month'}};
$date = sprintf("%.2d",$in{'Date'});
$compare_date = $year . $month . $date;
open(INF,"$logs") || print "Cannot open logs.txt file\n";
@hits= <INF>;
close(INF);
foreach $i (@hits) {
	($i >= $compare_date) && (@clean_hits=(@clean_hits,$i));
}
open(OUTF,">$logs");
print OUTF @clean_hits;
close(OUTF);
&Summary; 
}

##########  PrintHeader  ##########
sub PrintHeader { 
print <<EOT;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<HTML><HEAD><TITLE>Traffic Log</TITLE>
EOT


print <<EOT;
<script language="javascript">
function mOvr(src,clrOver){ 
	if (!src.contains(event.fromElement)){ 
		src.style.cursor = 'hand'; 
		src.bgColor = clrOver; 
	} 
} 
function mOut(src,clrIn){ 
	if (!src.contains(event.toElement)){ 
		src.style.cursor = 'default'; 
		src.bgColor = clrIn; 
	} 
} 
</script>
</HEAD>
<BODY bgcolor="336699" LINK="000066" VLINK="660088">
<center>
<table width="100%" border=0 bgcolor="F3F3F3" cellspacing=3 cellpadding=3>
<tr><td align=left><H1 align="center"><font color="000066">Traffic Log</font></H1></td></tr>
<tr><td align=left><table width="100%" border=0 bgcolor="F3F3F3" cellspacing=3 cellpadding=3>
<tr><td width=100 valign=top>
<BR>
<TABLE WIDTH="100%" BGCOLOR="000066" BORDER=0 CELLSPACING=1 CELLPADDING=1>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Summary</B></FONT></a></TD></TR>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?page=byDay&password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Hits by Day</B></FONT></a></TD></TR>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?page=byPage&password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Hits by Page</B></FONT></a></TD></TR>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?page=byEntry&password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Entry Pages</B></FONT></a></TD></TR>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?page=byBrowser&password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Browsers</B></FONT></a></TD></TR>
<TR><TD bgcolor="#336699" onmouseover='mOvr(this,"#333366");' onmouseout='mOut(this,"#336699");'><A HREF="$ENV{'SCRIPT_NAME'}?page=Purge&password=$in{'password'}"><FONT COLOR="FFFFFF"><B>Purge</B></FONT></a></TD></TR>
</TABLE><BR><BR><BR><BR><BR>
</td><td align=center valign=top>
EOT
} 

##########  PrintFooter  ##########
sub PrintFooter { 
print <<EOT;
</td></tr></table>
<BR><BR><BR><BR>
</td></tr></table>
<a href=http://www.spelts.com/><font size="-1" color=white>David Spelts Software &#169;</font></a>
</center></BODY></HTML>
EOT
} 

##########   ReadParse  ##########
sub ReadParse {

local (*in)= @_ if @_;
local ($i,$key,$val);

# Read in text
if (&MethGet) {
  $in=$ENV{'QUERY_STRING'};
  } elsif (&MethPost) {
  read(STDIN,$in,$ENV{'CONTENT_LENGTH'});
  }

@in=split(/[&;]/,$in);

foreach $i (0..$#in) {
  #Convert plus"s to spaces
  $in[$i] =~ s/\+/ /g;

  #Split into key and value.
  ($key, $val) = split(/=/,$in[$i],2); # splits on the first =.

  #Convert %XX from hex numbers to alphanumeric
  $key =~ s/%(..)/pack("c",hex($1))/ge;
  $val =~ s/%(..)/pack("c",hex($1))/ge;

  #Associate key and value
  $in{$key} .= "\0" if (defined($in{$key})); # \0 is the multiple separator
  $in{$key} .= $val;

}
return scalar(@in);
}

##########  MethGet  ##########
sub MethGet {
  return ($ENV{'REQUEST_METHOD'} eq "GET");
}

##########  MethPost  ##########
sub MethPost {
  return ($ENV{'REQUEST_METHOD'} eq "POST");
}

##########  DaySort  ##########
sub DaySort { 
  $daily_hits{$b} <=> $daily_hits{$a}; 
} 

##########  PageSort  ##########
sub PageSort { 
  $page_hits{$b} <=> $page_hits{$a}; 
} 

##########  EntrySort  ##########
sub EntrySort { 
  $entry_pages{$b} <=> $entry_pages{$a}; 
} 


##########  BrowserSort  ##########
sub BrowserSort { 
  $browsers{$b} <=> $browsers{$a}; 
} 
