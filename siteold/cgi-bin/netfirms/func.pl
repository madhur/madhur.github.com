
sub get_vars
{
	return ("http://$ENV{SERVER_NAME}","$ENV{DOCUMENT_ROOT}/www","menu.htm");
}




sub get_host {
	my ($ip_address,$ip_number,@numbers);
	if ($ENV{'REMOTE_HOST'}) {
		$host = $ENV{'REMOTE_HOST'};
	}
	else { 
		$ip_address = $ENV{'REMOTE_ADDR'};
		@numbers = split(/\./, $ip_address);
		$ip_number = pack("C4", @numbers);
		$host = (gethostbyaddr($ip_number, 2))[0];
	}
	if ($host eq "") {
		$host = "IP\: $ENV{'REMOTE_ADDR'}";
	}
	return $host;
}

sub error
 {
print <<EOF6
<p>$_[0]
<br>Please report this error to <a href=mailto:madhur_ahuja@yahoo.com>Madhur Ahuja</a>
<p>
EOF6
;

if ($_[1] eq "fatal") 
{
	print "<table width=\"95%\" border=0 cellspacing=1 cellpadding=5 align=center >\n";
	print "<tr>\n    <td colspan=\"2\"><b><font size=\"2\">Environment Variables</font></b></td>\n  </tr>\n";
	foreach $key (sort keys %ENV) {
  		print "  <tr>\n    <td><font size=\"2\">$key</font></td>\n    <td><font size=\"2\">$ENV{$key}&nbsp;</font></td>\n  </tr>\n";
}
	print "</table>\n";
}
exit (0);
}

	
sub get_time {
my ($min,$hour,$mday,$mon,$year,$wday,@month,@days);
@months = ('January','February','March','April','May','June','July','August','September','October','November','December');
@days = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');

($min,$hour,$mday,$mon,$year,$wday) = (localtime(time+($fix_time*3600)))[1,2,3,4,5,6];
$min = "0$min" if ($min < 10);
$hour = "0$hour" if ($hour < 10);
$mday = "0$mday" if ($mday < 10);
$year += 1900;
$this_day = ("$days[$wday], $months[$mon] $mday, $year at $hour:$min");
return $this_day;
}



1;