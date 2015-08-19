// LightSensor1.java

import ch.aplu.raspi.*;

public class LightSensor1
{
  public LightSensor1()
  {
    Robot robot = new Robot();
    LightSensor[] sensors = new LightSensor[4];
    for (int id = 0; id < 4; id++)
      sensors[id] = new LightSensor(id);
    while (!robot.isEscapeHit())
    {
      for (int id = 0; id < 4; id++)
        System.out.println(id + ": " + sensors[id].getValue());
      System.out.println();
      Tools.delay(1000);
    } 
    robot.exit();
  }

  public static void main(String[] args)
  {
    new LightSensor1();
  }
}
