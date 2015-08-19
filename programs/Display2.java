// Display1.java

import ch.aplu.raspi.*;

public class Display2
{
  public Display2()
  {
    Robot robot = new Robot();
    Display display = new Display();
    display.setText("1234");
    Tools.delay(4000);
    display.setText("1133", new int[] {0, 1, 1});
    Tools.delay(3000);
    display.setText(2244, new int[] {0, 1, 1});
    Tools.delay(3000);
    display.setText("0123456", new int[] {0, 1, 1});
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Display2();
  }
}
