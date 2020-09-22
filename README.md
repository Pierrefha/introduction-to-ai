# introduction-to-ai
This repo contains the practical assignments we had to do for the introduction to ai 1 lecture.
We covered a lot of theoretical ground and on some topics we had to hand out an assignment. The lecture followed the book "Artificial Intelligence: A Modern Approach" by Sturart J. Russell and Peter Norvig.
The book can currently be found as download in a github repo dedicated to ai ressources [here.](https://github.com/yanshengjia/ml-road)

### Structure
In each directory there is one folder containing the base code we were given and a description of the tasks.
The assignment folder contains my solution. So if you want to try something yourself, you can do so.

### Coding style
Sadly the base codes have never seen any style guides whatsoever. This was the first semester in which we were using python due to the high demands (we were told before it was done in lua) so I guess there we have a reason and big room for improvement.
For P1 I did not follow any style guide. I had more than enough trouble learning python while coding the assignment.
For P2 and P3 I used the flake8 linter for vim which does combine [pep8](https://www.python.org/dev/peps/pep-0008/) and [pyflakes.](https://pypi.org/project/pyflakes/)
P2 and P3 contain a unittest.py file. I did somewhat try out TDD(Test Driven Development) and had fun doing so. Unit testing and code style is something we rarely learn or talk about but should be encouraged in more lectures in my opionion.

### Subjects
#### P1
This assignment contains my first few ever written lines of python. After coding three assignments I can somewhat understand why it is so popular.
Since ai is all about search we had to implement some search algorithms.
##### First implementation: uninformed search
For the first part we had to code the basic uninformed search algorithm dfs, bfs,ucs.
##### Second implementation: informed search, A*
For the second part we had to code the A* algorithm to find an optional solution in a grid environment. For the grid environment the heuristics of choice was the euclidian distance / SLD(Straight Line Distance). A* is basicly informed search combined with a priority queue in which the lowest SLD is the prioritization criteria. Combined with a data structure to store the already visited nodes to avoid unnecessary iterations. After adding a new node we check if it enabled a shortest path to any node and replace the node and node cost respectively.

#### P2
This practical was about possible implementations for the [eight queens puzzle.](https://en.wikipedia.org/wiki/Eight_queens_puzzle)
#### First implementation: genetic algorithm
Implementing the genetic algorithm was a lot of fun and I was somewhat fascinated that by simply somewhat mimicing nature we can solve problems. Sadly It was not faster than the backtracking search. But there are a lot of tweaks one can adapt to improve this and finally get better results.
#### Second implementation: backtracking
Just use basic backtracking to find all possible solutions (not only the first one).

#### P3
This practical was about using knowledge based agents to solve the [wumpus world.](https://www.javatpoint.com/the-wumpus-world-in-artificial-intelligence)
A knowledge based agent does have an ask and tell interface with which he can 1) ask -> infer a solution based on current knowledge && 2) tell -> add knowledge to our knowledge base. We used propositional logic for this, which is basicly a simple subset of FOL(first-order logic). Leaving functions, variables, quantifiers out and only using 0-ary predicates (A,-A,B...) and the typical logical operators or, not and and.
##### First implementation: Resolution
For resolution we use sentences in CNF. Using resolution one can not proof that a certain sentence is satisfiable, only that a sentence is unsatisfiable by deducting the empty clause. As usual in ai we use a simple trick and just negate our query. By proving that our negated query deducts to the empty clause, we therefore prove that our original query is entailed by our knowledge base. (Some rules to enhance deduction is always pick one sentence which is a child of our query and one sentence that is a child of our knowledge. Since combining only our knowledge will not lead to new entailments.)
#### Second implementation: Forward-Chaining
For forward chaining we use horn clauses (clauses with at most one positive literal). These consist of the premise(first part) and the conclusion(second part).
example: A,B,C=>D where premise-> A,B,C and conclusion-> D
The forward-chaining algorithm basicly randomly picks facts from our knowledge base (stored in our agenda) and checks if these facts occur in our premise. As soon as every literal of our premise is satisfied, the conclusion holds and then will be added into our list of facts(agenda). If we somewhen find that our popped fact equals the query, we have succesfully deducted the query. If we pop every fact from our agenda without ever finding a solution, our knowledge does not infer the given query.

#### P4
P4 would have been about planning. Due to the corona situation we have missed some weeks and did not come to implement this. If I remember correctly we would have implemented graph planning algorithm for a certain problem given in PDDL(Problem Description Domain Language). PDDL is a simply parseable language that consists of two big parts. The domain describing the situation (variables, which actions we can take and their preconditions,results) and the problem (with an init state and a goal).
