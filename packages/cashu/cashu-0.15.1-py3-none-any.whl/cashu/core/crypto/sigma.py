import hashlib
from typing import Callable, List, Tuple

from secp import PrivateKey, PublicKey


def prove(
    f: Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]],
    xs: List[PrivateKey],
    Gs: List[PublicKey],
) -> Tuple[List[PublicKey], List[PrivateKey]]:
    """General sigma protocol prover

    Args:
        f (Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]]): The function to prove
        xs (List[PrivateKey]): List of private keys
        Gs (List[PublicKey]): List of base points

    Returns:
        Tuple[List[PublicKey], List[PrivateKey]]: The commitments to f(rs, Gs) and the responses to the challenge
    """
    rs = [PrivateKey() for _ in xs]
    T = f(rs, Gs)
    c = challenge(T)
    s: List[PrivateKey] = [rs[i] + xs[i] * c for i in range(len(xs))]
    return T, s


def verify(
    f: Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]],
    Gs: List[PublicKey],
    Ps: List[PublicKey],
    Ts: List[PublicKey],
    ss: List[PrivateKey],
) -> bool:
    """General sigma protocol verifier

    Args:
        f (Callable[[List[PrivateKey], List[PublicKey]], List[PublicKey]]): The function to prove
        Gs (List[PublicKey]): The base points
        Ps (List[PublicKey]): The commitments to f(xs, Gs)
        Ts (List[PublicKey]): The commitments to f(rs, Gs)
        ss (List[PrivateKey]): The responses to the challenge

    Returns:
        bool: True if the proof is valid
    """
    c = challenge(Ts)
    t = [Ps[i] * c + Ts[i] for i in range(len(Ps))]
    return t == f(ss, Gs)


def challenge(Gs: List[PublicKey]) -> bytes:
    """Challenge function: c = H(G1 || G2 || ... || Gn)

    Args:
        Gs (List[PublicKey]): List of public keys to hash

    Returns:
        bytes: The challenge
    """
    return hashlib.sha256(b"".join([G.serialize() for G in Gs])).digest()
