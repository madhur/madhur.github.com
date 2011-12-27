#!e:/perl/bin/perl.exe

my ($siteurl,$rooturl,$menufile)=&get_vars;
#
######################################################################
# ONLY EDIT THIS PART OF THE SCRIPT!!

$number_of_digits = "6";
$end = ".gif";

$pathtocounter = "$rooturl/counter/counter.txt";
$pathtoimages = "$rooturl/counter/";

$graphics = "yes";

# DO NOT EDIT BELOW THIS LINE!!
############################################################################

# Tell Browser

print ("Content-type: text/html\n\n");

# Get Count

open (COUNTER, "$pathtocounter");
$count = <COUNTER>;
chop ($count) if $count =~ /\n$/;
close (COUNTER);

# Increase Count

$count += 1;

open (COUNTER, ">$pathtocounter");
print COUNTER ("$count");
close (COUNTER);

@digits = split(//, $count);

if ($number_of_digits eq "") {
        $howmany = @digits;
} else {
        $howmany = $number_of_digits;
}

# Give empty digits a value

$spline = '%0' . $howmany . 'd';
$count = sprintf("$spline", $count);

@digitimages = split(//, $count);

# Print Output Counter

foreach $digitimage (@digitimages) {
	if ($graphics eq yes) {
        $image = "<img src=$pathtoimages" . "$digitimage" . "$end>";
	print ("$image");
	} else {
        $plain = $digitimage;
 	print ("$plain");
	}
}

exit;
