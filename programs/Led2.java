// Led1.java

import ch.aplu.raspi.*;
import java.awt.Color;

public class Led2
{
  public Led2()
  {
    Robot robot = new Robot();
    Led [] leds = {new Led(0), new Led(1), new Led(2), new Led(3)};
    for (Led led : leds)
    {
       led.setColor(Color.green);
       Tools.delay(2000);
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Led2();
  }
}
