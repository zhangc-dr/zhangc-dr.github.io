$1. DQN: {a_{t + 1}} = \mathop {\arg \max }\limits_{{a_{t + 1}}} {Q_{tar}}\left( {{s_{t + 1}},{a_{t + 1}}} \right),
MSE = {\left| {\gamma \left( {{r_t} + {Q_{tar}}\left( {{s_{t + 1}},{a_{t + 1}}} \right)} \right) - {Q_{eval}}\left( {{s_t},{a_t}} \right)} \right|^2}$.

$2. DDQN: {a_{t + 1}} = \mathop {\arg \max }\limits_{{a_{t + 1}}} {Q_{eval}}\left( {{s_{t + 1}},{a_{t + 1}}} \right),
MSE = {\left| {\gamma \left( {{r_t} + {Q_{tar}}\left( {{s_{t + 1}},{a_{t + 1}}} \right)} \right) - {Q_{eval}}\left( {{s_t},{a_t}} \right)} \right|^2}$.
