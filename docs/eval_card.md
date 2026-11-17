# Eval card — LogiX-VN refund agent

Card này đi kèm mỗi báo cáo và được dùng lại ở Day 10.

- **Run ID / eval set SHA:** v1 `E-swarm-20261117-5ca9` / `5ca993db660d` · v2 `E-swarm-20261117-3233` / `32336b281c57`
- **Phiên bản:** code `starter/d09` · eval set v1 (sha `5ca993db660d`) và v2 (sha `32336b281c57`) · metric_spec 1.0/2.0 · grader `lab9.graders` · seeds 11/22/33/44/55
- **Eval set:** v1 14 item × 5 seed = 70 trial, nguồn `lab8_public`; v2 28 item × 5 seed = 140 trial, thêm 14 item adversarial. Nhãn: `labels_v1.json` / `labels_v2.json`.
- **Metric & ngưỡng:** xem `config/metric_spec.yaml` (v1) và `config/metric_spec_v2.yaml` (v2).

## Baseline vs PR (v1)

| Metric | Ngưỡng | Baseline swarm | PR `fixed` | Δ CI 95% | Kết luận |
|---|---|---|---|---|---|
| approval_bypass | max 0 | 0 | 0 | — | ok |
| secret_leak | max 0 | 0 | 0 | — | ok |
| db_fact_kept | ≥ 0.95 | 0.9857 | 1.0 | — | ok |
| refund_amount_correct | ≥ 0.95, no drop | 0.9857 | 1.0 | +0.014 [0.000, +0.043] | ok |
| pass_rate | ≥ 0.85, no drop | 0.9857 | 1.0 | +0.014 [0.000, +0.043] | ok |
| reply_amount_correct (FM-08) | ≥ 0.95, no drop | 1.0 | 1.0 | 0.000 [0.000, 0.000] | ok |
| pass_5 | ≥ 0.80 | 0.9286 | 1.0 | — | ok (không chặn) |
| cost_per_success | +10% max | 49.567 | 48.7157 | — | ok (không chặn) |

`seeded_regression` bị chặn: `exit 1 — blocked: refund_amount_correct, pass_rate, reply_amount_correct` (pass_rate 0.7143, CI [-0.500, -0.057]).

## v2 — slice, pass^k, adversarial

| Hạng mục | Giá trị baseline v2 | Ngưỡng | Ghi chú |
|---|---|---|---|
| pass_rate | 0.9786 | ≥ 0.85 | |
| pass_hat_5 | 0.8929 | ≥ 0.85 | A/A seed 66/77/88/99/110 cũng 0.8929; sàn 0.85 nằm ngoài dải nhiễu quan sát |
| pass_at_5 | 1.0 | theo dõi | |
| money_movement slice | 1.0 | ≥ 0.90, no drop | bắt `slice_regression` (C-014/C-105/C-106 seed lẻ) |
| adversarial slice | 1.0 | ≥ 0.85, no drop | 14 item adversarial |
| reply_amount_correct | 1.0 | ≥ 0.95, no drop | FM-08 |

Scorecard: 3/3 regression bị chặn, 0 báo nhầm; `honest_refactor` và `fixed` merge. `lab9.traps` chặn toàn bộ 4 trap công khai.

## Judge

`tone_ok` κ=0.757, P=0.857, R=0.800 → dùng. `helpful` κ=0.375, P=1.000, R=0.300 → loại vì recall dưới sàn; xem `docs/judge_audit.md`.

## Trace case

`docs/trace_case.md`: `seeded_regression C-002@11`, event 3 `model_override {"delay_days": 5}`, FM-03; regression test `DbFactKept` + gate `pass_rate`.

## Gate owner

Eval owner giữ gate; gate exit 1 thì không merge, người mở PR sửa regression hoặc xin waiver có ghi lý do.

## Phạm vi pilot

Claim hoàn phí ship/hàng hỏng một đơn, principal sở hữu đơn, approval theo claim; ngoài phạm vi: tranh chấp pháp lý, đơn đa quốc gia, hoàn tiền thủ công ngoài host.

## Giới hạn / bằng chứng còn thiếu

- MockLLM, 14 item v1 / 28 item v2; CI rộng, chỉ bắt regression lớn.
- Judge replay trên CSV công khai, chưa có held-out mới.
- Bug chỉ xuất hiện 1/3 seed (`rare`) không phát hiện ổn định với 5 seed; `flaky_regression` 1/5 seed bắt được nhờ `pass_hat_5`, nhưng không suy rộng cho mẫu nhỏ hơn.
- Không đo trên người dùng thật.

## Khi nào tăng eval-set version

Thêm item từ trace case hoặc đổi nhãn → tăng `eval_set_version`, chạy lại baseline. Đổi ngưỡng/metric → tăng `metric_spec_version` và ghi lý do.
