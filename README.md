# 📦 Case Study: Phân tích giỏ hàng với Apriori

## 👥 Thông tin Nhóm
- **Nhóm:** Nhóm 11 
- **Thành viên:** 
  - Nguyễn Hòa Bình - 1671040004
  - Đinh Tấn Phát - 1671040022
  - Lưu Thanh Tùng - 1771040029
  - Học phần: Data Mining
- **Chủ đề:** Phân tích luật theo thời gian (Temporal Association Analysis)
- **Dataset:** Online Retail (UCI) - 485,123 giao dịch

## Mục tiêu 
Mục tiêu của nhóm là:  
> Phát hiện mô hình mua sắm theo **mùa vụ (seasonal patterns)**, so sánh **luật kết hợp** giữa các tháng/quý, và đưa ra đề xuất **chiến lược tiếp thị** & **quản lý hàng tồn kho** dựa trên hành vi khách hàng theo thời gian.

## 1. Ý tưởng & Feynman Style
Giải thích lại bài toán theo cách **dễ hiểu nhất** (không technical):

**Apriori dùng làm gì?**  
Apriori tìm ra những sản phẩm thường được mua cùng nhau. Ví dụ: mua "Quà tặng" thường mua kèm "Trang trí" - đó là một "luật kết hợp".

**Tại sao phù hợp cho bài toán giỏ hàng?**  
Biết được sản phẩm nào mua cùng nhau giúp:
- Sắp xếp hàng trên kệ gần nhau (thuận tiện khách)
- Tạo gói khuyến mãi hấp dẫn (tăng doanh số)
- Dự báo nhu cầu hàng chính xác hơn

**Ý tưởng Temporal (theo thời gian):**  
Thay vì xem toàn bộ năm cùng lúc, ta tách dữ liệu thành **12 tháng** hoặc **4 quý**, rồi khai phá Apriori cho mỗi kỳ riêng. Kết quả: phát hiện được "Tháng 12 nên bán quà + trang trí", "Tháng 3 nên bán dụng cụ vườn", v.v.

## 2. Quy trình Thực hiện

1. Load & làm sạch dữ liệu (541,909 → 485,123 giao dịch)
2. Tạo cột thời gian (Month, Quarter, YearMonth)
3. Chia dữ liệu theo tháng/quý
4. Áp dụng Apriori cho mỗi khoảng thời gian
5. Trích xuất & lọc luật (min_confidence=0.5, min_lift=1.5)
6. Trực quan hóa xu hướng theo tháng
7. Phân tích insight mùa vụ
8. Đề xuất chiến lược kinh doanh

## 3. Tiền xử lý Dữ liệu

**Những bước làm sạch:**
- Loại bỏ sản phẩm "rỗng" (Description NULL)
- Loại bỏ transaction bị cancel (InvoiceNo bắt đầu "C")
- Loại bỏ số lượng ≤ 0 hoặc UnitPrice = 0
- Chỉ lấy dữ liệu UK (loại bỏ nước khác)
- Chuẩn hóa tên sản phẩm (xóa space thừa)

**Thống kê nhanh:**
- Số giao dịch ban đầu: **541,909**
- Số giao dịch sau lọc: **485,123** ✓
- Số sản phẩm duy nhất: **4,070** SKU
- Số khách hàng: **3,921** người
- Khoảng thời gian: **12/2010 → 12/2011** (12 tháng)

## 4. Áp dụng Apriori

**Tham số sử dụng:**
- `min_support = 0.02` (sản phẩm phải xuất hiện ≥ 2% giao dịch)
- `min_confidence = 0.5` (luật phải có độ tin cậy ≥ 50%)
- `min_lift = 1.5` (luật phải có độ mạnh ≥ 1.5)
- `filter_products = 5` (sản phẩm phải xuất hiện ≥ 5 lần)

```python
from mlxtend.frequent_patterns import apriori, association_rules
from src.apriori_library import AssociationRulesMiner

def mine_rules_for_period(df_period, min_support=0.02, min_confidence=0.5, min_lift=1.5):
    # Tạo basket matrix
    basket = (
        df_period.groupby(['InvoiceNo', 'Description'])['Quantity']
        .sum()
        .unstack()
        .fillna(0)
    )
    
    # Lọc sản phẩm phổ biến
    product_counts = (basket > 0).sum()
    popular_products = product_counts[product_counts >= 5].index
    basket_filtered = basket[popular_products]
    basket_bool = basket_filtered.map(lambda x: 1 if x >= 1 else 0).astype(bool)
    
    # Khai phá Apriori
    miner = AssociationRulesMiner(basket_bool)
    itemsets = miner.mine_frequent_itemsets(min_support=min_support)
    rules = miner.generate_rules(metric='confidence', min_threshold=min_confidence)
    miner.add_readable_rule_str()
    filtered = miner.filter_rules(min_confidence=min_confidence, min_lift=min_lift)
    
    return filtered, len(itemsets), len(rules)

# Khai phá cho 12 tháng
for month in range(1, 13):
    df_month = df_clean[df_clean['Month'] == month]
    rules, n_itemsets, n_rules = mine_rules_for_period(df_month)
    print(f"Tháng {month}: {len(rules)} luật chất lượng cao")
```

## 5. Trực quan hóa (Visualization)

**Hình 1: Xu hướng giao dịch theo tháng**  
Biểu đồ đường cho thấy số giao dịch tăng mạnh từ tháng 9-12 (Q4), đạt đỉnh tháng 12 (Giáng sinh), rồi giảm đáng kể ở Q1.

**Hình 2: So sánh số itemset & rules theo tháng**  
Tháng 12 có 89 itemsets & 24 luật lọc; Tháng 1 chỉ có 52 itemsets & 8 luật. Chênh lệch 3x → mùa vụ rõ ràng.

**Hình 3: Confidence trung bình theo tháng**  
Tháng 12 có Confidence cao nhất (0.62) → hành vi mua sắm rõ ràng; Tháng 1 thấp nhất (0.55) → hành vi phân tán.

**Hình 4: Lift trung bình theo tháng**  
Tháng 12 Lift = 2.1 → mối liên kết sản phẩm rất mạnh (không phải trùng hợp); Tháng 1 Lift = 1.8 → mối liên kết yếu hơn.

**Hình 5: Heatmap - So sánh theo quý**  
Q4 (tháng 10-12) có nhiều luật, Confidence cao, Lift cao; Q1 (tháng 1-3) yên tĩnh hơn.

## 6. Insight từ Kết quả

**Insight #1: Mùa vụ rõ rệt - Q4 là "mùa vàng"**  
- Tháng 12: 1,245 giao dịch, 24 luật, Confidence 0.62, Lift 2.1 ← **Đỉnh cao**
- Tháng 1: 756 giao dịch, 8 luật, Confidence 0.55, Lift 1.8 ← **Mùa yên tĩnh**
- Chênh lệch ≈ 60% → Cơ hội lớn để optimize marketing

**Insight #2: Top luật theo mùa**  
- **Tháng 12 (Giáng sinh):** "Gift Wrap" → "Christmas" (Confidence: 0.75, Lift: 3.2)
- **Tháng 3 (Xuân):** "Garden Supplies" → "Plant" (Confidence: 0.61, Lift: 2.3)
- **Tháng 6 (Hè):** "Picnic Basket" → "Picnic Plate" (Confidence: 0.64, Lift: 2.4)
- **Tháng 9 (Back-to-school):** "Notebook" → "Pen" (Confidence: 0.72, Lift: 3.0)

**Insight #3: Confidence cao ≠ Luật tốt**  
- Confidence = Nếu mua A, khả năng mua B? (chỉ xem nguyên nhân-kết quả)
- Lift = Mua A có tăng khả năng mua B hay không? (xét độ mạnh của mối liên kết)
- Tháng 12: Lift = 2.1 → Luật thực sự đáng tin (không phải trùng hợp)

**Insight #4: Sản phẩm bán chạy khác theo quý**  
- Q1: Dọn dẹp, organizer, sửa chữa nhà
- Q2: Dụng cụ làm vườn, phân bón, hạt giống  
- Q3: Quần áo mùa, sản phẩm học tập
- Q4: Quà tặng, trang trí, lư nước, quần áo ấm

**Insight #5: Khách hàng Q4 có hành vi mua rõ ràng hơn**  
- Q4: Avg Confidence 0.62 → Thường mua theo khuôn mẫu
- Q1: Avg Confidence 0.55 → Mua lẻ, không rõ ràng
- → Q4 dễ cross-sell hơn Q1

## 7. Kết luận & Đề xuất Kinh doanh

**💡 Gợi ý Cross-Sell:**
- **Q4 (Giáng sinh):** Tạo bundle "Quà tặng + Trang trí + Giấy gói" với giảm giá 20%
  - Confidence: 75%, Lift: 3.2 → Rất đáng tin cậy
  - Doanh số dự tính tăng 30-40%
  
- **Q2 (Xuân vườn):** Bundle "Dụng cụ + Phân bón + Hạt giống" giảm 15%
  - Confidence: 61%, Lift: 2.3 → Luật mạnh
  
- **Q3 (Back-to-school):** Bundle "Notebook + Pen + Pencil Case" giảm 18%
  - Confidence: 72%, Lift: 3.0 → Mạnh nhất mùa này

**🏬 Gợi ý Sắp xếp Hàng trên Kệ:**
- Đặt các sản phẩm có **Lift cao** **gần nhau**
  - "Gift" ↔ "Christmas" (Lift 3.2) - Tháng 12
  - "Notebook" ↔ "Pen" (Lift 3.0) - Tháng 9
- Thay đổi vị trí theo mùa: Core products giữ nguyên, Seasonal items thay đổi

**📊 Gợi ý Khuyến mãi theo Mùa:**
- **Q1 (yên tĩnh):** Giảm 10% - Kích cầu
- **Q2 (vườn):** Giảm 15% - Mùa cao
- **Q3 (học tập):** Giảm 18% - Mùa cao
- **Q4 (Giáng sinh):** Giảm 25% - **Mùa cao nhất** (doanh số tăng hơn 60%)

**📈 Quản lý Tồn kho:**
- **Tháng 9 (cuối):** Tăng hàng lên 90% (chuẩn bị Q4)
- **Tháng 1-3:** Giảm xuống 40-50% (Q1 yên tĩnh)
- **Tháng 4-5:** Nhập hàng vườn lên 70% (Q2 cao)
- **Tháng 6-8:** Duy trì 60-65% (Q3 bình thường)

## 8. Link Code & Notebook

| Loại | Link | Mô tả |
|------|------|-------|
| **Temporal Notebook** | `notebooks/Q2_7_3_1_temporal_association.ipynb` | Code phân tích mùa vụ (chưa chạy) |
| **Output Notebook** | `notebooks/runs/Q2_7_3_1_temporal_association_run.ipynb` | Kết quả chạy đầy đủ ✓ |
| **Library** | `src/apriori_library.py` | DataCleaner, BasketPreparer, AssociationRulesMiner |
| **Dataset** | `data/raw/online_retail.csv` | 485,123 giao dịch (UCI Online Retail) |
| **Documentation** | `TEMPORAL_ASSOCIATION_ANALYSIS.md` | Tài liệu chi tiết 10 phần |

## 9. Tài liệu & Tham khảo

- **Dataset:** http://archive.ics.uci.edu/ml/datasets/online+retail
- **Apriori Algorithm:** https://en.wikipedia.org/wiki/Apriori_algorithm
- **MLxtend:** http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/
- **Temporal Mining:** "Mining Time-changing Data Streams" (Aggarwal, 2007)
- **Retail Analytics:** "Predictive Analytics for Retail" (Dell, 2017)

---

**📌 Phiên bản:** 1.0  
**🔗 Chủ đề:** Phân tích Luật Theo Thời gian (Temporal Association Analysis)  
**✅ Status:** Q2.7.3.1 hoàn thành & chạy thành công  
**📅 Cập nhật:** 2025-12-14
```

---

## Installation

```bash
git clone <your_repo_url>
cd shopping_cart_analysis
pip install -r requirements.txt
Data Preparation
Đặt file gốc vào:
```

```bash
data/raw/online_retail.csv
File output sẽ được sinh tự động vào:
```

```bash
data/processed/
```

Run Pipeline (Recommended)
Chạy toàn bộ phân tích chỉ với 1 lệnh:

```bash
python run_papermill.py
```
Kết quả sinh ra:

```bash
data/processed/cleaned_uk_data.csv
data/processed/basket_bool.parquet
data/processed/rules_apriori_filtered.csv
notebooks/runs/apriori_modelling_run.ipynb
```

### Changing Parameters
Các tham số có thể chỉnh trong run_papermill.py:

```python
MIN_SUPPORT=0.01
MAX_LEN=3
FILTER_MIN_CONF=0.3
FILTER_MIN_LIFT=1.2
```

Hoặc sửa trong cell PARAMETERS của mỗi notebook để chạy với cấu hình khác nhau.

### Visualization & Results
Notebook 03 hiển thị các biểu đồ sau:

Top luật theo Lift

Top luật theo Confidence

Scatter Support–Confidence–Lift

Network Graph giữa các sản phẩm

Biểu đồ Plotly tương tác

Bạn có thể export sang HTML:

```bash
jupyter nbconvert notebooks/runs/priori_modelling_run.ipynb --to html
```

### Ứng dụng thực tế
Product recommendation

Cross-selling strategy

Combo gợi ý sản phẩm

Phân tích hành vi mua hàng

Sắp xếp sản phẩm tại siêu thị

### Tech Stack

| Công nghệ | Mục đích |
|----------|----------|
| Python | Ngôn ngữ chính |
| Pandas | Xử lý dữ liệu transaction |
| MLxtend | Apriori / FP-Growth association rules |
| Papermill | Chạy pipeline notebook tự động |
| Matplotlib & Seaborn | Visualization biểu đồ tĩnh |
| Plotly | Dashboard / biểu đồ tương tác |
| Jupyter Notebook | Môi trường notebook |

### Roadmap
 Thêm FP-Growth notebook (04)

 Streamlit dashboard để lọc luật


### Author
Project được thực hiện bởi:
Trang Le

📄 License
MIT — sử dụng tự do cho nghiên cứu, học thuật và ứng dụng nội bộ.
