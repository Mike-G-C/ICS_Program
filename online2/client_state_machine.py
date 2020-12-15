from viper1 import *
from chat_utils import *
import json
import chat_group as grp
from SimpleGraphics import *
from math import sin, cos, tan, atan2, pi, sqrt, fabs, ceil, floor
from random import randrange
from time import time
from functools import partial, reduce

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s       # socket for the current client

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def play_with(self, peer):
        msg = json.dumps({"action": "play", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot play with yourself\n'
            self.out_msg += "Enter 'viper' to play with yourself\n"

        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)


    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        """
        :param my_msg:
        :param peer_msg:
        :return: self.out_msg: which will be displayed on the client side
        """
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg == 'score':
                    mysend(self.s, json.dumps({"action":"score"}))
                    score_list = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here is the current ranking:\n'
                    self.out_msg += score_list

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                # Tik Tac Toe Start HERE
                elif my_msg[0] == 'g':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.play_with(peer) == True:
                        self.out_msg += 'Connect to ' + peer + '. Start the game!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'


                elif my_msg == 'viper':
                    mysend(self.s, json.dumps({"action":"viper"}))
                    result = json.loads(myrecv(self.s))["results"]
                    if result == 'start game':
                        f()
                        setAutoUpdate(False)
                        counter = 0  # Frame counter
                        speed = 100  # Snake speeds in pixels per second
                        max_length = 100  # Current maximum length for the snakes
                        time_since_increase = 0  # How much time has elapsed since the last time the
                        # speed was increased and the snakes were lengthened?

                        # Create the player snake.  Randomly position the player in the upper left
                        # corner of the screen and point them toward the middle of the screen.
                        p1_x = randrange(5, getWidth() // 4 - 1)
                        p1_y = randrange(5, getHeight() // 4 - 1)
                        p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)

                        p1_lost = False  # Has the player lost?
                        p1_plost = False  # Previous frame's lost value
                        p1_queue = []  # x1, y1, x2, y2, ..., xn, yn
                        p1_score = 0  # The player's sore

                        # Load all of the images used by the game
                        background, snake, gameover = loadImages()

                        # Get the number of AI players from the user
                        num_ai = getAICount(snake)

                        # Set up each list so that it is populated with 3 values, then truncate the
                        # number of values in the list to the number of AI players selected for the
                        # game.
                        if num_ai > 0:
                            e_queues = [[randrange(3 * getWidth() // 4 + 1, getWidth() - 1), \
                                         randrange(3 * getHeight() // 4 + 1, getHeight() - 1)], \
                                        [randrange(3 * getWidth() // 4 + 1, getWidth() - 1),
                                         randrange(5, 1 * getHeight() // 4 - 1)], \
                                        [randrange(5, 1 * getWidth() // 4 - 1),
                                         randrange(3 * getHeight() // 4 + 1, getHeight() - 1)]][:num_ai]
                            e_lengths = [0, 0, 0][:num_ai]
                            e_scores = [0, 0, 0][:num_ai]
                            e_names = ["Computer1", "Computer2", "Computer3"][:num_ai]
                            e_colors = ["blue3", "black", "goldenrod2"][:num_ai]
                            e_lost = [False, False, False][:num_ai]
                            e_plost = [False, False, False][:num_ai]

                            # Compute each AI snake's initial heading
                            e_headings = []
                            for i in range(len(e_queues)):
                                e_headings.append(atan2(getHeight() / 2 - e_queues[i][1], \
                                                        getWidth() / 2 - e_queues[i][0]))

                        # Get ready to play!
                        countdown(COUNTDOWN_DURATION, snake)
                        state = "playing"
                        max_score = 0

                        # Make the snakes wider so they are easier to see
                        setWidth(3)
                        reset_time = 0

                        # Set up initial values for the frame rate timing
                        start = time()
                        elapsed = 1 / FRAME_RATE

                        # While the game has not been closed.
                        while not closed() and not (
                                max_score >= MAX_SCORE and state == "next_round" and time() > reset_time):
                            if state == "next_round" and time() > reset_time:
                                # Reset the maximum length and speed
                                speed = 100  # snake speeds in pixels per second
                                max_length = 100  # current maximum length for the snakes

                                # Set the player up to play again
                                p1_x = randrange(5, getWidth() // 4 - 1)
                                p1_y = randrange(5, getHeight() // 4 - 1)
                                p1_heading = atan2(getHeight() / 2 - p1_y, getWidth() / 2 - p1_x)
                                p1_lost = False
                                p1_plost = False  # Previous frame's lost value
                                p1_queue = []

                                # Set the AI players up to play again
                                e_queues = [[randrange(3 * getWidth() // 4 + 1, getWidth() - 1), \
                                             randrange(3 * getHeight() // 4 + 1, getHeight() - 1)], \
                                            [randrange(3 * getWidth() // 4 + 1, getWidth() - 1),
                                             randrange(5, 1 * getHeight() // 4 - 1)], \
                                            [randrange(5, 1 * getWidth() // 4 - 1),
                                             randrange(3 * getHeight() // 4 + 1, getHeight() - 1)]][:num_ai]
                                e_lengths = [0, 0, 0][:num_ai]
                                e_lost = [False, False, False][:num_ai]
                                e_plost = [False, False, False][:num_ai]

                                # Compute each AI snake's initial heading
                                e_headings = []
                                for i in range(len(e_queues)):
                                    e_headings.append(atan2(getHeight() / 2 - e_queues[i][1], \
                                                            getWidth() / 2 - e_queues[i][0]))

                                # Prepare for the next round
                                countdown(COUNTDOWN_DURATION, snake)
                                state = "playing"

                                # Reset the timer
                                start = time()
                                elapsed = 1 / FRAME_RATE

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

                            # Draw the enemy snakes
                            for i in range(len(e_queues)):
                                if len(e_queues[i]) >= 4:
                                    if e_lost[i] == True:
                                        setColor("red")
                                    else:
                                        setColor(e_colors[i])
                                    line(e_queues[i])
                                    ellipse(e_queues[i][-2] - 2, e_queues[i][-1] - 2, 5, 5)

                            # Read input
                            keys = getHeldKeys()

                            # Update the display values
                            setFont("Arial", 10)
                            setColor("Black")
                            text(5, 530, "Speed: " + str(round(speed, 1)), "w")
                            text(5, 545, "Max Length: " + str(max_length), "w")
                            text(5, 560, "Frame rate: " + str(round(1 / elapsed, 2)), "w")

                            # Respond to the input and update the player's position
                            if "Left" in keys:
                                p1_heading = p1_heading - pi * elapsed
                            if "Right" in keys:
                                p1_heading = p1_heading + pi * elapsed

                            #
                            # Part 1: A Moving Dot...
                            #

                            # Generate a new point if p1 is still alive
                            if not p1_lost:
                                p1_x = p1_x + cos(p1_heading) * speed * elapsed
                                p1_y = p1_y + sin(p1_heading) * speed * elapsed

                                #
                                # Part 2: A Long and Permanent Line
                                #
                                # Add the new point to the queue list
                                p1_queue.append(p1_x)
                                p1_queue.append(p1_y)

                            #
                            # Part 3: A Growing Snake
                            #

                            ''' An recursive Solution
                            def cal_length(queue_list, max_length):
                                length = 0
                                for i in range((len(queue_list) - 2) // 2):
                                    length += ((queue_list[i + 2] - queue_list[i]) ** 2 + (queue_list[i + 3] - queue_list[i + 1]) ** 2) ** 0.5
                                    if length > max_length:
                                        queue_list.pop(0)
                                        queue_list.pop(0)
                                        cal_length(queue_list, max_length) # Recursion
                            if not p1_lost:
                                cal_length(p1_queue, max_length)
                            '''

                            # Initialize the flag for the length
                            flag = True
                            while not p1_lost and flag:
                                # Code of check_length starts at line 58
                                flag, t = check_length(p1_queue, max_length)
                                # Update the queue list if p1's length exceeds
                                if flag:
                                    p1_queue = t

                            #
                            # Part 4: Colliding with Walls
                            #

                            # Avoid Index out of range error
                            if len(p1_queue) != 0:
                                # Alive: A boolean variable judging whether p1 is in the map
                                alive = 0 <= p1_queue[-2] <= 799 and 0 <= p1_queue[-1] <= 599
                                # Update p1_lost when p1 is not alive
                                if not alive:
                                    p1_lost = True

                            #
                            # Part 5: Colliding with Yourself
                            #

                            # Avoid Index out of range error
                            if len(p1_queue) >= 8:
                                # Code of check_intersect starts at line 76
                                if check_intersect(p1_queue[:-4], p1_queue[-4:]):
                                    p1_lost = True

                            #
                            # Part 6: Colliding with Other Snakes
                            #

                            # Loop for all AI snakes
                            for i in range(len(e_queues)):
                                # Code of check_intersect starts at line 76
                                if check_intersect(e_queues[i], p1_queue[-4:]):
                                    p1_lost = True
                                    # break
                                    # Break at here can reduce useless computation, however, we are not allowed to use it.

                            # Respond to the input and update the AI's position if they haven't lost
                            for i in range(len(e_queues)):
                                if e_lost[i] == False:
                                    # Avoid colliding with ourselves due to overlap between the current
                                    # segment touching the end of the previous one
                                    most_e_queue = e_queues[i][:-2]

                                    # Need the other two snakes so that we can check if we collided with
                                    # them.  Construct a list of the other snakes, and add to their heads to
                                    # make cut-offs harder.
                                    others = list(e_queues)
                                    for j in range(len(e_queues)):
                                        ox = others[j][-2] + cos(e_headings[j]) * speed * 0.6
                                        oy = others[j][-1] + sin(e_headings[j]) * speed * 0.6
                                        others[j] = others[j] + [ox, oy]

                                    others.pop(i)

                                    # Extend the player's queue to make it harder for the player to cut the
                                    # AI off
                                    if 'p1_queue' in locals() and len(p1_queue) > 0:
                                        extended_p1_queue = p1_queue + [p1_queue[-2] + cos(p1_heading) * speed * 0.6,
                                                                        p1_queue[-1] + sin(p1_heading) * speed * 0.6]
                                    else:
                                        extended_p1_queue = []

                                    angle = e_headings[i] - 0.6 * pi
                                    found = False
                                    while angle <= e_headings[i] + 0.6 * pi:
                                        (hits, x, y) = closestCollision(e_queues[i][-2], e_queues[i][-1],
                                                                        e_queues[i][-2] + cos(angle) * 10000,
                                                                        e_queues[i][-1] + sin(angle) * 10000,
                                                                        [extended_p1_queue, most_e_queue,
                                                                         BOUNDARY] + others)

                                        if hits == False:
                                            # This should never happen becase we should always at least hit
                                            # the boundary
                                            print(e_queues[i][-2], e_queues[i][-1], e_queues[i][-2] + cos(angle) * 2000,
                                                  e_queues[i][-1] + sin(angle) * 2000)
                                            raise ("hits is False when that shouldn't be possible")

                                        if hits and found == False:
                                            best_x = x
                                            best_y = y
                                            best_angle = angle
                                            found = True
                                        elif hits and found:
                                            if dist2(e_queues[i][-2], e_queues[i][-1], x, y) > dist2(e_queues[i][-2],
                                                                                                     e_queues[i][-1],
                                                                                                     best_x, best_y):
                                                best_x = x
                                                best_y = y
                                                best_angle = angle

                                        angle += 0.05 * pi

                                    old_heading = e_headings[i]

                                    if e_headings[i] < -pi / 2 and best_angle > pi / 2:
                                        best_angle -= 2 * pi
                                    if e_headings[i] > pi / 2 and best_angle < -pi / 2:
                                        best_angle += 2 * pi

                                    if e_headings[i] < best_angle:
                                        if best_angle - e_headings[i] < pi * elapsed:
                                            e_headings[i] = best_angle
                                        else:
                                            e_headings[i] = e_headings[i] + pi * elapsed
                                    elif e_headings[i] > best_angle:
                                        if e_headings[i] - best_angle < pi * elapsed:
                                            e_headings[i] = best_angle
                                        else:
                                            e_headings[i] = e_headings[i] - pi * elapsed

                                    e_headings[i] %= 2 * pi

                                    ex = e_queues[i][-2] + cos(e_headings[i]) * speed * elapsed
                                    ey = e_queues[i][-1] + sin(e_headings[i]) * speed * elapsed

                                    # Determine if the AI has crashed into any AI (including itself)
                                    for j in range(len(e_queues)):
                                        if i == j:
                                            if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, e_queues[j][:-2]):
                                                e_lost[i] = True
                                        else:
                                            if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, e_queues[j]):
                                                e_lost[i] = True

                                    # Determine if the AI has crashed into the player
                                    if 'p1_queue' in locals():
                                        if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, p1_queue):
                                            e_lost[i] = True

                                    # Determine if the player has crashed into a wall
                                    if fastCollides(e_queues[i][-2], e_queues[i][-1], ex, ey, BOUNDARY):
                                        e_lost[i] = True

                                    # Add the latest segment to the snake and truncate it to the correct
                                    # length
                                    e_queues[i].append(ex)
                                    e_queues[i].append(ey)
                                    e_lengths[i] += dist(e_queues[i][-4], e_queues[i][-3], e_queues[i][-2],
                                                         e_queues[i][-1])
                                    while e_lengths[i] > max_length:
                                        e_lengths[i] -= dist(e_queues[i][0], e_queues[i][1], e_queues[i][2],
                                                             e_queues[i][3])
                                        # Is this faster than popping two elements from the front of the list?
                                        e_queues[i] = e_queues[i][2:]

                            # Increase the speeds and lengths of the snakes
                            time_since_increase += elapsed
                            if time_since_increase > 0.1:
                                time_since_increase -= 0.1
                                speed += 0.1
                                max_length += 2

                            # If the player's lost status changed during this frame
                            if p1_lost != p1_plost:
                                # Give a point to every AI that is still alive
                                for j in range(len(e_queues)):
                                    if e_lost[j] == False:
                                        e_scores[j] += 1

                                # Update the maximum score
                                max_score = max([p1_score] + e_scores)

                            # If any of the enemy's list status changed during this frame
                            for i in range(len(e_queues)):
                                if e_lost[i] != e_plost[i]:
                                    # Give a point to the player if they are still alive
                                    if p1_lost == False:
                                        p1_score += 1

                                    # Give a point to every AI that is still alive
                                    for j in range(len(e_queues)):
                                        if e_lost[j] == False:
                                            e_scores[j] += 1

                                    # Update the maximum score
                                    max_score = max([p1_score] + e_scores)

                            # Display the scores
                            setColor("chartreuse2")
                            setFont("Arial", 15)
                            text(10, getHeight() - 20, "Human: " + str(p1_score), "w")
                            for j in range(len(e_scores)):
                                setColor(e_colors[j])
                                text((j + 1) * getWidth() / (len(e_scores) + 1), getHeight() - 20,
                                     e_names[j] + ": " + str(e_scores[j]), "w")

                            # Determine if the game has been won by counting the number of players
                            # that have not lost
                            if state == "playing":
                                winner_count = 0
                                if p1_lost == False:
                                    winner_count += 1
                                    winner = "Human"
                                for i in range(len(e_lost)):
                                    if e_lost[i] == False:
                                        winner_count += 1
                                        winner = e_names[i]

                                if winner_count <= 1:
                                    state = "next_round"
                                    reset_time = time() + 3

                            # Update the previous lost status to match the current lost status for the
                            # player and all of the AIs
                            p1_plost = p1_lost
                            for i in range(len(e_queues)):
                                e_plost[i] = e_lost[i]

                            # Count the frame
                            counter += 1

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
                                winner = "Human"

                            # Determine who the winners are
                            for i in range(len(e_scores)):
                                if e_scores[i] == max_score:
                                    if winner == "":
                                        winner = e_names[i]
                                    else:
                                        winner += " and " + e_names[i]

                            # Determine which set of frames to use, depending on whether the human is
                            # one of the game's winners
                            if "Human" not in winner:
                                frames = gameover
                            else:
                                frames = [snake]

                            # Display the gameover message, animating the backround image at 5 frames
                            # per second
                            start_time = time()
                            i = 0
                            global score
                            score = p1_score
                            while not closed():
                                clear()
                                drawImage(frames[i], 0, 0)

                                setFont("Arial", 30)
                                text(getWidth() / 2, getHeight() / 2 - 50, "Game Over!")
                                text(getWidth() / 2, getHeight() / 2 + 50, "The game was won by")
                                text(getWidth() / 2, getHeight() / 2 + 100, winner)
                                update()
                                if time() > start_time + 0.2:
                                    i = i + 1
                                    start_time = time()

                                if i >= len(frames):
                                    i = 0

                    mysend(self.s, json.dumps({"action" : "update", 'message' : p1_score}))



                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p' and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg

                if peer_msg["action"] == "connect":
                    # ----------your code here------#
                    print(peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                elif peer_msg["action"] == "play":
                    # ----------your code here------#
                    print(peer_msg)
                    self.peer = peer_msg["from"]
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You can play with ' + self.peer
                    self.out_msg += '------------------------------------\n'


                    # ----------end of your code----#

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:  # peer's stuff, coming in
                # ----------your code here------#
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.out_msg += peer_msg["message"]
                    self.state = S_LOGGEDIN
                else:
                    self.out_msg += peer_msg["from"] + peer_msg["message"]
                # ----------end of your code----#
            if self.state == S_LOGGEDIN:
                # Display the menu again
                self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
