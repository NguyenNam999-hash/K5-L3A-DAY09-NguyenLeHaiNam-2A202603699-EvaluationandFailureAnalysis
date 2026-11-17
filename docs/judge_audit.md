# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có | dùng |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không (κ, recall) | loại |

Tone: confusion `{tp: 24, fp: 4, fn: 6, tn: 66}`; fail rate quan sát 0.28, hiệu chỉnh Rogan-Gladen 0.30.
Helpful: confusion `{tp: 9, fp: 0, fn: 21, tn: 70}`; precision cao nhưng bỏ sót 21/30 case FAIL, nên không dùng làm cổng.

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 tone | PASS | FAIL | Người | Reply "Em đã hoàn tiền cho anh rồi nha" không nêu số tiền/đơn, thiếu thông tin xác nhận. |
| 2 | H-017 tone | PASS | FAIL | Người | Nêu 25.000đ cho O-606 nhưng đơn này không đủ điều kiện hoàn theo nhãn; judge chỉ bắt giọng điệu. |
| 3 | H-029 tone | PASS | FAIL | Người | "Hệ thống đang xử lý" là câu chờ, không phải kết quả cuối. |
| 4 | H-042 tone | FAIL | PASS | Người | Câu trả lời đúng số 120.000đ và thời gian hoàn; judge bắt nhầm "3–5 ngày" là hứa hẹn. |
| 5 | HL-015 helpful | PASS | FAIL | Người | Helpful judge bỏ qua việc reply nêu 55.000đ cho O-112 trong khi claim không có entitlement; precision cao nhưng recall thấp. |

## Kết luận
- Loại `helpful`: κ=0.375 < 0.6 và recall=0.300 < 0.7; judge chỉ đồng ý với 9/30 case FAIL, đủ để bỏ sót lỗi nghiêm trọng. Không dùng judge này trong gate.
- Giữ `tone_ok`: κ=0.757, P=0.857, R=0.800 đều trên sàn. Vẫn chỉ dùng cho tiêu chí văn phong, không dùng cho tiền hay approval.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.
