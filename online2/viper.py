from SimpleGraphics import *
from math import sin, cos, tan, atan2, pi, sqrt, fabs, ceil, floor
from random import randrange
from time import time
from functools import partial, reduce

MAX_SCORE = 10          # What score has to be achieved for the game to end?
COUNTDOWN_DURATION = 3  # How long is the countdown between rounds?

FRAME_RATE = 30 # Target framerate to maintain
BOUNDARY = [0, 0, 799, 0, 799, 599, 0, 599, 0, 0] # Line segments for the edges
                                                  # of the screen

def check_length(queue_list, max_length):
    length = 0
    # For n points, loop for n-1 times to sum up the distance of the lines
    for i in range((len(queue_list) - 2) // 2):
        length += ((queue_list[i + 2] - queue_list[i]) ** 2 + (queue_list[i + 3] - queue_list[i + 1]) ** 2) ** 0.5
    flag = True if length > max_length else False
    return flag, queue_list[2:]


def check_intersect(prv, new):
    # Reorganize the x, y coordinates in prv and store them in new lists
    prv_x = [prv[i * 2] for i in range(len(prv) // 2)]
    prv_y = [prv[i * 2 + 1] for i in range(len(prv) // 2)]
    ans = False
    # For n points, loop for n-1 times to check each line
    for i in range(len(prv_x) - 1):
        if doIntersect(prv_x[i], prv_y[i], prv_x[i + 1], prv_y[i + 1], new[0], new[1], new[2], new[3]):
            ans = True
            # break
            # Break at here can reduce useless computation, however, we are not allowed to use it.
    return ans


def doIntersect(ax, ay, bx, by, cx, cy, dx, dy):
  return doIntersectPos(ax, ay, bx, by, cx, cy, dx, dy)[0]


def onSegment(px, py, qx, qy, rx, ry):
  if qx <= px and qx <= rx and qx >= px and qx >= rx and \
     qy <= py and qy <= ry and qy >= py and qy >= ry:
    return True

  return False


def doIntersectPos(ax, ay, bx, by, cx, cy, dx, dy):
  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return False, 0, 0
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return False, 0, 0
  if ay < cy and ay < dy and by < cy and by < dy:
    return False, 0, 0
  if ay > cy and ay > dy and by > cy and by > dy:
    return False, 0, 0

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      return (True, ax, m_cd * ax + b_cd)

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      return (True, cx, m_ab * cx + b_ab)

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return (True, x, y)

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return (True, x, y)

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return (True, cx, cy)

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return (True, dx, dy)

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return (True, ax, ay)

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return (True, bx, by)

  return (False, 0, 0) # Doesn't fall in any of the above cases



def doIntersectDistPos(ax, ay, bx, by, seg):
  cx, cy, dx, dy = seg

  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return 1e12, False, 0, 0
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return 1e12, False, 0, 0
  if ay < cy and ay < dy and by < cy and by < dy:
    return 1e12, False, 0, 0
  if ay > cy and ay > dy and by > cy and by > dy:
    return 1e12, False, 0, 0

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      x, y = ax, m_cd * ax + b_cd
      return (dist2(ax, ay, x, y), True, x, y)

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      x, y = cx, m_ab * cx + b_ab
      return (dist2(ax, ay, x, y), True, x, y)

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return (dist2(ax, ay, x, y), True, x, y)

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return (dist2(ax, ay, x, y), True, x, y)

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return (dist2(ax, ay, cx, cy),True, cx, cy)

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return (dist2(ax, ay, dx, dy), True, dx, dy)

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return (0, True, ax, ay)

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return (dist2(ax, ay, bx, by), True, bx, by)

  return (1e12, False, 0, 0) # Doesn't fall in any of the above cases

#
#
def doIntersectTuple(ax, ay, bx, by, seg):
  cx, cy, dx, dy = seg

  # Bounding box checks
  if ax < cx and ax < dx and bx < cx and bx < dx:
    return False
  if ax > cx and ax > dx and bx > cx and bx > dx:
    return False
  if ay < cy and ay < dy and by < cy and by < dy:
    return False
  if ay > cy and ay > dy and by > cy and by > dy:
    return False

  # Compute the orientation values.  This has been inlined to improve
  # performance.
  val = (by - ay) * (cx - bx) - (bx - ax) * (cy - by)
  o1 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (by - ay) * (dx - bx) - (bx - ax) * (dy - by)
  o2 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (ax - dx) - (dx - cx) * (ay - dy)
  o3 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  val = (dy - cy) * (bx - dx) - (dx - cx) * (by - dy)
  o4 = 1 if val >= 1e-10 else (2 if val <= -1e-10 else 0)

  # General case
  if o1 != o2 and o3 != o4:
    # If (ax, ay, bx, by) is vertical
    if ax == bx:
      m_cd = (dy - cy) / (dx - cx)
      b_cd = cy - m_cd * cx
      return True

    # If (cx, cy, dx, dy) is vertical
    if cx == dx:
      m_ab = (by - ay) / (bx - ax)
      b_ab = ay - m_ab * ax
      return True

    # This can't be computed earlier in case bx - ax is 0, or dx - cx is 0
    m_ab = (by - ay) / (bx - ax)
    b_ab = ay - m_ab * ax
    m_cd = (dy - cy) / (dx - cx)
    b_cd = cy - m_cd * cx

    # If m_cd + m_ab is 0 or b_ab is 0 then we have to handle it as a special
    # case
    if m_cd + m_ab == 0 or b_ab == 0:
      y = -(m_ab * b_cd + m_cd * b_ab) / (m_cd - m_ab)
      x = (y - b_ab) / m_ab
      return True

    # General case
    x = (b_cd - b_ab) / (m_ab - m_cd)
    y = m_ab * x + b_ab
    return True

  # Special Cases
  # a, b and c are colinear and c lies on segment ab
  if o1 == 0 and onSegment(ax, ay, cx, cy, bx, by):
    return True

  # a, b and d are colinear and d lies on segment ab
  if o2 == 0 and onSegment(ax, ay, dx, dy, bx, by):
    return True

  # c, d and a are colinear and a lies on segment cd
  if o3 == 0 and onSegment(cx, cy, ax, ay, dx, dy):
    return True

  # c, d and b are colinear and b lies on segment cd
  if o4 == 0 and onSegment(cx, cy, bx, by, dx, dy):
    return True

  return False # Doesn't fall in any of the above cases


def dist(x1, y1, x2, y2):
  return sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1))


def dist2(x1, y1, x2, y2):
  return (x2-x1) * (x2-x1) + (y2-y1) * (y2-y1)


def fastCollides(ax, ay, bx, by, segments):
  it = iter(segments)
  it2 = iter(segments)
  if len(segments) >= 2:
    next(it2)
    next(it2)
  # Are the above 4 lines faster than it2 = iter(segments[2:])?  That
  # probably depends on the length of segments.

  endpts = list(zip(it, it, it, it)) + list(zip(it2, it2, it2, it2))
  full = map(partial(doIntersectTuple, ax, ay, bx, by), endpts)
  return reduce((lambda x, y: x or y), full, False)


def closestCollision(ax, ay, bx, by, seg_lists):
  full = []
  for segs in seg_lists:
    it = iter(segs)
    it2 = iter(segs)
    if len(segs) >= 2:
      next(it2)
      next(it2)
    # Are the above 4 lines faster than it2 = iter(segments[2:])?  That
    # probably depends on the length of segments.

    endpts = list(zip(it, it, it, it)) + list(zip(it2, it2, it2, it2))

    # Not sure if += or extend is faster
    #full.extend(map(partial(doIntersectDistPos, ax, ay, bx, by), endpts))
    full += map(partial(doIntersectDistPos, ax, ay, bx, by), endpts)

  mn = min(full)
  if mn[1] == False:
    return (False, 0, 0)
  else:
    return (True, mn[2], mn[3])


def countdown(duration, background):
  start = time()
  end = start + duration

  setColor("black")
  while not closed() and time() < end:
    # Clear the screen and drawn the background image
    clear()
    drawImage(background, 0, 0)

    # Display the countdown message
    setFont("Arial", 30)
    text(getWidth() / 2, getHeight() / 2, ceil(end - time()), "c")
    setFont("Arial", 16)
    text(getWidth() / 2, getHeight() / 2 - 50, "Game starting in...", "c")
    update()


def loadImages():
  # Load all of the images.  Display an error message and quit if the images
  # are not loaded successfully.
  try:
    allImages = loadImage("ViperImages.gif")
  except:
    print("An error was encountered while trying to load the images from")
    print("ViperImages.gif.  Please ensure that it resides in the same")
    print("folder / directory as your program.")
    close()
    quit()

  # Extract the plain background image
  background = tk.PhotoImage()
  background.tk.call(background, 'copy', allImages, '-from', 0, 0, 800, 600, '-to', 0, 0)

  # Extract the snake image
  snake = tk.PhotoImage()
  snake.tk.call(snake, 'copy', allImages, '-from', 0, 600, 800, 600+600, '-to', 0, 0)

  # Extract the gameover images
  gameover = []
  for i in range(6):
    temp = tk.PhotoImage()
    temp.tk.call(temp, 'copy', allImages, '-from', 0, 1200+600*i, 800, 1200+600*(i+1), '-to', 0, 0)
    gameover.append(temp)

  # Return all of the images
  return background, snake, gameover


# Play the game
def main():
  f()
  # Only redraw the screen when specifically requested to do so
  setAutoUpdate(False)

  counter = 0             # Frame counter
  speed = 100             # Snake speeds in pixels per second
  max_length = 100        # Current maximum length for the snakes
  time_since_increase = 0 # How much time has elapsed since the last time the
                          # speed was increased and the snakes were lengthened?

  # Create the player snake.  Randomly position the player in the upper left
  # corner of the screen and point them toward the middle of the screen.
  p1_x = randrange(5, getWidth() // 4 - 1)
  p1_y = randrange(5, getHeight() // 4 - 1)
  p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)

  p2_x = randrange(13, getWidth() - 1)
  p2_y = randrange(13, getHeight() - 1)
  p2_heading = atan2(getHeight() / 2 - p2_y, getWidth() / 2 - p2_x)

  p1_lost = False   # Has the player lost?
  p1_plost = False  # Previous frame's lost value
  p1_queue = []     # x1, y1, x2, y2, ..., xn, yn
  p1_score = 0      # The player's sore

  p2_lost = False   # Has the player lost?
  p2_plost = False  # Previous frame's lost value
  p2_queue = []     # x1, y1, x2, y2, ..., xn, yn
  p2_score = 0      # The player's sore

  # Load all of the images used by the game
  background, snake, gameover = loadImages()

  # Get ready to play!
  countdown(COUNTDOWN_DURATION, snake)
  state = "playing"
  max_score = 0

  # Make the snakes wider so they are easier to see
  setWidth(3)
  reset_time = 0

  # Set up initial values for the frame rate timing
  start = time()
  elapsed = 1/FRAME_RATE

  # While the game has not been closed.
  while not closed() and not (max_score >= MAX_SCORE and state == "next_round" and time() > reset_time):
    if state == "next_round" and time() > reset_time:
      # Reset the maximum length and speed
      speed = 100        # snake speeds in pixels per second
      max_length = 100   # current maximum length for the snakes

      # Set the player up to play again
      p1_x = randrange(5, getWidth() // 4 - 1)
      p1_y = randrange(5, getHeight() // 4 - 1)
      p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)
      p1_lost = False
      p1_plost = False  # Previous frame's lost value
      p1_queue = []

      p2_x = randrange(15, getWidth() // 4 - 1)
      p2_y = randrange(15, getHeight() // 4 - 1)
      p2_heading = atan2(getHeight() / 2 - p2_y, getWidth() / 2 - p2_x)
      p2_lost = False
      p2_plost = False  # Previous frame's lost value
      p2_queue = []

      # Prepare for the next round
      countdown(COUNTDOWN_DURATION, snake)
      state = "playing"

      # Reset the timer
      start = time()
      elapsed = 1/FRAME_RATE


    clear()
    drawImage(background, 0, 0)

    # Draw the player snake if it consists of at least one line segment
    if p1_lost == True:
        setColor("red")
    else:
        setColor("chartreuse2")
    ellipse(p1_x - 2, p1_y - 2, 5, 5)
    if 'p1_queue' in locals() and len(p1_queue) >= 4:
        line(p1_queue)

    if p2_lost == True:
        setColor("red")
    else:
        setColor("blue")
    ellipse(p2_x - 2, p2_y - 2, 5, 5)
    if 'p2_queue' in locals() and len(p2_queue) >= 4:
        line(p2_queue)



    # Read input
    keys = getHeldKeys()

    # Update the display values
    setFont("Arial", 10)
    setColor("Black")
    text(5, 530, "Speed: " + str(round(speed,1)), "w")
    text(5, 545, "Max Length: " + str(max_length), "w")
    text(5, 560, "Frame rate: " + str(round(1 / elapsed,2)), "w")

    # Respond to the input and update the player's position
    if "Left" in keys:
        p1_heading = p1_heading - pi * elapsed
    if "Right" in keys:
        p1_heading = p1_heading + pi * elapsed

    if "a" in keys:
        p2_heading = p2_heading - pi * elapsed
    if "d" in keys:
        p2_heading = p2_heading + pi * elapsed


    # Generate a new point if p1 is still alive
    if not p1_lost:
        p1_x = p1_x + cos(p1_heading) * speed * elapsed
        p1_y = p1_y + sin(p1_heading) * speed * elapsed


        # Add the new point to the queue list
        p1_queue.append(p1_x)
        p1_queue.append(p1_y)

    if not p2_lost:
        p2_x = p2_x + cos(p2_heading) * speed * elapsed
        p2_y = p2_y + sin(p2_heading) * speed * elapsed


        # Add the new point to the queue list
        p2_queue.append(p2_x)
        p2_queue.append(p2_y)

    #
    # Part 3: A Growing Snake
    #

    # Initialize the flag for the length
    flag1 = True
    while not p1_lost and flag1:
        # Code of check_length starts at line 58
        flag1, t = check_length(p1_queue, max_length)
        # Update the queue list if p1's length exceeds
        if flag1:
            p1_queue = t


    if len(p1_queue) != 0:
        # Alive: A boolean variable judging whether p1 is in the map
        alive = 0 <= p1_queue[-2] <= 799 and 0 <= p1_queue[-1] <= 599
        # Update p1_lost when p1 is not alive
        if not alive:
            p1_lost = True


    if len(p1_queue) >= 8:
        # Code of check_intersect starts at line 76
        if check_intersect(p1_queue[:-4], p1_queue[-4:]):
            p1_lost = True


    for i in range(len(p2_queue)):
        # Code of check_intersect starts at line 76
        if check_intersect(p2_queue, p1_queue[-4:]):
            p1_lost = True
            break

    flag2 = True
    while not p2_lost and flag2:
        # Code of check_length starts at line 58
        flag2, t = check_length(p2_queue, max_length)
        # Update the queue list if p1's length exceeds
        if flag2:
            p2_queue = t


    if len(p2_queue) != 0:
        # Alive: A boolean variable judging whether p1 is in the map
        alive = 0 <= p2_queue[-2] <= 799 and 0 <= p2_queue[-1] <= 599
        # Update p1_lost when p1 is not alive
        if not alive:
            p2_lost = True


    if len(p2_queue) >= 8:
        # Code of check_intersect starts at line 76
        if check_intersect(p2_queue[:-4], p2_queue[-4:]):
            p2_lost = True


    for i in range(len(p1_queue)):
        # Code of check_intersect starts at line 76
        if check_intersect(p1_queue, p2_queue[-4:]):
            p2_lost = True
            break


        # Determine if the AI has crashed into the player
        if 'p1_queue' in locals():
            if fastCollides(p2_queue[-2], p2_queue[-1], p2_x, p2_y, p1_queue):
              p2_lost = True


        if 'p2_queue' in locals():
            if fastCollides(p1_queue[-2], p1_queue[-1], p1_x, p1_y, p2_queue):
                p1_lost = True

    # Increase the speeds and lengths of the snakes
    time_since_increase += elapsed
    if time_since_increase > 0.1:
        time_since_increase -= 0.1
        speed += 0.1
        max_length += 2


      # Update the maximum score
    max_score = max([p1_score] + [p2_score])

    # If any of the enemy's list status changed during this frame
    # for i in range(len(e_queues)):
    if p2_lost != p2_plost:
        # Give a point to the player if they are still alive
        if p1_lost == False:
            p1_score += 1
    if p1_lost != p1_plost:
        # Give a point to the player if they are still alive
        if p2_lost == False:
            p2_score += 1
    #
    #
    # Display the scores
    setColor("chartreuse2")
    setFont("Arial", 15)
    text(10, getHeight() - 20, "Player1: " + str(p1_score), "w")
    text(200, getHeight() - 20, "Player2: " + str(p2_score), "w")
    text(600, getHeight() - 20, "Player1: 'Left' and 'Right' to control")
    text(600, getHeight() - 60, "Player2: 'a' and 'd' to control")
    # # Determine if the game has been won by counting the number of players
    # # that have not lost
    if state == "playing":
      winner_count = 0
      if p1_lost == False:
        winner_count += 1
        winner = "Player1"
      if p2_lost == False:
        winner_count += 1
        winner = "Player2"

      if winner_count <= 1:
        state = "next_round"
        reset_time = time() + 3
    #
    #
    # # Update the previous lost status to match the current lost status for the

    p1_plost = p1_lost
    p2_plost = p2_lost

    # # Count the frame
    counter += 1
    #
    if winner_count == 0 and state == "next_round":
      setFont("Arial", 30)
      setColor("black")
      text(getWidth() / 2, getHeight() / 2, "This Round Ended in a Draw")
    elif winner_count == 1 and state == "next_round":
      setFont("Arial", 30)
      setColor("black")
      text(getWidth() / 2, getHeight() / 2, "This Round was Won by " + winner)

    # Update the screen
    update()

    # Delay so that the current frame took 1/FRAME_RATE of a second
    current = time()
    elapsed = current - start
    while elapsed < 1 / FRAME_RATE:
      current = time()
      elapsed = current - start

    # Record the start time for the next frame
    start = current

  if not closed():
      # Find the winner of the game
      winner = ""
      if p1_score == max_score:
          winner = "Player1"
      else:
          winner = 'Player2'

    # per second
      start_time = time()
      i = 0
      while not closed():

          setFont("Arial", 30)
          text(getWidth() / 2, getHeight() / 2 - 50, "Game Over!")
          text(getWidth() / 2, getHeight() / 2 + 50, "The game was won by")
          text(getWidth() / 2, getHeight() / 2 + 100, winner)
          update()
          if time() > start_time + 0.2:
              i = i + 1
              start_time = time()
