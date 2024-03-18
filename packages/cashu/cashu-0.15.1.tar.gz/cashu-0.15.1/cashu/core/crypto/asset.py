from typing import Callable, List

from b_dhke import step1_alice, step2_bob, step3_alice
from b_dhke import verify as verify_b_dhke
from secp import PrivateKey, PublicKey
from sigma import challenge, prove


# commitment to the hidden and the nullifier values
def prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier(
    xs: List[PrivateKey], Gs: List[PublicKey]
) -> List[PublicKey]:
    """Pedersen commitment: # PoK(a, b, d): P1 = a*G1 + h1*H1 + s1*S1, P2 = a*G2 + h2*H2 + s2*S2, where a is the message and b and d are blinding factors
    and s is the nullifier"""
    assert len(Gs) == 6
    assert len(xs) == 6
    P1 = Gs[0] * xs[0] + Gs[1] * xs[1] + Gs[2] * xs[2]  # a*G1 + h1*H1 + s1*S1
    P2 = Gs[3] * xs[0] + Gs[4] * xs[4] + Gs[5] * xs[5]  # a*G2 + h2*H2 + s2*S2
    P3 = Gs[2] * xs[2]  # commitment to the nullifier
    return [P1, P2, P3]


def verify_with_nullifier(
    f: Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]],
    Gs: List[PublicKey],
    Ps: List[PublicKey],
    Ts: List[PublicKey],
    ss: List[PrivateKey],
    nullifier: PrivateKey,
) -> bool:
    # set the nullifier
    Ps[2] = Gs[2] * nullifier
    c = challenge(Ts)
    t = [Ps[i] * c + Ts[i] for i in range(len(Ps))]
    return t == f(ss, Gs)


print("------ Nullifier ------")
# proof of knowledge of message of two Pedersen commitments with nullifier
N = 6
# base points (agreed upon by the prover and the verifier)
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
# the third one is the nullifier
xs = [PrivateKey() for _ in range(N)]
nullifier = xs[2]
print(
    f"Opening: xs: {', '.join([f'x{i}='+x.private_key.hex() for i, x in enumerate(xs)])}"
)
print(f"Nullifier: {nullifier.private_key.hex()}")

# mix with ecash
# mint keys
a = PrivateKey()
A = a.pubkey
assert A


secret = "secret_message"
B_, r = step1_alice(secret)
C_, e, s = step2_bob(B_, a)
C = step3_alice(C_, r, A)
if verify_b_dhke(a, C, secret):
    print("Ecash Success ✅")
else:
    print("Ecash Failure ❌")

Ps = prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))
Ts, ss = prove(
    prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier,
    xs,
    Gs,
)

# verification
print(f"Verifier: proving with correct nullifier {nullifier.private_key.hex()}")
if verify_with_nullifier(
    prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier,
    Gs,
    Ps,
    Ts,
    ss,
    nullifier,
):
    print("Verifier: Success ✅")
else:
    print("Verifier: Failure ❌")

nullifier = PrivateKey()
print(f"Verifier: proving with wrong nullifier {nullifier.private_key.hex()}")
if verify_with_nullifier(
    prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier,
    Gs,
    Ps,
    Ts,
    ss,
    nullifier,
):
    print("Verifier: Success ❌")
else:
    print("Verifier: Failure ✅")
