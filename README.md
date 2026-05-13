# Giáo Trình Thiết Kế Nhà Vườn Nghỉ Dưỡng Nhiệt Đới

Bộ giáo trình nền tảng giúp người mới hiểu đúng bản chất thiết kế nhà vườn nghỉ dưỡng: đọc khu đất, tổ chức trải nghiệm, kiến trúc nhiệt đới, cây xanh nhiều tầng, đất nước, vật liệu, ánh sáng, bảo trì và quy trình làm việc với kiến trúc sư/cảnh quan/thi công.

## Xem Bản HTML

- Trang chính: [`index.html`](index.html)
- Bản giáo trình hoàn chỉnh: [`giao_trinh_nha_vuon_nghi_duong/giao_trinh_hoan_chinh.html`](giao_trinh_nha_vuon_nghi_duong/giao_trinh_hoan_chinh.html)

Khi bật GitHub Pages, trang sẽ hiển thị tại:

```text
https://<github-user>.github.io/<repo-name>/
```

## Nội Dung

| Phần | Mô tả |
|---|---|
| `giao_trinh_nen_tang_thiet_ke_nha_vuon_nghi_duong.md` | File khung gốc |
| `giao_trinh_nha_vuon_nghi_duong/00_muc_luc_va_huong_dan_hoc.md` | Mục lục và hướng dẫn học |
| `giao_trinh_nha_vuon_nghi_duong/modules/` | 12 module bài học chi tiết |
| `giao_trinh_nha_vuon_nghi_duong/phu_luc/` | Checklist, mẫu brief, mẫu khảo sát, lộ trình học |
| `giao_trinh_nha_vuon_nghi_duong/giao_trinh_hoan_chinh.html` | Bản HTML hợp nhất, giao diện đẹp, có Mermaid |
| `giao_trinh_nha_vuon_nghi_duong/kiem_dinh_chat_luong.md` | Báo cáo kiểm định chất lượng |

## Chuẩn Module

Mỗi module được chuẩn hóa theo 14 phần:

1. Mục tiêu học tập.
2. Vì sao module này quan trọng.
3. Tư duy cốt lõi.
4. Kiến thức nền cần hiểu đúng.
5. Nguyên lý thiết kế.
6. Sơ đồ trực quan Mermaid.
7. Quy trình áp dụng từng bước.
8. Ví dụ thực tế.
9. Lỗi thường gặp và cách tránh.
10. Checklist kiểm tra.
11. Bài tập thực hành.
12. Tiêu chí tự đánh giá.
13. Liên kết với các module khác.
14. Ghi chú giới hạn chuyên môn.

## GitHub Pages

Repo này dùng GitHub Pages dạng tĩnh:

- Source: branch `main`
- Folder: `/root`
- Entry point: `index.html`

File `.nojekyll` được thêm để GitHub Pages phục vụ nguyên trạng các file tĩnh.

## Ghi Chú Mermaid

Bản HTML tải Mermaid qua CDN:

```text
https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs
```

Vì vậy, sơ đồ Mermaid cần internet để render. Nội dung chữ, bảng và bố cục vẫn đọc được khi offline.
