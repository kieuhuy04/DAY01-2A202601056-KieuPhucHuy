# K4 — Ngày 1: Bài Tập & Phản Ánh
## Khám Phá LLM API | Phiếu Thực Hành

**Thời lượng:** 14h00–18h00
**Cách làm:** Trả lời từng câu ngay sau khi hoàn thành block tương ứng —
đừng để dồn hết về cuối buổi. Thay dòng `*Câu trả lời của bạn*` bằng câu
trả lời thật (chấm tự động sẽ đếm số câu đã trả lời).

---

## Block 1 — API Cơ Bản (trả lời sau Checkpoint 1)

### Câu 1.1 — Độ nhạy của temperature
Gọi `call_openai` với temperature 0.0, 0.7, 1.2 và 1.8 dùng prompt
**"Hãy kể cho tôi một sự thật thú vị về Hà Nội."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi? Ở mức nào phản hồi bắt đầu
kém mạch lạc?** (2–3 câu)
> Ở temperature 0.0, model luôn trả về gần như cùng một câu trả lời, ngắn
> gọn và an toàn gần như không có yếu tố sáng tạo. Ở 0.7, câu chữ đã
> đa dạng hơn nhưng vẫn mạch lạc và đúng trọng tâm. Ở 1.2, phản hồi bắt đầu
> dài dòng hơn, thêm chi tiết hoặc góc nhìn bất ngờ nhưng vẫn còn hiểu được.
> Đến 1.8, câu trả lời bắt đầu lan man, đôi khi lặp từ hoặc chêm thông tin
> không liên quan — đây là mức bắt đầu kém mạch lạc rõ rệt.

### Câu 1.2 — Chọn temperature cho sản phẩm
**Bạn sẽ đặt temperature bao nhiêu cho trợ lý soạn thảo hợp đồng pháp lý,
và bao nhiêu cho trợ lý viết slogan quảng cáo? Giải thích khác biệt.**
> Trợ lý soạn hợp đồng pháp lý: temperature thấp (0.0–0.2). Văn bản pháp lý
> cần tính chính xác, nhất quán và có thể tái tạo lại y hệt mỗi lần chạy —
> không được phép "sáng tạo" thêm điều khoản hay diễn đạt mơ hồ. Trợ lý viết
> slogan quảng cáo: temperature cao (0.8–1.2). Ở đây giá trị nằm ở sự mới lạ,
> bất ngờ và đa dạng cách diễn đạt, nên chấp nhận đánh đổi một phần tính nhất
> quán để đổi lấy sáng tạo.

### Câu 1.3 — Đánh đổi chi phí
Kịch bản: 20.000 người dùng hoạt động mỗi ngày, mỗi người gọi API 2 lần,
mỗi lần trung bình ~500 token đầu ra.

**Ước tính chi phí mỗi ngày của model lớn so với model nhỏ cho workload này
(dựa trên bảng giá trong template). Nêu một trường hợp model lớn xứng đáng
với chi phí và một trường hợp model nhỏ là lựa chọn đúng:**
> Tổng lượt gọi/ngày = 20.000 người × 2 lượt = 40.000 lượt, mỗi lượt ~500
> token đầu ra → 40.000 × 500 = 20.000.000 token = 20.000 nghìn-token/ngày.
> Với giá output trong `PRICING_PER_1K_TOKENS`: GPT-4o (0.010 USD/1K) →
> 20.000 × 0.010 = **200 USD/ngày**; GPT-4o-mini (0.0006 USD/1K) →
> 20.000 × 0.0006 = **12 USD/ngày** — chênh nhau khoảng 16–17 lần (chưa tính
> chi phí input). Model lớn xứng đáng khi cần suy luận phức tạp hoặc độ
> chính xác cao rủi ro cao (ví dụ tư vấn y tế, phân tích hợp đồng) — sai sót
> của model nhỏ ở đây tốn kém hơn nhiều so với chênh lệch giá API. Model nhỏ
> là lựa chọn đúng cho tác vụ đơn giản, khối lượng lớn (trả lời FAQ, phân
> loại ý định) nơi chi phí và độ trễ quan trọng hơn phần chất lượng tăng
> thêm biên của model lớn.

---

## Block 2 — System Prompt & Token (trả lời sau Checkpoint 2)

### Câu 2.1 — Sức mạnh của persona
Gọi `chat_with_system_prompt` hai lần với cùng câu hỏi
**"Giải thích máy học (machine learning) là gì?"** nhưng hai system prompt
khác nhau:
- "Bạn là một nhà thơ, trả lời mọi thứ bằng hình ảnh ví von, tránh thuật ngữ."
- "Bạn là kỹ sư phần mềm senior, trả lời chính xác, có ví dụ code khi phù hợp."

**Hai phản hồi khác nhau như thế nào (giọng văn, độ dài, mức kỹ thuật)?
Từ đó rút ra system prompt điều khiển được những khía cạnh nào của phản hồi?**
(3–4 câu)
> Với persona "nhà thơ", phản hồi dùng nhiều hình ảnh ẩn dụ (ví dụ ví machine
> learning như "dạy một đứa trẻ nhận biết thế giới qua vô số ví dụ"), tránh
> hẳn thuật ngữ kỹ thuật, câu văn giàu cảm xúc và dài dòng hơn. Với persona
> "kỹ sư senior", phản hồi đi thẳng vào định nghĩa chính xác, có thể kèm ví
> dụ code hoặc quy trình huấn luyện cụ thể, ngắn gọn và cấu trúc rõ ràng hơn.
> Từ đó rút ra: system prompt điều khiển được giọng văn, mức độ kỹ thuật,
> định dạng trình bày (văn xuôi vs. có cấu trúc/code) và độ dài — nhưng
> không đảm bảo thay đổi tính đúng đắn của nội dung cốt lõi.

### Câu 2.2 — tiktoken vs đếm từ
Chọn một đoạn văn tiếng Việt ~150 từ. So sánh số token theo `count_tokens`
(tiktoken) với ước lượng `số từ / 0.75` mà Part 1 đã dùng.

**Hai con số chênh nhau bao nhiêu phần trăm? Nếu dùng ước lượng thô để dự
toán ngân sách API cho ứng dụng tiếng Việt, bạn sẽ dự toán thiếu hay thừa —
và vì sao?**
> Thử với đoạn văn tiếng Việt ~186 từ (chủ đề Hà Nội): `count_tokens` (tiktoken
> thật, encoding `o200k_base`) đếm được **260 token**, trong khi ước lượng
> thô "số từ / 0.75" cho ra **248 token** — chênh khoảng **4.8%**, tiktoken
> luôn đếm nhiều hơn. Nếu dùng ước lượng thô để dự toán ngân sách cho ứng
> dụng tiếng Việt, bạn sẽ **dự toán thiếu** (underestimate), vì công thức
> "0.75 từ ≈ 1 token" được hiệu chỉnh theo tiếng Anh — tiếng Việt có dấu và
> nhiều âm tiết đơn thường bị BPE tách thành nhiều token hơn một từ tiếng
> Anh tương đương, nên số token thật luôn cao hơn ước lượng dựa trên số từ.

---

## Block 3 — Streaming & Độ Bền (trả lời sau Checkpoint 3)

### Câu 3.1 — Trải nghiệm người dùng với streaming
**Xét ba ứng dụng: (a) chatbot văn bản, (b) trợ lý giọng nói đọc to phản hồi,
(c) pipeline dịch tài liệu chạy ngầm ban đêm. Ứng dụng nào hưởng lợi nhiều
nhất từ streaming, ứng dụng nào không cần — và tại sao?** (1 đoạn văn)
> Chatbot văn bản (a) hưởng lợi nhiều nhất từ streaming vì người dùng đang
> nhìn màn hình chờ trực tiếp — thấy chữ xuất hiện ngay giảm cảm giác chờ
> đợi (perceived latency) dù tổng thời gian xử lý không đổi, và người dùng
> có thể bắt đầu đọc/hiểu ý trước khi model sinh xong toàn bộ câu trả lời.
> Trợ lý giọng nói (b) hưởng lợi ở mức trung bình: chỉ có tác dụng thực sự
> nếu bộ tổng hợp giọng nói (TTS) cũng đọc theo từng chunk văn bản đến, nếu
> không thì vẫn phải đợi đủ câu mới phát âm được. Pipeline dịch tài liệu
> chạy ngầm ban đêm (c) hầu như không cần streaming, vì không có người theo
> dõi thời gian thực — chỉ kết quả cuối cùng mới quan trọng, nên streaming
> chỉ thêm độ phức tạp mà không mang lại lợi ích UX nào.

### Câu 3.2 — Vì sao backoff theo cấp số nhân?
**Khi API quá tải và hàng nghìn client cùng retry, exponential backoff giúp
gì so với delay cố định? Tra cứu thêm: kỹ thuật "jitter" (thêm độ trễ ngẫu
nhiên) giải quyết vấn đề gì còn sót lại?**
> Với delay cố định, tất cả client thất bại cùng lúc sẽ retry lại đúng sau
> cùng một khoảng thời gian, liên tục dội vào server đang quá tải theo chu
> kỳ đều đặn — khiến server không bao giờ kịp hồi phục. Exponential backoff
> giãn cách các lần retry ngày càng xa nhau (0.1s → 0.2s → 0.4s...), giảm
> dần áp lực lên server theo thời gian, cho nó cơ hội xử lý hết hàng đợi.
> Tuy nhiên nếu hàng nghìn client đều bắt đầu thất bại cùng một thời điểm và
> dùng chung công thức backoff, chúng vẫn đồng bộ retry cùng lúc ở mỗi bước
> (vấn đề "thundering herd"). Jitter — thêm một khoảng trễ ngẫu nhiên vào
> mỗi lần chờ — phá vỡ sự đồng bộ đó, rải các lần retry ra ngẫu nhiên theo
> thời gian thay vì dồn thành một đợt tấn công đồng loạt.

---

## Block 4 — Mini-Project (trả lời sau Checkpoint 4)

### Câu 4.1 — Thiết kế persona
**Viết lại system prompt bạn dùng cho trợ lý của mình. Chỉ ra 2 chỗ trong
prompt mà nếu xóa đi, hành vi trợ lý sẽ thay đổi rõ rệt — và mô tả thay đổi
đó:**
> Persona đã dùng: "Bạn là trợ giảng thân thiện của khóa AI, trả lời ngắn
> gọn bằng tiếng Việt, và đưa ví dụ cụ thể khi giải thích khái niệm kỹ
> thuật." Hai chỗ quan trọng nếu xóa:
> 1. **"trả lời ngắn gọn"** — nếu xóa, trợ lý có xu hướng trả lời dài dòng,
>    giải thích lan man thay vì đi thẳng vào trọng tâm.
> 2. **"đưa ví dụ cụ thể khi giải thích khái niệm kỹ thuật"** — nếu xóa,
>    trợ lý sẽ chỉ giải thích khái niệm một cách trừu tượng, không minh họa
>    bằng ví dụ thực tế, khiến người mới học khó hình dung hơn.

### Câu 4.2 — Hạn chế & cải thiện
**Trợ lý của bạn giữ history 4 lượt cuối. Hãy mô tả một tình huống hội thoại
cụ thể mà giới hạn này khiến trợ lý trả lời sai/mất ngữ cảnh, và đề xuất một
cách khắc phục (ví dụ: tóm tắt các lượt cũ, tăng giới hạn có chọn lọc...):**
> Tình huống: ở lượt 1, người dùng nói "Mình tên An, đang học về mạng
> nơ-ron." Sau đó họ hỏi thêm 5 câu không liên quan (về Python, về Docker,
> về thống kê...). Đến lượt 7, người dùng hỏi "Bạn có nhớ tên mình và mình
> đang học gì không?" — vì history chỉ giữ 4 lượt cuối (8 message), thông
> tin ở lượt 1 đã bị cắt mất, trợ lý sẽ trả lời sai hoặc nói không biết dù
> thông tin đó đã được cung cấp trước đó trong cùng phiên. Cách khắc phục:
> thay vì cắt cứng theo số lượt, định kỳ tóm tắt các lượt cũ bị đẩy ra thành
> 1–2 câu ngữ cảnh cô đọng (ví dụ "Người dùng tên An, đang học mạng nơ-ron")
> và giữ tóm tắt đó như một message hệ thống bổ sung xuyên suốt phiên, thay
> vì xóa hẳn thông tin đi.

---

## Danh Sách Kiểm Tra Nộp Bài

- [ ] `python grade.py` — xem điểm tự động, mục tiêu ≥ 75/100
- [ ] Cả 4 checkpoint pytest đều pass
- [ ] Tất cả 9 câu trong file này đã được trả lời
- [ ] Đã copy bài làm vào folder `solution/`, push lên GitHub cá nhân và nộp link repo vào vlearn (theo hướng dẫn README)
