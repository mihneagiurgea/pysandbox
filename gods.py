# encoding: utf-8
# working at 10:05, pretty code at 10:25 :)
from collections import namedtuple

###
# Printing
###
from pprint import pprint

# type: GameState is just tuple(str...)
def pprint_state(state):
	if len(state) == 0:
		return "ø"
	else:
		return "{%s}" % ", ".join(state)

class Solution(object):

	def __init__(self, current_state, q=None, answer_to_solution=None, score=None):
		self.current_state = current_state
		self.q = q
		self.answer_to_solution = answer_to_solution
		self.score = score

	def __repr__(self):
		return self.pprint("")

	def pprint(self, indent):
		state_str = pprint_state(self.current_state)
		if not self.q:
			return "%s<Solution %s/>" % (indent, state_str, )

		q = "Ask God#%d: \"Are we in one of: %s?\"" % (self.q.god, pprint_state(self.q.q))
		s = "%s<Solution %s in %d Q(s)>\n%s%s" % (indent, state_str, self.score, indent, q)
		for k, v in self.answer_to_solution.iteritems():
			if not v.q:
				s += "\n%sIf %3s: %s" % (indent, k, v.pprint(""))
			else:
				s += "\n%sIf %3s:\n%s" % (indent, k, v.pprint(indent+"\t"))
		s += "\n%s</Solution>" % (indent, )
		return s


###
# GameSolver & Solution
###
class GameSolver(object):
	# Will find the solution with the minimal score, ordered by questions.

	def __init__(self, rules):
		self.rules = rules
		self.cache = {}

	def solve(self, state):
		# type: (GameState) -> Solution
		if state not in self.cache:
			self.cache[state] = self._solve(state)
		return self.cache[state]

	def _solve(self, state):
		if self.rules.is_terminal(state):
			return Solution(state, score=0)

		best_solution = None
		for question in self.rules.get_questions(state):
			solution = self._solve_for_q(state, question)
			if solution:
				if best_solution is None or solution.score < best_solution.score:
					best_solution = solution

		return best_solution

	def _solve_for_q(self, state, question):
		answer_to_solution = {}
		for answer, next_state in self.rules.get_answers(state, question).iteritems():
			if next_state == state:
				# This can happen, e.g. if you ask something to God that you know
				# is certainly random.
				solution = None
			else:
				solution = self.solve(next_state)
			if not solution:
				return None
			answer_to_solution[answer] = solution

		# Found a winnable state.
		score = self.rules.calc_score(answer_to_solution)
		return Solution(state, question, answer_to_solution, score=score)

###
# Game rules & logic
###
Question = namedtuple("Question", ["god", "q"])
GODS = (0, 1, 2)
ANSWERS = ("yes", "no")

class GameRules(object):

	@classmethod
	def get_init_state(cls):
		# type: () -> GameState
		return tuple(["TFR", "TRF", "FTR", "FRT", "RTF", "RFT"])

	@classmethod
	def is_terminal(cls, state):
		# type: (GameState) -> bool
		return len(state) <= 1

	@classmethod
	def get_questions(cls, state):
		# type: (GameState) -> List[Question]
		questions = []
		for subset in all_subsets(state):
			for god in GODS:
				questions.append(Question(god, subset))
		return questions

	@classmethod
	def get_answers(cls, state, question):
		# type: (GameState, Question) -> Dict[str, GameState]
		# If the current state is in the set of states posed in the question,
		# then we should expect a "Yes".
		yes = []
		for assig in state:
			expected_answer = assig in question.q
			if cls._is_valid(assig, question.god, expected_answer):
				yes.append(assig)
		no = []
		for assig in state:
			expected_answer = assig in question.q
			if cls._is_valid(assig, question.god, not expected_answer):
				no.append(assig)

		return {
			"yes": tuple(yes),
			"no": tuple(no),
		}

	@classmethod
	def _is_valid(cls, assig, idx, answered_truthfully):
		if answered_truthfully:
			# Then the God that answered cannot be "False" God.
			return assig[idx] != "F"
		else:
			# Otherwise, it cannot be "True" God.
			return assig[idx] != "T"

	@classmethod
	def calc_score(cls, answer_to_solution):
		assert answer_to_solution
		max_score = -1
		for answer, solution in answer_to_solution.iteritems():
			max_score = max(max_score, solution.score)
		return max_score + 1

###
# Utils
###
import itertools

def all_subsets(iterable):
	subsets = []
	for i in xrange(1, len(iterable)):
		subsets.extend(itertools.combinations(iterable, i))
	subsets.append(())
	subsets.append(iterable)
	return subsets

if __name__ == "__main__":
	solver = GameSolver(GameRules)
	state = GameRules.get_init_state()
	print repr(solver.solve(state))

	# q = Question(0, ('TFR', 'TRF'))
	# print "%r on\n\t\t %r" % (q, state, )
	# for k, v in GameRules.get_answers(state, q).items():
	# 	print "\t%3s: %r" % (k, v)

	# print GameRules.get_questions(state)
	# print GameRules.get_answers(state, q)

	# state = ('FTR', 'FRT')
	# print "===%s===" % (state, )
	# # print GameRules.get_questions(state)
	# q = Question(0, ('FTR', ))
	# print q
	# print GameRules.get_answers(state, q)









