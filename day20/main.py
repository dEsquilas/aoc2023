import math

def day_20(filename, test=False):

    with open(filename) as file:
        data = file.read().splitlines()

    # part 1 setup

    modules = {}
    modules_memories = {}

    for module in data:
        aux = module.split(" -> ")
        if "%" in aux[0] or "&" in aux[0]:
            type = aux[0][0]
            name = aux[0][1:]
        else:
            type = "broadcaster"
            name = aux[0]
        destinations = aux[1].split(", ")
        # type, destinations, current_status
        modules[name] = [type, destinations, 0]

    for module_name, module in modules.items():
        if module[0] == "&":
            modules_memories[module_name] = {}

    for module_memory_name, module in modules_memories.items():
        for module_name, module_data in modules.items():
            for d in module_data[1]:
                if module_memory_name == d:
                    modules_memories[module_memory_name][module_name] = 0

    low_sended = 0
    high_sended = 0

    # part 2 setup

    to_find = "rx"
    behind = None

    for module_name, module in modules.items():
        for d in module[1]:
            if d == to_find:
                behind = module_name
                break
        if behind != None:
            break

    if (behind == None or modules[behind][0] != "&") and not test:
        print("FATAL ERROR")
        exit()

    # supose that the signals are cyclic
    # get the input that need to be up

    p2_prevs = []
    for module_name, module in modules.items():
        for d in module[1]:
            if d == behind:
                p2_prevs.append(module_name)

    p2_found = {}
    for p2_prev in p2_prevs:
        p2_found[p2_prev] = False

    #end setup

    cycle = 0
    p1 = 0
    p2 = 0

    while True:

        cycle += 1

        if cycle == 1001:
            p1 = low_sended * high_sended
            if test:
                 break

        Q = [("broadcaster", 0, 0)]
        low_sended += 1

        if p2 != 0 and not test:
            break

        while Q:
            current_order = Q.pop(0)

            if not test and cycle > 1000:
                all_found = True
                for prev in p2_prevs:
                    if modules[prev][2] == 0 and p2_found[prev] == False:
                        p2_found[prev] = cycle
                for prev in p2_prevs:
                    if p2_found[prev] == False:
                        all_found = False
                        break
                if all_found:
                    to_lcm = []
                    for prev in p2_prevs:
                        to_lcm.append(p2_found[prev])
                    p2 = lcm(to_lcm)
                    break

            module_name = current_order[0]
            if module_name not in modules:
                continue
            recieved_signal = current_order[1]
            signal_comes_from = current_order[2]
            module_type = modules[module_name][0]
            module_destinations = modules[module_name][1]
            module_current_signal = modules[module_name][2]


            if module_type == "broadcaster":
                signal_to_send = recieved_signal
                for d in module_destinations:
                    Q.append((d, signal_to_send, module_name))
                    if signal_to_send == 1:
                        high_sended += 1
                    else:
                        low_sended += 1

            elif module_type == "%":
                if module_current_signal == 0:
                    signal_to_send = 1
                else:
                    signal_to_send = 0
                if recieved_signal == 1:
                    pass
                else:
                    modules[module_name][2] = signal_to_send
                    for d in module_destinations:
                        Q.append((d, signal_to_send, module_name))
                        if signal_to_send == 1:
                            high_sended += 1
                        else:
                            low_sended += 1

            elif module_type == "&":
                modules[module_name][2] = recieved_signal
                modules_memories[module_name][signal_comes_from] = recieved_signal
                all_high = True
                current_memories = modules_memories[module_name]

                for k,v in current_memories.items():
                    if v == 0:
                        all_high = False
                        break

                if all_high:
                    signal_to_send = 0
                else:
                    signal_to_send = 1

                for d in module_destinations:
                    Q.append((d, signal_to_send, module_name))
                    if signal_to_send == 1:
                        high_sended += 1
                    else:
                        low_sended += 1

    return p1,p2

def lcm(xs):
    res = 1
    for x in xs:
        res = (res*x) // math.gcd(x,res)
    return res

def test_day_20():
    assert day_20("test.txt", True)[0] == 32000000

test_day_20()
p1, p2 = day_20("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)