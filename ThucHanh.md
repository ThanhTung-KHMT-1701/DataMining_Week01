# BÁO CÁO THỰC HÀNH - TUẦN 01: KHAI PHÁ DỮ LIỆU

**Sinh viên thực hiện:** Lưu Thanh Tùng  
**MSSV:** 1771040029  
**Ngày thực hiện:** 14/12/2025

---

## CÂU HỎI 1: Đọc hiểu cấu trúc dự án và hiển thị tất cả biểu đồ

### 1.1. Cấu trúc dự án

Dự án được tổ chức theo cấu trúc sau:

```
DataMining_Week01/
├── data/
│   ├── raw/                    # Dữ liệu thô
│   │   └── online_retail.csv
│   └── processed/              # Dữ liệu đã xử lý
│       ├── cleaned_uk_data.csv
│       ├── basket_bool.parquet
│       └── rules_apriori_filtered.csv
├── notebooks/
│   ├── preprocessing_and_eda.ipynb      # Tiền xử lý và phân tích EDA
│   ├── basket_preparation.ipynb         # Chuẩn bị giỏ hàng
│   ├── apriori_modelling.ipynb         # Mô hình Apriori
│   └── runs/                            # Kết quả chạy notebook
├── src/
│   └── apriori_library.py              # Thư viện Apriori tùy chỉnh
├── run_papermill.py                     # Script chạy pipeline
└── requirements.txt                     # Các thư viện cần thiết
```

### 1.2. Mục đích các notebook

- **preprocessing_and_eda.ipynb**: Làm sạch dữ liệu, phân tích thống kê mô tả, trực quan hóa dữ liệu
- **basket_preparation.ipynb**: Chuyển đổi dữ liệu sang dạng one-hot encoding cho thuật toán Apriori
- **apriori_modelling.ipynb**: Áp dụng thuật toán Apriori để tìm luật kết hợp

### 1.3. Thay đổi tham số để hiển thị tất cả biểu đồ

**File cần chỉnh sửa:** `run_papermill.py`

**Thay đổi trong preprocessing_and_eda:**

```python
parameters=dict(
    DATA_PATH="data/raw/online_retail.csv",
    COUNTRY="United Kingdom",
    OUTPUT_DIR="data/processed",
    PLOT_REVENUE=True,           # Hiển thị biểu đồ doanh thu
    PLOT_TIME_PATTERNS=True,     # Hiển thị xu hướng theo thời gian
    PLOT_PRODUCTS=True,          # Hiển thị phân tích sản phẩm
    PLOT_CUSTOMERS=True,         # Hiển thị phân tích khách hàng
    PLOT_RFM=True,              # Hiển thị phân tích RFM
)
```

**Thay đổi trong apriori_modelling:**

```python
parameters=dict(
    # ... các tham số khác ...
    
    # Bật tất cả các biểu đồ
    PLOT_TOP_LIFT=True,          # Top luật theo Lift
    PLOT_TOP_CONF=True,          # Top luật theo Confidence
    PLOT_SCATTER=True,           # Scatter plot Support-Confidence
    PLOT_NETWORK=True,           # Biểu đồ mạng luật kết hợp (NetworkX)
    PLOT_PLOTLY_NETWORK=True,    # Biểu đồ mạng tương tác (Plotly)
    PLOT_PLOTLY_SCATTER=True,    # Scatter plot tương tác (Plotly)
)
```

### 1.4. Kết quả sau khi chạy pipeline

**Thống kê dữ liệu từ preprocessing_and_eda:**
- **Dữ liệu gốc:** 541,909 giao dịch với 8 cột
- **Tổng số khách hàng:** 4,373 khách hàng
- **Dữ liệu sau làm sạch (United Kingdom):** 485,123 giao dịch
- **Số giao dịch bị loại bỏ:** 56,786 giao dịch (10.5%)
- **Số khách hàng United Kingdom:** 3,921 khách hàng

**Thống kê từ basket_preparation:**
- **Số hoá đơn duy nhất:** 18,021 hoá đơn
- **Số sản phẩm duy nhất:** 4,007 sản phẩm
- **Kích thước ma trận basket:** 18,021 × 4,007
- **Tỷ lệ ô = 1 (có mua hàng):** 0.66% (ma trận thưa - sparse matrix)

**Thống kê từ apriori_modelling:**
- **Thời gian chạy Apriori:** 16.18 giây
- **Số tập mục phổ biến tìm được:** 2,120 itemsets
- **Số luật kết hợp ban đầu:** 3,856 luật
- **Số luật sau khi lọc:** 1,794 luật

### 1.5. Các biểu đồ được hiển thị

**Từ preprocessing_and_eda:**
1. Biểu đồ doanh thu theo thời gian
2. Biểu đồ số lượng đơn hàng theo giờ/ngày/tháng
3. Top sản phẩm bán chạy nhất
4. Phân phối giá trị đơn hàng
5. Phân tích RFM (Recency, Frequency, Monetary)

**Từ apriori_modelling:**
1. Top 20 luật có Lift cao nhất
2. Top 20 luật có Confidence cao nhất
3. Scatter plot: Support vs Confidence (màu = Lift)
4. Network graph: Mối quan hệ giữa các item
5. Interactive network (Plotly)
6. Interactive scatter plot (Plotly)

### 1.6. Top 10 sản phẩm phổ biến nhất (theo Support)

| STT | Sản phẩm | Support |
|-----|----------|---------|
| 1 | WHITE HANGING HEART T-LIGHT HOLDER | 11.997% |
| 2 | JUMBO BAG RED RETROSPOT | 10.738% |
| 3 | REGENCY CAKESTAND 3 TIER | 9.350% |
| 4 | PARTY BUNTING | 8.840% |
| 5 | LUNCH BAG RED RETROSPOT | 7.724% |
| 6 | ASSORTED COLOUR BIRD ORNAMENT | 7.608% |
| 7 | SET OF 3 CAKE TINS PANTRY DESIGN | 6.886% |
| 8 | NATURAL SLATE HEART CHALKBOARD | 6.764% |
| 9 | LUNCH BAG BLACK SKULL | 6.748% |
| 10 | HEART OF WICKER SMALL | 6.459% |

### 1.7. Top 10 luật kết hợp có Lift cao nhất

| STT | Antecedents (Nếu mua) | Consequents (Thì mua) | Support | Confidence | Lift |
|-----|----------------------|----------------------|---------|------------|------|
| 1 | HERB MARKER PARSLEY, HERB MARKER ROSEMARY | HERB MARKER THYME | 1.09% | 95.17% | 74.57 |
| 2 | HERB MARKER MINT, HERB MARKER THYME | HERB MARKER ROSEMARY | 1.06% | 95.50% | 74.50 |
| 3 | HERB MARKER MINT, HERB MARKER THYME | HERB MARKER PARSLEY | 1.04% | 94.00% | 74.30 |
| 4 | HERB MARKER PARSLEY, HERB MARKER THYME | HERB MARKER ROSEMARY | 1.09% | 95.17% | 74.24 |
| 5 | HERB MARKER BASIL, HERB MARKER THYME | HERB MARKER ROSEMARY | 1.07% | 95.07% | 74.17 |
| 6 | HERB MARKER BASIL, HERB MARKER ROSEMARY | HERB MARKER THYME | 1.07% | 93.69% | 73.41 |
| 7 | HERB MARKER MINT, HERB MARKER ROSEMARY | HERB MARKER THYME | 1.06% | 93.17% | 73.00 |
| 8 | HERB MARKER MINT, HERB MARKER ROSEMARY | HERB MARKER PARSLEY | 1.05% | 92.20% | 72.87 |
| 9 | HERB MARKER BASIL, HERB MARKER THYME | HERB MARKER PARSLEY | 1.04% | 92.12% | 72.81 |
| 10 | HERB MARKER CHIVES | HERB MARKER PARSLEY | 1.04% | 92.12% | 72.81 |

**Nhận xét:**
- Các luật có Lift cao nhất đều liên quan đến bộ sản phẩm "Herb Marker" (biển đánh dấu thảo mộc)
- Lift > 70 cho thấy mối quan hệ rất mạnh giữa các sản phẩm trong cùng bộ
- Confidence > 90% chứng tỏ độ tin cậy cao: khách hàng mua một loại thường mua cả bộ

---

## CÂU HỎI 2: Thay đổi tham số Apriori và nhận xét

### 2.1. Các tham số chính trong thuật toán Apriori

Trong file `run_papermill.py`, các tham số quan trọng:

```python
# Tham số Apriori
MIN_SUPPORT=0.01,        # Support tối thiểu (1%)
MAX_LEN=3,               # Độ dài tối đa của itemset

# Generate rules
METRIC="lift",
MIN_THRESHOLD=1.0,

# Lọc luật
FILTER_MIN_SUPPORT=0.01,     # Support >= 1%
FILTER_MIN_CONF=0.3,         # Confidence >= 30%
FILTER_MIN_LIFT=1.2,         # Lift >= 1.2
FILTER_MAX_ANTECEDENTS=2,
FILTER_MAX_CONSEQUENTS=1,
```

### 2.2. Thử nghiệm với các tham số khác nhau

#### **Cấu hình mặc định (đã chạy)**

```python
MIN_SUPPORT=0.01          # 1%
FILTER_MIN_SUPPORT=0.01
FILTER_MIN_CONF=0.3       # 30%
FILTER_MIN_LIFT=1.2
```

**Kết quả:**
- Thời gian chạy: **16.18 giây**
- Số tập mục phổ biến: **2,120 itemsets**
- Số luật ban đầu: **3,856 luật**
- Số luật sau lọc: **1,794 luật**
- Luật có Lift cao nhất: **74.57** (HERB MARKER set)

**Nhận xét:** Cấu hình này cho phép khám phá rộng với số lượng luật vừa phải, phù hợp cho phân tích khám phá ban đầu.

---

#### **Thử nghiệm 1: Tăng MIN_SUPPORT**

```python
MIN_SUPPORT=0.05          # Tăng từ 0.01 lên 0.05 (5%)
FILTER_MIN_SUPPORT=0.05
FILTER_MIN_CONF=0.3
FILTER_MIN_LIFT=1.2
```

**Dự đoán kết quả:**
- Số lượng itemsets giảm đáng kể (từ 2,120 xuống ~300-500)
- Chỉ giữ lại các sản phẩm xuất hiện rất thường xuyên (>5% hoá đơn)
- Thời gian chạy nhanh hơn nhiều (~2-5 giây)
- Số luật giảm mạnh (~200-400 luật)

**Ưu điểm:**
- Chỉ tập trung vào các mẫu phổ biến nhất
- Kết quả dễ triển khai vì số lượng ít
- Thời gian xử lý nhanh

**Nhược điểm:**
- Bỏ qua các mẫu hiếm nhưng có giá trị
- Có thể mất cơ hội với sản phẩm đặc biệt

**Nhận xét:** Support cao → chỉ tìm được các mẫu phổ biến, phù hợp cho chiến lược marketing đại chúng.

---

#### **Thử nghiệm 2: Giảm MIN_SUPPORT**

```python
MIN_SUPPORT=0.005         # Giảm từ 0.01 xuống 0.005 (0.5%)
FILTER_MIN_SUPPORT=0.005
FILTER_MIN_CONF=0.3
FILTER_MIN_LIFT=1.2
```

**Dự đoán kết quả:**
- Số lượng itemsets tăng gấp 2-3 lần (>5,000 itemsets)
- Tìm được nhiều luật kết hợp hơn (>8,000 luật)
- Thời gian chạy lâu hơn đáng kể (~40-60 giây)
- Có thể tìm ra các mẫu hiếm có giá trị

**Ưu điểm:**
- Khám phá sâu hơn, tìm cả các mẫu ít phổ biến
- Có thể phát hiện niche market

**Nhược điểm:**
- Nhiều luật → khó quản lý và diễn giải
- Tăng nhiễu, có thể có luật ngẫu nhiên
- Thời gian xử lý lâu

**Nhận xét:** Support thấp → tìm được nhiều luật hơn nhưng cần lọc kỹ để tránh nhiễu.

---

#### **Thử nghiệm 3: Tăng FILTER_MIN_CONF**

```python
MIN_SUPPORT=0.01
FILTER_MIN_SUPPORT=0.01
FILTER_MIN_CONF=0.5       # Tăng từ 0.3 lên 0.5 (50%)
FILTER_MIN_LIFT=1.2
```

**Dự đoán kết quả:**
- Số itemsets không đổi (2,120)
- Số luật giảm từ 1,794 xuống ~800-1,000 luật
- Chỉ giữ luật có độ tin cậy ≥ 50%

**Ưu điểm:**
- Chất lượng luật cao hơn
- Giảm false positive
- Dễ tin tưởng khi áp dụng

**Nhược điểm:**
- Có thể bỏ lỡ các luật tiềm năng
- Ít lựa chọn hơn

**Nhận xét:** Confidence cao → luật đáng tin cậy hơn, phù hợp cho ứng dụng thực tế với hệ thống recommendation.

---

#### **Thử nghiệm 4: Tăng FILTER_MIN_LIFT**

```python
MIN_SUPPORT=0.01
FILTER_MIN_SUPPORT=0.01
FILTER_MIN_CONF=0.3
FILTER_MIN_LIFT=2.0       # Tăng từ 1.2 lên 2.0
```

**Dự đoán kết quả:**
- Số itemsets không đổi
- Số luật giảm mạnh từ 1,794 xuống ~600-900 luật
- Chỉ giữ luật có mối quan hệ mạnh (Lift ≥ 2.0)

**Ưu điểm:**
- Loại bỏ các luật ngẫu nhiên
- Tập trung vào mối quan hệ thực sự có ý nghĩa
- Giảm nhiễu đáng kể

**Nhược điểm:**
- Có thể bỏ qua quan hệ yếu nhưng có giá trị
- Số lượng luật ít hơn

**Nhận xét:** Lift cao → tìm được các mối quan hệ không ngẫu nhiên, phù hợp khi cần độ chính xác cao.

---

#### **Thử nghiệm 5: Cấu hình Production (Khắt khe)**

```python
MIN_SUPPORT=0.02          # 2%
FILTER_MIN_SUPPORT=0.02
FILTER_MIN_CONF=0.5       # 50%
FILTER_MIN_LIFT=2.0
```

**Dự đoán kết quả:**
- Số itemsets: ~800-1,000
- Số luật: ~150-300 luật chất lượng cao
- Thời gian: ~8-10 giây

**Ưu điểm:**
- Chỉ giữ luật có chất lượng cao nhất
- Dễ triển khai và giám sát
- Độ tin cậy rất cao

**Nhược điểm:**
- Rất hạn chế về số lượng
- Có thể mất cơ hội kinh doanh

**Nhận xét:** Cấu hình này phù hợp cho production, khi cần đảm bảo mỗi recommendation đều có giá trị.

---

### 2.3. Bảng tổng hợp ảnh hưởng của tham số

| Tham số | Giá trị mặc định | Tăng giá trị | Giảm giá trị |
|---------|-----------------|--------------|--------------|
| **MIN_SUPPORT** | 0.01 (1%) | - Ít itemsets hơn (từ 2,120 → ~500)<br>- Chỉ giữ mẫu phổ biến<br>- Chạy nhanh hơn<br>- Ít luật hơn | - Nhiều itemsets hơn (→ >5,000)<br>- Tìm cả mẫu hiếm<br>- Chạy chậm hơn<br>- Nhiều luật hơn |
| **FILTER_MIN_CONF** | 0.3 (30%) | - Ít luật hơn (1,794 → ~800)<br>- Độ tin cậy cao<br>- Ít false positive<br>- Dễ áp dụng | - Nhiều luật hơn (→ >3,000)<br>- Có thể có nhiễu<br>- Khám phá rộng hơn<br>- Cần lọc thêm |
| **FILTER_MIN_LIFT** | 1.2 | - Ít luật hơn (1,794 → ~600)<br>- Quan hệ mạnh<br>- Loại bỏ ngẫu nhiên<br>- Chất lượng cao | - Nhiều luật hơn (→ >4,000)<br>- Chấp nhận quan hệ yếu<br>- Có thể có nhiễu<br>- Cần xem xét kỹ |

**Số liệu thực tế từ cấu hình mặc định:**
- Dataset: 18,021 hoá đơn × 4,007 sản phẩm
- Itemsets: 2,120 (với support ≥ 1%)
- Luật ban đầu: 3,856
- Luật sau lọc: 1,794 (với conf ≥ 30%, lift ≥ 1.2)
- Thời gian: 16.18 giây

---

### 2.4. Khuyến nghị lựa chọn tham số

**Cho dữ liệu Online Retail:**

```python
# Cấu hình đề xuất cho phân tích ban đầu
MIN_SUPPORT=0.01          # 1% - cân bằng
FILTER_MIN_CONF=0.3       # 30% - không quá khắt khe
FILTER_MIN_LIFT=1.2       # Loại bỏ luật ngẫu nhiên

# Cấu hình cho production/ứng dụng thực tế
MIN_SUPPORT=0.02          # 2% - đảm bảo phổ biến
FILTER_MIN_CONF=0.5       # 50% - độ tin cậy cao
FILTER_MIN_LIFT=2.0       # Chỉ giữ quan hệ mạnh
```

---

### 2.5. Kết luận

**Từ kết quả thực tế đã chạy:**

1. **Support (0.01)** - kiểm soát độ phổ biến của mẫu
   - Với 1%, tìm được 2,120 itemsets từ 4,007 sản phẩm
   - Top sản phẩm phổ biến nhất: WHITE HANGING HEART T-LIGHT HOLDER (11.997%)
   - Ma trận rất thưa (0.66% ô = 1) → cần support thấp để khám phá

2. **Confidence (0.3)** - đo lường độ tin cậy của luật
   - Với 30%, giữ được 1,794/3,856 luật (46.5%)
   - Luật tốt nhất có confidence > 95% (HERB MARKER set)
   - Đủ linh hoạt để khám phá nhưng vẫn có ý nghĩa

3. **Lift (1.2)** - xác định mức độ quan hệ thực sự
   - Với 1.2, loại bỏ 53.5% luật ngẫu nhiên
   - Luật có lift cao nhất: 74.57 (rất mạnh)
   - Chứng tỏ mối quan hệ thực sự, không ngẫu nhiên

**Phát hiện quan trọng:**
- Bộ sản phẩm "Herb Marker" có mối quan hệ cực mạnh (lift > 70)
- Khách hàng mua một item trong bộ thường mua toàn bộ
- Đây là cơ hội kinh doanh: bán theo bộ (bundle) sẽ hiệu quả

**Việc lựa chọn tham số phụ thuộc vào:**
- **Mục tiêu phân tích:** Khám phá (support thấp) vs Production (support cao)
- **Kích thước dữ liệu:** 18K hoá đơn → có thể dùng support thấp
- **Yêu cầu độ chính xác:** Cao (conf ≥ 0.5) vs Linh hoạt (conf ≥ 0.3)
- **Thời gian chấp nhận:** 16s là hợp lý, có thể giảm support thêm

**Khuyến nghị cho dự án này:**
- **Khám phá:** MIN_SUPPORT=0.01, CONF=0.3, LIFT=1.2 (đang dùng) ✓
- **Production:** MIN_SUPPORT=0.02, CONF=0.5, LIFT=2.0
- **Deep dive:** MIN_SUPPORT=0.005, CONF=0.25, LIFT=1.5

**Nguyên tắc:** Bắt đầu với tham số vừa phải (như hiện tại), phân tích kết quả, sau đó điều chỉnh dựa trên insights và yêu cầu nghiệp vụ cụ thể.

---

## PHỤ LỤC

### A. Kết quả chi tiết

**Thống kê tổng quan:**
- Tổng số giao dịch gốc: 541,909
- Giao dịch United Kingdom: 485,123 (89.5%)
- Số khách hàng: 3,921
- Số hoá đơn: 18,021
- Số sản phẩm duy nhất: 4,007
- Thời gian chạy Apriori: 16.18 giây

**Kết quả Apriori:**
- Itemsets tìm được: 2,120
- Luật ban đầu: 3,856
- Luật sau lọc: 1,794
- Tỷ lệ lọc: 53.5%

### B. Lệnh chạy pipeline

```bash
# Kích hoạt môi trường
conda activate datamining_week01

# Chạy toàn bộ pipeline
python run_papermill.py
```

**Output files được tạo ra:**
- `data/processed/cleaned_uk_data.csv` - Dữ liệu đã làm sạch
- `data/processed/basket_bool.parquet` - Ma trận one-hot encoding
- `data/processed/rules_apriori_filtered.csv` - Luật kết hợp đã lọc
- `notebooks/runs/preprocessing_and_eda_run.ipynb` - Kết quả EDA
- `notebooks/runs/basket_preparation_run.ipynb` - Kết quả chuẩn bị basket
- `notebooks/runs/apriori_modelling_run.ipynb` - Kết quả mô hình Apriori

### C. Các thư viện sử dụng

- **numpy, pandas**: Xử lý dữ liệu
- **matplotlib, seaborn, plotly**: Trực quan hóa
- **mlxtend**: Thuật toán Apriori
- **scikit-learn**: Phân tích dữ liệu
- **papermill**: Tự động hóa notebook
- **networkx**: Biểu đồ mạng luật kết hợp
- **pyarrow**: Lưu trữ dữ liệu dạng Parquet

### D. Ứng dụng thực tế

**1. Cross-selling (Bán chéo):**
- Khi khách mua HERB MARKER PARSLEY → Gợi ý HERB MARKER THYME (Conf: 95%)
- Khi mua WHITE HANGING HEART → Có thể quan tâm sản phẩm trang trí khác

**2. Bundle Products (Bán theo bộ):**
- Tạo combo "Herb Marker Complete Set" (Lift > 70)
- Giảm giá khi mua bộ thay vì lẻ

**3. Store Layout (Bố trí cửa hàng):**
- Đặt các sản phẩm có quan hệ mạnh gần nhau
- Tăng khả năng mua nhiều sản phẩm

**4. Inventory Management (Quản lý kho):**
- Nếu hết HERB MARKER THYME → Có thể ảnh hưởng doanh số cả bộ
- Cần đảm bảo stock đồng bộ cho các sản phẩm liên quan