// Led1.java

import ch.aplu.raspi.*;
import java.awt.Color;

public class Led1
{
  public Led1()
  {
    Robot robot = new Robot();
    Led.setColorAll(100, 0, 0);
    Tools.delay(2000);
    Led.setColorAll(Color.blue);
    Tools.delay(2000);
    Led.setColorAll(new Color(100, 100, 0));
    Tools.delay(2000);
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Led1();
  }
}
