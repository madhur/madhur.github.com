#!e:/perl/bin/perl.exe

######################################################################
#  BEFORE TRYING TO EDIT THIS SCRIPT, READ THE README FILE
###################################################################### 
#
#     The Dream Catcher's Web Free CGI Scripts 
#     Message Board
#     Created by Seth Leonard
#
#     http://dreamcatchersweb.com/scripts/
#
#     (c)2000 Seth Leonard
#     All Rights Reserved
#
######################################################################
my ($siteurl,$rooturl,$menufile)=&get_vars;

$userdir = "users";
$datafile = "data.txt";
$messagedir = "messages";
$responsedir = "responses";
$archivedir = "archives";
$dateprogram = "date";

$bgcolor = "FFFFFF";
$textcolor = "000000";
$linkcolor = "0000FF";
$boardname = "Message Board";
$loginpage = "$siteurl/board/login.html";
$script = "$siteurl/cgi-bin/board.cgi";

############################################################################

&getdate;

if ($ENV{'QUERY_STRING'}) {
	$namevalues = $ENV{'QUERY_STRING'};
} else {
	read(STDIN, $namevalues, $ENV{'CONTENT_LENGTH'});
}

@pairs = split(/&/, $namevalues);
	foreach $pair (@pairs) {
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$value =~ s/<!--(.|\n)*-->//g;
	$value =~ s/<([^>]|\n)*>//g;
	$INPUT{$name} = $value;
}

$action = $INPUT{'action'};

if ($action eq 'login') {
	&login;
}
if ($action eq 'main') {
	&main;
}
if ($action eq 'view') {
	&view;
}
if ($action eq 'post') {
	&post;
}
if ($action eq 'userarchive') {
	&userarchive;
}
if ($action eq 'viewarchive') {
	&viewarchive;
}
if ($action eq 'editarchive') {
	&editarchive;
}
if ($action eq 'deletearchive') {
	&deletearchive;
}
if ($action eq 'archivemessage') {
	&archivemessage;
}
if ($action eq 'register') {
	&register;
}

############################################################################
# REGISTER
############################################################################

sub register {

unless ($INPUT{'user'}) {
	&requireuser;
}

&user;

$filetoexist = "$userdir/$user.user";

@atribs = stat("$filetoexist");

if ($atribs[7] > 0 || $INPUT{'user'} eq 'guest') {

	&usernametaken;
}

$INPUT{'password'} =~ tr/ /-/;

$cryptpassword = crypt($INPUT{'password'}, sb);

open (NEWUSER, ">$userdir/$user.user");

print NEWUSER ("$cryptpassword\n");
if ($INPUT{'alias1'}) {
	print NEWUSER ("$INPUT{'alias1'}");
}
if ($INPUT{'alias2'}) {
	print NEWUSER ("\t");
	print NEWUSER ("$INPUT{'alias2'}");
}
if ($INPUT{'alias3'}) {
	print NEWUSER ("\t");
	print NEWUSER ("$INPUT{'alias3'}");
}
if ($INPUT{'alias4'}) {
	print NEWUSER ("\t");
	print NEWUSER ("$INPUT{'alias4'}");
}
if ($INPUT{'alias5'}) {
	print NEWUSER ("\t");
	print NEWUSER ("$INPUT{'alias5'}");
}
print NEWUSER ("\n");


if ($INPUT{'email'} && $INPUT{'email'} =~ /(.*)@(.*)/) {
	print NEWUSER ("$INPUT{'email'}\n");
} else {
	print NEWUSER ("none\n");
}

print NEWUSER ("$INPUT{'archive'}\n");

close (NEWUSER);

if ($INPUT{'archive'} eq 'yes') {

	open (NEWARCHIVE, ">$archivedir/$user.archive");
	close (NEWARCHIVE);

}

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>Thank You For Registering</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>Thank you for Registering</font></center><hr>
<b>Welcome to $boardname $userview,</b><br><br>
Please go to the <a href=$loginpage>login page</a> and login using the username '<i>$userview</i>' and the password '<i>$INPUT{'password'}</i>'.<br><br>
Thank you!

<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

exit;

}

############################################################################
# MAIN MENU
############################################################################

sub login {

&user;

&checkpassword;

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>Welcome To $boardname</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>Welcome to $boardname</font></center><hr>
<center><b>You have the following options:</b><br><br>

<table border=0>
<tr><td>
<form method=get action=$script>
<input type=hidden name=action value=main>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="View the Board">
</form>
</td><td>
<form method=get action=$script>
<input type=hidden name=action value=viewarchive>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="View an Archive">
</form></td>
html

unless ($user eq 'guest') {

print <<"html";
<td>
<form method=get action=$script>
<input type=hidden name=action value=editarchive>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="Edit your Archive">
</form>
</td>
html
}

print <<"html";
</tr></table>
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

exit;

}

############################################################################
# VIEW BOARD
############################################################################

sub main {

&user;

&checkpassword;
&getuserinfo;

opendir (MESSAGES, "$messagedir");
@files = readdir(MESSAGES);
close (MESSAGES);

$numberoffiles = @files;
$numberoffiles -= 1;

@rmessages = @files[2..$numberoffiles];

foreach $message (@rmessages) {
        $x = 1;
        while ($x < @rmessages) {
                if ($rmessages[$x - 1] > $rmessages[$x]) {
                        @rmessages[$x - 1, $x] = @rmessages[$x, $x - 1];
                }
                $x++;
        }
}

@messages = reverse(@rmessages);

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>$boardname</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><b><font size=6>$boardname</font></b></center>
<hr>
<ul>

html

foreach $message (@messages) {
	
	chop ($message);
	chop ($message);
	chop ($message);
	chop ($message);
	open (MESSAGE, "$messagedir/$message.txt");
	($subject, $name, $postunder, $responses, $date, $puser, $post) = <MESSAGE>;
	close (MESSAGE);

	chop ($subject) if ($subject =~ /\n$/);
	chop ($name) if ($name =~ /\n$/);
	chop ($postunder) if ($postunder =~ /\n$/);
	chop ($responses) if ($responses =~ /\n$/);
	chop ($date) if ($date =~ /\n$/);
	chop ($puser) if ($puser =~ /\n$/);
	chop ($post) if ($post =~ /\n$/);

	@responses = split(/\t/, $responses);
	$responses = @responses;

	print ("<li><a href=\"$script?action=view&message=$message&location=messages&user=$user&password=$INPUT{'password'}\">$subject</a> - <b>$name</b> <i>$date</i></li>\n");

}

if ($user eq 'guest') {

print <<"html";

</ul>
<hr>
<center>
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

} else {

print <<"html";

</ul>
<hr>
<form method=post action=$script>
<input type=hidden name=action value=post>
<input type=hidden name=postunder value=main>
<input type=hidden name=status value=original>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<table cellpadding=0 cellspacing=0 width=100%>
<tr><td width=15%><b>Name:</b></td><td>
<SELECT NAME="name">
<OPTION SELECTED="selected" VALUE="$userview">$userview</OPTION>

html

unless ($aliases == 0) {
	foreach $alias (@aliases) {
		print ("<OPTION VALUE=\"$alias\">$alias</OPTION>\n");
	}
}

print <<"html";

</SELECT>
</td></tr>
<tr><td width=15%><b>Subject:</b></td><td><input type=text name=subject size=40 maxlength=75</td></tr>
html

if ($userarchive eq 'available') {
	print ("<tr><td width=15%><b>Archive:</b></td><td>\n");
	print ("<INPUT TYPE=radio NAME=archive VALUE=yes> Yes\n");
	print ("<INPUT TYPE=radio NAME=archive VALUE=no CHECKED=checked> No\n");
	print ("</td></tr>\n");
}

print <<"html";
</table>
<b>Post:</b><br>
<TEXTAREA NAME="message" ROWS="10" COLS="75"></TEXTAREA><br><br>
<input type=submit value=Post> <input type=reset>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

}

exit;

}

############################################################################
# VIEW A MESSAGE
############################################################################

sub view {

&user;

&checkpassword;

if ($INPUT{'location'} eq 'messages') {
	$dir = $messagedir;
} else {
	$dir = $responsedir;
}

open (MESSAGE, "$dir/$INPUT{'message'}.txt");
($subject, $name, $postunder, $responses, $date, $puser, $post) = <MESSAGE>;
close (MESSAGE);

chop ($subject) if ($subject =~ /\n$/);
chop ($name) if ($name =~ /\n$/);
chop ($postunder) if ($postunder =~ /\n$/);
chop ($responses) if ($responses =~ /\n$/);
chop ($date) if ($date =~ /\n$/);
chop ($puser) if ($puser =~ /\n$/);
chop ($post) if ($post =~ /\n$/);

&getpostunderinfo;
&getpostuserinfo;

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>$subject</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>$subject</font></center><hr>
<table cellpadding=0 cellspacing=0 width=100%>
<tr><td width=15%><b>Posted By:</b></td><td>$name</td></tr>
html

if ($INPUT{'location'} eq 'messages') {
	$no = "yes";
} else {
	print ("<tr><td width=15%><b>Response to:</b></td><td><a href=\"$script?action=view&message=$postunder&location=messages&user=$user&password=$INPUT{'password'}\">$osubject</a> posted by $oname</td></tr>\n");
}

print <<"html";
<tr><td width=15%><b>Email:</b></td><td>$pemail</td></tr>
<tr><td width=15%><b>Date:</b></td><td>$date</td></tr>
html

if ($puserarchive eq 'available') {
	print ("<tr><td width=15%><b>Archive:</b></td><td><a href=\"$script?action=userarchive&archive=$puser&user=$user&password=$INPUT{'password'}\">Available</a></td></tr>\n");
} else {
	print ("<tr><td width=15%><b>Archive:</b></td><td>Not Available</td></tr>\n");
}

print <<"html";
</table>
<hr>
$post
<hr>
<b>Responses:</b>
<ul>
html

unless ($responses eq "") {

	@responses = split(/x/, $responses);

	foreach $response (@responses) {

		&getresponseinfo;
		print ("<li><a href=\"$script?action=view&message=$response&location=responses&user=$user&password=$INPUT{'password'}\">$rsubject</a> -- $rname<br></li>\n");
	}
}

print <<"html";
</ul>
<hr>
html

if ($user eq 'guest') {

print <<"html";

<center>
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

} else {

&getuserinfo;

print <<"html";
<font size=4><b>Post Response:</font></b><br><br>
<form method=post action=$script>
<input type=hidden name=action value=post>
<input type=hidden name=postunder value=$INPUT{'message'}>
html

if ($INPUT{'location'} eq 'messages') {
	$status = "original";
} else {
	$status = "response";
}

print <<"html";
<input type=hidden name=status value=$status>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<table cellpadding=0 cellspacing=0 width=100%>
<tr><td width=15%><b>Name:</b></td><td>
<SELECT NAME="name">
<OPTION SELECTED="selected" VALUE="$userview">$userview</OPTION>

html

unless ($aliases == 0) {
	foreach $alias (@aliases) {
		print ("<OPTION VALUE=\"$alias\">$alias</OPTION>\n");
	}
}

chop ($subject) if ($subject =~ /\n$/);

if ($subject =~ /Re:/) {
	$newsubject = $subject;
} else {
	$newsubject = "Re: $subject";
}

print <<"html";

</SELECT>
</td></tr>
<tr><td width=15%><b>Subject:</b></td><td><input type=text name=subject size=40 maxlength=75 value="$newsubject"></td></tr>
html

if ($userarchive eq 'available') {
	print ("<tr><td width=15%><b>Archive:</b></td><td>\n");
	print ("<INPUT TYPE=radio NAME=archive VALUE=yes> Yes\n");
	print ("<INPUT TYPE=radio NAME=archive VALUE=no CHECKED=checked> No\n");
	print ("</td></tr>\n");
}

print <<"html";
</table>
<b>Post:</b><br>
<TEXTAREA NAME="message" ROWS="10" COLS="75"></TEXTAREA><br><br>
<input type=submit value=Post> <input type=reset>
<hr>
<center>
[ <a href=\"$script?action=main&user=$user&password=$INPUT{'password'}\">$boardname</a> ]
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

}

exit;

}

############################################################################
# POST A MESSAGE
############################################################################

sub post {

$INPUT{'message'} =~ s/\cM\n/<br>/g;
$post = $INPUT{'message'};

&user;

&checkpassword;

open (DATA, "$datafile");
$count = <DATA>;
close (DATA);

chop ($count) if ($count =~ /\n$/);

$count += 1;

open (DATA, ">$datafile");
print DATA ("$count");
close (DATA);

if ($INPUT{'postunder'} eq 'main') {

	open (NEWFILE, ">$messagedir/$count.txt");
	print NEWFILE ("$INPUT{'subject'}\n");
	print NEWFILE ("$INPUT{'name'}\n");
	print NEWFILE ("$INPUT{'postunder'}\n");
	print NEWFILE ("\n");
	print NEWFILE ("$date\n");
	print NEWFILE ("$user\n");
	print NEWFILE ("$post\n");
	close (NEWFILE);

} else {

	open (NEWFILE, ">$responsedir/$count.txt");
	print NEWFILE ("$INPUT{'subject'}\n");
	print NEWFILE ("$INPUT{'name'}\n");
	print NEWFILE ("$INPUT{'postunder'}\n");
	print NEWFILE ("\n");
	print NEWFILE ("$date\n");
	print NEWFILE ("$user\n");
	print NEWFILE ("$post\n");
	close (NEWFILE);

	if ($INPUT{'status'} eq 'original') {
		$dir = $messagedir;
	} else {
		$dir = $responsedir;
	}

	open (UNDER, "$dir/$INPUT{'postunder'}.txt");
	@lines = <UNDER>;
	close (UNDER);

	chop ($lines[3]) if ($lines[3] =~ /\n$/);
	if ($lines[3] eq "") {
		$responses = $count;
	} else {
		$responses = $count . 'x' . $lines[3];
	}
	open (UNDER, ">$dir/$INPUT{'postunder'}.txt");
	print UNDER ("$lines[0]");
	print UNDER ("$lines[1]");
	print UNDER ("$lines[2]");
	print UNDER ("$responses\n");
	print UNDER ("$lines[4]");
	print UNDER ("$lines[5]");
	print UNDER ("$lines[6]");
	close (UNDER);

}

if ($INPUT{'archive'} eq 'yes') {

	open (ARCHIVE, ">>$archivedir/$user.archive");
	print ARCHIVE ("$INPUT{'subject'}\t");
	print ARCHIVE ("$date\t");
	print ARCHIVE ("$post\n");
	close (ARCHIVE);

	open (ARCHIVE, "$archivedir/$user.archive");
	@lines = <ARCHIVE>;
	close (ARCHIVE);

	$lines = @lines;

	if ($lines > 10) {

		open (ARCHIVE, ">$archivedir/$user.archive");
		print ARCHIVE ("$lines[$lines - 10]");
		print ARCHIVE ("$lines[$lines - 9]");
		print ARCHIVE ("$lines[$lines - 8]");
		print ARCHIVE ("$lines[$lines - 7]");
		print ARCHIVE ("$lines[$lines - 6]");
		print ARCHIVE ("$lines[$lines - 5]");
		print ARCHIVE ("$lines[$lines - 4]");
		print ARCHIVE ("$lines[$lines - 3]");
		print ARCHIVE ("$lines[$lines - 2]");
		print ARCHIVE ("$lines[$lines - 1]");
	}
}

&getuserinfo;

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>$INPUT{'subject'}</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>$INPUT{'subject'}</font></center><hr>
<table cellpadding=0 cellspacing=0 width=100%>
<tr><td width=15%><b>Posted By:</b></td><td>$INPUT{'name'}</td></tr>
<tr><td width=15%><b>Email:</b></td><td>$email</td></tr>
<tr><td width=15%><b>Date:</b></td><td>$date</td></tr>

html

if ($userarchive eq 'available') {

	print ("<tr><td width=15%><b>Archive:</b></td><td><a href=\"$script?action=userarchive&archive=$INPUT{'user'}&user=$user&password=$INPUT{'password'}\">Available</a></td></tr>\n");

} else {

	print ("<tr><td width=15%><b>Archive:</b></td><td>Not Available</td></tr>\n");
}

print <<"html";

</table>
<hr>
$post
<hr>
<center>
<table border=0>
<tr><td>
<form method=get action=$script>
<input type=hidden name=action value=login>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="Main Menu">
</form>
</td><td>
<form method=get action=$script>
<input type=hidden name=action value=main>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="$boardname">
</form>
</td></tr></table></center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

exit;

}

############################################################################
# VIEW A USER'S ARCHIVE
############################################################################

sub userarchive {

&user;

$archive = $INPUT{'archive'};
$archive =~ tr/ /_/;
$archiveview = $INPUT{'archive'};
$archiveview =~ tr/_/ /;

open (ARCHIVE, "$archivedir/$archive.archive");
@lines = <ARCHIVE>;
close (ARCHIVE);

print ("Content-type: text/html\n\n");

print <<"html";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<TITLE>$archiveview Archive</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<font size=5>$archiveview Archive</font><hr>
<ul>
html

$archivenum = 0;
foreach $line (@lines) {
	($subject, $date, $post) = split(/\t/, $line);
	print ("<li><a href=\"$script?action=archivemessage&archivenumber=$archivenum&archive=$archive&user=$user&password=$INPUT{'password'}\">$subject</a> posted on $date</li>\n");
	$archivenum += 1;
}

print <<"html";
</ul>
<hr>
<center>
[ <a href=\"$script?action=main&user=$user&password=$INPUT{'password'}\">$boardname</a> ]
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</BODY>
</HTML>
html

exit;

}

############################################################################
# PAGE TO INPUT USER FOR ARCHIVE
############################################################################

sub viewarchive {

&user;

&checkpassword;

print ("Content-type: text/html\n\n");

print <<"html";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<TITLE>View an Archive</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>View an Archive</font></center><hr>
<form method=get action=$script>
<b>Please type the name of the user who's archive you would like to view:</b><br><br>
<input type=text name=archive size=12>
<input type=hidden name=action value=userarchive>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
<input type=submit value="View Archive">
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</body>
</html>

html

exit;

}

############################################################################
# EDIT ARCHIVE
############################################################################

sub editarchive {

&user;

&checkpassword;

open (ARCHIVE, "$archivedir/$user.archive");
@lines = <ARCHIVE>;
close (ARCHIVE);

print ("Content-type: text/html\n\n");

print <<"html";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<TITLE>Edit Your Archive</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<font size=5>Edit Your Archive</font><hr>
<b>Select which archive message you would like to delete:</b><br><br>
<form method=get action=$script>
<input type=hidden name=action value=deletearchive>
<input type=hidden name=user value="$user">
<input type=hidden name=password value="$INPUT{'password'}">
html

$archivenum = 0;
foreach $line (@lines) {
	($subject, $date, $post) = split(/\t/, $line);
	print ("<input type=radio name=delete value=$archivenum> <b>$subject</b> posted on $date<br>\n");
	$archivenum += 1;
}

print <<"html";
<hr>
<input type=submit value="Delete Archive Message">
<hr>
<center>
[ <a href=\"$script?action=main&user=$user&password=$INPUT{'password'}\">$boardname</a> ]
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
<hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</BODY>
</HTML>
html

exit;

}

############################################################################
# DELETE ARCHIVE MESSAGES
############################################################################

sub deletearchive {

&user;

&checkpassword;

open (ARCHIVE, "$archivedir/$user.archive");
@lines = <ARCHIVE>;
close (ARCHIVE);

$thecount = 0;

open (ARCHIVE, ">$archivedir/$user.archive");

foreach $line (@lines) {

	if ($thecount == $INPUT{'delete'}) {
		$thecount += 1;
	} else {
		print ARCHIVE ("$line");
		$thecount += 1;
	}
}

print ("Location: $script?action=userarchive&archive=$user&user=$user&password=$INPUT{'password'}\n\n");

exit;

}

############################################################################
# VIEW AN ARCHIVE MESSAGE
############################################################################

sub archivemessage {

&user;

$archive = $INPUT{'archive'};
$archive =~ tr/ /_/;
$archiveview = $INPUT{'archive'};
$archiveview =~ tr/_/ /;

$archivenumber = $INPUT{'archivenumber'};

open (ARCHIVE, "$archivedir/$archive.archive");
@lines = <ARCHIVE>;
close (ARCHIVE);

($subject, $date, $post) = split(/\t/, $lines[$archivenumber]);

$puser = $archive;

&getpostuserinfo;

print ("Content-type: text/html\n\n");

print <<"html";

<HTML>
<HEAD>
<TITLE>$subject</TITLE>
</HEAD>
<BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>
<center><font size=6>$subject</font></center><hr>
<table cellpadding=0 cellspacing=0 width=100%>
<tr><td width=15%><b>Posted By:</b></td><td>$archiveview</td></tr>
<tr><td width=15%><b>Email:</b></td><td>$pemail</td></tr>
<tr><td width=15%><b>Date:</b></td><td>$date</td></tr>
</table>
<hr>
$post
<hr>
<center>
[ <a href=\"$script?action=userarchive&archive=$archive&user=$user&password=$INPUT{'password'}\">$archiveview Archive</a> ]
[ <a href=\"$script?action=main&user=$user&password=$INPUT{'password'}\">$boardname</a> ]
[ <a href=\"$script?action=login&user=$user&password=$INPUT{'password'}\">Main Menu</a> ]
</center>
</BODY>
</HTML>
html

exit;

}

############################################################################
# SUB ROUTINES
############################################################################

sub getuserinfo {

	open (USER, "$userdir/$user.user");
	@userinfo = <USER>;
	close (USER);

	foreach $line (@userinfo) {
		chop ($line) if ($line =~ /\n$/);
	}

	if ($userinfo[1] eq "") {
		$aliases = 0;
	} else {
		@aliases = split(/\t/, $userinfo[1]);
		$aliases = @aliases;
	}

	if ($userinfo[2] eq 'none') {
		$email = "Not Given";
	} else {
		$email = "<a href=mailto:$userinfo[2]>$userinfo[2]</a>";
	}

	if ($userinfo[3] eq 'yes') {
		$userarchive = "available";
	} else {
		$userarchive = "not available";
	}

}


sub checkpassword {

	unless ($user eq 'guest') {

		unless (-e "$userdir/$user.user") {
			&userdoesntexist;
		}

		$userpassword = crypt($INPUT{'password'}, sb);

		open (USER, "$userdir/$user.user");
		$password = <USER>;
		close (USER);

		chop ($password) if ($password =~ /\n$/);

		unless ($password eq $userpassword) {
			print ("Content-type: text/html\n\n");
			print ("<html><BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>\n");
			print ("<font size=5>You Entered an Illegal Password</font>\n");
			print ("</body></html>\n");
			exit;
		}
	}

}

sub getdate {

	$day = `$dateprogram +"%d"`;
	chop ($day) if ($day =~ /\n$/);

	unless ($day == 10 || $day == 20 || $day == 30) {
		$day =~ tr/0/ /;
	}

	$date = `$dateprogram +"%B $day, %Y"`;
	chop ($date) if ($date =~ /\n$/);

}

sub usernametaken {

	print ("Content-type: text/html\n\n");
	print ("<html><BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>\n");
	print ("<font size=5>The User Name you selected is already in use, please choose another</font>\n");
	print ("</body></html>\n");
	exit;

}

sub userdoesntexist {

	print ("Content-type: text/html\n\n");
	print ("<html><BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>\n");
	print ("<font size=5>You Entered an Illegal User Name</font>\n");
	print ("</body></html>\n");
	exit;
}

sub requireuser {

	print ("Content-type: text/html\n\n");
	print ("<html><BODY BGCOLOR=$bgcolor TEXT=$textcolor LINK=$linkcolor>\n");
	print ("<font size=5>You Did Not Enter a User Name, Please Do So</font>\n");
	print ("</body></html>\n");
	exit;
}

sub getpostuserinfo {

	open (USER, "$userdir/$puser.user");
	@puserinfo = <USER>;
	close (USER);

	foreach $line (@puserinfo) {
		chop ($line) if ($line =~ /\n$/);
	}

	if ($puserinfo[1] eq "") {
		$paliases = 0;
	} else {
		@paliases = split(/\t/, $puserinfo[1]);
		$paliases = @paliases;
	}

	if ($puserinfo[2] eq 'none') {
		$pemail = "Not Given";
	} else {
		$pemail = "<a href=mailto:$puserinfo[2]>$puserinfo[2]</a>";
	}

	if ($puserinfo[3] eq 'yes') {
		$puserarchive = "available";
	} else {
		$puserarchive = "not available";
	}

}

sub getpostunderinfo {

	$filetoexist = "$messagedir/$postunder.txt";

	@atribs = stat("$filetoexist");

	if ($atribs[7] > 0) {

		open (OVER, "$filetoexist");
		($osubject, $oname, $opostunder, $oresponses, $odate, $opuser, $opost) = <OVER>;
		close (OVER);

	} else {

		open (OVER, "$responsedir/$postunder.txt");
		($osubject, $oname, $opostunder, $oresponses, $odate, $opuser, $opost) = <OVER>;
		close (OVER);

	}

	chop ($osubject) if ($osubject =~ /\n$/);
	chop ($oname) if ($oname =~ /\n$/);
	chop ($opostunder) if ($opostunder =~ /\n$/);
	chop ($oresponses) if ($oresponses =~ /\n$/);
	chop ($odate) if ($odate =~ /\n$/);
	chop ($opuser) if ($opuser =~ /\n$/);
	chop ($opost) if ($opost =~ /\n$/);
}

sub getresponseinfo {

	open (OVER, "$responsedir/$response.txt");
	($rsubject, $rname, $rpostunder, $rresponses, $rdate, $rpuser, $rpost) = <OVER>;
	close (OVER);

	chop ($rsubject) if ($rsubject =~ /\n$/);
	chop ($rname) if ($rname =~ /\n$/);
	chop ($rpostunder) if ($rpostunder =~ /\n$/);
	chop ($rresponses) if ($rresponses =~ /\n$/);
	chop ($rdate) if ($rdate =~ /\n$/);
	chop ($rpuser) if ($rpuser =~ /\n$/);
	chop ($rpost) if ($rpost =~ /\n$/);

}

sub user {

	$user = $INPUT{'user'};
	$userview = $INPUT{'user'};
	$userview =~ tr/_/ /;
	$user =~ tr/ /_/;

}
