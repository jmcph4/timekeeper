# Timekeeper #
---

Timekeeper is a plain and simple time audit tool. You interact with Timekeeper via a simple interactive shell, with a small and direct set of commands for interacting with logs and slices.

To start using Timekeeper:

    git clone https://github.com/jmcph4/timekeeper.git
    cd timekeeper
    python main.py

## Concepts ##
### Slice ###
A *slice* is a slice of your time. It has four things:

 - start time
 - end time
 - category
 - description

### Log ###
A *log* is simply a collection of slices. It's a story about how you spend your time.

## Technical ##
Timekeeper's implementation is as simple as its purpose. A Python 3.x package, with two modules defined:

 - `slice`
 - `log`

