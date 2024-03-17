from gymnasium.envs.registration import register

register(
    id='RROEnv-v0',
    entry_point='rro_env.env:DockerYardEnv',
)