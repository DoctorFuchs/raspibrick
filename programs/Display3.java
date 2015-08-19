// Display1.java

import ch.aplu.raspi.*;

public class Display3
{
  public Display3()
  {
    Robot robot = new Robot();
    Display display = new Display();
    display.setScrollableText("123-456-789-AbC");
    while (!robot.isEscapeHit())
    {
      Tools.delay(700);
      int rc = display.scrollToLeft();
      System.out.println("rc: " + rc);
      if (rc == 4)
      {
        Tools.delay(1500);
        display.setText("");
        Tools.delay(1500);
        display.setToStart();
      }
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Display3();
  }
}
