#!e:/perl/bin/perl.exe
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser); 
require 'cgi-lib.pl';
require 'func.pl';


my ($siteurl,$rooturl,$menufile)=&get_vars;

our %in;
my $linkfile='links.txt';
my @categ=("Downloads","HTML/CGI/PERL","Java","Linux","Networking","OS","Programming","Products","Information","Personal","Other");

print "content-type:text/html\n\n";

if($ENV{'QUERY_STRING'} eq "")
{
	$in{'category'}=$categ[0];
}

&ReadParse(*in);

print <<EOF1;

<html>

<head>
<title>Links</title>
<base href=$siteurl>

<script language=javascript1.2>

function showFilled(Value) {
  return (Value > 9) ? "" + Value : "0" + Value;
}
function StartClock24() {
  TheTime = new Date;
  document.clock.showTime.value = showFilled(TheTime.getHours()) + ":" + showFilled(TheTime.getMinutes()) + ":" + showFilled(TheTime.getSeconds());
  setTimeout("StartClock24()",1000)
}
</script>

<script language="JavaScript">
<!--
function MM_jumpMenu(targ,selObj,restore){
  eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
  if (restore) selObj.selectedIndex=0;
}
//-->
</script>



<link rel="stylesheet" type="text/css" href="programming.css" />

EOF1
;

open(MYFILE1,"$rooturl/$menufile") || &error("\n$rooturl/$menufile Cannot open file1","fatal");
while(<MYFILE1>)
{
	print $_;
}

close MYFILE1;

if($in{'category'} =~/^[A-Za-z ]+/ and $in{'url'} eq "")
{

	print <<EOF1;
	
	<h1 align=center>Links</h1>
	
	<table width="98%" border="0" cellspacing="0" align="center">
  <tr  > 
    <td height="60"> 
      <div align=left><a href="/cgi-bin/links.cgi?action=add"><font face="Verdana, Arial, Helvetica, sans-serif" size="2"><img src="post.gif" width="32" height="20" align="top" border="0"><font color="#006699">Submit a URL</font></font></a> </div>
    </td>
  </tr>
  <tr  > 
    <td height="50"><font face="Verdana, Arial, Helvetica, sans-serif" size="2">Feel free 
      to add your site here! <br>
      Remember to<b> Reload</b> your browser, if your URL doesn't appear.</font></td>
    <td height="50" align="right"> 
      <form name="form">
        <select name="category" onChange="MM_jumpMenu('self',this,0)">
          <option selected>Categories</option>
EOF1
;
	  foreach my $temp(@categ)
	  {        
          	print "<option value=\"/cgi-bin/links.cgi?category=$temp\">$temp</option>";
          }


print <<EOF1

        </select>
      </form>
    </td>
  </tr>
  <tr  > 
    <td colspan="2" height="500" valign="top">
EOF1
;
   
     foreach my $temp(@categ)
     {        
          	print "<a href='/cgi-bin/links.cgi?category=$temp'><font size=1 face='Arial, Helvetica, sans-serif'>$temp</font></a> |";
     }
     
print <<EOF1

      <hr size="1">
      <img src="line.gif" width="525" height="1"> 
      <table width="100%" border="0">
        <tr> 
          <td width="100%"> 
            <div align="left"><b><font face="Verdana, Arial, Helvetica, sans-serif" size="2">$in{'category'}</font></b> 
              <hr size="1">
            </div>
          </td>
        </tr>
        <tr> 
          <td width="100%"> 
            <ul>
EOF1
;
	open MYFILE,"$rooturl/$linkfile" or &error("cannot open file");
	while(<MYFILE>)
	{
		
		my @fields=split(/\|/,$_);
		if($fields[0] eq $in{'category'})
		{
			
			print <<EOF1
			<img src="arrow.gif"><a href=$fields[1] target="_blank"><font size="2">$fields[3]</font></a><br>
			<font size="2">$fields[2]</font><br>
			<font size="1">$fields[1] added on: $fields[4]</font><br><br>
			
EOF1
;
		}	
	}
	close MYFILE;

print <<EOF1
            </ul>
          </td>
        </tr>
      </table>
      <br>
    </td>
  </tr>
  <tr  > 
    <td colspan="3">&nbsp; </td>
  </tr>
  <tr  > 
    <td colspan="4" height="24">&nbsp;</td>
  </tr>
</table>
<div align="center"> <br>


	
EOF1
;
	
	
}
else
{
	if($in{'action'} eq "add")
	{

	
		print <<EOF1
		<head>
			<script language=javascript1.2>
		
			function showFilled(Value) {
			  return (Value > 9) ? "" + Value : "0" + Value;
			}
			function StartClock24() {
			  TheTime = new Date;
			  document.clock.showTime.value = showFilled(TheTime.getHours()) + ":" + showFilled(TheTime.getMinutes()) + ":" + showFilled(TheTime.getSeconds());
			  setTimeout("StartClock24()",1000)
			}
			
			function checkForm() {  
			 var found = 0;
			 document.message.url.value=trim(document.message.url.value);
			 document.message.title.value=trim(document.message.title.value);
			 document.message.descript.value=trim(document.message.descript.value);
			 if(document.message.url.value.indexOf("http://")==-1 || document.message.url.value.indexOf(".")==-1) {
			   alert("Please enter a valid url!");
			   document.message.url.focus();
			   return false;
			 }
			 if(document.message.title.value == "") {
			   alert("Please enter a title!");
			   document.message.title.focus();
			   return false;
			 }    
			 if(document.message.descript.value == "") {
			   alert("Please enter a short description!");
			   document.message.descript.focus();
			   return false;
			 }
			 for (i=0; i<document.message.category.length; i++) {
			   if (document.message.category[i].checked == true) {
			     found = 1;
			     break;
			   }
			 }
			 if (found == 1) {
			   return true;
			 } else {
			   alert("Please choose a category!");
			   return false;
			 }
			}
			function trim(value) {
			 startpos=0;
			 while((value.charAt(startpos)==" ")&&(startpos<value.length)) {
			   startpos++;
			 }
			 if(startpos==value.length) {
			   value="";
			 }
			 else {
			   value=value.substring(startpos,value.length);
			   endpos=(value.length)-1;
			   while(value.charAt(endpos)==" ") {
			     endpos--;
			   }
			   value=value.substring(0,endpos+1);
			 }
			 return(value);
			}
			
			</script>
	
		</head>
		
		
	<table width="600" border="0" cellspacing="0" align="center">
	  <tr bgcolor> 
	    <td rowspan="6" width="12">&nbsp;</td>
	    <td colspan="5" height="24">&nbsp;</td>
	  </tr>
	  <tr bgcolor> 
	    <td rowspan="4" width="32">&nbsp;</td>
	    <td rowspan="3" width="12"> 
	      <p>&nbsp;</p>
	    </td>
	    <td height="50"><b><font size="4" face="Verdana, Arial, Helvetica, sans-serif">Submit 
	      Link Page Form</font></b></td>
	    <td height="50"> 
	      <div align="right"><a href="/cgi-bin/links.cgi?category=$categ[0]"> <font face="Verdana, Arial, Helvetica, sans-serif" size="2">Back 
	        to Link Page</font></a></div>
	    </td>
	    <td rowspan="3" width="18">&nbsp;</td>
	  </tr>
	  <tr  > 
	    <td height="50" colspan="2"><font face="Verdana, Arial, Helvetica, sans-serif" size="2">Add 
	      your site here! <br>
	      Remember to<b> Reload</b> your browser, if your URL doesn't appear.</font></td>
	  </tr>
	  <tr  > 
	    <td colspan="2"> 
	      <form method="get" action="http://localhost/cgi-bin/links.cgi" name="message">
	        <table width="100%" border="0" align="center"   height="429" cellspacing="0">
	          <tr> 
	            <td> 
	              <table width="100%" border="0">
	                <tr> 
	                  <td colspan="2"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">URL:</font> 
	                    <br>
	                    <input type="text" name="url" value="http://" size="45" maxlength="90">
	                  </td>
	                </tr>
	                <tr> 
	                  <td colspan="2"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Title:</font> 
	                    <br>
	                    <input type="text" name="title" size="45" maxlength="90">
	                  </td>
	                </tr>
	                <tr> 
	                  <td colspan="2"><font size="2" face="Verdana, Arial, Helvetica, sans-serif">Short 
	                    Description:</font><br>
	                    <textarea name="descript" rows="5" cols="55"></textarea>
	                    <input type="hidden" name="add" value="new">
	                  </td>
	                </tr>
	                <tr> 
	                  <td colspan="2" height="190"> 
	                    <p> <font face="Verdana, Arial, Helvetica, sans-serif" size="2"> 
	                      Page Category:</font></p>
	                    <table width="90%" border="0" cellspacing="0" cellpadding="1" align="left">
EOF1
;
			for(my $j=0;$j<$#categ;$j=$j+2)
			{	                  
	                  	print <<EOF1
	                  	
	                      <tr> 
	                        <td width="51%"> <font face="Verdana, Arial, Helvetica, sans-serif"> 
	                          <input type="radio" name="category" value="$categ[$j]">
	                          <font size="2">$categ[$j]</font></font></td>
	                        <td width="49%"> <font face="Verdana, Arial, Helvetica, sans-serif"> 
	                          <input type="radio" name="category" value="$categ[$j+1]">
	                          <font size="2">$categ[$j+1]</font></font></td>
	                      </tr>
EOF1
;
			}
			
			print <<EOF1

	                    </table>
	                  </td>
	                </tr>
	              </table>
	              <input type="submit" value="Submit Url" onClick="return checkForm()">
	              <input type="reset" value="Reset">
	              <br>
	              <br>
	              <a href="/cgi-bin/links.cgi?category=$categ[0]"><font face="Verdana, Arial, Helvetica, sans-serif" size="2">Back 
	              to Link Page</font></a></td>
	          </tr>
	        </table>
	      </form>
	    </td>
	  </tr>
	  <tr  > 
	    <td colspan="4">&nbsp;</td>
	  </tr>
	  <tr  > 
	    <td colspan="5">&nbsp;</td>
	  </tr>
	</table>
	  <br>

EOF1
;
	}	
	else
	{
		my $time=&get_time;
		
		if(-e "$rooturl/$linkfile")
		{
			
			open MYFILE,">>$rooturl/$linkfile" or &error("\nCannot open file");
		}
		else
		{
			open MYFILE,">$rooturl/$linkfile" or &error("\nCannot open file");
			
		}
		
		print MYFILE "$in{'category'}|$in{'url'}|$in{'descript'}|$in{'title'}|$time|$ENV{'REMOTE_ADDR'}\n";
		
		close MYFILE;
		
		print <<EOF6
		
		<head>
		<title>Success</title>
		<meta http-equiv="pragma" content="no-cache">
		<meta http-equiv="refresh" content="3;URL=/cgi-bin/links.cgi?category=$categ[0]">
		<style type="text/css">
		<!--
		td {  font-family: Verdana, Arial, Helvetica, sans-serif; }
		-->
		</style>
		</head>
		
		<table width="640" border="0" cellspacing="0" align="center" height="260">
		  <tr> 
		    <td rowspan="6"   width="16">&nbsp;</td>
		    <td colspan="4" height="12"  >&nbsp;</td>
		    <td rowspan="6"   width="29">&nbsp;</td>
		  </tr>
		  <tr> 
		    <td rowspan="4" bgcolor="#E6E6FF" width="34">&nbsp;</td>
		    <td rowspan="4" height="154"   width="10">&nbsp;</td>
		    <td></td>
		    <td width="171"  ><a href="/cgi-bin/links.cgi?category=$categ[0]"><font size="2">return to links Page</font></a></td>
		  </tr>
		  <tr> 
		    <td colspan="2"   height="15">&nbsp;</td>
		  </tr>
		  <tr> 
		    <td colspan="2"   height="100" valign="top"> <u><font size="2">Thanks 
		      for adding a link.</font></u><font size="2"><br>
		      <br>
		      Your URL <font color=yellow>http://madhur.netfirms.com</font> was added successfully!<br>
		      You should be transfered back to the Link Page in 3 seconds.</font> </td>
		  </tr>
		  <tr> 
		    <td colspan="2"  >&nbsp;</td>
		  </tr>
		  <tr> 
		    <td colspan="4"   height="12">&nbsp;</td>
		  </tr>
		</table>
EOF6
;
		
	}


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
	