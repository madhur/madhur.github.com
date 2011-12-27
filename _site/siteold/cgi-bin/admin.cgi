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

$passwordfile = "password.txt";

$messagedir = "messages";
$responsedir = "responses";

$adminscript = "http://$ENV{SERVER_NAME}/cgi-bin/admin.cgi";

############################################################################

read(STDIN, $namevalues, $ENV{'CONTENT_LENGTH'});

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

if ($action eq 'delete') {
	&delete;
}

if ($action eq 'change') {
	&change;
}

############################################################################
# HTML PAGE TO DELETE ENTRIES
############################################################################

opendir (MESSAGES, "$messagedir");
@files = readdir(MESSAGES);
close (MESSAGES);

$numberoffiles = @files;
$numberoffiles -= 1;

@rmessages = @files[2..$numberoffiles];
@messages = reverse(@rmessages);

$messagenumber = @messages;

print ("Content-type: text/html\n\n");

print <<"html";

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2//EN">
<HTML>
<HEAD>
<TITLE>Delete Entries</TITLE>
</HEAD>
<BODY bgcolor=ffffff>
<form method=post action=$adminscript>
<input type=hidden name=action value=delete>
<b>Password:</b> <input type=text name=password size=12>
<hr>
<b>You currently have $messagenumber messages posted</b>.<br><br><i>Please enter the number of messages you would like to remain on the board.  For example, if you enter '100', your board will only show 100 messages. The oldest messages will be deleted.  

All messages deleted will also have their responses deleted. The number that you will cut to is only shown on the main board, so you could cut it to 100 messages, but still have 300 responses to those 100 messages.</i>
<hr>
<b>Cut Board Messages to : <input type=text name=number size=5></b> <input type=submit value="Delete"></form>
<hr>
<form method=post action=$adminscript>
<input type=hidden name=action value=change>
<b>Change Administration Password</b><br><br>
Old Password: <input type=text name=password size=12> New Password: <input type=text name=newpassword size=12> <input type=submit value="Change Password"></form><hr>
<a href=http://dreamcatchersweb.com/scripts/>&copy;1997 Dream Catchers Technologies, Inc.</a>
</BODY>
</HTML>

html

exit;


############################################################################
# CHANGE PASSWORD
############################################################################

sub change {

$userpassword = crypt($INPUT{'password'}, sb);

open (USER, "$passwordfile");
$password = <USER>;
close (USER);

chop ($password) if ($password =~ /\n$/);

unless ($password eq $userpassword) {
	print ("Content-type: text/html\n\n");
	print ("<html><BODY BGCOLOR=ffffff>\n");
	print ("<font size=5>You Entered an Illegal Password</font>\n");
	print ("</body></html>\n");
	exit;
}

$newpassword = crypt($INPUT{'newpassword'}, sb);

open (USER, ">$passwordfile");
print USER ("$newpassword");
close (USER);

print ("Content-type: text/html\n\n");
print ("<html><BODY BGCOLOR=ffffff>\n");
print ("<font size=5>Your New Password is $INPUT{'newpassword'}</font>\n");
print ("</body></html>\n");

exit;

}

############################################################################
# DELETE MESSAGES
############################################################################

sub delete {

$userpassword = crypt($INPUT{'password'}, sb);

open (USER, "$passwordfile");
$password = <USER>;
close (USER);

chop ($password) if ($password =~ /\n$/);

unless ($password eq $userpassword) {
	print ("Content-type: text/html\n\n");
	print ("<html><BODY BGCOLOR=ffffff>\n");
	print ("<font size=5>You Entered an Illegal Password</font>\n");
	print ("</body></html>\n");
	exit;
}

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

$messagenumber = @messages;

$deletepast = $INPUT{'number'};
$messagenumber -= 1;

@deletemessages = @messages[$deletepast..$messagenumber];

$deletenumber = 0;

foreach $deletemessage (@deletemessages) {

	unlink ("$messagedir/$deletemessage");

	chop ($deletemessage);
	chop ($deletemessage);
	chop ($deletemessage);
	chop ($deletemessage);

	$deleted[$deletenumber] = $deletemessage;
	$deletenumber += 1;

}

opendir (MESSAGES, "$responsedir");
@files = readdir(MESSAGES);
close (MESSAGES);

$numberoffiles = @files;
$numberoffiles -= 1;

@responses = @files[2..$numberoffiles];

foreach $response (@responses) {

	open (RESPONSE, "$responsedir/$response");
	($subject, $name, $postunder, $responses, $date, $puser, $post) = <RESPONSE>;
	close (RESPONSE);

	chop ($postunder) if ($postunder =~ /\n$/);

	chop ($response);
	chop ($response);
	chop ($response);
	chop ($response);

	foreach $deleted (@deleted) {
		if ($postunder eq $deleted) {
			$deleted[$deletenumber] = $response;
			$deletenumber += 1;
			unlink ("$responsedir/$response.txt");
		}
	}
}

print ("Location: $adminscript\n\n");

exit;

}
