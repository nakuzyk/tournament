# Intro to Relational Databases (final project)

### Install

This project requires **Python 2.7** and the following Python libraries installed:

- [Psycopg2](http://initd.org/psycopg/)

Once you have python 2.7 and psycorg installed, visit [instructions](https://www.udacity.com/wiki/ud197/install-vagrant) for help with installing Vagrant and Virtual Box.

### How to Run
1) Change current directory to the `tournament`
2) Type `psql`, and then type `\i tournament.sql` 
3) Finally, run the program from the command line `$ python tournament_test.py`
4) You should be able to see the following output once all your tests have passed:
<pre>
<code>
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
</code>
</pre>