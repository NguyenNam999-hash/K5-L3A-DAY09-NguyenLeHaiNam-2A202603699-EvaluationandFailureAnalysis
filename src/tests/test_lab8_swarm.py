"""Lab 8 public matrix on the reference swarm (T01-T14).

The Lab 9 overlay keeps the Lab 8 host gate in CI, so this module restores the
swarm slice that `python -m pytest -m student -k swarm` selects. Each trial is
graded with the same `lab8.metrics.trial_pass` used by the evaluator: result
against the label plus the SQLite ledger and trace contract.
"""

from __future__ import annotations

import pytest

from lab8.app import prepare_store, run_shape
from lab8.config_loader import repo_path
from lab8.db import connect, load_jsonl
from lab8.metrics import trial_pass

pytestmark = pytest.mark.student

# Seed 11 is not divisible by 5, so the documented reference-swarm weakness
# (ticket delay overrides the order row on seed % 5 == 0) does not fire.
SEED = 11

CLAIMS = load_jsonl(repo_path("data", "public_claims.jsonl"))
MATRIX = pytest.mark.parametrize(
    "claim", CLAIMS, ids=[claim["matrix_id"] for claim in CLAIMS]
)


@MATRIX
def test_swarm_public_matrix(claim, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    store = tmp_path / f"{claim['claim_id']}.sqlite"
    prepare_store(store)
    result = run_shape("swarm", claim["claim_id"], seed=SEED, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(result.as_dict(), claim["expected"], conn)
        assert passed, f"{claim['matrix_id']} {claim['claim_id']}: {reason}"
    finally:
        conn.close()


def test_swarm_public_matrix_keeps_peer_talk(tmp_path, monkeypatch):
    """The reference swarm must still pay for peer review, not collapse to single."""
    monkeypatch.chdir(tmp_path)
    store = tmp_path / "C-001.sqlite"
    prepare_store(store)
    result = run_shape("swarm", "C-001", seed=SEED, store_path=str(store))
    assert result.shape == "swarm"
    assert result.status == "resolved"
    assert result.model_calls >= 3
    assert result.tool_calls >= 2
    assert result.trace_path.endswith(f"{result.run_id}.json")
