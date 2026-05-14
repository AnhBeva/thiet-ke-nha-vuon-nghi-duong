# Bài 38. Xuất Video Nháp

## 1. Mục tiêu bài học

Bạn biết xuất video nháp chất lượng thấp để kiểm tra chuyển động, ánh sáng và lỗi model trước khi render bản cuối.

## 2. Bài này nằm ở đâu trong toàn bộ dự án

Video cuối tốn thời gian render. Video nháp giúp phát hiện lỗi sớm với chi phí thấp.

## 3. Từ khóa tiếng Việt cần hiểu

- **Video nháp:** bản xuất thử để kiểm tra.
- **Độ phân giải:** kích thước khung hình video.
- **Khung hình/giây:** độ mượt chuyển động.

## 4. Bản chất và nguyên lý

Đừng render bản đẹp khi chưa xem bản nháp. Lỗi camera, đèn nhấp nháy, cây che khung hình hoặc tốc độ sai thường chỉ lộ rõ khi xem video.

## 5. Kiến thức nền vừa đủ

Bản nháp có thể dùng độ phân giải thấp. Mục tiêu là kiểm tra hành trình, không phải chất lượng ảnh.

## 6. Quy trình thao tác trong SketchUp hoặc D5

1. Chọn thiết lập xuất thấp.
2. Xuất video nháp.
3. Xem toàn bộ từ đầu đến cuối.
4. Ghi thời điểm lỗi.
5. Sửa camera, ánh sáng hoặc model.

## 7. Bài tập áp dụng vào chính dự án

Xuất một video nháp walkthrough và xem lại ít nhất hai lần.

## 8. Đầu ra bắt buộc

File video nháp trong `04_Video` và bảng lỗi kèm mốc thời gian.

## 9. Tiêu chuẩn đạt

Phát hiện được lỗi chính trước bản cuối, có danh sách sửa rõ, không bỏ qua đoạn camera khó chịu.

## 10. Lỗi thường gặp và cách sửa

Lỗi thường gặp là thấy nháp xấu nên chỉnh màu quá nhiều. Hãy ưu tiên sửa chuyển động và lỗi cảnh trước.

## 11. Câu hỏi tự duyệt

- Có đoạn nào quá nhanh không?
- Có vật thể nào che camera không?
- Ánh sáng có thay đổi khó chịu không?

## 12. Liên kết bài trước/bài sau

Bài trước tạo camera path. Bài sau xuất video cuối sau khi sửa lỗi.

