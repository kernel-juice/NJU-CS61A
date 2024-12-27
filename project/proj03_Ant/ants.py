"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

################
# Core Classes #
################


class Place:
    """A Place holds insects and has an exit to another Place."""
    is_hive = False

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        # Phase 1: Add an entrance to the exit
        # BEGIN PROBLEM 2
        if isinstance(self.exit, Place):
            self.exit.entrance = self
        # END PROBLEM 2

    def add_insect(self, insect):
        """Asks the insect to add itself to this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.add_to(self)

    def remove_insect(self, insect):
        """Asks the insect to remove itself from this place. This method exists so
        that it can be overridden in subclasses.
        """
        insect.remove_from(self)

    def __str__(self):
        return self.name


class Insect:
    """An Insect, the base class of Ant and Bee, has health and a Place."""

    next_id = 0  # Every insect gets a unique id number
    damage = 0
    # ADD CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 10
    is_waterproof = False
    # END PROBLEM 10

    def __init__(self, health, place=None):
        """Create an Insect with a health amount and a starting PLACE."""
        self.health = health
        self.place = place

        # assign a unique ID to every insect
        self.id = Insect.next_id
        Insect.next_id += 1

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the insect from its place if it
        has no health remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_health(2)
        >>> test_insect.health
        3
        """
        self.health -= amount
        if self.health <= 0:
            self.zero_health_callback()
            self.place.remove_insect(self)

    def action(self, gamestate):
        """The action performed each turn."""

    def zero_health_callback(self):
        """Called when health reaches 0 or below."""

    def add_to(self, place):
        self.place = place

    def remove_from(self, place):
        self.place = None

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.health, self.place)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    implemented = False  # Only implemented Ant classes should be instantiated
    food_cost = 0
    is_container = False
    double_buff = False
    # ADD CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 1
    "*** YOUR CODE HERE ***"
    # END PROBLEM Optional 1

    def __init__(self, health=1):
        super().__init__(health)

    @classmethod
    def construct(cls, gamestate):
        """Create an Ant for a given GameState, or return None if not possible."""
        if cls.food_cost > gamestate.food:
            print('Not enough food remains to place ' + cls.__name__)
            return
        return cls()

    def can_contain(self, other):
        return False

    def store_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def remove_ant(self, other):
        assert False, "{0} cannot contain an ant".format(self)

    def add_to(self, place):
        if place.ant is None:
            place.ant = self
        else:
            # BEGIN PROBLEM 8
            # assert place.ant is None, 'Two ants in {0}'.format(place)
            if self.is_container and ContainerAnt.can_contain(self, place.ant):
                self.ant_contained = place.ant
                place.ant = self
            elif place.ant.is_container and ContainerAnt.can_contain(place.ant, self):
                place.ant.ant_contained = self
            else:
                raise AssertionError('Two ants in {0}'.format(place))
        Insect.add_to(self, place)
        # END PROBLEM 8

    def remove_from(self, place):
        if place.ant is self:
            place.ant = None
        elif place.ant is None:
            assert False, '{0} is not in {1}'.format(self, place)
        else:
            place.ant.remove_ant(self)
        Insect.remove_from(self, place)

    def buff(self):
        """Double this ants's damage, if it has not already been buffed."""
        # BEGIN PROBLEM 12
        if not self.double_buff:
            self.double_buff = True
            self.damage *= 2
        # END PROBLEM 12


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 1
    food_cost = 2
    # END PROBLEM 1

    def action(self, gamestate):
        """Produce 1 additional food for the colony.

        gamestate -- The GameState, used to access game state information.
        """
        # BEGIN PROBLEM 1
        gamestate.food += 1
        # END PROBLEM 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    damage = 1
    # ADD/OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 1
    food_cost = 3
    # END PROBLEM 1
    # BEGIN PROBLEM 4
    min_range = 0
    max_range = float('inf')
    # END PROBLEM 4

    def nearest_bee(self):
        """Return the nearest Bee in a Place (that is not the hive) connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).
        """
        # BEGIN PROBLEM 3 and 4
        assert isinstance(self.place, Place)
        dist_now = 0
        nearest_place = self.place

        while dist_now < self.min_range:
            nearest_place = nearest_place.entrance
            if not nearest_place.entrance:
                return None
            dist_now += 1

        while dist_now <= self.max_range:
            if nearest_place.bees:
                return random_bee(nearest_place.bees)
            elif nearest_place.entrance.is_hive:
                return None
            else:
                nearest_place = nearest_place.entrance
                dist_now += 1
        return None
        # END PROBLEM 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the target Bee, reducing its health."""
        if target is not None:
            target.reduce_health(self.damage)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


def random_bee(bees):
    """Return a random bee from a list of bees, or return None if bees is empty."""
    assert isinstance(bees, list), \
        "random_bee's argument should be a list but was a %s" % type(
            bees).__name__
    if bees:
        return random.choice(bees)

##############
# Extensions #
##############


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 4
    min_range = 0
    max_range = 3
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM 4


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    food_cost = 2
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 4
    min_range = 5
    max_range = float('inf')
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM 4


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 5
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM 5

    def __init__(self, health=3):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and remove the FireAnt from its place if it
        has no health remaining.

        Make sure to reduce the health of each bee in the current place, and apply
        the additional damage if the fire ant dies.
        """
        # BEGIN PROBLEM 5
        temp_place = self.place
        Ant.reduce_health(self, amount)
        if self.place == None:
            amount += self.damage
        for bee in temp_place.bees[:]:
            bee.reduce_health(amount)
        # END PROBLEM 5


# BEGIN PROBLEM 6
# The WallAnt class
class WallAnt(Ant):

    name = 'Wall'
    food_cost = 4
    implemented = True

    def __init__(self, health=4):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)
# END PROBLEM 6


# BEGIN PROBLEM 7
# The HungryAnt Class
class HungryAnt(Ant):

    name = 'Hungry'
    food_cost = 4
    chew_duration = 3
    implemented = True

    def __init__(self, health=1):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)
        self.chew_countdown = 0

    def action(self, gamestate):
        """
        if it is chewing, decrement its chew_countdown counter.
        Otherwise, eat a random Bee in its place by reducing the Bee's health to 0 and restart the chew_countdown timer.
        """
        if self.chew_countdown:
            self.chew_countdown -= 1
        elif self.place.bees:
            poor_bee = random_bee(self.place.bees)
            poor_bee.reduce_health(poor_bee.health)
            self.chew_countdown = self.chew_duration
# END PROBLEM 7


class ContainerAnt(Ant):
    """
    ContainerAnt can share a space with other ants by containing them.
    """
    is_container = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ant_contained = None

    def can_contain(self, other):
        # BEGIN PROBLEM 8
        if self.ant_contained or isinstance(other, ContainerAnt):
            return False
        else:
            return True
        # END PROBLEM 8

    def store_ant(self, ant):
        # BEGIN PROBLEM 8
        self.ant_contained = ant
        # END PROBLEM 8

    def remove_ant(self, ant):
        if self.ant_contained is not ant:
            assert False, "{} does not contain {}".format(self, ant)
        self.ant_contained = None

    def remove_from(self, place):
        # Special handling for container ants
        if place.ant is self:
            # Container was removed. Contained ant should remain in the game
            place.ant = place.ant.ant_contained
            Insect.remove_from(self, place)
        else:
            # default to normal behavior
            Ant.remove_from(self, place)

    def action(self, gamestate):
        # BEGIN PROBLEM 8
        if self.ant_contained:
            self.ant_contained.action(gamestate)
        # END PROBLEM 8


class BodyguardAnt(ContainerAnt):
    """BodyguardAnt provides protection to other Ants."""

    name = 'Bodyguard'
    food_cost = 4
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 8
    implemented = True   # Change to True to view in the GUI

    def __init__(self, health=2):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)
    # END PROBLEM 8


# BEGIN PROBLEM 9
# The TankAnt class
class TankAnt(ContainerAnt):

    name = 'Tank'
    food_cost = 6
    damage = 1
    implemented = True

    def __init__(self, health=2):
        """Create an Ant with a HEALTH quantity."""
        super().__init__(health)

    def action(self, gamestate):
        for bee in self.place.bees[:]:
            bee.reduce_health(self.damage)
        if self.ant_contained:
            self.ant_contained.action(gamestate)
# END PROBLEM 9


class Water(Place):
    """Water is a place that can only hold waterproof insects."""

    def add_insect(self, insect):
        """Add an Insect to this place. If the insect is not waterproof, reduce
        its health to 0."""
        # BEGIN PROBLEM 10
        Place.add_insect(self, insect)
        if not insect.is_waterproof:
            insect.reduce_health(insect.health)
        # END PROBLEM 10


# BEGIN PROBLEM 11
class ScubaThrower(ThrowerAnt):

    name = 'Scuba'
    food_cost = 6
    implemented = True
    is_waterproof = True
# END PROBLEM 11


# BEGIN PROBLEM 12
class QueenAnt(ScubaThrower):  # You should change this line
    # END PROBLEM 12
    """The Queen of the colony. The game is over if a bee enters her place."""

    name = 'Queen'
    food_cost = 7
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 12
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM 12

    @classmethod
    def construct(cls, gamestate):
        """
        Returns a new instance of the Ant class if it is possible to construct, or
        returns None otherwise. Remember to call the construct() method of the superclass!
        """
        # BEGIN PROBLEM 12
        if not gamestate.have_queen:
            gamestate.have_queen = True
            return super().construct(gamestate)

        # END PROBLEM 12

    def action(self, gamestate):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.
        """
        # BEGIN PROBLEM 12
        super().action(gamestate)
        temp_place = self.place.exit
        while temp_place:
            if temp_place.ant:
                temp_place.ant.buff()
                if temp_place.ant.is_container and temp_place.ant.ant_contained:
                    temp_place.ant.ant_contained.buff()
            temp_place = temp_place.exit

        # END PROBLEM 12

    def reduce_health(self, amount):
        """Reduce health by AMOUNT, and if the QueenAnt has no health
        remaining, signal the end of the game.
        """
        # BEGIN PROBLEM 12
        Insect.reduce_health(self, amount)
        if self.health <= 0:
            ants_lose()
        # END PROBLEM 12

    # BEGIN PROBLEM 12
    def remove_from(self, place):
        return
    # END PROBLEM 12


###################
# Extra Challenge #
###################

class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    food_cost = 4
    # BEGIN PROBLEM EC
    slow_turns = 3
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM EC

    def throw_at(self, target):
        if target:
            target.slow(self.slow_turns)

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())


class ScaryThrower(ThrowerAnt):
    """ThrowerAnt that intimidates Bees, making them back away instead of advancing."""

    name = 'Scary'
    food_cost = 6
    # BEGIN PROBLEM EC
    scare_turns = 2
    implemented = True   # Change to True to view in the GUI
    # END PROBLEM EC

    def throw_at(self, target):
        # BEGIN PROBLEM EC
        if target:
            target.scare(self.scare_turns)
        # END PROBLEM EC

    def action(self, gamestate):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee())

#####################
# Optional Problems #
#####################


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place.
    This class is optional.
    """

    name = 'Ninja'
    damage = 1
    food_cost = 5
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 1
    implemented = False   # Change to True to view in the GUI
    # END PROBLEM Optional 1

    def action(self, gamestate):
        # BEGIN PROBLEM Optional 1
        "*** YOUR CODE HERE ***"
        # END PROBLEM Optional 1


class LaserAnt(ThrowerAnt):
    # This class is optional. Only one test is provided for this class.

    name = 'Laser'
    food_cost = 10
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM Optional 2
    implemented = False   # Change to True to view in the GUI
    # END PROBLEM Optional 2

    def __init__(self, health=1):
        super().__init__(health)
        self.insects_shot = 0

    def insects_in_front(self):
        # BEGIN PROBLEM Optional 2
        return {}
        # END PROBLEM Optional 2

    def calculate_damage(self, distance):
        # BEGIN PROBLEM Optional 2
        return 0
        # END PROBLEM Optional 2

    def action(self, gamestate):
        insects_and_distances = self.insects_in_front()
        for insect, distance in insects_and_distances.items():
            damage = self.calculate_damage(distance)
            insect.reduce_health(damage)
            if damage:
                self.insects_shot += 1


########
# Bees #
########

class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    slow_turns = 0
    was_scared = False
    scare_turns = 0
    # OVERRIDE CLASS ATTRIBUTES HERE
    # BEGIN PROBLEM 10
    is_waterproof = True
    # END PROBLEM 10

    def sting(self, ant):
        """Attack an ANT, reducing its health by 1."""
        ant.reduce_health(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Special handling for NinjaAnt
        # BEGIN PROBLEM Optional 1
        return self.place.ant is not None
        # END PROBLEM Optional 1

    def action(self, gamestate):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        gamestate -- The GameState, used to access game state information.
        """
        slowing = False
        scaring = False
        if self.scare_turns:
            scaring = True
            destination = self.place.entrance
        else:
            destination = self.place.exit

        if self.slow_turns:
            self.slow_turns -= 1
            slowing = True

        if self.blocked():
            self.sting(self.place.ant)
        elif self.health > 0 and destination is not None:
            if destination.is_hive:
                if scaring:
                    self.scare_turns -= 1
                return
            elif slowing and gamestate.time % 2 == 1:
                return
            if scaring:
                self.scare_turns -= 1
            self.move_to(destination)

    def add_to(self, place):
        place.bees.append(self)
        super().add_to(place)

    def remove_from(self, place):
        place.bees.remove(self)
        super().remove_from(place)

    def slow(self, length):
        """Slow the bee for a further LENGTH turns."""
        # BEGIN PROBLEM EC
        self.slow_turns += length
        # END PROBLEM EC

    def scare(self, length):
        """
        If this Bee has not been scared before, cause it to attempt to
        go backwards LENGTH times.
        """
        # BEGIN PROBLEM EC
        if not self.was_scared:
            self.was_scared = True
            self.scare_turns += length
        # END PROBLEM EC


class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2


class Boss(Wasp):
    """The leader of the bees. Damage to the boss by any attack is capped.
    """
    name = 'Boss'
    damage_cap = 8

    def reduce_health(self, amount):
        super().reduce_health(min(amount, self.damage_cap))


class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """
    is_hive = True

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees():
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, gamestate):
        exits = [p for p in gamestate.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(gamestate.time, []):
            bee.move_to(random.choice(exits))
            gamestate.active_bees.append(bee)

###################
# Game Components #
###################


class GameState:
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, beehive, ant_types, create_places, dimensions, food=2):
        """Create an GameState for simulating a game.

        Arguments:
        beehive -- a Hive full of bees
        ant_types -- a list of ant classes
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.have_queen = False
        self.food = food
        self.beehive = beehive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(beehive, create_places)

    def configure(self, beehive, create_places):
        """Configure the places in the colony."""
        self.base = AntHomeBase('Ant Home Base')
        self.places = OrderedDict()
        self.bee_entrances = []

        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = beehive
                self.bee_entrances.append(place)
        register_place(self.beehive, False)
        create_places(self.base, register_place,
                      self.dimensions[0], self.dimensions[1])

    def ants_take_actions(self):  # Ask ants to take actions
        for ant in self.ants:
            if ant.health > 0:
                ant.action(self)

    def bees_take_actions(self, num_bees):  # Ask bees to take actions
        for bee in self.active_bees[:]:
            if bee.health > 0:
                bee.action(self)
            if bee.health <= 0:
                num_bees -= 1
                self.active_bees.remove(bee)
        if num_bees == 0:  # Check if player won
            raise AntsWinException()
        return num_bees

    def simulate(self):
        """Simulate an attack on the ant colony. This is called by the GUI to play the game."""
        num_bees = len(self.bees)
        try:
            while True:
                self.beehive.strategy(self)  # Bees invade from hive
                yield None  # After yielding, players have time to place ants
                self.ants_take_actions()
                self.time += 1
                yield None  # After yielding, wait for throw leaf animation to play, then ask bees to take action
                num_bees = self.bees_take_actions(num_bees)
        except AntsWinException:
            print('All bees are vanquished. You win!')
            yield True
        except AntsLoseException:
            print(
                'The bees reached homebase or the queen ant queen has perished. Please try again :(')
            yield False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        ant_type = self.ant_types[ant_type_name]
        ant = ant_type.construct(self)
        if ant:
            self.places[place_name].add_insect(ant)
            self.food -= ant.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the game."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status


class AntHomeBase(Place):
    """AntHomeBase at the end of the tunnel, where the queen normally resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a AntHomeBase. However, if a Bee attempts to
        enter the AntHomeBase, a AntsLoseException is raised, signaling the end
        of a game.
        """
        assert isinstance(insect, Bee), 'Cannot add {0} to AntHomeBase'
        raise AntsLoseException()


def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()


def ants_lose():
    """Signal that Ants lose."""
    raise AntsLoseException()


def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]


def bee_types():
    """Return a list of all implemented Bee classes."""
    all_bee_types = []
    new_types = [Bee]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_bee_types.extend(new_types)
    return all_bee_types


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass


class AntsLoseException(GameOverException):
    """Exception to signal that the ants lose."""
    pass


###########
# Layouts #
###########


def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)


def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################


class AssaultPlan(dict):
    """The Bees' plan of attack for the colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_health, time, count):
        """Add a wave at time with count Bees that have the specified health."""
        bees = [bee_type(bee_health) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    def all_bees(self):
        """Place all Bees in the beehive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]