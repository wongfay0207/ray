import unittest

import ray
import ray.rllib.agents.ppo as ppo
from ray.rllib.utils.framework import try_import_tf
from ray.rllib.utils.test_utils import framework_iterator, check_compute_action

tf = try_import_tf()


class TestDDPPO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ray.init()

    @classmethod
    def tearDownClass(cls):
        ray.shutdown()

    def test_ddppo_compilation(self):
        """Test whether a DDPPOTrainer can be built with both frameworks."""
        config = ppo.ddppo.DEFAULT_CONFIG.copy()
        config["num_gpus_per_worker"] = 0
        num_iterations = 2

        for _ in framework_iterator(config, "torch"):
            trainer = ppo.ddppo.DDPPOTrainer(config=config, env="CartPole-v0")
            for i in range(num_iterations):
                trainer.train()
            check_compute_action(trainer)


if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))
