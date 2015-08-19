// Motor2.java

import ch.aplu.raspi.*;

public class Motor2
{
  public Motor2()
  {
    Robot robot = new Robot();
    Motor motA = new Motor(Motor.LEFT);
    Motor motB = new Motor(Motor.RIGHT);
    motA.forward();
    motB.forward();
    int n = 0;
    System.out.println("\nPress Escape to stop");
    while (!robot.isEscapeHit())
    {
      Tools.delay(200);
      System.out.println("n = " + n);
      n++;
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Motor2();
  }
}
