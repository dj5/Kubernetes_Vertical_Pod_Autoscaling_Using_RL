import tensorflow as tf
import numpy as np
import kubernetes.client
from kubernetes.client.rest import ApiException
from getlimit import get_limits
import time
from cpumemory import metricsCpu
from performAction import perform_action
import pandas as pd
import time
import os
dir_path="/home/enduser/rl/weights"
print(get_limits(),metricsCpu())


# Define the environment
class KubernetesEnvironment:
    def __init__(self):
        # Initialize the Kubernetes API client
        # self.k8s_client = kubernetes.client.ApiClient()
        
        # # Define the resource to scale
        # self.resource_name = 'cpu'
        
        # # Define the Kubernetes deployment name
        # self.deployment_name = 'my-deployment'
        
        # # Define the Kubernetes namespace
        # self.namespace = 'my-namespace'
        
        # Get the current resource utilization
        self.state = self.get_state()
        
    def get_state(self):
        try:
            # Get the Kubernetes deployment object
            
            # Get the current replica coun
            cpu= get_limits()[0]
            memory=get_limits()[1]
            cpuact=metricsCpu()[0]
            memact=metricsCpu()[1]
            df=pd.read_csv("pods.csv")#pd.DataFrame(columns=['CPU'])
            
            
            # Get the current resource utilization
            
                
            utilization = cpuact/cpu
            df.loc[len(df.index)]=[str(utilization),time.ctime()]
            df.to_csv("pods.csv",index=False)
            
            return np.array([ utilization])
        
        except ApiException as e:
            print("Exception when calling AppsV1Api->read_namespaced_deployment: %s\n" % e)
        
    def step(self, action):
        try:
            # Scale the deployment based on the action
            #replicas = max(1, int(self.state[0] + action))
            perform_action(action)
            # deployment = self.k8s_client\
            #     .call_api('/apis/apps/v1/namespaces/{}/deployments/{}'.format(self.namespace, self.deployment_name),
            #               'PATCH',
            #               body={'spec': {'replicas': replicas}},
            #               response_type='V1Deployment')
            
            # Get the new resource utilization
            #wait for pod to start 
            time.sleep(15)
            print("sleep")
            utilization = self.get_state()
            
            # Compute the reward

            # reward = 1.0 - utilization
            
            if utilization>0.1 and utilization<0.6:
                # If both CPU and memory utilization are above the threshold, the agent gets a positive reward
                reward = 1
            else: # utilization>0.6:
                # If both CPU and memory utilization are below the threshold, the agent gets a negative reward
                reward = -1
            #else:
                # If only one of the utilization metrics is above the threshold, the agent gets a small positive reward
                #reward = 0.3

            
            # Update the state
            self.state = np.array([utilization])
            
            return self.state, reward
        
        except ApiException as e:
            print("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)

# Define the agent
class KubernetesAgent:
    def __init__(self, env):
        self.env = env
        self.q_network = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(1,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        self.q_network.compile(optimizer='adam', loss='mse')
        if len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])>0:
          self.q_network.load_weights(dir_path+"/cp.ckpt")          
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(0, 2)
        else:
            print(np.array([state]).shape)
            return np.argmax(self.q_network.predict(np.array([state]).reshape((1,1)))[0])
        
    def train(self, batch_size=16, gamma=0.99):
        # Get a batch of transitions from the environment
        batch_states = []
        batch_targets = []
        for i in range(batch_size):
            state = self.env.state
            action = self.act(state)
            next_state, reward = self.env.step(action)
            print("reward ", reward,i)
            df_r= pd.read_csv("reward.csv")
            df_r.loc[len(df_r.index)]=[reward,time.ctime()]
            df_r.to_csv("reward.csv",index=False)
            print("metrics",metricsCpu()[0])
            df_a= pd.read_csv("action.csv")
            df_a.loc[len(df_r.index)]=[action,time.ctime()]
            df_a.to_csv("action.csv",index=False)
            
            # Compute the target value
            if next_state[0] == 1:
                target = reward
            else:
                print(next_state)
                print(np.array([next_state]).shape)
                next_q_value = np.max(self.q_network.predict(np.array([next_state]).reshape((1,1)))[0])
                target = reward + gamma * next_q_value
            
            # Add the transition to the batch
            batch_states.append(state)
            batch_targets.append([target])
            
        print(np.array(batch_states).shape,np.array(batch_states), 'train')
        # Update the Q network
        checkpoint_path = "/home/enduser/weights/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                 save_weights_only=True,
                                                 verbose=1)
        history=self.q_network.fit(np.array(batch_states).reshape((16,1)), np.array(batch_targets), epochs=1, verbose=0,callbacks=[cp_callback])
        print("Loss: ",history.history['loss'])
        # self.q_network.save("/home/enduser/rl/weights/rl_weights")        
        # Decay the exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
# Define the environment and agent
env = KubernetesEnvironment()
agent = KubernetesAgent(env)

# Train the agent
#try:
for episode in range(100):
    state = env.state
    total_reward = 0.0
    for step in range(100):
        action = agent.act(state)
        next_state, reward = env.step(action)
        total_reward += reward
        print("Total Reward: ", total_reward)
        agent.train()
        if next_state[0] == 1:
            break
        state = next_state
    print('Episode {}: Total reward = {}'.format(episode + 1, total_reward))
#except:
 #pass
