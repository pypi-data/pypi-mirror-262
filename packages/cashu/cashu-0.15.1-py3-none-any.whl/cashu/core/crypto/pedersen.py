from typing import Callable, List

from secp import PrivateKey, PublicKey
from sigma import challenge, prove, verify


def pedersen_map(xs: List[PrivateKey], Gs: List[PublicKey]) -> List[PublicKey]:
    """Pedersen commitment: P = \sum{x_i*G_i}{i=1}^n
    For example: # PoK(a, b): x_1*G_1 + x_2*G_2 = P where x_1 is the value commitment and x_2 is the blinding factor
    """
    assert len(xs) == len(Gs)
    sum = Gs[0] * xs[0]
    for i in range(1, len(xs)):
        sum = sum + Gs[i] * xs[i]
    return [sum]


def prove_knowledge_and_eq_of_message_in_pedersen_commitments(
    xs: List[PrivateKey], Gs: List[PublicKey]
) -> List[PublicKey]:
    """Pedersen commitment: # PoK(a, b, d): P1 = a*G1 + b*H1, P2 = a*G2 + d*H2, where a is the message and b and d are blinding factors"""
    assert len(Gs) == 4
    assert len(xs) == 3, f"len(xs)={len(xs)} != 3"
    P1 = Gs[0] * xs[0] + Gs[1] * xs[1]  # a*G1 + b*H1
    P2 = Gs[2] * xs[0] + Gs[3] * xs[2]  # c*G2 + d*H2 where c == a
    return [P1, P2]


# proof of knowledge of opening of Pedersen commitment
N = 2
# base points (agreed upon by the prover and the verifier)
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
# hidden values of the commitment
xs = [PrivateKey() for _ in range(N)]
print(
    "Prover: want to hide opening x0 and x1 of commitment Ps and prove that I know them"
)
print(
    f"Opening: xs: {', '.join([f'x{i}='+x.private_key.hex() for i, x in enumerate(xs)])}"
)
# commitment to the hidden values
Ps = pedersen_map(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))
# proof
Ts, ss = prove(pedersen_map, xs, Gs)
# verification
if verify(pedersen_map, Gs, Ps, Ts, ss):
    print("Verifier: Success ✅")
else:
    print("Verifier: Failure ❌")


print("------")
# proof of knowledge of message of two Pedersen commitments
N = 4
# base points (agreed upon by the prover and the verifier)
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
# first one is the message and the two others are the blinding factors
xs = [PrivateKey() for _ in range(N - 1)]

print(
    "Prover: want to hide message x0 in Ps[0] and x0 in Ps[1] and prove that they are the same"
)
print(
    f"Opening: xs: {', '.join([f'x{i}='+x.private_key.hex() for i, x in enumerate(xs)])}"
)
# commitment to the hidden values
Ps = prove_knowledge_and_eq_of_message_in_pedersen_commitments(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))
# proof
Ts, ss = prove(prove_knowledge_and_eq_of_message_in_pedersen_commitments, xs, Gs)
# verification
if verify(prove_knowledge_and_eq_of_message_in_pedersen_commitments, Gs, Ps, Ts, ss):
    print("Verifier: Success")
else:
    print("Verifier: Failure ❌")

print("------")
# test case: prover does not know the opening of the commitment
N = 4
# base points (agreed upon by the prover and the verifier)
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
# first one is the message and the two others are the blinding factors, the last one is the message
# but the last message is not the same as the first one
xs = [PrivateKey() for _ in range(N)]

print(
    "Prover: want to hide message x0 in Ps[0] and x3 in Ps[1] and prove that they are the same, but x0 != x3"
)
print(
    f"Opening: xs: {', '.join([f'x{i}='+x.private_key.hex() for i, x in enumerate(xs)])}"
)


def prove_knowledge_and_eq_of_message_in_pedersen_commitments_broken(
    xs: List[PrivateKey], Gs: List[PublicKey]
) -> List[PublicKey]:
    """Pedersen commitment: # PoK(a, b, d): a*G1 + b*H1 = c*G2 + d*H2, where a, c are the messages and b and d are blinding factors"""
    assert len(Gs) == 4
    assert len(xs) == 4
    assert xs[0] != xs[3]  # this is the broken part
    P1 = Gs[0] * xs[0] + Gs[1] * xs[1]  # a*G1 + b*H1
    P2 = Gs[2] * xs[3] + Gs[3] * xs[2]  # c*G2 + d*H2 where c != a
    return [P1, P2]


# commitment to the hidden values
Ps = prove_knowledge_and_eq_of_message_in_pedersen_commitments_broken(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))
# proof
Ts, ss = prove(prove_knowledge_and_eq_of_message_in_pedersen_commitments, xs[:3], Gs)
# verification
if verify(prove_knowledge_and_eq_of_message_in_pedersen_commitments, Gs, Ps, Ts, ss):
    print("Verifier: Success ❌")
else:
    print("Verifier: Failure ✅")

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


Ps = prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))


Ts, ss = prove(
    prove_knowledge_and_eq_of_message_in_pedersen_commitments_with_nullifier,
    xs,
    Gs,
)

# verification


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


print("------ Balance proof ------")
# proof of knowledge of message of two Pedersen commitments where the difference between them is a constant (balance proof)
N = 2
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
amount_1 = 400
amount_2 = 200
null = 1
print(f"Ampint 1: {amount_1}, Amount 2: {amount_2}")
difference = amount_1 - amount_2
print(f"Difference: {difference}")
xs = [
    PrivateKey(amount_1.to_bytes(32, "big")),
    PrivateKey(),
    PrivateKey(),
    PrivateKey((amount_2.to_bytes(32, "big"))),
]
# set the blinding factor of the null commitment to xs[1] + xs[2]
xs.append(xs[1] + xs[2])  # xs[4]

assert Gs[1] * (xs[1] + xs[2]) == Gs[1] * xs[4]
print(f"xs[1] + xs[3] = {(xs[1] + xs[3]).private_key.hex()}")
# assert xs[2].private_key == PrivateKey((null.to_bytes(32, "big"))).private_key
# print(
#     f"Amount commitment difference: {(Gs[0] * xs[0] - Gs[0] * xs[3]).serialize().hex()} (or {(Gs[0] * difference).serialize().hex()})"
# )
print(
    f"Opening: xs: {', '.join([f'x{i}='+x.private_key.hex() for i, x in enumerate(xs)])}"
)


def prove_knowledge_and_balance(
    xs: List[PrivateKey], Gs: List[PublicKey]
) -> List[PublicKey]:
    """
    Prove that the difference between the amount commitments is a constant d.

    We have two amount commitments: P1 and P2, and the commitment to the difference P3.
    We demand that the difference in the blinding factors of P1 and P2 is zero. Then, P3 = d*G.
    We publish the commitments P1, P2, P3, and the difference d.

    PoK(a, b, h_1, h_2, h_3):
    P1 = a*G + h_1*H + h_2*H and
    P2 = b*G + h_3*H2 and
    P3 = (a - b)*G and
    h_1 + h_2 = h_3
    """
    assert len(Gs) == 2
    assert len(xs) == 5
    # amount commitment (xs[0] = amount_1) + null commitment with blinding factor xs[2]
    P1 = Gs[0] * xs[0] + Gs[1] * xs[1] + Gs[1] * xs[2]
    # amount commitment (xs[3] = amount_2)
    P2 = Gs[0] * xs[3] + Gs[1] * xs[4]
    # balance proof Gs[1] * (xs[1] + x2[3] - xs[4]) == 0 -> P3 = Gs[0] * (xs[0] - xs[3])
    P3 = (P1 - P2) + Gs[
        0
    ] * difference  # should be zero (check this?) # if you don't set r's so that their sum is zero, there would be Gs[1] * delta_r here
    return [P1, P2, P3]


Ps = prove_knowledge_and_balance(xs, Gs)
print("Prover: Commitment Ps: ", ", ".join([P.serialize().hex() for P in Ps]))

Ts, ss = prove(prove_knowledge_and_balance, xs, Gs)


# verification
def verify_with_balance(
    f: Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]],
    Gs: List[PublicKey],
    Ps: List[PublicKey],
    Ts: List[PublicKey],
    ss: List[PrivateKey],
    difference: int,
) -> bool:
    c = challenge(Ts)
    t = [Ps[i] * c + Ts[i] for i in range(len(Ps))]
    return t == f(ss, Gs)


print(f"Verifier: proving with difference {difference}")
if verify_with_balance(prove_knowledge_and_balance, Gs, Ps, Ts, ss, difference):
    print("Verifier: Success ✅")
else:
    print("Verifier: Failure ❌")

difference += 1
print(f"Verifier: proving with difference {difference}")
if verify_with_balance(prove_knowledge_and_balance, Gs, Ps, Ts, ss, difference):
    print("Verifier: Success ❌")
else:
    print("Verifier: Failure ✅")


print("----- Range proof -----")
# prove that a value is in a given range by proving that it can be represented as 256 bits
# range proof
N = 256
Gs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]
Hs = [PrivateKey().pubkey or PublicKey() for _ in range(N)]

amount = 100
xs = [PrivateKey() for _ in range(N)]
rs = [PrivateKey() for _ in range(N)]


def bit_decomposition(a: int, n: int) -> List[int]:
    """Decompose 'a' into a list of bits."""
    return [(a >> i) & 1 for i in range(n)]


print(f"Amount: {amount}, Bit decomposition: {bit_decomposition(amount, N)}")


def create_bit_commitment(
    a_bits: List[int],
    Gs: List[PublicKey],
    Hs: List[PublicKey],
    xs: List[PrivateKey],
    rs: List[PrivateKey],
) -> List[PublicKey]:
    """Create a bit commitment.
    Different notation than before:
        Gs are base points for bit commitments, Hs are base points for the blinding factors.
        xs are the bit commitments, rs are the blinding factors.
    """
    Ps = []
    assert len(Gs) == len(Hs) == len(xs) == len(rs) == len(a_bits)
    for i, bit in enumerate(a_bits):
        print(
            f"bit: {bit}, Gs[i]: {Gs[i].serialize().hex()}, Hs[i]: {Hs[i].serialize().hex()} "
        )
        if bit:
            Ps.append(Gs[i] * bit + Hs[i] * rs[i])
        else:
            Ps.append(Hs[i] * rs[i])
    return Ps


Ts, ss = prove(create_bit_commitment, bit_decomposition(amount, N), Gs, Hs, xs, rs)
