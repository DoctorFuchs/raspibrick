// RaspiClientConsole.java

import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import ch.aplu.util.*;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.Charset;

public class RaspiClientConsole
{
  class StreamReader extends Thread
  {
    private InputStream is;

    public StreamReader(InputStream is)
    {
      this.is = is;
    }

    public void run()
    {
      while (true)
      {
        String response = "";
        try
        {  
          response = readResponse(is);
        }
        catch (Exception ex)
        {
          System.out.println("Exception in readResponse: " + ex.getMessage());
//          System.exit(1);
          break;
        }  
        int rc = 0;
        try
        {
          rc = Integer.parseInt(response);
        }
        catch (NumberFormatException ex)
        {
        }
        if (rc >= 0)
        {
          System.out.print("Response: " + response);
          System.out.println(" in " + timer.getTime() / 1000 + " ms");
        }
        else
          System.out.println("Response (error): " + responseMsg[-rc]);
      }
    }

    private String readResponse(InputStream is) throws IOException
    {
      if (is == null)
        return "";
      byte[] buf = new byte[4096];
      ByteArrayOutputStream baos = new ByteArrayOutputStream();
      boolean done = false;
      while (!done)
      {
        int len = is.read(buf);
        if (len == -1)
          throw new IOException("Stream closed");
        baos.write(buf, 0, len);
        if (buf[len - 1] == 10)  // \n
          done = true;
      }
      String s = baos.toString("UTF-8");
      return s.substring(0, s.length() - 1);  // Remove \n
    }

  }

  String[] responseMsg =
  {
    "OK", "SEND_FAILED", "ILLEGAL_METHOD",
    "ILLEGAL_INSTANCE", "CMD_ERROR", "ILLEGAL_PORT", "CREATION_FAILED"
  };

  private String ipAddress = "apluraspi";
  private int port = 1299;
  private OutputStream os = null;
  private InputStream is = null;    
  private HiResTimer timer = new HiResTimer();

  public RaspiClientConsole()
  {
    ch.aplu.util.Console c = new ch.aplu.util.Console();
    try
    {
      System.out.println("Trying to connect to " + ipAddress);
      Socket s = new Socket(ipAddress, port);
      System.out.println("Connection established.");
      System.out.println("Enter command<cr>");
      os = s.getOutputStream();
      is = s.getInputStream();
      StreamReader sr = new StreamReader(is);
      sr.start();
      String command = "";
      while (true)
      {
        command = c.readLine();
        if (command.length() == 0)
        {
          System.out.println("Illegal command");
          continue;
        }
        timer.start();
        sendCommand(command);
      }
    }
    catch (Exception ex)
    {
      ex.printStackTrace();
    }
  }

  private void sendCommand(String cmd) throws IOException
  {
    if (cmd == null || cmd.length() == 0 || os == null)
      throw new IOException("sendCommand failed.");
    cmd += "\n";  // Append \n
    byte[] ary = cmd.getBytes(Charset.forName("UTF-8"));
    os.write(ary);
    os.flush();
  }

  public static void main(String[] args)
  {
    new RaspiClientConsole();
  }
}
