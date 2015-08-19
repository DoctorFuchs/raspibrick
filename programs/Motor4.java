// Motor4.java

import ch.aplu.raspi.*;

public class Motor4
{
  public Motor4()
  {
    Robot robot = new Robot("192.168.0.2", false);
    robot.connect(false);
    Motor mot = new Motor(Motor.LEFT);
    mot.forward();
    Tools.delay(3000);
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Motor4();
  }
}
