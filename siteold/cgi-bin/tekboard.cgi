#!e:/perl/bin/perl
############################################################################
#
#                           TEKBOARD.CGI  V2.0
#
#                            By Metertek 1999
#                           Metertek@yahoo.com
#
#                     Call script using a similar tag
#
#   <a href="http://www.domain.com/cgi-bin/tekboard.cgi">Message Board</a> 
#
############################################################################
#                                variables

$boardfile = "$ENV{'DOCUMENT_ROOT'}/tekboard.txt";
$tablebackground = 'bgcolor="#0080FF"';
$background = 'bgcolor="#8080FF"';
$textcolor = '"#000080"';
$alink = 'link="#00FF00"';
$vlink = 'vlink="#00FF00"';
$postimage = 'http://your.domain.com/yourdir/message.jpg';
$homelink = 'http://your.domain.com/yourdir/home.html';
$bookname = 'Message Board';
$boardtext ='Welcome to our Message Board, Post a message now.'; 
$adminpass = 'metertek';
$addsecs = '0';
$linktoadmin = '1';
$usehomelink = '1';
$useboardtext = '1';
@cusses = ("Damn","damn","Heck","heck","Poo","poo","Bloody","bloody");

#
############################################################################
#                       DO NOT ALTER PERL BELOW HERE

$domain = 'http://'.$ENV{'SERVER_NAME'};
$path = $ENV{'DOCUMENT_ROOT'};
$referrer = $ENV{'HTTP_REFERER'};
$cgiurl = $domain.$ENV{'SCRIPT_NAME'};
$home = 'http://members.xoom.com/metertek/archive/';
$ip = $ENV{'REMOTE_ADDR'}; 
$pagemark = 'Tekboard Message Entries';
$return ='<font size=1><FORM METHOD=POST ACTION="'.$cgiurl.'"><INPUT TYPE="SUBMIT" 
NAME="RETURN" VALUE="'.$bookname.'">';
$reply =' &nbsp; <INPUT TYPE="SUBMIT" NAME="REPLY" VALUE="Reply"></FORM>';

&date;
&read;

if ($INPUT{'REPLY'}) { $reply=1; $replylink=$INPUT{'LINK'}; &create; }
if ($INPUT{'RETURNADMIN'}) { $adminpass=$password; &admin; }
if ($INPUT{'REMOVE'}) { &remove; &admin;}
if ($INPUT{'SENDPASS'}) { &admin; }
if ($INPUT{'SIGN'}) { &create; }
if ($INPUT{'ADD'}) { &editboard; }
&showboard;
exit;

#
############################################################################

sub read {

if ($ENV{'QUERY_STRING'}) {$namevalues = $ENV{'QUERY_STRING'};}
else {read(STDIN, $namevalues, $ENV{'CONTENT_LENGTH'});}

@pairs = split(/&/, $namevalues);
	foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
        $value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        $value =~ s/<!--(.|\n)*-->//g;
        if ($name ne '') { &action; }
        $value =~ s/<([^>]|\n)*>//g;
	$INPUT{$name} = $value;}
        
}

############################################################################

sub date { 

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time+$addsecs); 
@months = ("01","02","03","04","05","06","07","08","09","10","11","12"); 
@days = ("Sun","Mon","Tue","Wed","Thu","Fri","Sat");

   if ($sec < 10) {$sec = "0$sec";}
   if ($min < 10) {$min = "0$min";}
   if ($hour < 10) {$hour = "0$hour";}
   if ($hour > 11) {$ap = "PM";}
   if ($hour < 12) {$ap = "AM";}
   if ($mday < 10) {$mday = "0$mday";}
   
$millyear = $year + 1900;   
$date = "@days[$wday]$mday/@months[$mon]/$millyear";
$time = "$hour:$min:$sec$ap";

} 

############################################################################

sub action {

if ($name eq 'admin') { &adminpass; }

else {
if ($name =~ 'adminlink') {
@adminlink = split(/\&/,$name); $name = $adminlink[1];
$returnadmin=' &nbsp; <INPUT TYPE="SUBMIT" NAME="RETURNADMIN" VALUE="Admin">'; }

open (FILE, "$boardfile"); @lines = <FILE>; close(FILE); &getreplies;
open (BOARD,"$boardfile");
foreach $line (@lines) {
&getvalues; 

if ($name eq $link) {
$title=$bookname; $headertext='Subject: "'.$postsubject.'"'; 
$responsetext='</center><font size=1>'.$replylinktext.'<br>Posted by: '.$username.'<br>IP Address: '.$userip.'<br>Date posted: '
.$messdate.'<br>Time posted: '.$messtime.'<br>Email: <A HREF="Mailto:'.$usermail.'">
'.$usermail.'</a><p><center><font size=2>'.$postmessage.'<br><br><br>'.$return.
'<INPUT TYPE="HIDDEN" NAME="LINK" VALUE="'.$link.'">
<INPUT TYPE="HIDDEN" NAME="SUBJECT" VALUE="'.$postsubject.'">'.$returnadmin.$reply; &response; }

}}
close (BOARD);

if ($name eq 'RETURN') { &showboard; }

}

############################################################################

sub response {

print ("Content-type: text/html\n\n");
print ("<HTML>\n");
print ("<HEAD>\n");
print ("<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n");
print ("<TITLE>$title</TITLE></HEAD>\n");
print ("<BODY $background $alink $vlink text=$textcolor>\n");
print ("<center><font face=verdana size=\"\+2\">$headertext</font>\n");
print ("<hr><table border=0 width=90% height=70%><tr><td align=center>\n");
print ("<font face=\"verdana\" size=2><b>$responsetext\n");
print ("</b></font></td></tr></table><hr width=90%>\n");
print ("<font face=\"verdana\" color=\"\#000080\"size=1><b><center>\n");
print ("TEKBOARD.CGI<br><a href=\"$home\">© Metertek Perl Scripts</a></font></center>\n");
print ("</BODY>\n");
print ("</HTML>\n");

$title ='';
$headertext='';
$responsetext = '';
exit;

}

############################################################################

sub editboard {

$num = 0;
$name = $INPUT{'NAME'}; 
$email = $INPUT{'EMAIL'};
$comments = $INPUT{'COMMENTS'};
$subject = $INPUT{'SUBJECT'};
$replyto = $INPUT{'REPLYTO'};
$space = ' ';
$enter = '\cM\n';
$replace = '<br>';
$comments =~ s/$enter/$replace/g; $comments =~ s/\(\(/</g;
$comments =~ s/\)\)/>/g; $comments =~ s/\|/I/g;
if ($name eq '') { $num = ($num + 1); }
if ($email eq '') { $num = ($num + 1); }
if ($comments eq '') { $num = ($num + 1); }
if ($subject eq '') { $num = ($num + 1); }

if ($num ne 0) {
$title='TEKBOARD ERROR MESSAGE';
$headertext='Please complete all Form Fields';
$responsetext=$num.' Form fields not completed<p><FORM>
<INPUT TYPE=button VALUE="RETRY" onClick="history.go(-1)"></FORM>'; &response;}

&censor;

open (FILE, "$boardfile");
@lines = <FILE>;
close(FILE);

open (BOARD,">$boardfile");
if (@lines < 1) {print BOARD "<!--$pagemark-->\n"; close (BOARD);
open (FILE, "$boardfile"); @lines = <FILE>; close(FILE);
open (BOARD,">$boardfile");}

if ($replyto eq '') {
foreach $line (@lines) {
if ($line =~ /<!--$pagemark-->/) { 
print BOARD ("<!--$pagemark-->\n");
print BOARD ("$date|$time|$ip|$name|$email|$subject|$comments|0||0|\n");}
else {print BOARD ("$line");} 
}
}
else {
foreach $line (@lines) { &getvalues; 
if ($replyto eq $link) { $line =~ s/$enter/$replace/g; $replies=$replies+1; 
if ($replylink ne '') { $replylink =~ s/$enter/$replace/g;
print BOARD ("$messdate|$messtime|$userip|$username|$usermail|$postsubject|$postmessage|$replies|$replylink|$tierlevel|\n");
} else {
print BOARD ("$messdate|$messtime|$userip|$username|$usermail|$postsubject|$postmessage|$replies||$tierlevel|\n");
}
$tierlevel=$tierlevel+1;
print BOARD ("$date|$time|$ip|$name|$email|$subject|$comments|0|reply=$link|$tierlevel|\n"); }
else {print BOARD ("$line");} 
}
}
close (BOARD);
}

############################################################################

sub create {

if ($reply eq 1) { $desctext='Post a Reply'; $buttontext='POST REPLY'; 
$re='Re: '; $INPUT{'SUBJECT'} =~ s/$re/$replace/g; $replysub = $re.$INPUT{'SUBJECT'}; }
else { $desctext='Add a Message'; $buttontext='ADD MESSAGE'; $replysub ='';}

print ("Content-type: text/html\n\n");
print ("<HTML>\n");
print ("<HEAD>\n");
#print ("<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n");
print ("<TITLE>$bookname</TITLE></HEAD>\n");
print ("<BODY $background $alink $vlink text=$textcolor><CENTER>\n");
print ("<font face=verdana size=\"\+3\">$desctext</font>\n");
print ("<hr><br><font face=\"verdana\" size=2><b>\n");
print ("To $desctext complete all fields below</b></font><P>\n");
print ("<TABLE border=0 cellspacing=0 cellpadding=0 width=100%><TR>\n");
print ("<TD width=35% align=center><FORM METHOD=POST ACTION=\"$cgiurl\">\n");
if ($reply eq 1) { print ("<INPUT TYPE=\"HIDDEN\" NAME=\"REPLYTO\" VALUE=\"$replylink\">\n"); }
print ("<font face=\"verdana\" size=2><b>Name<br></b></font>\n");
print ("<INPUT TYPE=\"TEXT\" NAME=\"NAME\" size=25 maxlength=30><br>\n");
print ("<font face=\"verdana\" size=2><b>Email<br></b></font>\n");
print ("<INPUT TYPE=\"TEXT\" NAME=\"EMAIL\" size=25 maxlength=30><br>\n");
print ("<font face=\"verdana\" size=2><b>Subject<br></b></font>\n");
print ("<INPUT TYPE=\"TEXT\" NAME=\"SUBJECT\" size=25 value=\"$replysub\" maxlength=30></TD>\n");
print ("<TD width=55% align=center>\n");
print ("<font face=\"verdana\" size=2><b>Comments<br></b></font>\n");
print ("<TEXTAREA name=\"COMMENTS\" COLS=32 ROWS=6 wrap=virtual></TEXTAREA></TD></TR>\n");
print ("</TABLE><P><INPUT TYPE=\"SUBMIT\" NAME=\"ADD\" VALUE=\"$buttontext\"> \n");
print ("<INPUT TYPE=\"SUBMIT\" NAME=\"RETURN\" VALUE=\"CANCEL\"> <INPUT TYPE=\"RESET\" VALUE=\"CLEAR FORM\"></FORM><P>\n");
print ("<hr width=90%>\n");
print ("<font face=verdana color=\"\#000080\"size=1><b><center>\n");
print ("TEKBOARD.CGI 1999<br><a href=\"$home\">© Metertek Perl Scripts</a></font></center>\n");
print ("</BODY>\n");
print ("</HTML>\n");

exit;

}

############################################################################

sub showboard {

print ("Content-type: text/html\n\n");
print ("<HTML>\n");
print ("<HEAD>\n");
print ("<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n");
print ("<TITLE>$bookname</TITLE></HEAD>\n");
print ("<BODY $background $alink $vlink text=$textcolor><CENTER>\n");
print ("<font face=verdana size=\"\+3\">$bookname</font><HR>\n");

if ($linktoadmin eq 1) {
print ("<font size=1><b><a href=\"$cgiurl?admin\">Script Administration</a></b></font> &nbsp\; &nbsp\; \n");
}
if ($usehomelink eq 1) {
print ("<font size=1><b><a href=\"$homelink\">Home</a></b></font>  &nbsp\; &nbsp\; \n");
}
print ("<font size=1><b><a href=\"$cgiurl\" target=top>New Window</a></b></font>\n");

if ($useboardtext eq 1) {print ("<P><font size=2><b>$boardtext</b></font>\n"); }

print ("<FORM METHOD=POST ACTION=\"$cgiurl\">\n");
print ("<P><TABLE BORDER=0 cellspacing=0 cellpadding=5 width=140% height=48%><TR>\n");
print ("<TD $background><font face=\"verdana\" size=2><b>\n");

open (FILE, "$boardfile");
@lines = <FILE>;
close(FILE);

if(@lines >1) { open (BOARD,"$boardfile"); foreach $line (@lines) { 
if ($line =~ /<!--$pagemark-->/) { $fileexist=1; }
else { &getvalues; &printpost; }} close (BOARD); }

else { print "Message Board Empty"; }

print ("</b></font></TD></TR></TABLE><p><center>\n");
print ("<FORM METHOD=POST ACTION=\"$cgiurl\">\n");
print ("<INPUT TYPE=\"SUBMIT\" NAME=\"SIGN\" VALUE=\"ADD MESSAGE\">\n");
print ("<br><hr width=90%>\n");
print ("<font face=verdana size=1><b><center>\n");
print ("TEKBOARD.CGI 1999<br><a href=\"$home\">© Metertek Perl Scripts</a></font></center>\n");
print ("</BODY>\n");
print ("</HTML>\n");

exit;

}

############################################################################

sub censor {

$censor = '****';

foreach $cuss (@cusses) {
if ($comments =~ $cuss) { $comments =~ s/$cuss/$censor/g; }
if ($name =~ $cuss) { $name =~ s/$cuss/$censor/g; }
if ($email =~ $cuss) { $email =~ s/$cuss/$censor/g; }
if ($subject =~ $cuss) { $subject =~ s/$cuss/$censor/g; }
}

}

############################################################################

sub getvalues {

@data = split(/\|/,$line); $messdate = $data[0]; $messtime = $data[1]; 
$userip = $data[2]; $username = $data[3]; $usermail = $data[4]; 
$postsubject = $data[5]; $postmessage = $data[6]; $replies = $data[7]; 
$replylink = $data[8]; $tierlevel = $data[9]; $link=$userip.$messdate.$messtime;

}

############################################################################

sub getreplies {

open (BOARD,"$boardfile");
foreach $line (@lines) { 
&getvalues; if ($replylink eq 'reply='.$name) {
$linktext='Reply: <a href="'.$cgiurl.'?'.$link.'">'.$username.' '.$messdate.'</a><br>';
if ($replylinktext eq '') { $replylinktext=$linktext; }
else { $replylinktext=$replylinktext.$linktext; }
}}
close (BOARD);
}

############################################################################

sub printpost {

$tab=' &nbsp; &nbsp; &nbsp;';

if ($replies ne 0) { 
if ($replies eq 1) { $posts='Post'; } else { $posts='Posts'; }
$replytext = $replies.' Reply '.$posts; }
else { $replytext='No Reply Posts'; }

if ($tierlevel eq 0) { $tier=''; } 
if ($tierlevel eq 1) { $tier=$tab; }
if ($tierlevel eq 2) { $tier=$tab.$tab; } 
if ($tierlevel eq 3) { $tier=$tab.$tab.$tab; }
if ($tierlevel eq 4) { $tier=$tab.$tab.$tab.$tab; } 
if ($tierlevel eq 5) { $tier=$tab.$tab.$tab.$tab.$tab; }
if ($tierlevel eq 6) { $tier=$tab.$tab.$tab.$tab.$tab.$tab; } 
if ($tierlevel eq 7) { $tier=$tab.$tab.$tab.$tab.$tab.$tab.$tab; }
if ($tierlevel eq 8) { $tier=$tab.$tab.$tab.$tab.$tab.$tab.$tab.$tab; } 
if ($tierlevel eq 9) { $tier=$tab.$tab.$tab.$tab.$tab.$tab.$tab.$tab.$tab; }

print ("$tier<a href=\"$cgiurl?$userip$messdate$messtime\">\n");
print ("<img src=\"$postimage\" width=15 height=20 border=0 alt=\"$replytext\">\n");
print ("<font size=2>$postsubject</a><font size=1> -- posted by \n");
print ("<A HREF=\"Mailto:$usermail\">$username</a> on $messdate at $messtime<br>\n");

}

############################################################################

sub remove {

$removepost = $INPUT{'ENTRYLINK'};

open (FILE, "$boardfile");
@lines = <FILE>;
close(FILE);

open (BOARD,">$boardfile");
foreach $line (@lines) { &getvalues;
if ($link eq $removepost) { $postupdate=$replylink; $dellevel=$tierlevel; }
elsif ($tierlevel > $dellevel) { $delmess=$delmess+1; }
elsif ($tierlevel eq $dellevel) { $dellevel='10000'; print BOARD ("$line"); }
elsif ($tierlevel < $dellevel) { $dellevel='10000'; print BOARD ("$line"); }
else { print BOARD ("$line"); }
}
close (BOARD);

open (FILE, "$boardfile"); @lines = <FILE>; close(FILE);
open (BOARD,">$boardfile");
foreach $line (@lines) { &getvalues; $messupdate='reply='.$link;
if($messupdate eq $postupdate) { $replies=$replies-1;
print BOARD ("$messdate|$messtime|$userip|$username|$usermail|$postsubject|$postmessage|$replies|$replylink|$tierlevel|\n");
}
else { print BOARD ("$line"); }
}
close (BOARD);

$adminpass = $password;

}

############################################################################

sub adminpass {

print ("Content-type: text/html\n\n");
print ("<HTML>\n");
print ("<HEAD>\n");
print ("<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n");
print ("<TITLE>$bookname Admin Validation</TITLE></HEAD>\n");
print ("<BODY $background $alink $vlink text=$textcolor><CENTER>\n");
print ("<font face=verdana size=\"\+3\">Admin Password Validation</font><hr>\n");
print ("<TABLE BORDER=0 height=70% width=100%><tr><td align=center>\n");
print ("<font face=\"verdana\" size=2><b>\n");
if ($wrongpass eq 1) {print ("WRONG PASSWORD ENTERED<P>\n");}
print ("Enter the $bookname Administration Password below</b></font><P>\n");
print ("<BR><FORM METHOD=POST ACTION=\"$cgiurl\">\n");
print ("<INPUT TYPE=\"password\" NAME=\"PASSWORD\" size=20>\n");
print (" <INPUT TYPE=\"SUBMIT\" NAME=\"SENDPASS\" VALUE=\"VALIDATE\"></FORM>\n");
print ("</td></tr></table><hr width=90%>\n");
print ("<font face=\"verdana\" color=\"\#000080\"size=1><b><center>\n");
print ("TEKBOARD.CGI 1999<br><a href=\"$home\">© Metertek Perl Scripts</a></font></center>\n");
print ("</BODY>\n");
print ("</HTML>\n");

exit;

}

############################################################################

sub admin {

$password = $INPUT{'PASSWORD'};
if ($adminpass ne $password) {$wrongpass = 1; &adminpass;}

open (FILE, "$boardfile");
@lines = <FILE>;
close(FILE);

print ("Content-type: text/html\n\n");
print ("<HTML>\n");
print ("<HEAD>\n");
print ("<META HTTP-EQUIV=\"Pragma\" CONTENT=\"no-cache\">\n");
print ("<TITLE>$bookname Administration</TITLE></HEAD>\n");
print ("<BODY $background $alink $vlink text=$textcolor><CENTER>\n");
print ("<font face=verdana size=\"\+3\">$bookname Admin</font>\n");
print ("<hr><font face=\"verdana\" size=2><b>\n");
print ("<a href = \"$cgiurl\">Back to $bookname</a><P>\n");
if (@lines > 1) {print ("Choose an entry to remove from $bookname</font><P>\n");}
print ("</b><TABLE BORDER=4 cellspacing=0 cellpadding=5>\n");

if(@lines < 2) {
print ("<TR><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=2><b>$bookname empty\n");
}

else {
print ("<TR><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>User Names</b></font></td>\n");
print ("<TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>Date of entry</b></font></td>\n");
print ("<TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>Message</b></font></td>\n");
print ("<TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>Action</b></font></td></TR>\n");
}

if(@lines > 1) {
open (BOARD,"$boardfile");
foreach $line (@lines) { &getvalues;
if ($line=~/$pagemark/) { $textfileexist=1; }
else {
print ("<TR><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>\n");
print ("$username</font></td><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>\n");
print ("$messdate</font></td><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b>\n");
print ("<a href=\"$cgiurl?adminlink&$link\">$postsubject</a></font></td><TD $tablebackground align=center>\n");
print ("<font face=\"verdana\" size=1><b><FORM METHOD=POST ACTION=\"$cgiurl\">\n");
print ("<INPUT TYPE=\"HIDDEN\" NAME=\"ENTRYLINK\" VALUE=\"$link\">\n");
print ("<INPUT TYPE=\"SUBMIT\" NAME=\"REMOVE\" VALUE=\"REMOVE\">\n");
print ("</b></font></td></tr></FORM><p>\n");
}
}
close (BOARD);
}

print ("</font></TD></TR></TABLE><p><hr width=90%>\n");
print ("<font face=\"verdana\" color=\"\#000080\"size=1><b><center>\n");
print ("TEKBOARD.CGI 1999<br><a href=\"$home\">© Metertek Perl Scripts</a></font></center>\n");
print ("</BODY>\n");
print ("</HTML>\n");

exit;

}