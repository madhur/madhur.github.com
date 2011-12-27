#!e:/perl/bin/perl.exe
########################################################################
# Graphical Message Board
# Version 4.0
# Copyright 1998 Techno Trade Online Solutions http://www.technotrade.com
# Written By : Sammy Afifi   sammy@technotrade.com
# Date Last Modified : Sep 1, 1998
########################################################################

  ###  These Variables hold the location of the .gif images, default is the same directory
  ###  as the cgi script. Change these values if your cgi-bin will not accept .gif's 
  ###  example : $post1 = "http://www.myserver.com/images/post1.gif"
  ###
  my ($siteurl,$rooturl,$menufile)=&get_vars;
  $post1  = "post1.gif";
  $post2  = "post2.gif";
  $post3  = "post3.gif";
  $post4  = "post4.gif";
  $exit   = "exit.gif";
  $left1  = "left1.gif";
  $left2  = "left2.gif";
  $right1 = "right1.gif";
  $right2 = "right2.gif";
  $admin  = "admin.gif";
  $key    = "key.gif";

  ##### You need to change the following 2 variables #####
  $formaction = "$siteurl/cgi-bin/board4.cgi";  # Where the CGI script is
  $basedir = $rooturl;  # base directory where data files go (/usr/www/joe/data/)


  $editorpassword = "gold";   # your password for deleting

  $badwords = "shit|prick|fuck|bitch|cunt|suck|tits";  
  #### Did your mother teach you to say that ?

  &parse_form;

  ############################################################
  #
  #  ***  do not change these variables  ***
  #
  $numdatafields = 6;
  $messagenumber = $input{'messagenumber'}; # which message number to start at
  $direction     = $input{'direction'};          # which way to go (right, left or list)
  $boardname     = $input{'boardname'};          #  text file for the messages
  # get rid of dangerous characters
  $boardname =~ s/\>//g;
  $boardname =~ s/\<//g;
  $boardname =~ s/\+//g;
  $boardname =~ s/\|//g;
  $boardname =~ s/\\//g;
  $boardname =~ s/\///g;

  $gobackurl     = $input{'gobackurl'};  # this is the URL where the user will go to when they click on EXIT
  $boardtitle    = $input{'boardtitle'}; # this stores the title of your message board


  $direction = "list" if (($formaction ne "") && ($direction eq ""));

  ### these are used internally by the script
  $messagetitle  = $input{'messagetitle'};
  $messagesource = $input{'messagesource'};
  $messagebody   = $input{'messagebody'};
  $msgname       = $input{'msgname'};
  $msgemail      = $input{'msgemail'};
  $msgurl        = $input{'msgurl'};
  $msgdate       = $input{'msgdate'};
  $gotomessage   = $input{'gotomessage'};
  $viewtype      = $input{'viewtype'};

  
  &readfile; # Read the Message Board Data File 

  if ($direction eq "right") {
         $gotorecord = $messagenumber;
         &fetchmessage;
   }
  if ($direction eq "left") {
         $gotorecord = $messagenumber;
         &fetchmessage;
   }
  if ($direction eq "post") {
         &postmessage;
   }
  if ($direction eq "postdata") {
         &postmessagetofile;
         &readfile;
         &displaysubjects;
   }
  if ($direction eq "list") {
         &displaysubjects;
   }
  if ($direction eq "goto") {
         $gotorecord = $messagenumber;
         &getrecordnum;
         if($viewtype eq "Delete") {
            if ($editorpassword eq $input{'delpass'}) {
              &delete_messages;
              &readfile;
            }
            &displaysubjects;
         }
         &fetchmessage if ($numselected == 1);
         &displayselected;
   }

    &print_content;
    &print_header;
    print "<CENTER><H2>Missing Parameters</H2></CENTER><BR>\n";
    print "If you're reading this, then you didn't call the script properly, you need to pass some variables such as boardname, direction, formaction etc. Please refer to the instructions at the <A HREF=\"http://www.technotrade.com\">CGI Archive</A> on how to call this script.\n";
    for ($x = 0; $x <= $numselected; $x++) {
      print "$sortedposts[$x] <BR>\n";
    }
    &print_footer;
    exit;



###############################
sub hidden_fields {
  
  print "<INPUT type=hidden  name=\"boardname\" value=\"" . $boardname . "\">\n";
  print "<INPUT type=hidden name=\"formaction\" value=\"" . $formaction . "\" >\n";
  print "<INPUT type=hidden  name=\"boardtitle\" value=\"" . $boardtitle . "\">\n";
  print "<INPUT type=hidden name=\"gobackurl\" value=\"" . $gobackurl . "\" >\n";

}

###############################
#
#
#
###############################
sub fetchmessage {
    &print_content;
    &print_header;
    &readmessage;
    print "<CENTER>\n";
    print "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 width=500>\n";
    print "<TR><TD>\n";
    print "  <TABLE width=\"100%\" border=0 cellpadding=0>\n";
    print "  <TR><TD bgcolor=\"#00007f\" height=20>\n";
    print "   <FONT size=1 color=#ffffff face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>$boardtitle</B>\n";
    print "   </FONT>\n";
    print "  </TD>\n";
    print "</TR>\n";
    print "  <TR><TD bgcolor=\"#ffffff\" height=20>\n";
    print "   <FONT size=1 color=#000000 face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>$msgtitles[$gotorecord]</B></FONT></TD></TR></TABLE>\n";
    print "</TD></TR><TR><TD>\n";
    print "<FORM>\n";
    print "<TEXTAREA NAME=\"messagebody\" COLS=\"62\" ROWS=\"7\" WRAP=PHYSICAL>\n";
    print "Posted by: " . $msgnames[$gotorecord] . " (" . $msgemails[$gotorecord] . ")  " . $msgdates[$gotorecord] . "\n";
    print "$msgbodys[$gotorecord]";    
    
    print "</TEXTAREA><BR>\n";
    print "<FONT SIZE=2 COLOR=400040><B>&nbsp;&nbsp;" . $msgdates[$gotorecord] . "</B></FONT>\n";
    print "<FONT SIZE=3 COLOR=400040>\n";
    print "\&nbsp; \&nbsp; \&nbsp; \&nbsp; \&nbsp; \n";
    print "By : " . $msgnames[$gotorecord] . "\n";
    print "\&nbsp;\&nbsp;\&nbsp;\&nbsp;\&nbsp;\n";
    if ($msgemails[$gotorecord] ne "") {
       print "<A HREF=\"mailto:" . $msgemails[$gotorecord] . "\">E-Mail</A>\n";
      }
    if ($msgurls[$gotorecord] ne "") {
        print "\&nbsp;\&nbsp;\&nbsp;\&nbsp;\&nbsp;\n";
        print "<A HREF=\"" . $msgurls[$gotorecord] . "\">Homepage</A>\n";
     }
    print "</FONT>\n";
    print "</FORM>\n";
    print "</TD></TR>\n";
    print "<TR><TD bgcolor=\"#c0c0c0\">\n";
    print "<TABLE>\n";
    print "<TR>\n";
    print "<TD Width=71>\n";
    if ($gotorecord == 1) {
       print "<!IMG SRC=\"$left2\" align=center>\n";
     }
    else {
      print "<form action=\"" . $formaction . "\" method=\"post\">\n";
      print "<input type=image align=center name=\"send\" border=0 SRC=\"$left1\">\n";
      print "<input type=hidden name=\"direction\" value=\"left\">\n";
      print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $prevposting ."\">\n";
      &hidden_fields;
      print "</form>\n";
    }
    print "</TD>\n";


    # post new
    print "<TD Width=71>\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post1\">\n";
    print "<input type=hidden name=\"direction\" value=\"post\">\n";
    print "<INPUT type=hidden  name=\"messagetitle\" value=\"\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord ."\">\n";
#    $msgsource = $rpostedbyname . " (" . $rpostedbyemail . ")  " . $rmessagedate;
#    $msgsource =~ s/\"/\'/g;  # replace double quotes with single quotes
#    print "<INPUT type=hidden  name=\"messagesource\" value = \"" . $msgsource . "\">\n";
    print "</form>\n";
    print "</TD>\n";


    #post a reply to
    print "<TD Width=71>\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post2\">\n";
    print "<input type=hidden name=\"direction\" value=\"post\">\n";
    print "<INPUT type=hidden  name=\"messagetitle\" value=\"" . $msgtitles[$gotorecord] . "\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord ."\">\n";
 #   $msgsource = $rpostedbyname . " (" . $rpostedbyemail . ")  " . $rmessagedate;
 #   $msgsource =~ s/\"/\'/g;  # replace double quotes with single quotes
 #   print "<INPUT type=hidden  name=\"messagesource\" value = \"" . $msgsource . "\">\n";
    print "</form>\n";
    print "</TD>\n";




    # list postings
    print "<TD Width=71>\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post3\">\n";
    print "<input type=hidden name=\"direction\" value=\"list\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord . "\">\n";
#    print "<INPUT type=hidden  name=\"messagetitle\" value=\"" . $rmessagetitle . "\">\n";
    print "</form>\n";
    print "</TD>\n";

    print "<TD Width=20></TD><TD Width=71>\n";

    if ($gotorecord == $numpostings) {
      print "<!IMG SRC=\"$right2\" align=center >\n";
     }
    else {
      print "<form action=\"" . $formaction . "\" method=\"post\">\n";
      print "<input type=image  align=center name=\"send\" border=0 SRC=\"$right1\">\n";
      print "<input type=hidden name=\"direction\" value=\"right\">\n";
      print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $nextposting . "\">\n";
    &hidden_fields;
 #     print "<INPUT type=hidden  name=\"messagetitle\" value=\"" . $rmessagetitle . "\">\n";
      print "</form>\n";
    }
    print "</TD>\n";

    print "<TD Width=71>\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<A HREF=\"$gobackurl\"><IMG SRC=\"$exit\" align=right border=0></A>\n";
    print "</TD>\n";


    print "</TR>\n";
    print "</TABLE>\n";
    print "</TD></TR>\n";
    print "</TABLE>\n";
    print "<FONT SIZE=3 COLOR=000080>Message Board By <A HREF=\"http://www.technotrade.com\">Techno Trade Online Solutions</A></FONT>\n";
    print "</CENTER>\n";
    &print_footer;
    exit;
}

######################################
#
#
#
######################################
sub postmessage {
    &print_content;
    &print_header;
    print "<CENTER>\n";
    print "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 width=500 bgcolor=\"#c0c0c0\">\n";
    print "<TR><TD>\n";
    print "<TR><TD>\n";
    print "  <TABLE width=\"100%\" border=0 cellpadding=0>\n";
    print "  <TR><TD bgcolor=\"#00007f\" height=20>\n";
    print "   <FONT size=1 color=#ffffff face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>$boardtitle</B>\n";
    print "   </FONT>\n";
    print "  </TD>\n";
    print "</TR>\n";
    print "  <TR><TD bgcolor=\"#ffffff\" height=20>\n";
    print "   <FONT size=1 color=#000000 face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>Post a Message</B></FONT></TD></TR></TABLE>\n";
    print "</TD></TR><TR><TD>\n";
    print "<FORM METHOD=POST ACTION=\"" . $formaction . "\">\n";
    $messagetitle =~ s/\"/\'/g;

    if ($messagetitle ne "") {
      $firstthree = substr($messagetitle,0,3); # get the first three chars to see if it = RE:
      if ($firstthree ne "RE:") 
       {
         $messagetitle = "RE: " . $messagetitle;
       }
    }
    print  "&nbsp;&nbsp;Title: <INPUT NAME=\"messagetitle\" SIZE=\"35\" MAXLENGTH=\"35\" Value=\"" . $messagetitle . "\">";
    &hidden_fields;

    print "<TEXTAREA NAME=\"messagebody\" COLS=\"62\" ROWS=\"7\" WRAP=PHYSICAL>\n";
    print "</TEXTAREA><BR>\n";
    print  "<PRE>  Name   : <INPUT NAME=\"msgname\" SIZE=\"35\" MAXLENGTH=\"25\">\n";
    print  "  E-Mail : <INPUT NAME=\"msgemail\" SIZE=\"35\" MAXLENGTH=\"50\"><BR>";
#    print  "&nbsp;&nbsp;URL  : <INPUT NAME=\"msgurl\" SIZE=\"40\" MAXLENGTH=\"60\" value=\"http://\">";
    print "</PRE>\n";
    print "<TABLE Width=100% cellpadding=0 cellspacing=0>";
    print "<TR><TD Width=40%></TD><TD width=30% Align=right>";
    print "<input type=hidden name=\"direction\" value=\"postdata\">\n";
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $messagenumber . "\">\n";
    print "</FONT>\n";

    print "<input type=image align=left name=\"send\" border=0 SRC=\"$post4\">\n";
    print "</FORM>\n";


    # list postings
    print "</TD><TD Width=30% align=right>";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=right name=\"send\" border=0 SRC=\"$post3\">\n";
    print "<input type=hidden name=\"direction\" value=\"list\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord . "\">\n";
#    print "<INPUT type=hidden  name=\"messagetitle\" value=\"" . $rmessagetitle . "\">\n";
    print "</form>\n";
    print "</TD></TR></TABLE>";

    print "</TD></TR>\n";
    print "</TABLE>\n";
    print "</CENTER>\n";
    &print_footer;
    exit;
}

##################################
#
#
#
##################################
sub postmessagetofile {

   $ct = time;
   $timedifference = 10800;
   local($sec,$min,$hour,$mday,$mon,$yday,$wday,$isdst) = localtime($ct - $timedifference);
   $min = "0" . $min if ($min < 10);
   $hour = "0" . $hour if ($hour < 10);
   $mon++;
   $sec = "0" . $sec if ($sec < 10);
   $mon = "0" . $mon if ($mon < 10);
   $mday = "0" . $mday if ($mday < 10);
   $yday = "0" . $yday if ($yday < 10);
   
   $yday = 1900 + $yday;


    $msgdate = "$mon/$mday/$yday $hour:$min";

    open(FILE1,">>$basedir$boardname");
    $messagebody =~ s/\cM//g;
    $messagebody =~ s/\n/\<\*R\*\>/g;
    $messagebody = &clean_string($messagebody);
    $msgname = &clean_string($msgname);
    $msgtitle = &clean_string($msgtitle);
    $msgemail = &clean_string($msgemail);

    print FILE1 "$messagetitle|$msgdate|$msgname|$msgemail|$msgurl|$messagebody\n";
    close(FILE1);
}
##################################
#
# deletes badwords from a string
#
sub clean_string {
   local($st) = @_;

   $st =~ s/\b$badwords\b//gi;
   return($st);
}

#####################################
#
#
#
#####################################
sub readmessage {
    $gotorecord = 0 if ($gotorecord < 1);

    $prevposting = $gotorecord - 1;
    $nextposting = $gotorecord + 1;
    $nextposting = $numpostings if ($nextposting > $numpostings);
    return(1);
}

#####################################################
# display a drop down window of all the Subjects of all postings
#####################################################
sub displaysubjects {

    $position = 0;
    &print_content;
    &print_header;

    print "<CENTER>\n";
    print "<TABLE BORDER=1 CELLPADDING=0 CELLSPACING=0 width=500>\n";
    print "<TR><TD>\n";
    print "  <TABLE width=\"100%\" border=0 cellpadding=0>\n";
    print "  <TR><TD bgcolor=\"#00007f\" height=20>\n";
    print "   <FONT size=1 color=#ffffff face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>$boardtitle</B>\n";
    print "   </FONT>\n";
    print "  </TD>\n";
    print "</TR>\n";
    print "  <TR><TD bgcolor=\"#ffffff\" height=20 align=center>\n";
    print "   <FONT size=1 color=#000000 face=\"MS Sans Serif\">\n";
    print "    <B>Subject Listing</B></FONT></TD></TR></TABLE>\n";

    print "</TD></TR>\n";
    print "<TR><TD align=center>\n";

    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<SELECT name=\"gotomessage\" SIZE=10 MULTIPLE>\n";
    print "<OPTION VALUE=0>...Date...... Time ......................................... Subject - Author..................................\n";
    
    for ($x=$numpostings; $x >= 1;$x--) {
        print "<OPTION VALUE=\"$x\">$msgdates[$x] .. $msgtitles[$x] - $msgnames[$x] \n";
     }

    print "</SELECT>\n";
    &hidden_fields;
    print "<input type=hidden name=\"direction\" value=\"goto\">\n";
    print "<TABLE width=100% cellpadding=2 cellspacing=0 border=0>";
    print "<TR><TD Align=center valign=top>";
    print "<INPUT TYPE=submit VALUE=\" Click Here To View Selected Message(s) \" NAME=\"viewtype\"><BR>";
    print "<FONT SIZE=-1>Click and drag with your mouse to select multiple messages</FONT>";
    print "</TD><TD align=center valign=top>\n";
    print "<INPUT NAME=\"delpass\" SIZE=4 TYPE=\"password\"><IMG SRC=\"$key\"><BR>";
    print "<INPUT TYPE=\"SUBMIT\" NAME=\"viewtype\" VALUE=\"Delete\"><BR>";
    #print "<FONT SIZE=-1>Administrator-only</FONT>\n";
    print "</TD></TR></TABLE>";
    print "</FORM>\n";
    print "</TD></TR>\n";
    print "<TR><TD  bgcolor=\"#c0c0c0\">\n";
    print "<TABLE bgcolor=\"#c0c0c0\">\n";
    print "<TR>\n";
    print "<TD Width=200></TD>\n";

    # post new
    print "<TD Width=100  bgcolor=\"#c0c0c0\">\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post1\">\n";
    print "<input type=hidden name=\"direction\" value=\"post\">\n";
    print "<INPUT type=hidden  name=\"messagetitle\" value=\"\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord ."\">\n";
 #   print "<INPUT type=hidden  name=\"messagesource\" value = \"" . $msgsource . "\">\n";
    print "</form>\n";
    print "</TD>\n";

    print "<TD Width=100 align=right bgcolor=\"#c0c0c0\">\&nbsp;</TD>\n";
    print "<TD Width=75 bgcolor=\"#c0c0c0\">\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<A HREF=\"$gobackurl\"><IMG SRC=\"$exit\" border=0></A>\n";
    print "</TD>\n";
    print "</TR>\n";
    print "</TABLE>\n";
    print "</TD></TR>\n";
    print "</TABLE>\n";
    print "<FONT SIZE=3 COLOR=000080>Message Board By <A HREF=\"http://www.technotrade.com\">Techno Trade Online Solutions</A></FONT>\n";
    print "</CENTER>\n";
    &print_footer;
    exit;
}


#####################################################
#
#####################################################
sub displayselected {
    &print_content;
    &print_header;

    print "<CENTER>\n";
    print "<TABLE BORDER=1 CELLPADDING=1 CELLSPACING=0 width=500>\n";
    print "<TR><TD>\n";
    print "  <TABLE width=\"100%\" border=0 cellpadding=0>\n";
    print "  <TR><TD bgcolor=\"#00007f\" height=20>\n";
    print "   <FONT size=1 color=#ffffff face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>$boardtitle</B>\n";
    print "   </FONT>\n";
    print "  </TD>\n";
    print "</TR>\n";
    print "  <TR><TD bgcolor=\"#ffffff\" height=20 align=center>\n";
    print "   <FONT size=1 color=#000000 face=\"MS Sans Serif\">\n";
    print "    &nbsp;<B>Group Listing</B></FONT></TD></TR></TABLE>\n";
    print "</TD></TR><TR><TD>\n";

    $position = 1;
    $sp = 0;
     for ($gc = 1; $gc <= $numpostings; $gc++) {

         if ($gc == $sortedposts[$sp]) {
            print "<TR><TD>\n";

            print "<form action=\"" . $formaction . "\" method=\"post\">\n";
            print "<input type=image align=right name=\"send\" border=0 SRC=\"$post2\">\n";
            print "<input type=hidden name=\"direction\" value=\"post\">\n";
            print "<INPUT type=hidden  name=\"messagetitle\" value=\"" . $msgtitles[$gc] . "\">\n";
            &hidden_fields;
            print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $position ."\">\n";
            $msgsource = $msgnames[$gc] . " (" . $msgemails[$gc] . ")  " . $msgdates[$gc];
            $msgsource =~ s/\"/\'/g;  # replace double quotes with single quotes
           # print "<INPUT type=hidden  name=\"messagesource\" value = \"" . $msgsource . "\">\n";
            print "</form>\n";

            print "<FONT SIZE=3 COLOR=004080><B>Subject</B></FONT> : $msgtitles[$gc]<BR>\n";
            print "<FONT SIZE=3 COLOR=004080><B>Date</B></FONT> &nbsp;&nbsp;&nbsp;&nbsp;: $msgdates[$gc]<BR>\n";
            print "<FONT SIZE=3 COLOR=004080><B>By</B></FONT> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: $msgnames[$gc] \n";
            print "&nbsp;&nbsp;&nbsp;<A HREF=\"mailto:$msgemails[$gc]\">E-mail</A> &nbsp;&nbsp;&nbsp;\n" if ($msgemails[$gc] ne "");
            print "<A HREF=\"$msgurls[$gc]\">URL</A>\n" if ($msgurls[$gc] ne "");
            print "<BR><BR>\n";
            $msgbodys[$gc] =~ s/\n/\<BR\>/g;
            print "$msgbodys[$gc]";
            print "</TD></TR>\n";
            $sp++;
          }
     }

    print "</TD></TR>\n";
    print "<TR><TD bgcolor=\"#c0c0c0\">\n";
    print "<TABLE>\n";
    print "<TR>\n";
    print "<TD Width=150></TD>\n";

    # post new
    print "<TD Width=100>\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post1\">\n";
    print "<input type=hidden name=\"direction\" value=\"post\">\n";
    print "<INPUT type=hidden  name=\"messagetitle\" value=\"\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord ."\">\n";
 #   print "<INPUT type=hidden  name=\"messagesource\" value = \"" . $msgsource . "\">\n";
    print "</form>\n";
    print "</TD>\n";

    print "<TD>\n";
    print "<form action=\"" . $formaction . "\" method=\"post\">\n";
    print "<input type=image align=center name=\"send\" border=0 SRC=\"$post3\">\n";
    print "<input type=hidden name=\"direction\" value=\"list\">\n";
    &hidden_fields;
    print "<INPUT type=hidden  name=\"messagenumber\" value=\"" . $gotorecord . "\">\n";
    print "</form>\n";
    print "</TD>\n";
    
    print "<TD Width=50></TD>\n";
    print "<TD Width=75>\n";
    print "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
    print "<A HREF=\"$gobackurl\"><IMG SRC=\"$exit\" border=0></A>\n";
    print "</TD>\n";
    print "</TR>\n";
    print "</TABLE>\n";
    print "</TD></TR>\n";
    print "</TABLE>\n";
    print "</CENTER>\n";
    &print_footer;
    exit;
}

#####################################################
#
#####################################################
sub delete_messages {

    open(BF,">$basedir$boardname");
    flock(BF,2);
    for ($gc = 1; $gc <= $numpostings; $gc++) {
       if (&inselected($gc) == 0) {
        print BF "$boardlines[$gc-1]\n";
      }
     }
    close(BF);
}

#################################
# returns true or false if a given number exists in the selected array (sortedposts)
sub inselected {
  local($check) = @_;
  
  foreach $sel (@sortedposts) {
    return(1) if ($sel == $check);
  }
  return(0);  
}

#####################
#
#####################
sub readfile {

    open(FILE1,"$basedir$boardname"); 
    @boardlines = <FILE1>;
    close(FILE1);

    # number of lines in the file
    $numpostings = @boardlines;

    # get rid of new line chars and control Z's
    # and count how many Postings there are
    for($xc = 1; $xc <= $numpostings;$xc++) {
       $boardlines[$xc - 1]  =~ s/\cM//g;
       $boardlines[$xc - 1]  =~ s/\n//g;
       ($msgtitles[$xc],$msgdates[$xc],$msgnames[$xc],$msgemails[$xc],$msgurls[$xc],$msgbodys[$xc]) = split(/\s*\|\s*/,$boardlines[$xc - 1],$numdatafields);
       $msgbodys[$xc] =~ s/<\*R\*\>/\n/g;
    }
}


# This subroutine is called when the user has selected a message to goto from the drop down menu
# it returns the message number which is located in the first part of the string (before the period)
sub getrecordnum {
   $gotorecord = $gotomessage;
   @selectedposts = split(/\s*\ \s*/,$gotomessage);
   $numselected = @selectedposts;
   $gotorecord = 1 if ( ($numselected == 1) && ($gotorecord eq "") );
   @sortedposts = sort {$a <=> $b} @selectedposts;
   shift(@sortedposts) if ($sortedposts[0] == 0);
   $numsortedposts = @sortedposts;
}


#########################################################
sub parse_form {

   read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
   if (length($buffer) < 5) {
         $buffer = $ENV{QUERY_STRING};
    }
   @pairs = split(/&/, $buffer);
   foreach $pair (@pairs) {
      ($name, $value) = split(/=/, $pair);

      $value =~ tr/+/ /;
      $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

      if ($input{$name} eq "") {
         $input{$name} = $value;
      } else {
         $input{$name} = $input{$name} . " " . $value;
      }
   }

}

#########################################################
sub print_content {

    # Check to see if we're running on one of those cough cough NT machines
    print "HTTP/1.0 200 OK\r\n" if $ENV{PERLXS} eq "PerlIS";
    print "Content-type: text/html\n\n";

}

sub print_header {
print<<HEAD;

<HTML>
<HEAD><TITLE>$boardtitle</Title></HEAD>
<BODY BGCOLOR=#ffffff TEXT=#000000 LINK=#0000FF VLINK=#800040 ALINK=#800040>

HEAD
}

sub print_footer {
print<<FOOT;

</BODY>
</HTML>

FOOT
}



