import java.applet.*;
import java.awt.*;
import java.io.*;
import java.net.URL;
/*
<applet code=myip.class width=200 height=200> </applet>
*/


public class myip  extends Applet
{
	String ip;
	public void init()
	{
		URL base=getCodeBase();
		String codebase=base.toString();
		System.out.println(codebase);
		
		try
		{
			BufferedReader br=new BufferedReader(new FileReader(codebase+"temp.txt"));	
			ip=br.readLine();
			br.close();
			
			
		}
		catch(IOException e)
		{}
		
	}
	public void paint(Graphics g)
	{
		g.drawString(ip,20,20);
	}
}