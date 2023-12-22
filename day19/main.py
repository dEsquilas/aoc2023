MORE_THAN = 1
LESS_THAN = 2
GO_TO = 3

class Rule:
    def __init__(self, data):

        self.oper = 0
        self.destination = ""
        self.variable_value = 0
        self.variable_name = ""

        if ">" in data:
            self.oper = MORE_THAN
            self.variable_value = int(data.split(">")[1].split(":")[0])
            self.variable_name = data.split(">")[0]
            self.destination = data.split(">")[1].split(":")[1]
        elif "<" in data:
            self.oper = LESS_THAN
            self.variable_value = int(data.split("<")[1].split(":")[0])
            self.variable_name = data.split("<")[0]
            self.destination = data.split("<")[1].split(":")[1]
        else:
            self.oper = GO_TO
            self.destination = data
            self.variable_name = None

    def print(self):
        if self.oper == MORE_THAN:
            print(self.variable_name, " > ", self.variable_value, " destination ", self.destination)
        elif self.oper == LESS_THAN:
            print(self.variable_name, " < ", self.variable_value, " destination ", self.destination)
        else:
            print("Go to ", self.destination)

    def apply(self, variables_group):

        if self.variable_name == None:
            return self.destination

        for v in variables_group:
            if v.name == self.variable_name:
                if self.oper == GO_TO:
                    return self.destination
                if self.oper == MORE_THAN:
                    if v.value > self.variable_value:
                        return self.destination
                if self.oper == LESS_THAN:
                    if v.value < self.variable_value:
                        return self.destination

        return None


class Workflow:
    def __init__(self, data):
        self.rules = []

        tmp = data.split(",")

        for t in tmp:
            self.rules.append(Rule(t))

    def apply(self, variable_group):
        for r in self.rules:
            ret = r.apply(variable_group)
            if ret is not None:
                return ret

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = int(value)


def apply_workflow(workflows, workflow_name, variables):

    ret = workflows[workflow_name].apply(variables)
    if ret == "A":
        return True
    if ret == "R":
        return False

    return apply_workflow(workflows, ret, variables)

def day_19(filename):

    with open(filename) as file:
        data = file.read().split("\n\n")

    p1 = 0
    p2 = 0

    tmp_workflow = data[0].split("\n")
    workflows = {}
    for wf  in tmp_workflow:
        wf = wf.replace("}", "")
        tmp = wf.split("{")
        workflows[tmp[0]] = Workflow(tmp[1])

    tmp_variables = data[1].split("\n")
    variables_groups = []
    for v in tmp_variables:
        group = []
        aux = v.replace("}", "").replace("{", "").split(",")
        for a in aux:
            tmp = a.split("=")
            group.append(Variable(tmp[0], tmp[1]))
        variables_groups.append(group)

    # part 1

    for group in variables_groups:
        if apply_workflow(workflows, "in", group):
            for v in group:
                p1 += v.value


    # part 2
    ranges = {
        "x": [1, 4000],
        "a": [1, 4000],
        "s": [1, 4000],
        "m": [1, 4000],
    }

    out_ranges = apply_ranges(workflows, "in", ranges)

    for rg in out_ranges:
        c = 1
        for k,v in rg.items():
            c *= v[1] - v[0] + 1
        p2 += c



    return p1,p2


def apply_ranges(workflows, workflow_name, current_range):

    out_ranges = []
    cwf = workflows[workflow_name]

    # just modify the current range for apply the rules

    for rule in cwf.rules:
        # check if interval is in rules
        if rule.oper == GO_TO:
            if rule.destination == "A":
                out_ranges.append(current_range)
            elif rule.destination == "R":
                pass
            else:
                out_ranges += apply_ranges(workflows, rule.destination, current_range)
        else:
            min_range = current_range[rule.variable_name][0]
            max_range = current_range[rule.variable_name][1]
            if rule.oper == LESS_THAN:
                if max_range < rule.variable_value:
                    if rule.destination == "A":
                        out_ranges.append(current_range)
                    elif rule.destination == "R":
                        pass
                    else:
                        out_ranges += apply_ranges(workflows, rule.destination, current_range)
                else:
                    if min_range >= rule.variable_value:
                        # nothing to do, just go to the next rule
                        pass
                    if min_range < rule.variable_value:
                        # variable shuld generate 2 ranges
                        subrange1 = current_range.copy()
                        subrange2 = current_range.copy()

                        subrange1[rule.variable_name] = [current_range[rule.variable_name][0], rule.variable_value - 1]
                        subrange2[rule.variable_name] = [rule.variable_value, current_range[rule.variable_name][1]]

                        if rule.destination == "A":
                            out_ranges.append(subrange1)
                        elif rule.destination == "R":
                            pass
                        else:
                            out_ranges += apply_ranges(workflows, rule.destination, subrange1) # the first part, should be parsed
                        current_range = subrange2 # the second parte should be checked with the rest of the rules

            if rule.oper == MORE_THAN:
                if min_range > rule.variable_value:
                    if rule.destination == "A":
                        out_ranges.append(current_range)
                    elif rule.destination == "R":
                        pass
                    else:
                        out_ranges += apply_ranges(workflows, rule.destination, current_range)
                else:
                    if max_range <= rule.variable_value:
                        # nothing to do, just go to the next rule
                        pass
                    if max_range > rule.variable_value:
                        # variable shuld generate 2 ranges
                        subrange1 = current_range.copy()
                        subrange2 = current_range.copy()

                        subrange1[rule.variable_name] = [current_range[rule.variable_name][0], rule.variable_value]
                        subrange2[rule.variable_name] = [rule.variable_value + 1, current_range[rule.variable_name][1]]

                        if rule.destination == "A":
                            out_ranges.append(subrange2)
                        elif rule.destination == "R":
                            pass
                        else:
                            out_ranges += apply_ranges(workflows, rule.destination, subrange2)
                        current_range = subrange1 # the first part should be checked with the rest of the rules

    return out_ranges

def test_day_19():
    assert day_19("test.txt") == (19114, 167409079868000)

test_day_19()
p1, p2 = day_19("input.txt")
print("Part 1: ", p1)
print("Part 2: ", p2)