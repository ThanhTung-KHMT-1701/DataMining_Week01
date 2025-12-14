# 📦 Case Study: Phân tích giỏ hàng với Apriori

## Thông tin Nhóm
- **Nhóm:** Nhóm 11
- **Thành viên:** 
  - Nguyễn Hòa Bình - 1671040004
  - Đinh Tấn Phát - 1671040022
  - Lưu Thanh Tùng - 1771040029
- **Chủ đề:** Chủ đề 4: Phân tích độ nhạy tham số (Parameter Sensitivity)
- **Dataset:** Online Retail Dataset (UCI Machine Learning Repository)

---

## Mục tiêu 
Mục tiêu của nhóm là phân tích dữ liệu giao dịch bán lẻ để:
- Tìm ra các sản phẩm thường được mua cùng nhau
- Khai thác luật kết hợp (Association Rules) để đề xuất chiến lược cross-selling
- Tối ưu hóa việc sắp xếp sản phẩm và xây dựng chương trình khuyến mãi hiệu quả

---

## 1. Ý tưởng & Feynman Style

### Apriori dùng làm gì?
**Giải thích đơn giản:** Thuật toán Apriori giống như một "thám tử" tìm kiếm các mẫu hình (patterns) trong giỏ hàng của khách. Nó giúp trả lời câu hỏi: *"Khi khách mua sản phẩm A, họ thường mua thêm sản phẩm nào?"*

Ví dụ: Nếu phát hiện 80% khách mua bánh mì thì cũng mua bơ, cửa hàng có thể:
- Đặt bánh mì và bơ gần nhau
- Làm combo khuyến mãi "bánh mì + bơ"
- Gợi ý mua bơ khi khách cho bánh mì vào giỏ

### Tại sao phù hợp cho bài toán giỏ hàng?
- **Dữ liệu giao dịch lớn:** Dataset có hàng trăm nghìn giao dịch với hàng nghìn sản phẩm
- **Tìm mối liên hệ ẩn:** Phát hiện các tổ hợp sản phẩm mà con người khó nhận ra
- **Hỗ trợ quyết định kinh doanh:** Đưa ra khuyến nghị cụ thể dựa trên dữ liệu thực tế

### Ý tưởng thuật toán
1. **Tìm sản phẩm phổ biến:** Xác định các sản phẩm/tổ hợp xuất hiện thường xuyên (frequent itemsets)
2. **Sinh luật kết hợp:** Từ các tổ hợp phổ biến, tạo ra các luật dạng "nếu mua A → thì mua B" với độ tin cậy cao

---

## 2. Quy trình Thực hiện

```mermaid
graph LR
    A[1. Load Data] --> B[2. Làm sạch dữ liệu]
    B --> C[3. Tạo ma trận basket]
    C --> D[4. Áp dụng Apriori]
    D --> E[5. Trích xuất luật]
    E --> F[6. Trực quan hóa]
    F --> G[7. Phân tích insight]
```

1. **Load & Explore Data** - Tải dữ liệu và phân tích sơ bộ
2. **Làm sạch dữ liệu** - Loại bỏ giao dịch không hợp lệ, giá trị thiếu
3. **Tạo ma trận basket** - Chuyển đổi dữ liệu thành ma trận boolean (transaction × product)
4. **Áp dụng Apriori** - Khai thác frequent itemsets với min_support
5. **Trích xuất luật** - Sinh association rules với confidence và lift
6. **Trực quan hóa** - Vẽ biểu đồ phân tích các luật
7. **Phân tích insight** - Rút ra kết luận và đề xuất kinh doanh

---

## 3. Tiền xử lý Dữ liệu

### Những bước làm sạch:
1. **Loại bỏ sản phẩm "rỗng"**
   - Xóa các dòng có `Description` = null hoặc rỗng
   
2. **Loại bỏ transaction bị cancel** 
   - Lọc các `InvoiceNo` bắt đầu bằng "C" (giao dịch hoàn trả)
   
3. **Loại bỏ số lượng âm**
   - Chỉ giữ lại `Quantity > 0`
   
4. **Lọc theo quốc gia**
   - Tập trung vào thị trường UK (`Country = "United Kingdom"`)
   
5. **Loại bỏ giá trị bất thường**
   - Lọc `UnitPrice > 0`
   - Xóa các mã sản phẩm đặc biệt (POST, BANK CHARGES, etc.)

### Thống kê sau làm sạch:
- **Số giao dịch gốc:** 541,909
- **Số giao dịch sau lọc (UK):** 485,123 ✅
- **Loại bỏ:** 56,786 giao dịch (10.5%)
- **Số sản phẩm duy nhất:** 4,005 sản phẩm
- **Số khách hàng:** 4,372 khách hàng
- **Khoảng thời gian:** 01/12/2010 - 09/12/2011

---

## 4. Áp dụng Apriori

### Tham số sử dụng:
```python
# Khai thác frequent itemsets
MIN_SUPPORT = 0.01      # 1% - Itemset phải xuất hiện trong ít nhất 1% giao dịch
MAX_LEN = 3             # Độ dài tối đa của itemset (tối đa 3 sản phẩm)

# Sinh association rules
METRIC = "lift"         # Sử dụng lift làm chỉ số chính
MIN_THRESHOLD = 1.0     # Lift tối thiểu = 1.0

# Lọc luật chất lượng cao
FILTER_MIN_SUPPORT = 0.01    # Support ≥ 1%
FILTER_MIN_CONF = 0.3        # Confidence ≥ 30%
FILTER_MIN_LIFT = 1.2        # Lift ≥ 1.2 (có tương quan dương)
```

### Code thực hiện:

```python
from mlxtend.frequent_patterns import apriori, association_rules
from apriori_library import AssociationRulesMiner

# Khởi tạo miner
miner = AssociationRulesMiner(basket_bool=basket_df)

# 1. Khai thác frequent itemsets
frequent_itemsets = miner.mine_frequent_itemsets(
    min_support=0.01,
    max_len=3
)
print(f"Tìm được {len(frequent_itemsets)} frequent itemsets")

# 2. Sinh association rules
rules = miner.generate_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=1.0
)
print(f"Tìm được {len(rules)} luật ban đầu")

# 3. Lọc luật chất lượng cao
filtered_rules = miner.filter_rules(
    rules,
    min_support=0.01,
    min_confidence=0.3,
    min_lift=1.2,
    max_antecedents=2,
    max_consequents=1
)
print(f"Sau lọc: {len(filtered_rules)} luật chất lượng cao")

# Hiển thị top 10 luật theo lift
filtered_rules.sort_values("lift", ascending=False).head(10)
```

---

## 5. Trực quan hóa (Visualization)

### Hình 1: Top 20 Luật theo Lift
![Top Rules by Lift](notebooks/runs/apriori_modelling_run.ipynb#plot-lift)
- Biểu đồ cột hiển thị 20 luật có lift cao nhất
- Màu sắc thể hiện mức độ confidence
- **Insight:** Các tổ hợp sản phẩm trang trí, đồ gia dụng có lift rất cao (3.0+)

### Hình 2: Top 20 Luật theo Confidence
![Top Rules by Confidence](notebooks/runs/apriori_modelling_run.ipynb#plot-conf)
- Các luật có độ tin cậy cao nhất (>50%)
- Phù hợp cho hệ thống recommendation
- **Insight:** Khách mua sản phẩm A có xác suất rất cao mua sản phẩm B

### Hình 3: Scatter Plot - Support vs Confidence
![Scatter Plot](notebooks/runs/apriori_modelling_run.ipynb#plot-scatter)
- Trục X: Support (độ phổ biến)
- Trục Y: Confidence (độ tin cậy)
- Kích thước bong bóng: Lift
- Màu sắc: Số sản phẩm trong antecedents
- **Insight:** Xác định vùng "sweet spot" - luật vừa phổ biến, vừa tin cậy, vừa có lift cao

### Hình 4: Network Graph - Mối quan hệ sản phẩm
![Network Graph](notebooks/runs/apriori_modelling_run.ipynb#plot-network)
- Nodes: Sản phẩm
- Edges: Luật kết hợp (độ dày = lift)
- **Insight:** Nhận diện các "hub products" - sản phẩm trung tâm kết nối với nhiều sản phẩm khác

### Hình 5: Interactive Plotly Visualization
![Interactive Plot](notebooks/runs/apriori_modelling_run.ipynb#plotly)
- Biểu đồ tương tác 3D với Support, Confidence, Lift
- Hover để xem chi tiết từng luật
- **Insight:** Khám phá dữ liệu một cách trực quan và linh hoạt

---

## 6. Insight từ Kết quả

### Insight #1: Sản phẩm trang trí có mối liên hệ mạnh
- **Phát hiện:** Các sản phẩm trang trí (decorative items) thường được mua cùng nhau với lift > 3.0
- **Ví dụ:** "PINK REGENCY TEACUP AND SAUCER" → "GREEN REGENCY TEACUP AND SAUCER"
- **Đề xuất:** Tạo bộ sưu tập (collection) hoặc combo set cho các sản phẩm cùng theme

### Insight #2: Mẫu mua sắm theo mùa
- **Phát hiện:** Các sản phẩm giáng sinh (Christmas items) có support cao trong Q4
- **Ví dụ:** Đèn LED, đồ trang trí noel xuất hiện cùng nhau
- **Đề xuất:** Chuẩn bị inventory và campaign marketing theo seasonal trends

### Insight #3: Cross-selling hiệu quả cho sản phẩm bổ sung
- **Phát hiện:** Sản phẩm "bổ sung" có confidence > 50%
- **Ví dụ:** Mua ly → mua đĩa lót (saucer), mua túi → mua hộp đựng
- **Đề xuất:** Hiển thị "frequently bought together" trên website/app

### Insight #4: Khách hàng mua theo bộ/set
- **Phát hiện:** Nhiều luật có antecedents và consequents là các sản phẩm cùng màu/cùng họa tiết
- **Ví dụ:** Tách trà các màu khác nhau (PINK, GREEN, BLUE) trong cùng dòng REGENCY
- **Đề xuất:** Tạo product bundles, khuyến khích mua theo bộ với giá ưu đãi

### Insight #5: Sản phẩm "gateway" - Hub products
- **Phát hiện:** Một số sản phẩm phổ biến kết nối với nhiều sản phẩm khác
- **Ví dụ:** WHITE HANGING HEART, JUMBO BAG là các hub products
- **Đề xuất:** Đầu tư marketing mạnh cho các hub products, đặt ở vị trí chiến lược trong store

---

## 7. Kết luận & Đề xuất Kinh doanh

### Gợi ý Cross-sell
1. **Recommendation System:** 
   - Khi khách thêm sản phẩm A vào giỏ, hiển thị sản phẩm B với thông báo "Frequently bought together"
   - Ưu tiên các luật có confidence > 40% và lift > 2.0

2. **Email Marketing:**
   - Gửi email gợi ý sản phẩm bổ sung dựa trên lịch sử mua hàng
   - Personalization theo các luật kết hợp

### Gợi ý sắp xếp hàng trên kệ
1. **Đặt sản phẩm liên quan gần nhau:**
   - Các sản phẩm trong cùng một luật (A → B) nên đặt cạnh nhau hoặc cùng khu vực
   - Ví dụ: Tách trà và đĩa lót, đồ trang trí cùng theme

2. **Tạo display theo theme:**
   - Tận dụng insight về sản phẩm cùng màu/họa tiết
   - Tạo góc trưng bày "Complete the set"

### Gợi ý khuyến mãi
1. **Bundle Promotion:**
   - Tạo combo từ các luật có lift cao: "Mua A + B giảm 15%"
   - Ví dụ: "Bộ tách trà REGENCY - Mix & Match 20% off"

2. **Seasonal Campaign:**
   - Chạy campaign theo mùa dựa trên time patterns
   - Q4: Tập trung vào Christmas decorations bundles
   - Q2: Home & Garden items

3. **Tiered Pricing:**
   - "Mua 2 tặng 1" cho các sản phẩm trong cùng itemset
   - Khuyến khích tăng basket size

### Tối ưu hóa Inventory
- **Stock items theo cặp:** Đảm bảo sản phẩm A và B (có trong luật) luôn có sẵn cùng lúc
- **Forecast demand:** Dự đoán nhu cầu sản phẩm B dựa trên sales của sản phẩm A

---

## 8. Link Code & Notebook

### Notebooks thực thi:
- **Preprocessing & EDA:** [`notebooks/runs/preprocessing_and_eda_run.ipynb`](notebooks/runs/preprocessing_and_eda_run.ipynb)
- **Basket Preparation:** [`notebooks/runs/basket_preparation_run.ipynb`](notebooks/runs/basket_preparation_run.ipynb)
- **Apriori Modelling:** [`notebooks/runs/apriori_modelling_run.ipynb`](notebooks/runs/apriori_modelling_run.ipynb)

### Source Code:
- **Main Library:** [`src/apriori_library.py`](src/apriori_library.py)
- **Pipeline Script:** [`run_papermill.py`](run_papermill.py)

### Repository:
- **GitHub:** `https://github.com/ThanhTung-KHMT-1701/DataMining_Week01`
- **Branch:** `Tuan02_NguyenHoaBinh`

---

## 9. Slide trình bày
- **Link Slide:** [Google Slides / PowerPoint link - Cập nhật sau]
- **Link Demo:** [Nếu có web demo]

---

## 10. Phân tích độ nhạy tham số (Parameter Sensitivity)

### Mục tiêu
Đánh giá ảnh hưởng của tham số `min_support` đến kết quả thuật toán Apriori.

### Phương pháp
Test với 4 giá trị min_support khác nhau: **0.01, 0.015, 0.02, 0.03**

### Kết quả thử nghiệm

| min_support | Frequent Itemsets | Rules (sau lọc) | Avg Confidence | Avg Lift | Max Lift | Thời gian |
|-------------|-------------------|-----------------|----------------|----------|----------|-----------|
| **0.01 (1%)** | 2,120 | 1,794 | 0.535 | 13.570 | 74.567 | 52.14s |
| **0.015 (1.5%)** | 755 | 456 | 0.514 | 9.803 | 39.557 | 4.05s |
| **0.02 (2%)** ⭐ | 400 | **175** | 0.499 | 8.842 | 27.200 | **1.51s** |
| **0.03 (3%)** | 145 | 21 | 0.587 | 10.053 | 15.865 | 0.30s |

### Biểu đồ so sánh - Số lượng luật
```
0.01 (1%):   ████████████████████████████████████████ (1,794 luật)
0.015 (1.5%): ██████████ (456 luật)
0.02 (2%):    ███ (175 luật) ⭐ KHUYẾN NGHỊ
0.03 (3%):     (21 luật)
```

### Quan sát chính

1. **Mối quan hệ nghịch đảo**
   - min_support ↑ → Số lượng luật ↓ (giảm mạnh từ 1,794 → 21)
   - Đúng với lý thuyết: Support cao → ít itemset đạt ngưỡng

2. **Trade-off Số lượng vs Thời gian**
   - min_support = 0.01: Quá nhiều luật (1,794), khó phân tích, chậm (52s)
   - min_support = 0.03: Quá ít luật (21), bỏ lỡ insight

3. **Chất lượng luật (Lift)**
   - Lift cao nhất ở min_support = 0.01 (Max: 74.567)
   - Nhưng trung bình (Avg Lift) tương đối ổn định (8-13)

4. **Top patterns phát hiện**
   - **HERB MARKER series**: Lift 74+ ở min_support=0.01
     - Ví dụ: `HERB MARKER PARSLEY + ROSEMARY → THYME` (Lift: 74.567)
   - **REGENCY TEACUP**: Xuất hiện ở mọi ngưỡng - sản phẩm best-seller
   - **Christmas items**: Mối liên hệ mạnh (Lift: 27.2)

### 🏆 Khuyến nghị "Ngưỡng hợp lý"

**Tham số tối ưu cho dataset này:**
```python
MIN_SUPPORT = 0.02  # 2%
```

**Lý do:**
- Tạo ra **175 luật chất lượng** - đủ để phân tích, không quá nhiễu
- Thời gian xử lý nhanh: **1.51 giây**
- Cân bằng tốt giữa số lượng và chất lượng
- Avg Lift = 8.842, Max Lift = 27.2 (mạnh và ý nghĩa)
- Phù hợp cho triển khai thực tế

**Khi nào dùng giá trị khác:**
- **min_support = 0.01**: Khi muốn khám phá sâu, phân tích research
- **min_support = 0.03**: Khi chỉ quan tâm best-sellers, cần kết quả nhanh

### Chi tiết đầy đủ
Xem file [`Parameter_Sensitivity_Analysis.md`](Parameter_Sensitivity_Analysis.md) để biết thêm chi tiết về phân tích.

### Chạy lại thử nghiệm
```bash
cd C:\KHMT\DataMining\DataMining_Week01
& C:/Users/binhn/anaconda3/envs/shopping_env/python.exe test_parameter_sensitivity.py
```

---

## 🚀 Cách chạy Project

### Prerequisites:
```bash
# Tạo môi trường conda
conda create -n shopping_env python=3.11
conda activate shopping_env

# Cài đặt dependencies
pip install -r requirements.txt
```

### Chạy Pipeline:
```bash
# Chạy toàn bộ pipeline với Papermill
python run_papermill.py
```

### Xem kết quả:
- Notebooks đã chạy: `notebooks/runs/`
- Dữ liệu processed: `data/processed/`
- Association rules: `data/processed/rules_apriori_filtered.csv`
- Parameter sensitivity results: `data/processed/parameter_sensitivity_results.csv`

---

## 📚 Tài liệu tham khảo

1. **Dataset:** [UCI Machine Learning Repository - Online Retail](https://archive.ics.uci.edu/ml/datasets/Online+Retail)
2. **Apriori Algorithm:** Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.
3. **MLxtend Library:** [Association Rules Documentation](http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/)
4. **Parameter Sensitivity Analysis:** [Internal Document](Parameter_Sensitivity_Analysis.md)

---
**📧 Contact:** Nhóm 11 - KHMT  
**📅 Last Updated:** December 13, 2025
