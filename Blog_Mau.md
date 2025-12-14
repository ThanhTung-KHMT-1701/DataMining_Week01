# 📦 Case Study: Phân tích giỏ hàng với Apriori

## 👥 Thông tin Nhóm
- **Nhóm:** 
- **Thành viên:** 
  - …
  - …
- **Chủ đề:** 
- **Dataset:** Online Retail (UCI)

## Mục tiêu 
Mục tiêu của nhóm là:  
> *(viết 1–3 dòng)*

## 1. Ý tưởng & Feynman Style
Giải thích lại bài toán theo cách **dễ hiểu nhất** (không technical):
- Apriori dùng làm gì?
- Tại sao phù hợp cho bài toán giỏ hàng?
- Ý tưởng thuật toán (1–2 câu thôi)

## 2. Quy trình Thực hiện

1) Load & làm sạch dữ liệu  
2) Tạo ma trận basket  
3) Áp dụng Apriori  
4) Trích xuất luật  
5) Trực quan hóa  
6) Phân tích insight  

## 3. Tiền xử lý Dữ liệu
- Những bước làm sạch:
  - Loại bỏ sản phẩm "rỗng"
  - Loại bỏ transaction bị cancel (InvoiceNo bắt đầu "C")
  - Loại bỏ số lượng âm

- Thống kê nhanh:
  - Số giao dịch sau lọc:
  - Số sản phẩm duy nhất:

## 4. Áp dụng Apriori
**Tham số sử dụng:**
- `min_support = ...`
- `min_threshold = ...`
- `max_len = ... (nếu có)`

```python
from mlxtend.frequent_patterns import apriori, association_rules

frequent_itemsets = apriori(basket_df, min_support=0.002, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules.sort_values("lift", ascending=False, inplace=True)
rules.head()
```

## 5. Trực quan hóa (Visualization)
- Hình 1: caption mô tả…
- Hình 2: caption mô tả…


## 6. Insight từ Kết quả
**Insight #1:**  
**Insight #2:**  
**Insight #3:**  
**Insight #4:**  
**Insight #5:**  

## 7. Kết luận & Đề xuất Kinh doanh
- Gợi ý cross-sell…
- Gợi ý sắp xếp hàng trên kệ…
- Gợi ý khuyến mãi theo mùa…


## 8. Link Code & Notebook
- Notebook:
- Repo:

## 9. Slide trình bày
- Link Slide:


