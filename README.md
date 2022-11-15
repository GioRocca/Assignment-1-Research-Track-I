Assignment 1 Research Track I
=============================

Student: [Giovanni Rocca](https://github.com/GioRocca) (S4802954), Professor: [Carmine Tommaso Recchiuto](https://github.com/CarmineD8)
--------------------------------------------------------------------------------------------------------------------------------------

Goal of the simulation
----------------------

The goal for this simulation is to program a robot, making it able to scan the surrounding area and recognise the objects around him (silver and gold tokens in our assignment).
Every time the robot finds a silver token he must grab it, bring it next to a gold one and then release it.
The robot has to do these operations for every tokens he find and only after pairing all the silver tokens to a gold one (1 by 1) the program can terminate and the robot stops.

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, simply run the assignment.py script to test out the simulator typing:

```bash
$ python2 run.py assignment.py
```


Robot API
---------

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.


```python
R.motors[0].m0.power = ...
R.motors[0].m1.power = ...
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.


### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).


### Flowchart ###

![Flowchart](/images/Cattura_Flowchart.PNG "Flowchart")

### Possible Improvements ###

Some possible improvements for this kind of robot can be, for example:

* Project the robot to bring the nearest or the furthest silver token scanning all the surrounding area instead of bring the first he can see;

* Project the robot to release the silver token to the nearest or the furthest gold token instead of release the silver one to the first gold token that he sees;

* Project the robot to avoid the tokens and pass around them when he has already grabbed one.

