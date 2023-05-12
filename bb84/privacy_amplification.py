import numpy as np

from UniversalHashing import TwoUniversalHash

weak_shared_secret = np.array([0, 1, 0])
alice_seed = 11
uh = TwoUniversalHash(3, 2, 0.75, alice_seed)
alice_shared_secret = uh.hash(weak_shared_secret)

bob_seed = alice_seed
uh = TwoUniversalHash(3, 2, 0.75, bob_seed)
bob_shared_secret = uh.hash(weak_shared_secret)

print(alice_shared_secret)
print(bob_shared_secret)
