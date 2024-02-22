
import numpy as np

# Parâmetros do gerenciamento de estoque
max_stock = 100
max_order = 50
demand_per_day = [10, 20, 30, 40, 50]  # Exemplo de demanda diária
price_per_item = 10  # Lucro por item vendido

# Parâmetros do Q-learning
alpha = 0.1  # Taxa de aprendizado
gamma = 0.9  # Fator de desconto
epsilon = 0.1  # Probabilidade de escolha aleatória (exploração)
num_episodes = 1000  # Número de episódios de treinamento
max_steps_per_episode = 100  # Limite de passos por episódio

# Classe para o ambiente de gerenciamento de estoque
class StockEnv:
    def __init__(self, max_stock, max_order, demand_per_day):
        self.max_stock = max_stock
        self.max_order = max_order
        self.demand_per_day = demand_per_day
        self.state = 0

    def step(self, action):
        order = min(action, self.max_stock - self.state)
        self.state += order
        demand = np.random.choice(self.demand_per_day)
        sales = min(self.state, demand)
        reward = sales * price_per_item
        self.state -= sales
        if demand > sales:
            reward -= (demand - sales) * 15
        if self.state > 0:
            reward -= self.state * 2
        done = False
        return self.state, reward, done, {}

    def reset(self):
        self.state = 0
        return self.state

# Inicialização do ambiente e da Q-table
env = StockEnv(max_stock, max_order, demand_per_day)
Q_table = np.zeros((max_stock + 1, max_order + 1))

# Função para escolher a próxima ação
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        action = np.random.randint(0, max_order + 1)
    else:
        action = np.argmax(Q_table[state])
    return action

# Treinamento do agente
for episode in range(num_episodes):
    state = env.reset()
    for step in range(max_steps_per_episode):
        action = choose_action(state)
        new_state, reward, done, _ = env.step(action)

        # Atualização da Q-table
        Q_table[state, action] = Q_table[state, action] + alpha * (reward + gamma * np.max(Q_table[new_state]) - Q_table[state, action])
        state = new_state

# O Q-table agora possui os valores de Q para cada par de estado-ação,
# que podem ser usados para tomar decisões de estoque após o treinamento.

def simulate(env, Q_table, num_days):
    total_reward = 0  # Total de recompensas acumuladas
    state = env.reset()  # Começamos com o estoque vazio

    for day in range(num_days):
        action = np.argmax(Q_table[state])  # Escolha a ação com o maior valor Q para o estado atual
        new_state, reward, done, _ = env.step(action)  # Execute a ação

        print(f"Day {day+1}: State {state}, Action {action}, Reward {reward}, New State {new_state}")
        
        total_reward += reward
        state = new_state  # Atualize o estado

    print(f"Total reward after {num_days} days: {total_reward}")

# Simule o ambiente por um determinado número de dias usando o agente treinado
num_days_to_simulate = 3000  # Número de dias para simular
simulate(env, Q_table, num_days_to_simulate)

