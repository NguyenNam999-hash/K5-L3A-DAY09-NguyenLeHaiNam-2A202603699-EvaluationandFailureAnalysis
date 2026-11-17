# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
python -m lab9.trace_case --shape fixed --claim C-002 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-002@11`, run ID `E-seeded_regression-20261117-5ca9` |
| Triệu chứng | Lab 8 grader fail: `status resolved != denied`; ledger ghi 20.000 cho O-202 trong khi label yêu cầu 0. |
| Bước sai đầu tiên | Event 3 `model_override {"delay_days": 5}`: agent thay `delay_days=2` của DB bằng 5 ngày trong ticket. |
| Vì sao là bước *đầu tiên* | Event 1–2 chỉ handoff và `lookup_order` trả đúng order DB (`delay_days=2`); sai bắt đầu ở event 3, trước quote và refund. |
| Failure mode | `FM-03 ticket_trust` (`docs/failure_taxonomy.md`) |
| Đối chứng | `fixed C-002@11`: không có event `model_override`; event 3 quote `amount_vnd: 0`, kết quả `denied`. |
| Regression test | `tests/test_lab9_graders.py::test_override_event_breaks_db_fact` (`DbFactKept`) và `tests/test_lab9_graders.py::test_clean_trial_passes_everything`; gate v1 chặn `seeded_regression` ở `pass_rate`. |
| Chưa chắc chắn | Trace chứng minh agent đã ghi override, nhưng không chứng minh lý do nội tại vì MockLLM seed quyết định nhánh; không suy ra được model thật sẽ làm vậy. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
