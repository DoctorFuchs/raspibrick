// Ultrasonic1.java

import ch.aplu.raspi.*;

public class Ultrasonic1
{
  public Ultrasonic1()
  {
    Robot robot = new Robot();
    UltrasonicSensor us = new UltrasonicSensor();
    while (!robot.isEscapeHit())
    {
      double v = us.getValue();
      System.out.println("v = " + v);
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Ultrasonic1();
  }
}
