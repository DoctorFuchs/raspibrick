// Motor1.java

import ch.aplu.raspi.*;

public class Motor1
{
  public Motor1()
  {
    Robot robot = new Robot();
    Motor mot = new Motor(Motor.LEFT);
    mot.forward();
    Tools.delay(3000);
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Motor1();
  }
}
