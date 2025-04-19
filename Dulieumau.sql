INSERT INTO bookstore_category (name) VALUES 
('Văn học'),
('Khoa học'),
('Tâm lý'),
('Tiểu thuyết'),
('Lịch sử'),
('Kỹ năng sống'),
('Thiếu nhi'),
('Công nghệ'),
('Triết học');


INSERT INTO bookstore_book (id, title, author, price, stock, category_id, imagePath, status, description) VALUES
(1, 'Đắc Nhân Tâm', 'Dale Carnegie', 120000, 15, 3, 'book_images/1.jpg', 'available', 'Đắc nhân tâm là quyển sách nổi tiếng nhất...'),
(2, 'Nhà Giả Kim', 'Paulo Coelho', 89000, 20, 4, 'book_images/2.jpg', 'available', 'Tác phẩm kể về Santiago...'),
(3, 'Sapiens: Lược Sử Loài Người', 'Yuval Noah Harari', 180000, 10, 2, 'book_images/3.jpg', 'available', 'Sapiens là một câu chuyện lịch sử...'),
(4, 'Kinh Tế Học Hài Hước', 'Steven D. Levitt & Stephen J. Dubner', 135000, 8, 2, 'book_images/4.jpg', 'available', 'Cuốn sách ứng dụng những công cụ của kinh tế học...'),
(5, 'Chiến Tranh Tiền Tệ', 'Song Hongbing', 150000, 5, 2, 'book_images/5.jpg', 'available', 'Tác phẩm nghiên cứu về lịch sử và bản chất của tiền tệ...'),
(6, 'Việt Nam Sử Lược', 'Trần Trọng Kim', 160000, 7, 5, 'book_images/6.jpg', 'available', 'Cuốn sách viết về lịch sử Việt Nam...'),
(7, 'Tâm Lý Học Đám Đông', 'Gustave Le Bon', 95000, 0, 3, 'book_images/7.jpg', 'unavailable', 'Nghiên cứu đầu tiên về tâm lý học đám đông...'),
(8, 'Hoàng Hôn Rực Rỡ', 'Khaled Hosseini', 140000, 18, 4, 'book_images/8.jpg', 'available', 'Câu chuyện cảm động về tình bạn...'),
(9, 'Vật Lý Vui', 'Walter Lewin', 125000, 14, 2, 'book_images/9.jpg', 'available', 'Cuốn sách làm cho vật lý trở nên thú vị...'),
(10, 'Người Trong Muôn Nghề', 'Spiderum', 145000, 22, 6, 'book_images/10.jpg', 'available', 'Tuyển tập những câu chuyện thật từ những người đang làm việc...'),
(11, 'Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 75000, 30, 7, 'book_images/11.jpg', 'available', 'Tác phẩm kinh điển của văn học thiếu nhi Việt Nam...'),
(12, 'Trí Tuệ Nhân Tạo', 'Kai-Fu Lee', 195000, 8, 8, 'book_images/12.jpg', 'available', 'Cuốn sách về AI và tương lai của loài người...'),
(13, 'Bứt Phá Giới Hạn Bản Thân', 'Tony Robbins', 168000, 16, 6, 'book_images/13.jpg', 'available', 'Cuốn sách hướng dẫn cách vượt qua những rào cản tâm lý...'),
(14, 'Thế Giới Phẳng', 'Thomas L. Friedman', 210000, 7, 2, 'book_images/14.jpg', 'available', 'Phân tích về quá trình toàn cầu hóa...'),
(15, 'Nghệ Thuật Tư Duy Rành Mạch', 'Rolf Dobelli', 130000, 19, 3, 'book_images/15.jpg', 'available', 'Tổng hợp 99 lỗi tư duy phổ biến...'),
(16, 'Lược Sử Thời Gian', 'Stephen Hawking', 155000, 11, 2, 'book_images/16.jpg', 'available', 'Tác phẩm nổi tiếng giải thích các khái niệm phức tạp...'),
(17, 'Tôi Tài Giỏi, Bạn Cũng Thế', 'Adam Khoo', 110000, 25, 6, 'book_images/17.jpg', 'available', 'Phương pháp học tập hiệu quả và phát triển tư duy...'),
(18, 'Triết Học Nghệ Thuật Sống', 'Luc Ferry', 148000, 6, 9, 'book_images/18.jpg', 'available', 'Cuốn sách giới thiệu về các trường phái triết học lớn...');

INSERT INTO bookstore_user (username, password, full_name, role, address, email, phone, status ) VALUES
('customer1', 'pass123', 'Nguyen Van A', 'customer', '123 Hanoi', 'customer1@example.com', '0123456789', 'active'),
('customer2', 'pass123', 'Đinh Phúc Thành', 'customer', 'abc', 'thanh@gmail.com', '0123456789', 'active'),
('customer3', 'pass123', 'Đinh Phúc Thành2', 'customer', 'abc', 'thanh1@gmail.com', '0123456789', 'active'),
('admin1', 'pass123', 'chí', 'admin', 'abc', 'thanh2@gmail.com', '0123456789', 'active'),
('staff1', 'pass123', 'chí', 'staff', 'abc', 'thanh3@gmail.com', '0123456789', 'active'),
('manager1', 'pass123', 'abc', 'manager', 'abc', 'thanh4@gmail.com', '0123456789', 'active');

-- Tạo dữ liệu mẫu cho bảng Order
INSERT INTO bookstore_order (user_id, address, status, total_amount, created_at, updated_at)
VALUES
(1, '123 Đường ABC, Quận 1, TP.HCM', 'Completed', 215000, '2023-01-10 08:30:00', '2023-01-12 10:15:00'),
(2, '456 Đường XYZ, Quận 2, TP.HCM', 'Completed', 350000, '2023-02-15 14:20:00', '2023-02-17 09:45:00'),
(3, '789 Đường MNP, Quận 3, TP.HCM', 'Cancelled', 180000, '2023-03-05 16:40:00', '2023-03-06 08:30:00'),
(1, '123 Đường ABC, Quận 1, TP.HCM', 'Completed', 390000, '2023-04-12 11:15:00', '2023-04-14 13:20:00'),
(2, '456 Đường XYZ, Quận 2, TP.HCM', 'Pending', 280000, '2023-05-20 09:50:00', '2023-05-20 09:50:00'),
(1, '202 Đường HIJ, Quận 5, TP.HCM', 'Confirmed', 260000, '2023-06-08 15:30:00', '2023-06-09 10:45:00'),
(3, '789 Đường MNP, Quận 3, TP.HCM', 'Pending', 350000, '2023-07-14 17:20:00', '2023-07-14 17:20:00'),
(1, '123 Đường ABC, Quận 1, TP.HCM', 'Completed', 95000, '2023-08-22 10:10:00', '2023-08-24 11:30:00'),
(1, '202 Đường HIJ, Quận 5, TP.HCM', 'Cancelled', 120000, '2023-09-30 13:45:00', '2023-10-01 08:15:00'),
(2, '456 Đường XYZ, Quận 2, TP.HCM', 'Completed', 540000, '2023-11-05 16:25:00', '2023-11-07 14:30:00');

-- Tạo dữ liệu mẫu cho bảng OrderDetail
INSERT INTO bookstore_orderdetail (order_id, book_id, quantity, price)
VALUES
(1, 1, 1, 120000),
(1, 4, 1, 95000),
(2, 5, 1, 350000),
(3, 6, 1, 180000),
(4, 3, 1, 210000),
(4, 6, 1, 180000),
(5, 11, 1, 280000),
(6, 7, 1, 85000),
(6, 1, 1, 120000),
(6, 10, 1, 30000),
(6, 14, 1, 25000),
(7, 5, 1, 350000),
(8, 2, 1, 95000),
(9, 1, 1, 120000),
(10, 3, 1, 210000),
(10, 5, 1, 350000);