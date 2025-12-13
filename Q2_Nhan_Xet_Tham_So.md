# Q2: Nhận xét về tác động của tham số Support, Confidence, Lift

## Tham số hiện tại trong `run_papermill.py`

```python
# Tham số Apriori
MIN_SUPPORT=0.01        # Support tối thiểu để tìm itemset
MAX_LEN=3              # Độ dài tối đa của itemset

# Lọc luật
FILTER_MIN_SUPPORT=0.01  # Support tối thiểu của luật
FILTER_MIN_CONF=0.3      # Confidence tối thiểu
FILTER_MIN_LIFT=1.2      # Lift tối thiểu
```

## 1. Tác động của MIN_SUPPORT (Support)

**Support** = P(A ∩ B) - Xác suất xuất hiện đồng thời của các sản phẩm trong giao dịch

### Thay đổi để test:
- **MIN_SUPPORT=0.01** (1%) - Giá trị mặc định
- **MIN_SUPPORT=0.005** (0.5%) - Thấp hơn
- **MIN_SUPPORT=0.02** (2%) - Cao hơn

### Nhận xét:
- **Support cao (0.02)**: 
  - ✅ Chỉ tìm được các mẫu phổ biến, xuất hiện trong nhiều giao dịch
  - ✅ Giảm thời gian tính toán, ít luật hơn
  - ❌ Có thể bỏ lỡ các mẫu thú vị nhưng ít gặp
  
- **Support thấp (0.005)**:
  - ✅ Tìm được nhiều mẫu hơn, kể cả các mẫu ít gặp
  - ✅ Phát hiện được các cơ hội cross-selling cho sản phẩm niche
  - ❌ Thời gian tính toán lâu hơn, nhiều luật hơn
  - ❌ Có thể tạo ra nhiều luật không có ý nghĩa (noise)

**Khuyến nghị**: Bắt đầu với 0.01, giảm xuống nếu cần nhiều luật hơn

---

## 2. Tác động của FILTER_MIN_CONF (Confidence)

**Confidence** = P(B|A) = P(A ∩ B) / P(A) - Xác suất mua B khi đã mua A

### Thay đổi để test:
- **FILTER_MIN_CONF=0.3** (30%) - Giá trị mặc định
- **FILTER_MIN_CONF=0.2** (20%) - Thấp hơn
- **FILTER_MIN_CONF=0.5** (50%) - Cao hơn

### Nhận xét:
- **Confidence cao (0.5)**:
  - ✅ Luật có độ tin cậy cao, khả năng xảy ra cao
  - ✅ Phù hợp cho gợi ý sản phẩm (recommendation)
  - ❌ Ít luật hơn, có thể bỏ lỡ cơ hội
  
- **Confidence thấp (0.2)**:
  - ✅ Nhiều luật hơn để phân tích
  - ❌ Nhiều luật yếu, không chắc chắn
  - ❌ Có thể gây nhiễu trong hệ thống gợi ý

**Khuyến nghị**: 
- Dùng 0.3-0.4 cho phân tích khám phá
- Dùng 0.5+ cho hệ thống gợi ý sản phẩm

---

## 3. Tác động của FILTER_MIN_LIFT (Lift)

**Lift** = P(B|A) / P(B) - Mức độ ảnh hưởng của A lên B so với ngẫu nhiên

### Thay đổi để test:
- **FILTER_MIN_LIFT=1.2** - Giá trị mặc định
- **FILTER_MIN_LIFT=1.0** - Không lọc
- **FILTER_MIN_LIFT=1.5** - Cao hơn

### Ý nghĩa Lift:
- **Lift > 1**: A và B xuất hiện cùng nhau nhiều hơn ngẫu nhiên (tương quan dương)
- **Lift = 1**: A và B độc lập
- **Lift < 1**: A và B loại trừ lẫn nhau (tương quan âm)

### Nhận xét:
- **Lift cao (1.5+)**:
  - ✅ Luật có mối liên hệ mạnh, có ý nghĩa thực tế
  - ✅ Tốt cho marketing campaign
  - ❌ Ít luật hơn
  
- **Lift thấp (1.0-1.2)**:
  - ✅ Nhiều luật hơn
  - ❌ Bao gồm cả các luật yếu, ít ý nghĩa
  - ❌ Có thể chỉ là ngẫu nhiên

**Khuyến nghị**: 
- Dùng 1.2-1.5 cho phân tích chung
- Dùng 2.0+ để tìm các mối liên hệ mạnh

---

## Thử nghiệm: Thay đổi tham số

### Kịch bản 1: Tìm nhiều luật hơn
```python
MIN_SUPPORT=0.005       # Giảm từ 0.01
FILTER_MIN_CONF=0.2     # Giảm từ 0.3
FILTER_MIN_LIFT=1.0     # Giảm từ 1.2
```
**Kết quả**: Nhiều luật hơn, bao gồm cả luật yếu

### Kịch bản 2: Tìm luật chất lượng cao
```python
MIN_SUPPORT=0.02        # Tăng từ 0.01
FILTER_MIN_CONF=0.5     # Tăng từ 0.3
FILTER_MIN_LIFT=2.0     # Tăng từ 1.2
```
**Kết quả**: Ít luật nhưng rất mạnh và có ý nghĩa

### Kịch bản 3: Cân bằng (Khuyến nghị)
```python
MIN_SUPPORT=0.01
FILTER_MIN_CONF=0.4
FILTER_MIN_LIFT=1.5
```
**Kết quả**: Cân bằng giữa số lượng và chất lượng luật

---

## Hướng dẫn chạy thử nghiệm

1. Mở file `run_papermill.py`
2. Thay đổi các tham số theo kịch bản muốn test
3. Chạy lệnh:
```powershell
cd C:\KHMT\DataMining\DataMining_Week01
& C:/Users/binhn/anaconda3/envs/shopping_env/python.exe run_papermill.py
```
4. So sánh kết quả trong `notebooks/runs/apriori_modelling_run.ipynb`
5. Ghi lại số lượng luật tìm được và đánh giá chất lượng

---

## Kết luận

- **Support**: Kiểm soát độ phổ biến của mẫu
- **Confidence**: Kiểm soát độ tin cậy của luật
- **Lift**: Kiểm soát mức độ liên kết có ý nghĩa

**Chiến lược tốt nhất**: 
1. Bắt đầu với tham số trung bình
2. Chạy và đánh giá kết quả
3. Điều chỉnh dần dần theo mục tiêu cụ thể
4. Luôn kiểm tra ý nghĩa thực tế của luật, không chỉ dựa vào số liệu
