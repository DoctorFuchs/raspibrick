// Display1.java

import ch.aplu.raspi.*;

public class Display4
{
  public Display4()
  {
    Robot robot = new Robot();
    Display display = new Display();
 //   display.ticker("1234567890");
 //   display.ticker("1234567890", 2);
    display.ticker("1234567890", 2, 8);
    int count = 0;
    while (display.isTickerAlive())
    {
      System.out.println("alive at " + count);
      count +=1;
      Tools.delay(500);
    }
      
    //display.ticker("1234567890", 2, 8)
    System.out.println("All done");
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Display4();
  }
}
