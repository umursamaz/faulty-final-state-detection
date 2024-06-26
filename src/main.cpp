#include <adaptive_distinguishing_sequence.hpp>
#include <logging.hpp>
#include <mealy.hpp>
#include <reachability.hpp>
#include <read_mealy.hpp>
#include <separating_family.hpp>
#include <splitting_tree.hpp>
#include <test_suite.hpp>
#include <transfer_sequences.hpp>
#include <trie.hpp>

#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <map>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
/*
 * The reason I use getopt, instead of some library (I've used
 * docopts and boost in the past), is that I want no dependencies.
 * I've installed this software several times, and it was never
 * easy because of its dependencies.
 */
#ifdef _WIN32
extern "C" {
#include <windows_getopt.h>
}
#else
#include <unistd.h>
#endif

using namespace std;

static const char USAGE[] =
    R"(Generate or stream a test suite for a given FSM.

    Usage:
      main [options]

    Options:
      -h             Show this screen
      -v             Show version
      -m <arg>       Operation mode: all, fixed, random
      -p <arg>       How to generate prefixes: minimal, lexmin, buggy, longest
      -s <arg>       How to generate suffixes: hsi, hads, none
      -k <num>       Number of extra states to check for (minus 1)
      -l <num>       (l <= k) Redundancy free part of tests
      -r <num>       Expected length of random infix word
      -x <seed>      32 bits seeds for deterministic execution (0 is not valid)
      -e             More memory efficient
      -f <filename>  Input filename ('-' or don't specify for stdin)
      -o <filename>  Output filename ('-' or don't specify for stdout)
)";

enum Mode { ALL, FIXED, RANDOM, WSET };
enum PrefixMode { MIN, LEXMIN, BUGGY, DFS };
enum SuffixMode { HSI, HADS, NOSUFFIX };

struct main_options {
	bool help = false;
	bool version = false;

	bool skip_dup = true;

	Mode mode = ALL;
	PrefixMode prefix_mode = MIN;
	SuffixMode suffix_mode = HADS;

	unsigned long k_max = 3;      // 3 means 2 extra states
	unsigned long l = 2;          // length 0, 1 will be redundancy free
	unsigned long rnd_length = 8; // in addition to k_max
	unsigned long seed = 0;       // 0 for unset/noise

	string input_filename;  // empty for stdin
	string output_filename; // empty for stdout
};

main_options parse_options(int argc, char ** argv) {
	main_options opts;

	static const map<string, Mode> mode_names = {
	    {"all", ALL}, {"fixed", FIXED}, {"random", RANDOM}, {"wset", WSET}};
	static const map<string, PrefixMode> prefix_names = {
	    {"minimal", MIN}, {"lexmin", LEXMIN}, {"buggy", BUGGY}, {"longest", DFS}};
	static const map<string, SuffixMode> suffix_names = {
	    {"hsi", HSI}, {"hads", HADS}, {"none", NOSUFFIX}};

	try {
		int c;
		while ((c = getopt(argc, argv, "hvem:p:s:k:l:r:x:f:o:")) != -1) {
			switch (c) {
			case 'h': // show help message
				opts.help = true;
				break;
			case 'v': // show version
				opts.version = true;
				break;
			case 'm': // select operation mode
				opts.mode = mode_names.at(optarg);
				break;
			case 'p': // select prefix mode
				opts.prefix_mode = prefix_names.at(optarg);
				break;
			case 's': // select suffix mode
				opts.suffix_mode = suffix_names.at(optarg);
				break;
			case 'k': // select extra states / k-value
				opts.k_max = stoul(optarg);
				break;
			case 'l': //
				opts.l = stoul(optarg);
				break;
			case 'r': // expected random length
				opts.rnd_length = stoul(optarg);
				break;
			case 'x': // seed
				opts.seed = stoul(optarg);
				break;
			case 'e':
				opts.skip_dup = false;
				break;
			case 'f': // input filename
				opts.input_filename = optarg;
				break;
			case 'o': // output filename
				opts.output_filename = optarg;
				break;
			case ':': // some option without argument
				throw runtime_error(string("No argument given to option -") + char(optopt));
			case '?': // all unrecognised things
				throw runtime_error(string("Unrecognised option -") + char(optopt));
			}
		}
	} catch (exception & e) {
		cerr << e.what() << endl;
		cerr << "Could not parse command line options." << endl;
		cerr << "Please use -h to see the available options." << endl;
		exit(2);
	}

	opts.l = min(opts.l, opts.k_max);
	return opts;
}

using time_logger = silent_timer;

char lowercase_letters[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};

// Helper function to print the word vector
void print_word(const word & w, std::ostream & out) {
	for (const auto & input_value : w) {
		if (input_value >= 0 &&
		    input_value < sizeof(lowercase_letters) / sizeof(lowercase_letters[0]))
			out << lowercase_letters[input_value] << " ";
		else
			out << input_value << " ";
	}
}
// Function to collect all unique states in the ADS sequence
void collect_unique_states(const adaptive_distinguishing_sequence & sequence,
                           std::unordered_set<size_t> & unique_states) {
	for (const auto & pair : sequence.CI) {
		unique_states.insert(pair.second);
	}

	for (const auto & child : sequence.children) {
		collect_unique_states(child, unique_states);
	}
}
size_t get_number_of_states(const std::string & filename) {
	std::ifstream file(filename);
	if (!file.is_open()) {
		throw std::runtime_error("Unable to open file: " + filename);
	}

	std::set<std::string> states;
	std::string line;
	while (std::getline(file, line)) {
		std::istringstream iss(line);
		std::string token;
		while (iss >> token) {
			if (token.find("->") != std::string::npos) {
				// Skip the rest of the line as it's a transition
				break;
			}
			if (token != "digraph" && token != "{" && token != "}" &&
			    token != "[label=\"a / 0\"];" && token != "[label=\"a / 1\"];" &&
			    token != "[label=\"b / 0\"];" && token != "[label=\"b / 1\"];" &&
			    token != "[label=\"a / 0\"]" && token != "[label=\"a / 1\"]" &&
			    token != "[label=\"b / 0\"]" && token != "[label=\"b / 1\"]") {
				states.insert(token);
			}
		}
	}
	/*
	std::cout << "States found in the DOT file:" << std::endl;
	for (const auto & state : states) {
	    std::cout << state << std::endl;
	}
	*/
	return states.size();
}

// Function to output the contents of the adaptive_distinguishing_sequence in a tree-like format
void output_sequence(const adaptive_distinguishing_sequence & sequence, std::ostream & out,
                     const std::string & prefix = "", bool is_last = true) {
	std::string indent_str = prefix + (is_last ? "└── " : "├── ");
	out << indent_str << "Depth: " << sequence.depth << std::endl;

	indent_str = prefix + (is_last ? "    " : "│   ");
	out << indent_str << "Word: ";
	print_word(sequence.w, out);
	out << std::endl;

	out << indent_str << "CI Pairs:" << std::endl;
	for (const auto & pair : sequence.CI) {
		out << indent_str << "(" << pair.first + 1 << ", " << pair.second + 1 << ")" << std::endl;
	}

	out << indent_str << "Children:" << std::endl;
	for (size_t i = 0; i < sequence.children.size(); ++i) {
		output_sequence(sequence.children[i], out, indent_str, i == sequence.children.size() - 1);
	}
}

// Function to detect all leaf nodes and print their initial states along with the word that created
// the leaf node
void print_leaf_nodes(const adaptive_distinguishing_sequence & sequence, std::ostream & out,
                      const word & parent_word = {}) {
	word current_word = parent_word;
	current_word.insert(current_word.end(), sequence.w.begin(), sequence.w.end());

	if (sequence.children.empty()) {
		out << sequence.CI[0].second + 1 << " -> ";

		print_word(current_word, out);
		out << std::endl;
	} else {
		for (const auto & child : sequence.children) {
			print_leaf_nodes(child, out, current_word);
		}
	}
}

int main(int argc, char * argv[]) try {
	/*
	 * First we parse the command line options.
	 * We quit when asked for help or version
	 */

	const auto args = parse_options(argc, argv);

	if (args.help) {
		cout << USAGE << endl;
		exit(0);
	}

	if (args.version) {
		cout << "Version 2 (July 2017)" << endl;
		exit(0);
	}

	const bool no_suffix = args.suffix_mode == NOSUFFIX;
	const bool use_distinguishing_sequence = args.suffix_mode == HADS;

	const bool randomize_hopcroft = true;
	const bool randomize_lee_yannakakis = true;

	if (args.output_filename != "" && args.output_filename != "-") {
		throw runtime_error("File ouput is currently not supported");
	}

	/*
	 * Then all the setup is done. Parsing the automaton,
	 * construction all types of sequences needed for the
	 * test suite.
	 */
	const auto machine_and_translation = [&] {
		const auto & filename = args.input_filename;
		time_logger t_("reading file " + filename);
		if (filename == "" || filename == "-") {
			return read_mealy_from_dot(cin);
		}
		if (filename.find(".txt") != string::npos) {
			const auto m = read_mealy_from_txt(filename);
			const auto t = create_translation_for_mealy(m);
			return make_pair(move(m), move(t));
		} else if (filename.find(".dot") != string::npos) {
			return read_mealy_from_dot(filename);
		}

		clog << "warning: unrecognized file format, assuming .dot\n";
		return read_mealy_from_dot(filename);
	}();

	const auto & machine = reachable_submachine(move(machine_and_translation.first), 0);
	const auto & translation = machine_and_translation.second;

	// every thread gets its own seed
	const auto random_seeds = [&] {
		vector<uint_fast32_t> seeds(4);
		if (args.seed != 0) {
			seed_seq s{args.seed};
			s.generate(seeds.begin(), seeds.end());
		} else {
			random_device rd;
			generate(seeds.begin(), seeds.end(), ref(rd));
		}
		return seeds;
	}();

	auto all_pair_separating_sequences = [&] {
		if (no_suffix) return splitting_tree(0, 0);

		const auto splitting_tree_hopcroft = [&] {
			time_logger t("creating hopcroft splitting tree");
			return create_splitting_tree(
			    machine, randomize_hopcroft ? randomized_hopcroft_style : hopcroft_style,
			    random_seeds[0]);
		}();

		return splitting_tree_hopcroft.root;
	}();

	auto sequence = [&] {
		if (no_suffix) return adaptive_distinguishing_sequence(0, 0);

		const auto tree = [&] {
			time_logger t("Lee & Yannakakis I");
			if (use_distinguishing_sequence)
				return create_splitting_tree(machine,
				                             randomize_lee_yannakakis
				                                 ? randomized_lee_yannakakis_style
				                                 : lee_yannakakis_style,
				                             random_seeds[1]);
			else
				return result(machine.graph_size);
		}();

		const auto sequence_ = [&] {
			time_logger t("Lee & Yannakakis II");
			return create_adaptive_distinguishing_sequence(tree);
		}();

		return sequence_;
	}();

	auto transfer_sequences = [&] {
		if (args.mode == WSET) return vector<word>{};

		time_logger t("determining transfer sequences");
		switch (args.prefix_mode) {
		case LEXMIN:
			return create_transfer_sequences(canonical_transfer_sequences, machine, 0,
			                                 random_seeds[2]);
		case MIN:
			return create_transfer_sequences(minimal_transfer_sequences, machine, 0,
			                                 random_seeds[2]);
		case BUGGY:
			return create_transfer_sequences(buggy_transfer_sequences, machine, 0, random_seeds[2]);
		case DFS:
			return create_transfer_sequences(longest_transfer_sequences, machine, 0,
			                                 random_seeds[2]);
		}
	}();

	auto const inputs = create_reverse_map(translation.input_indices);

	const auto separating_family = [&] {
		if (no_suffix) {
			separating_set s{{word{}}};
			vector<separating_set> suffixes(machine.graph_size, s);
			return suffixes;
		}

		time_logger t("making seperating family");
		return create_separating_family(sequence, all_pair_separating_sequences);
	}();

	/*
	 * We will be trying to output the adaptive_distinguishing_sequence here,
	 * done: Disable all other outputs
	 * TODO: Disable no suffix mode to force adaptive_distinguishing_sequence creation
	 */
	size_t total_number_of_states = get_number_of_states(args.input_filename) - 1;
	std::unordered_set<size_t> unique_states;
	collect_unique_states(sequence, unique_states);
	std::cout << machine.graph_size << total_number_of_states << "DUYGU" << endl;

	if (unique_states.size() == total_number_of_states) {
		std::ofstream tree_file("../tree_output.txt");
		if (tree_file.is_open()) {
			output_sequence(sequence, tree_file);
			tree_file.close();
		}

		// Output leaf nodes to a file
		std::ofstream leaf_file("../ads_sequence.txt");
		if (leaf_file.is_open()) {
			print_leaf_nodes(sequence, leaf_file);
			leaf_file.close();
		}
	} else {
		std::cerr << "ADS sequence does not cover all states. Skipping write to ads_sequence.txt."
		          << std::endl;
	}

	output_sequence(sequence, std::cout);
	print_leaf_nodes(sequence, std::cout);

	/*
	 * From here on, we will be spamming the output with test cases.
	 * Depending on the operation mode, this will be either a finite
	 * or infinite test suite.
	 */
	const bool fixed_part = args.mode == ALL || args.mode == FIXED;
	const bool random_part = args.mode == ALL || args.mode == RANDOM;

	// we will remove redundancies using a radix tree/prefix tree/trie
	trie<input> test_suite;
	word buffer;
	const auto output_word = [&inputs](const auto & w) {
		// for (const auto & x : w) {
		// 	cout << inputs[x] << ' ';
		// }
		// cout << endl;
	};

	if (args.mode == WSET) {
		for (const auto & wp : separating_family) {
			for (const auto & w : wp.local_suffixes) {
				test_suite.insert(w);
			}
		}
		// test_suite.for_each(output_word);

		return 0;
	}

	if (fixed_part) {
		// For the exhaustive/preset part we first collect all words
		// (while removing redundant ones) before outputting them.
		time_logger t("outputting all preset tests");

		vector<word> mid_sequences(1);
		test(machine, transfer_sequences, mid_sequences, separating_family, args.l + 1,
		     {[&buffer](auto const & w) { buffer.insert(buffer.end(), w.begin(), w.end()); },
		      [&buffer, &test_suite]() {
			      test_suite.insert(buffer);
			      buffer.clear();
			      return true;
		      }});

		auto first_suite = flatten(test_suite);
		mt19937 g;
		shuffle(first_suite.begin(), first_suite.end(), g);
		for (auto const & w : first_suite) output_word(w);
		first_suite.clear();

		test(machine, transfer_sequences, mid_sequences, separating_family, args.k_max - args.l,
		     {[&buffer](auto const & w) { buffer.insert(buffer.end(), w.begin(), w.end()); },
		      [&buffer, &test_suite, &output_word, &args]() {
			      if (!args.skip_dup || test_suite.insert(buffer)) {
				      output_word(buffer);
			      }
			      buffer.clear();
			      return bool(cout);
		      }});
	}

	if (random_part) {
		// For the random part we immediately output new words, since
		// there is no way of collecting an infinite set first...
		// Note that this part terminates when the stream is closed.
		time_logger t("outputting all random tests");
		const auto k_max_ = fixed_part ? args.k_max + 1 : 0;

		randomized_test(
		    machine, transfer_sequences, separating_family, k_max_, args.rnd_length,
		    {[&buffer](auto const & w) { buffer.insert(buffer.end(), w.begin(), w.end()); },
		     [&buffer, &test_suite, &output_word, &args]() {
			     // TODO: probably we want to bound the size of the prefix tree
			     if (!args.skip_dup || test_suite.insert(buffer)) {
				     output_word(buffer);
			     }
			     buffer.clear();
			     return bool(cout);
		     }},
		    random_seeds[3]);
	}

} catch (exception const & e) {
	cerr << "Exception thrown: " << e.what() << endl;
	return 1;
}