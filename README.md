# Hybrid adaptive distinguishing sequences part

In FSM-based test generation, a key feature of smart tests are efficient state
identifiers. This tool generates a test suite based on the adaptive
distinguishing sequences as described by Lee and Yannakakis (1994). Many Mealy
machines do not admit such sequences, but luckily the s can be extended
in order to obtain a complete test suite.

_NOTE_: This repository was originally located at
[here](https://gitlab.science.ru.nl/moerman/Yannakakis).
But I realised that installing the software was not as easy as it should be,
and so I cleaned up dependencies, while keeping the original repository fixed.
(Also some people might still use the old link.)

## Introduction

This tool will generate a complete test suite for a given specification. The
specification should be given as a completely-specified, deterministic Mealy
machine (or finite state machine, FSM). Also the implementation is assumed to
be complete and deterministic. If the implementation passes the test suite,
then it is guaranteed to be equivalent or to have at least k more states.
The parameter k can be chosen. The size of the test suite is polynomial in the
number of states of the specification, but exponential in k.

There are many ways to generate such a complete test suite. Many variations,
W, Wp, HSI, ADS, UIOv, ..., exist in literature. Implemented here (as of
writing) are HSI, ADS and the hybrid-ADS method. Since the ADS method is not
valid for all Mealy machines, this tool extends the method to be complete,
hence the name "hybrid-ADS". This is a new method (although very similar to the
HSI and ADS methods).

In addition to choosing the state identifier, one can also choose how the
prefixes for the tests are generated. Typically, one will use shortest paths,
but longer ones can be used too.

All algorithms implemented here can be randomised, which can greatly reduce
the size of the test suite.

Most of the algorithms are found in the directory `lib/` and their usage is best
illustrated in `src/main.cpp`. The latter can be used as a stand-alone tool.
The input to the executable are `.dot` files (of a specific type). Please look
at the provided example to get started.

## Building

There are no dependencies to install.
You can build the tool with `cmake`:

```
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
make
```

I hope most of the code is portable c++11. But I may have used some c++14
features. (If this is a problem for you, please let me know.)

### Windows

David Huistra tried to build the tool on Windows using MinGW. That did not
work. (Dynamic linker errors, probably because I am using c++11.) But it does
work with Visual Studio 2015. For this, you can instruct `cmake` to generate
a solution file:

```
mkdir build
cd build
cmake -G "Visual Studio 14" -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
```

See [here](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html)
for other versions of Visual Studio (not tested). After `cmake` you can open
the solution file and build the project. NOTE: The `Debug` build does not work
properly (I will have to look into this), so I recommend building the
`RelWithDebInfo` configuration.

## Java

For now the java code, which acts as a bridge between LearnLib and this c++
tool, is included here (can be out-dated). But it should earn its own repo at
some point. Also, my javanese is a bit rusty...

## Implementation details

Currently states and inputs are encoded internally as integer values (because
this enables fast indexing). Only for I/O, maps are used to translate between
integers and strings. To reduce the memory footprint `uint16_t`s are used, as
the range is big enough for our use cases (`uint8_t` is clearly too small for
the number of states, but could be used for alphabets).

A prefix tree (or trie) is used to reduce the test suite, by removing common
prefixes. However, this can quickly grow in size. Be warned!

## To run

To run main.cpp in this project, if you are using Windows OS, first, you must open Linux shell. Then you must go to build folder. Finally, you can run, with the options in main.cpp. Here is an example:

```
Users/User/Desktop/hybrid-ads-master$ `cd build`
Users/User/Desktop/hybrid-ads-master/build$ `./main -f ../examples/new_example.dot -m fixed`
```

As an output you will have:

```
3 -> a a b a b a
1 -> a a b a b a
5 -> a a b a
6 -> a b a
4 -> a b a b a
2 -> a b a b a
```

# Minimal FSM Generator part

## To run

First, you must go to inside of this project. Then you can run this project from main.py with a given number of states.
Here is an example to run:

```
C:\Users\User\Desktop\hybrid-ads-master> cd .\Minimal-FSM-Generator\
C:\Users\User\Desktop\hybrid-ads-master\Minimal-FSM-Generator> python .\main.py 3
```

Here is the output:

```
scc -> [[2, 0], [1]]
Multiple groups, trying connections
o Connected the 0 transition of 1 to 2
scc -> [[1, 2, 0]]
Done!
Loops -> 1  Operations -> 1
Is minimal => False
scc -> [[1], [0], [2]]
Multiple groups, trying connections
oo Connected the 1 transition of 0 to 1
i Connected the 1 transition of 1 to 2
scc -> [[2, 1, 0]]
Done!
Loops -> 1  Operations -> 2
Is minimal => True
successfully wrote the example into ../examples/ads_example.dot
```

And if you go to ads_example.dot, you will have this output for this example:

```
digraph distinguishable {
	s0 -> s0 [label="a / 0"];
	s1 -> s1 [label="a / 1"];
	s2 -> s1 [label="a / 1"];

	s0 -> s1 [label="b / 1"];
	s1 -> s2 [label="b / 1"];
	s2 -> s0 [label="b / 0"];
}
```

Note: If you do not specify the number of states, it will automatically give 15

# Overall

To run this overall project as automated, you can again run this project from automate.py in Windows OS.
For this, again you must build the Hybrid ADS. But you only need to do this the first time you run it.
After you build, every setup will be automated. You can also examine automate.py code for advanced settings.

To run automate.py:

```
C:\Users\User\Desktop\hybrid-ads-master> python .\automate.py 5
```
