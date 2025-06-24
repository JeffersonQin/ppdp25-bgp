import maude


class CheckRepetitionHook(maude.Hook):
    def to_list(self, term: str):
        if term == "nilPL":
            return []
        ret = term.split(" :: ")
        for i in range(len(ret)):
            # remove trailing and ending spaces/brackets
            ret[i] = ret[i].strip()
            if ret[i].startswith("("):
                ret[i] = ret[i][1:-1]
        return ret


    def _is_repetition(self, sub: list, full: list):
        if not sub:
            return True
        if not full:
            return True
        if len(full) % len(sub) != 0:
            return False
        repeat_count = len(full) // len(sub)
        return sub * repeat_count == full


    def is_valid_dp(self, q: list, p: list, c: list, r: list, rp: list, rs: list):
        return q[-len(rp):] == rp and self._is_repetition(r, q[:-len(rp)]) \
            and self._is_repetition(r, c) \
            and p[:len(rs)] == rs and p[-len(rp):] == rp and self._is_repetition(r, p[len(rs):-len(rp)]) \
            and len(p) >= len(c)


    def is_dp(self, q: list, p: list, c: list):
        n = len(c)
        Rs = []

        for size in range(1, n // 2 + 1):
            if n % size == 0:
                r = c[:size]
                if r * (n // size) == c:
                    Rs.append(r)
        Rs.append(c)
        
        for r in Rs:
            for i in range(len(r) + 1):
                rp = r[:i]
                rs = r[i:]
                if self.is_valid_dp(q, p, c, r, rp, rs):
                    return True

        return False


    def run(self, term, data):
        module = term.symbol().getModule()
        args = term.arguments()
        queue = next(args)
        production = next(args)
        consumption = next(args)

        q_list = self.to_list(str(queue))
        p_list = self.to_list(str(production))
        c_list = self.to_list(str(consumption))

        if self.is_dp(q_list, p_list, c_list):
            return module.parseTerm("true")
        else:
            return module.parseTerm("false")
