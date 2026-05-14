# Module 36. Công Nghệ Ẩn, An Ninh, An Toàn Và Tiện Nghi Không Phô Trương

## 1. Vai trò của module trong toàn bộ giáo trình

Module này đưa công nghệ vào nhà vườn như một lớp hạ tầng âm thầm: tiện nghi, an ninh, an toàn, năng lượng, tưới, chiếu sáng, mạng, cảm biến và vận hành. Nó nhận ngôn ngữ thiết kế từ Module 35 và phối hợp với MEP, cấu tạo, bàn giao, bảo trì từ Module 32-34.

Công nghệ đúng không làm nhà thành showroom thiết bị. Nó giúp nhà sống ổn định hơn, ít người phải can thiệp hơn, phát hiện lỗi sớm hơn và vẫn giữ được vẻ tĩnh, kín đáo của nhà nghỉ dưỡng.

## 2. Mục tiêu học tập

- Hiểu công nghệ ẩn là hạ tầng vận hành, không phải đồ chơi phô trương.
- Biết xác định hệ thống cần có: mạng, điện dự phòng, cảm biến, an ninh, an toàn, chiếu sáng, tưới, thông gió, chống ẩm.
- Biết kiểm tra rủi ro khóa hãng, mất mạng, mất điện, hỏng thiết bị, lộ dây, lộ camera và mất quyền truy cập.
- Tạo được ma trận công nghệ ẩn để làm việc với kiến trúc sư, MEP, an ninh và đơn vị tích hợp hệ thống.

## 3. Tư duy cốt lõi

> Công nghệ tốt nhất trong nhà vườn là công nghệ người dùng gần như không thấy, nhưng luôn có mặt khi cần, dễ thay thế khi lỗi và không làm công trình phụ thuộc vào một hãng duy nhất.

## 4. Bản chất vấn đề

Nhà vườn nghỉ dưỡng thường dùng không liên tục, có nhiều vùng ngoài trời, nhiều ẩm, nhiều cây, nhiều thiết bị phụ trợ và đôi khi xa trung tâm. Nếu thiếu công nghệ đúng, nhà dễ gặp lỗi âm thầm: rò nước, bơm hỏng, cây thiếu tưới, đèn lỗi, camera mù điểm, khóa kẹt, mạng yếu, điện chập chờn, người chăm không báo đúng.

Ngược lại, nếu nhồi công nghệ sai, công trình thành phức tạp, lộ thiết bị, khó sửa, phụ thuộc app, phụ thuộc tài khoản cá nhân và lỗi thời nhanh. Bản chất của module là thiết kế lớp kỹ thuật có thể vận hành trong nền, được che giấu đúng cách, có phương án thủ công và có hồ sơ bàn giao rõ.

## 5. Kiến thức nền cần hiểu đúng

### 5.1. Hạ tầng mạng và điều khiển

**Khái niệm:** Mạng gồm internet, router, switch, Wi-Fi, cáp tín hiệu, tủ kỹ thuật và hệ điều khiển.

**Bản chất:** Nhà thông minh yếu thường bắt đầu từ mạng yếu và tủ kỹ thuật không có chỗ bảo trì.

**Hệ quả triển khai:** Thiết kế tủ rack, tuyến cáp, vùng phủ sóng, UPS và khả năng reset/khôi phục rõ ràng.

### 5.2. An ninh kín đáo

**Khái niệm:** An ninh gồm cổng, khóa, camera, cảm biến cửa, vùng báo động, đèn an ninh và quản lý quyền vào.

**Bản chất:** An ninh tốt phải giảm điểm mù nhưng không biến nhà nghỉ dưỡng thành công trình phòng thủ thô cứng.

**Hệ quả triển khai:** Giấu camera, đèn, cảm biến theo kiến trúc; kiểm quyền truy cập theo người, thời điểm và khu vực.

### 5.3. An toàn chủ động

**Khái niệm:** An toàn gồm rò nước, điện, khói, khí độc nếu có, trơn ngã, ngập, gió bão, sét và sự cố thiết bị.

**Bản chất:** Nhiều rủi ro cần được phát hiện sớm trước khi con người nhìn thấy.

**Hệ quả triển khai:** Dùng cảm biến phù hợp, cảnh báo phân cấp và quy trình xử lý khi chủ nhà không có mặt.

### 5.4. Tiện nghi không phô trương

**Khái niệm:** Tiện nghi gồm chiếu sáng, rèm, quạt, điều hòa, thông gió, âm thanh, tưới, bơm, nước nóng, ổ cắm và sạc.

**Bản chất:** Tiện nghi tốt giúp dùng nhà dễ hơn nhưng không làm lộ dây, bảng điều khiển, thiết bị hoặc ánh sáng gắt.

**Hệ quả triển khai:** Chốt kịch bản sử dụng theo hoạt động, dùng công tắc vật lý rõ ràng và app chỉ là lớp bổ sung.

### 5.5. Tính thay thế và chống khóa hãng

**Khái niệm:** Chống khóa hãng là tránh phụ thuộc vào một hệ sinh thái, một app hoặc một tài khoản duy nhất.

**Bản chất:** Thiết bị điện tử có vòng đời ngắn hơn công trình. Nhà 20-50 năm phải thay được công nghệ nhiều lần.

**Hệ quả triển khai:** Ưu tiên chuẩn mở, đường ống chờ, dây dự phòng, API/backup nếu cần, tài khoản sở hữu bởi chủ nhà và hồ sơ cấu hình đầy đủ.

## 6. Các nguyên lý chính

| Nguyên lý | Vì sao quan trọng | Cách áp dụng |
|---|---|---|
| Ẩn nhưng tiếp cận được | Thiết bị giấu quá kỹ sẽ khó sửa. | Che bằng kiến trúc nhưng có nắp, lối mở, nhãn và bản vẽ. |
| App không thay thế công tắc | Mất mạng hoặc người lớn tuổi vẫn phải dùng được. | Mỗi chức năng quan trọng có điều khiển vật lý dễ hiểu. |
| Ưu tiên hạ tầng trước thiết bị | Thiết bị thay đổi nhanh, hạ tầng thay đổi khó. | Đầu tư cáp, ống, tủ, nguồn dự phòng, vùng kỹ thuật. |
| Bảo mật là một phần thiết kế | Nhà thông minh mở thêm rủi ro truy cập. | Quản lý tài khoản, mật khẩu, phân quyền, cập nhật và nhật ký truy cập. |
| Tự động hóa phải có giới hạn | Tự động sai có thể gây khó chịu hoặc nguy hiểm. | Dùng kịch bản rõ, ngưỡng cảnh báo và chế độ thủ công. |

## 7. Công cụ phân tích

- Ma trận công nghệ ẩn theo khu vực và chức năng.
- Sơ đồ tủ kỹ thuật, tuyến cáp, Wi-Fi và vùng phủ sóng.
- Bảng kịch bản an ninh, an toàn và tiện nghi.
- Danh mục thiết bị có vòng đời, bảo hành, phương án thay thế.
- Checklist quyền truy cập, tài khoản, backup và bàn giao cấu hình.
- Bảng rủi ro mất điện, mất mạng, hỏng thiết bị và vận hành thủ công.

## 8. Quy trình áp dụng từng bước

1. Liệt kê hoạt động thật: đến nhà, rời nhà, ở qua đêm, đi vắng dài ngày, mưa lớn, mất điện, có khách, có người chăm.
2. Chuyển hoạt động thành kịch bản công nghệ: mở cổng, bật đèn, an ninh, tưới, thông gió, cảnh báo, khóa vùng.
3. Xác định hệ thống cần ẩn và vị trí cần bảo trì: tủ mạng, tủ điện, cảm biến, camera, bơm, van, bộ điều khiển.
4. Phối hợp với kiến trúc để giấu thiết bị mà không phá ngôn ngữ thiết kế.
5. Thiết kế chế độ thủ công cho cổng, khóa, đèn, tưới, bơm, thông gió và các hệ quan trọng.
6. Chạy thử theo kịch bản thật: ban đêm, mưa lớn, mất mạng, mất điện, khách đến, chủ nhà ở xa.
7. Bàn giao tài khoản, sơ đồ, cấu hình, mật khẩu, bảo hành và quy trình cập nhật.

## 9. Ví dụ thực tế

| Tình huống | Dấu hiệu nhận biết | Nguyên nhân | Hướng xử lý |
|---|---|---|---|
| Camera lộ và phá mặt tiền | Thiết bị nổi bật ở cổng, hiên, góc mái. | Không phối hợp công nghệ từ thiết kế kiến trúc. | Chọn vị trí kín, màu phù hợp, góc nhìn đủ và có lối bảo trì. |
| Mất mạng là mất điều khiển | Đèn, cổng, tưới, khóa phụ thuộc app. | Không có điều khiển vật lý hoặc mạng cục bộ. | Bổ sung công tắc, khóa cơ, lịch cục bộ và chế độ bypass. |
| Wi-Fi yếu ở hiên và vườn | Camera, loa, điều khiển tưới chập chờn. | Không khảo sát vùng phủ sóng ngoài trời. | Thiết kế AP ngoài trời, cáp mạng và nguồn phù hợp. |
| Báo động giả nhiều | Cây, thú nhỏ, mưa, ánh sáng gây kích hoạt. | Chọn cảm biến và ngưỡng sai. | Phân vùng, chỉnh ngưỡng, kết hợp camera xác minh. |
| Chủ nhà không sở hữu tài khoản | Nhà thầu giữ app, mật khẩu, cấu hình. | Bàn giao thiếu. | Quy định tài khoản thuộc chủ nhà và có biên bản bàn giao số. |

## 10. Lỗi thường gặp và cách tránh

| Lỗi | Vì sao sai | Hậu quả | Cách tránh |
|---|---|---|---|
| Chọn thiết bị trước khi có kịch bản | Dễ mua thừa hoặc thiếu. | Phức tạp nhưng không giải quyết vấn đề thật. | Bắt đầu từ hoạt động và rủi ro vận hành. |
| Tin hoàn toàn vào không dây | Ngoài trời, tường dày, ẩm và khoảng cách làm tín hiệu yếu. | Hệ thống chập chờn. | Kéo dây cho điểm quan trọng, dùng không dây có chọn lọc. |
| Không dự phòng điện | Mất điện là mất an ninh và cảnh báo. | Nhà rủi ro khi đi vắng. | Dùng UPS, pin dự phòng hoặc máy phát/solar nếu phù hợp. |
| Không tính an ninh mạng | Thiết bị kết nối có thể bị truy cập sai. | Rò dữ liệu, mất quyền điều khiển. | Phân quyền, đổi mật khẩu, cập nhật firmware, tách mạng khách. |
| Giấu thiết bị không có cửa bảo trì | Đẹp lúc bàn giao nhưng sửa phải đục phá. | Chi phí sửa cao. | Thiết kế nắp thăm, nhãn và bản vẽ hoàn công. |

## 11. Checklist kiểm tra

| Câu hỏi kiểm tra | Dấu hiệu đạt | Rủi ro nếu chưa đạt | Hành động sửa |
|---|---|---|---|
| Có ma trận công nghệ theo kịch bản chưa? | Có đến nhà, rời nhà, đi vắng, mưa lớn, mất điện, mất mạng. | Mua thiết bị rời rạc. | Lập kịch bản trước khi chọn thiết bị. |
| Thiết bị có được ẩn nhưng sửa được không? | Có vị trí, nắp thăm, nguồn, nhãn và bản vẽ. | Sửa phải phá hoàn thiện. | Phối hợp lại với kiến trúc và MEP. |
| Có chế độ thủ công không? | Cổng, khóa, đèn, tưới, bơm dùng được khi app lỗi. | Nhà bị phụ thuộc hệ thống. | Bổ sung công tắc, khóa cơ, bypass. |
| Có quản lý quyền truy cập không? | Tài khoản chủ nhà, phân quyền người chăm/khách/nhà thầu. | Mất kiểm soát sau bàn giao. | Lập biên bản bàn giao số. |
| Có kế hoạch thay thế thiết bị không? | Biết vòng đời, bảo hành, chuẩn kết nối, vị trí thay. | Công nghệ lỗi thời làm nhà khó vận hành. | Lập asset register và lộ trình nâng cấp. |

## 12. Bài tập thực hành

| Mức | Bài tập |
|---|---|
| Cơ bản | Liệt kê 10 tình huống cần công nghệ hỗ trợ trong nhà vườn. |
| Khá | Lập ma trận công nghệ ẩn theo khu vực: cổng, sân, hiên, phòng chính, phòng ngủ, kỹ thuật, vườn. |
| Tốt | Tạo kịch bản mất điện/mất mạng và phương án vận hành thủ công. |
| Xuất sắc | Review một đề xuất smart home và chỉ ra rủi ro khóa hãng, bảo mật, bảo trì, thẩm mỹ và bàn giao. |

## 13. Tiêu chí tự đánh giá

| Mức | Biểu hiện |
|---|---|
| Cơ bản | Nhận biết được nhóm công nghệ cần có. |
| Khá | Giải thích được công nghệ nào cần ẩn, công nghệ nào cần điều khiển vật lý. |
| Tốt | Tạo được ma trận công nghệ, quyền truy cập và kịch bản lỗi. |
| Xuất sắc | Kiểm soát được công nghệ như một lớp hạ tầng bền, kín đáo, bảo mật và có thể thay thế. |

## 14. Liên kết với các module khác

Nhận đầu vào từ Module 16, 20, 31, 32, 34 và 35. Tạo đầu vào cho Module 37 về hồ sơ tài sản, lịch bảo trì, vòng đời thiết bị, cảnh báo sớm và nâng cấp dài hạn.

## 15. Ghi chú giới hạn chuyên môn

Module này giúp chủ nhà đặt đề bài và kiểm soát công nghệ ở mức tiêu chí. Thiết kế điện, mạng, an ninh, PCCC, chống sét, tự động hóa, bảo mật, tích hợp hệ thống và tuân thủ pháp lý phải do chuyên gia đủ năng lực kiểm tra và chịu trách nhiệm theo dự án thật.
