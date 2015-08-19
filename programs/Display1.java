// Display1.java

import ch.aplu.raspi.*;

public class Display1
{
  public Display1()
  {
    Robot robot = new Robot();
    Display display = new Display();
    for (int digit = 0; digit < 4; digit++)
    {
      display.setDigit('A', digit);
      Tools.delay(1000);
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Display1();
  }
}
