import play_connect4
import train_3dc4_v1

# Initialize environment
env = play_connect4.Connect4()

# Initialize agent
agent = train_3dc4_v1.DQNAgent(state_size=64, action_size=16, hidden_size=32, learning_rate=0.001, discount_rate=0.99, exploration_rate=1.0, batch_size=32)

# Train agent
for episode in range(1000):
    state, player = env.InitializeBoard()
    #print(state)
    done = False
    while not done:
        action = agent.act(state)
        #next_state, reward, done = env.step(action)
        next_state, reward = env.DropPiece(env.board, action, env.player)
        reward *= -1
        done = env.CheckWin(env.board, env.player)
        if not done :
            done = env.CheckTie(env.board)
        #next_state, reward, done = env.DropPiece(env.board, action ,env.player)
        agent.remember(state, action, reward, next_state, done)
        agent.replay()
        state = next_state
        env.SetPlayer(env.player)
    env.PrintBoard(env.board)
    agent.decay_exploration_rate(episode)

# Play against agent
state = env.InitializeBoard()
done = False
while not done:
    action = agent.act(state)
    next_state, reward, done = env.step(action)
    state = next_state
    env.print_board()
    if done:
        if reward == 1:
            print("You won!")
        elif reward == -1:
            print("You lost!")
        else:
            print("It's a tie!")
