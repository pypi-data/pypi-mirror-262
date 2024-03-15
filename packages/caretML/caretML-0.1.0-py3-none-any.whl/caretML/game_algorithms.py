def monte_carlo_tree_search(root_state, num_simulations=1000, exploration_constant=1.4):
    """
    Perform Monte Carlo Tree Search (MCTS) for game tree exploration.

    Parameters:
        root_state (object): Initial state of the game tree.
        num_simulations (int): Number of simulations to run.
        exploration_constant (float): Exploration constant for UCB1 algorithm.

    Returns:
        object: Best action to take based on MCTS.
    """
    class Node:
        def __init__(self, state):
            self.state = state
            self.children = []
            self.visits = 0
            self.total_score = 0

    def select(node):
        while node.children:
            node = max(node.children, key=lambda x: x.total_score / x.visits + exploration_constant * np.sqrt(np.log(node.visits) / x.visits))
        return node

    def expand(node):
        actions = node.state.get_legal_actions()
        for action in actions:
            child_state = node.state.take_action(action)
            child_node = Node(child_state)
            node.children.append(child_node)

    def simulate(node):
        return node.state.simulate()

    def backpropagate(node, score):
        while node:
            node.visits += 1
            node.total_score += score
            node = node.parent

    root_node = Node(root_state)
    for _ in range(num_simulations):
        selected_node = select(root_node)
        expand(selected_node)
        if selected_node.children:
            selected_child = np.random.choice(selected_node.children)
            score = simulate(selected_child)
            backpropagate(selected_child, score)
        else:
            score = simulate(selected_node)
            backpropagate(selected_node, score)

    best_action = max(root_node.children, key=lambda x: x.visits).state.get_best_action()
    return best_action
