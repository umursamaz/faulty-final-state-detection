def write_result(file_path, num_states, correct_fsm_seed, faulty_fsm_seed, is_singleton, singleton_iter, suspected_states, applied_input):
    with open(file_path, 'w') as f:
        f.write("num_states, fsm_seed, faulty_seed\n")
        f.write(f"{num_states}, {correct_fsm_seed}, {faulty_fsm_seed}\n")
        f.write("is_singleton, singleton_iter\n")
        f.write(f"{is_singleton}, {singleton_iter}\n")
        f.write("suspected_states\n")
        f.write(",".join(map(str, suspected_states)) + "\n")
        f.write("applied_input\n")
        if is_singleton:
          f.write(",".join(applied_input) + "\n")

    