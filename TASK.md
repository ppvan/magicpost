# Tính năng chung

# Tiến độ task

## Chức năng cho lãnh đạo công ty

- [x] Quản lý hệ thống các điểm giao dịch và điểm tập kết.
- [x] Quản lý tài khoản trưởng điểm điểm tập kết và điểm giao dịch. Mỗi điểm giao dịch hoặc điểm tập kết có một tài khoản trưởng điểm.
- [ ] Thống kê hàng gửi, hàng nhận trên toàn quốc, từng điểm giao dịch hoặc điểm tập kết.

## Chức năng cho trưởng điểm tại điểm giao dịch

- [x] Cấp tài khoản cho giao dịch viên tại điểm giao dịch.
- [ ] Thống kê hàng gửi, hàng nhận tại điểm giao dịch.

## Chức năng cho giao dịch viên tại điểm giao dịch

- [ ] Ghi nhận hàng cần gửi của khách (người gửi), in giấy biên nhận chuyển phát và phát cho khách hàng (tham khảo Hình 1 trong phụ lục).
- [ ] Tạo đơn chuyển hàng gửi đến điểm tập kết mỗi/trước khi đem hàng gửi đến điểm tập kết.
- [ ] Xác nhận (đơn) hàng về từ điểm tập kết.
- [ ] Tạo đơn hàng cần chuyển đến tay người nhận.
- [ ] Xác nhận hàng đã chuyển đến tay người nhận theo .
- [ ] Xác nhận hàng không chuyển được đến người nhận và trả lại điểm giao dịch.
- [ ] Thống kê các hàng đã chuyển thành công, các hàng chuyển không thành công và trả lại điểm giao dịch.

## Chức năng cho trưởng điểm tại điểm tập kết

- [x] Quản lý tài khoản nhân viên tại điểm tập kết.
- [ ] Thống kê hàng đi, đến.

## Chức năng cho nhân viên tại điểm tập kết

- [ ] Xác nhận (đơn) hàng đi từ điểm giao dịch chuyển đến.
- [ ] Tạo đơn chuyển hàng đến điểm tập kết đích (ứng với điểm giao dịch đích, tức điểm giao dịch phụ trách vùng ứng với địa chỉ của người nhận).
- [ ] Xác nhận (đơn) hàng nhận về từ điểm tập kết khác.
- [ ] Tạo đơn chuyển hàng đến điểm giao dịch đích.

## Chức năng cho khách hàng

- [x] Tra cứu trạng thái và tiến trình chuyển phát của kiện hàng mình gửi.


--------------------------------

zipcode = 100920
status: ['']

path
|item_id| zipcode | is_here
    1        100      false
    1         101      true

paths
|item_id| office1| office2|hub1|hub2|
1          2'     3   1      1  2