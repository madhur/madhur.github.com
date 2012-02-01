function openwin(mystr,height,width)
{
height=height+20;
width=width+20;
newwindow=window.open(mystr ,'TheNewpop','toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=0,resizable=0,height='+height+' width='+width);
newwindow.focus();

}