// Motor2.java

import ch.aplu.raspi.*;

public class Motor3
{
  public Motor3()
  {
    Robot robot = new Robot();
    Motor mot = new Motor(Motor.LEFT);
    mot.forward();
    Tools.delay(3000);
    mot.backward();
    Tools.delay(3000);
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Motor3();
  }
}
