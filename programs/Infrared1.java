// Infrared1.java

import ch.aplu.raspi.*;

public class Infrared1
{
  public Infrared1()
  {
    Robot robot = new Robot();
    InfraredSensor[] sensors = new InfraredSensor[5];
    for (int id = 0; id < 5; id++)
      sensors[id] = new InfraredSensor(id);
    while (!robot.isEscapeHit())
    {
      for (int id = 0; id < 5; id++)
        System.out.println(id + ": " + sensors[id].getValue());
      System.out.println();
      Tools.delay(1000);
    }
    robot.exit();
  }

  public static void main(String[] args)
  {
    new Infrared1();
  }
}
