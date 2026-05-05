# Hệ thống OCR CCCD / Passport

## 1. Tổng quan
Dự án xây dựng một hệ thống OCR end-to-end nhằm trích xuất thông tin từ ảnh CCCD (Căn cước công dân) và Hộ chiếu.  
Hệ thống có khả năng xử lý ảnh trong nhiều điều kiện khác nhau và trả về dữ liệu có cấu trúc dạng JSON.



## 2. Pipeline xử lý
1. Input Image
2. Tiền xử lý (resize, deskew)
3. Nhận diện tài liệu
4. Nhận diện vùng thông tin (bbox)
5. OCR (trích xuất text)
6. Hậu xử lý (format, validation)
7. JSON Output



## 3. API Endpoints
   - **Tên API**: /ocr
   - **Phương thức**: POST  
   - **Request**: file ảnh
   - **Response**:  
   
     ```json
      {
        "Số": "079203001234",
        "Họ và tên": "NGUYỄN VĂN A",
        "Ngày sinh": "01/01/2000",
        "Giới tính": "Nam",
        "Quê quán": "Xã Tân Phú, Huyện Đồng Phú, Tỉnh Bình Phước",
        "Nơi thường trú": "Phường Phú Lợi, TP. Thủ Dầu Một, Tỉnh Bình Dương",
        "Có giá trị đến": "01/01/2035"
      }
      ```  
   
## 4. Đánh giá
- Độ chính xác OCR
- Độ chính xác nhận diện vùng (mAP)
- Thời gian xử lý mỗi ảnh



## 5. Kết quả
- Trích xuất thông tin có cấu trúc từ CCCD/Hộ chiếu
- Độ chính xác > 80%
- API hoạt động nhanh và ổn định



## 6. Công nghệ sử dụng
- **FastAPI:** Backend API
- **OpenCV:** Xử lý ảnh
- **YOLO:** Nhận diện đối tượng
- **PaddleOCR / VietOCR:** Nhận dạng văn bản
