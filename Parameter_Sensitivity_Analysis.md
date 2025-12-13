# 7.3.4 Chủ đề 4: Phân tích độ nhạy tham số (Parameter Sensitivity)

## 🎯 Mục tiêu
Phân tích ảnh hưởng của tham số `min_support` đến kết quả thuật toán Apriori:
- Số lượng luật tìm được
- Chất lượng luật (confidence, lift)
- Các cụm sản phẩm (itemsets)

## 📊 Phương pháp thử nghiệm

### Tham số test
Chúng ta sẽ thử nghiệm với 4 giá trị `min_support` khác nhau:

| Kịch bản | min_support | Ý nghĩa |
|----------|-------------|---------|
| **Rất thấp** | 0.005 (0.5%) | Tìm cả mẫu hiếm |
| **Thấp** | 0.01 (1%) | Giá trị mặc định |
| **Trung bình** | 0.02 (2%) | Chỉ mẫu phổ biến |
| **Cao** | 0.03 (3%) | Rất phổ biến |

### Các tham số cố định
```python
MAX_LEN = 3
FILTER_MIN_CONF = 0.3
FILTER_MIN_LIFT = 1.2
FILTER_MAX_ANTECEDENTS = 2
FILTER_MAX_CONSEQUENTS = 1
```

---

## 🧪 Kết quả thử nghiệm

### Thử nghiệm 1: min_support = 0.01 (1%)

**Kết quả:**
```
Frequent itemsets: 2,120
Association rules (trước lọc): 3,856
Association rules (sau lọc): 1,794
Thời gian chạy: 52.14s
```

**Top 5 luật theo Lift:**
```
1. HERB MARKER PARSLEY, HERB MARKER ROSEMARY → HERB MARKER THYME
   Support: 0.0109, Confidence: 0.952, Lift: 74.567

2. HERB MARKER MINT, HERB MARKER THYME → HERB MARKER ROSEMARY
   Support: 0.0106, Confidence: 0.955, Lift: 74.502

3. HERB MARKER MINT, HERB MARKER THYME → HERB MARKER PARSLEY
   Support: 0.0104, Confidence: 0.940, Lift: 74.297

4. HERB MARKER PARSLEY, HERB MARKER THYME → HERB MARKER ROSEMARY
   Support: 0.0109, Confidence: 0.952, Lift: 74.244

5. HERB MARKER BASIL, HERB MARKER THYME → HERB MARKER ROSEMARY
   Support: 0.0107, Confidence: 0.951, Lift: 74.170
```

**Nhận xét:**
- ✅ **Ưu điểm:**
  - Tìm được nhiều mẫu nhất (2,120 itemsets)
  - Phát hiện các tổ hợp sản phẩm niche với Lift cực cao (74+)
  - Tốt cho phân tích khám phá sâu
  - Phát hiện series HERB MARKER có mối liên hệ rất mạnh
  
- ❌ **Nhược điểm:**
  - Thời gian tính toán lâu nhất (52.14s)
  - Quá nhiều luật (1,794) - khó quản lý và phân tích
  - Nhiều luật có thể không có ý nghĩa thực tế cao

---

### Thử nghiệm 2: min_support = 0.015 (1.5%)

**Kết quả:**
```
Frequent itemsets: 755
Association rules (trước lọc): 738
Association rules (sau lọc): 456
Thời gian chạy: 4.05s
```

**Top 5 luật theo Lift:**
```
1. REGENCY TEA PLATE GREEN → REGENCY TEA PLATE ROSES
   Support: 0.0156, Confidence: 0.836, Lift: 39.557

2. REGENCY TEA PLATE ROSES → REGENCY TEA PLATE GREEN
   Support: 0.0156, Confidence: 0.738, Lift: 39.557

3. SMALL MARSHMALLOWS PINK BOWL → SMALL DOLLY MIX DESIGN ORANGE BOWL
   Support: 0.0186, Confidence: 0.779, Lift: 27.529

4. SMALL DOLLY MIX DESIGN ORANGE BOWL → SMALL MARSHMALLOWS PINK BOWL
   Support: 0.0186, Confidence: 0.657, Lift: 27.529

5. WOODEN HEART CHRISTMAS SCANDINAVIAN → WOODEN STAR CHRISTMAS SCANDINAVIAN
   Support: 0.0204, Confidence: 0.723, Lift: 27.200
```

**Nhận xét:**
- ✅ **Ưu điểm:**
  - Cân bằng tốt hơn: 456 luật (có thể quản lý)
  - Thời gian chạy nhanh hơn nhiều (4.05s vs 52.14s)
  - Vẫn giữ được các luật có Lift cao
  
- ⚖️ **Đặc điểm:**
  - Bắt đầu lọc bỏ các mẫu quá hiếm
  - Tập trung vào sản phẩm phổ biến hơn (REGENCY series)
  - Số lượng luật hợp lý cho phân tích

---

### Thử nghiệm 3: min_support = 0.02 (2%) ⭐ KHUYẾN NGHỊ

**Kết quả:**
```
Frequent itemsets: 400
Association rules (trước lọc): 218
Association rules (sau lọc): 175
Thời gian chạy: 1.51s
```

**Top 5 luật theo Lift:**
```
1. WOODEN HEART CHRISTMAS SCANDINAVIAN → WOODEN STAR CHRISTMAS SCANDINAVIAN
   Support: 0.0204, Confidence: 0.723, Lift: 27.200

2. WOODEN STAR CHRISTMAS SCANDINAVIAN → WOODEN HEART CHRISTMAS SCANDINAVIAN
   Support: 0.0204, Confidence: 0.768, Lift: 27.200

3. ROSES REGENCY TEACUP AND SAUCER, GREEN REGENCY TEACUP AND SAUCER → PINK REGENCY TEACUP AND SAUCER
   Support: 0.0273, Confidence: 0.703, Lift: 18.043

4. PINK REGENCY TEACUP AND SAUCER, ROSES REGENCY TEACUP AND SAUCER → GREEN REGENCY TEACUP AND SAUCER
   Support: 0.0273, Confidence: 0.903, Lift: 17.455

5. PINK REGENCY TEACUP AND SAUCER, GREEN REGENCY TEACUP AND SAUCER → ROSES REGENCY TEACUP AND SAUCER
   Support: 0.0273, Confidence: 0.854, Lift: 16.101
```

**Nhận xét:**
- ✅ **Ưu điểm:**
  - **Số lượng luật tối ưu: 175** - đủ để phân tích, không quá nhiễu
  - **Thời gian xử lý rất nhanh: 1.51s**
  - Chỉ giữ lại mẫu phổ biến có ý nghĩa
  - Lift vẫn cao (27.2) - luật mạnh
  - **Cân bằng tốt nhất giữa số lượng, chất lượng và thời gian**
  
- ⚖️ **Đặc điểm:**
  - Tập trung vào sản phẩm best-seller
  - Phù hợp triển khai thực tế
  - Luật có độ tin cậy cao về mặt thống kê

---

### Thử nghiệm 4: min_support = 0.03 (3%)

**Kết quả:**
```
Frequent itemsets: 145
Association rules (trước lọc): 22
Association rules (sau lọc): 21
Thời gian chạy: 0.30s
```

**Top 5 luật theo Lift:**
```
1. GREEN REGENCY TEACUP AND SAUCER → PINK REGENCY TEACUP AND SAUCER
   Support: 0.0320, Confidence: 0.618, Lift: 15.865

2. PINK REGENCY TEACUP AND SAUCER → GREEN REGENCY TEACUP AND SAUCER
   Support: 0.0320, Confidence: 0.821, Lift: 15.865

3. PINK REGENCY TEACUP AND SAUCER → ROSES REGENCY TEACUP AND SAUCER
   Support: 0.0302, Confidence: 0.776, Lift: 14.635

4. ROSES REGENCY TEACUP AND SAUCER → PINK REGENCY TEACUP AND SAUCER
   Support: 0.0302, Confidence: 0.570, Lift: 14.635

5. GARDENERS KNEELING PAD CUP OF TEA → GARDENERS KNEELING PAD KEEP CALM
   Support: 0.0300, Confidence: 0.721, Lift: 14.476
```

**Nhận xét:**
- ✅ **Ưu điểm:**
  - Rất nhanh (0.30s)
  - Chỉ các sản phẩm bán chạy nhất
  - Ít noise
  - Confidence trung bình cao nhất (0.587)
  
- ❌ **Nhược điểm:**
  - **Quá ít luật (21)** - không đủ để phân tích đa dạng
  - Bỏ lỡ nhiều insight thú vị
  - Không phù hợp cho cross-selling đa dạng
  - Chỉ còn lại REGENCY series (mainstream)

---

## 📊 So sánh tổng quan

### Bảng tổng hợp

| Metric | min_support=0.01 | min_support=0.015 | min_support=0.02 ⭐ | min_support=0.03 |
|--------|------------------|-------------------|---------------------|------------------|
| **Frequent Itemsets** | 2,120 | 755 | 400 | 145 |
| **Rules (trước lọc)** | 3,856 | 738 | 218 | 22 |
| **Rules (sau lọc)** | 1,794 | 456 | **175** | 21 |
| **Thời gian (s)** | 52.14 | 4.05 | **1.51** | 0.30 |
| **Avg Confidence** | 0.535 | 0.514 | 0.499 | 0.587 |
| **Avg Lift** | 13.570 | 9.803 | 8.842 | 10.053 |
| **Max Lift** | **74.567** | 39.557 | 27.200 | 15.865 |

### Biểu đồ minh họa

```
Số lượng luật sau lọc theo min_support
│
│  ████████████████████████████████████████ (1,794)
│  ████████████████████████████████████████
│  ████████████████████████████████████████
│  ████████████████████████████████████████
│            ██████████ (456)
│            ██████████
│                 ███ (175) ⭐
│                  (21)
└─────────────────────────────────────────
  0.01      0.015     0.02      0.03
```

---

## 🎓 Quan sát & Phân tích

### 1. Số lượng luật
- **Xu hướng:** Giảm mạnh khi tăng min_support (1,794 → 456 → 175 → 21)
- **Lý do:** Support cao → ít itemset đạt ngưỡng → ít luật được sinh
- **Insight:** "Sweet spot" nằm ở **min_support = 0.02** (175 luật)

### 2. Chất lượng luật

**Confidence:**
- Khá ổn định (0.499 - 0.587)
- Cao nhất ở min_support = 0.03 (0.587) nhưng có quá ít luật
- min_support = 0.02 vẫn đạt 0.499 - chấp nhận được

**Lift:**
- **Avg Lift cao nhất** ở min_support = 0.01 (13.570)
- **Max Lift giảm** khi tăng min_support: 74.567 → 39.557 → 27.200 → 15.865
- **Insight:** min_support thấp phát hiện được mẫu hiếm có Lift cực cao (HERB MARKER: 74+)

### 3. Cụm sản phẩm

**min_support = 0.01 (thấp):**
- Phát hiện nhiều cụm nhỏ, đa dạng
- HERB MARKER series (niche products)
- Tốt cho: Niche marketing, long-tail products

**min_support = 0.02-0.03 (cao):**
- Chỉ còn cụm lớn, mainstream
- REGENCY TEACUP series (best-sellers)
- CHRISTMAS SCANDINAVIAN (seasonal items)
- Tốt cho: Mass market, mainstream promotion

### 4. Thời gian xử lý
- **Giảm mạnh:** 52.14s → 4.05s → 1.51s → 0.30s
- **Trade-off:** Thời gian vs Số lượng insight
- **min_support = 0.02:** Tối ưu (1.51s, đủ nhanh cho production)

### 5. Patterns phát hiện được

**Patterns độc đáo ở min_support thấp (0.01):**
- HERB MARKER series: Lift 74+ (cực mạnh)
- Các combo sản phẩm niche

**Patterns phổ biến ở mọi ngưỡng:**
- REGENCY TEACUP AND SAUCER (PINK, GREEN, ROSES)
- WOODEN CHRISTMAS SCANDINAVIAN items
- GARDENERS KNEELING PAD series

---

## 💡 Rút ra "Ngưỡng hợp lý" cho bài toán

### Tiêu chí đánh giá
1. **Số lượng luật:** 50-200 luật (đủ để phân tích, không quá nhiễu) ✅
2. **Chất lượng:** Confidence > 30%, Lift > 1.2 ✅
3. **Thời gian:** < 2 phút ✅
4. **Ý nghĩa thực tế:** Phải có sản phẩm đủ phổ biến để triển khai ✅

### 🏆 Khuyến nghị

#### Cho bài toán này (Online Retail UK):
```python
MIN_SUPPORT = 0.02  # 2% - Tối ưu cho dataset này ⭐
```

**Lý do:**
- ✅ Tìm được **400 frequent itemsets**
- ✅ Sinh ra **175 luật chất lượng** (đạt tiêu chí 50-200)
- ✅ Thời gian chạy rất nhanh: **1.51 giây** 
- ✅ Cân bằng tốt nhất giữa mẫu phổ biến và đa dạng
- ✅ Đủ luật để triển khai nhiều chiến lược marketing
- ✅ Avg Confidence: 0.499, Avg Lift: 8.842 - Chất lượng tốt
- ✅ Max Lift: 27.2 - Vẫn có luật mạnh
- ✅ Phù hợp cho production deployment

#### So sánh với các giá trị khác:

| Tiêu chí | min_support=0.01 | min_support=0.015 | min_support=0.02 ⭐ | min_support=0.03 |
|----------|------------------|-------------------|---------------------|------------------|
| Số luật | ❌ Quá nhiều (1,794) | ⚠️ Hơi nhiều (456) | ✅ Vừa phải (175) | ❌ Quá ít (21) |
| Thời gian | ❌ Chậm (52s) | ✅ Nhanh (4s) | ✅ Rất nhanh (1.5s) | ✅ Cực nhanh (0.3s) |
| Chất lượng | ✅ Lift cao nhất | ✅ Tốt | ✅ Tốt | ⚠️ Ít đa dạng |
| Triển khai | ❌ Khó quản lý | ⚠️ Có thể | ✅ Dễ dàng | ❌ Thiếu options |

#### Khi nào dùng min_support khác?

**min_support = 0.01 (1%)** - Khi:
- Muốn khám phá sâu các mẫu hiếm
- Có nhiều thời gian tính toán và phân tích
- Quan tâm đến niche products và long-tail
- Research và exploratory analysis
- **Ví dụ thực tế:** Phân tích cho cửa hàng chuyên sản phẩm đặc biệt

**min_support = 0.015 (1.5%)** - Khi:
- Muốn cân bằng giữa 0.01 và 0.02
- Cần nhiều luật hơn nhưng không quá nhiều
- **Ví dụ thực tế:** Phân tích cho chuỗi cửa hàng vừa và nhỏ

**min_support = 0.02 (2%)** - ⭐ KHUYẾN NGHỊ - Khi:
- Triển khai recommendation system production
- Cần kết quả nhanh và đáng tin cậy
- Tập trung vào sản phẩm phổ biến
- **Ví dụ thực tế:** Website e-commerce, mobile app, email marketing

**min_support = 0.03 (3%)** - Khi:
- Chỉ quan tâm sản phẩm best-seller
- Cần kết quả cực nhanh cho dashboard/report
- Muốn ít luật nhưng chắc chắn
- **Ví dụ thực tế:** Quick insights cho management meeting

---

## 🔬 Script để chạy thử nghiệm

### File đã tạo sẵn: `test_parameter_sensitivity.py`

Script tự động test với các giá trị min_support khác nhau và so sánh kết quả.

**Chạy script:**
```bash
cd C:\KHMT\DataMining\DataMining_Week01
conda activate shopping_env
python test_parameter_sensitivity.py
```

**Output:**
- Kết quả chi tiết cho từng test được in ra console
- File CSV: `data/processed/parameter_sensitivity_results.csv`
- Bảng so sánh tổng hợp
- Biểu đồ ASCII trực quan
- Khuyến nghị tham số tối ưu

**Kết quả đã chạy (December 13, 2025):**
```
Testing min_support = 0.01 (1.0%)
✅ RESULTS:
   Frequent itemsets: 2,120
   Rules (before filter): 3,856
   Rules (after filter): 1,794
   Time: 52.14s

Testing min_support = 0.015 (1.5%)
✅ RESULTS:
   Frequent itemsets: 755
   Rules (after filter): 456
   Time: 4.05s

Testing min_support = 0.02 (2.0%) ⭐
✅ RESULTS:
   Frequent itemsets: 400
   Rules (after filter): 175
   Time: 1.51s

Testing min_support = 0.03 (3.0%)
✅ RESULTS:
   Frequent itemsets: 145
   Rules (after filter): 21
   Time: 0.30s

⭐ RECOMMENDED min_support: 0.020 (2.0%)
```

---

## 📝 Kết luận

### Findings chính:

1. **Mối quan hệ nghịch đảo rõ ràng**
   - min_support ↑ → số luật ↓ (giảm từ 1,794 → 21)
   - Đúng với lý thuyết Apriori

2. **Điểm tối ưu được xác định**
   - **min_support = 0.02 (2%)** là lựa chọn tốt nhất cho dataset Online Retail UK
   - Cân bằng tốt nhất: 175 luật, 1.51s, Lift trung bình 8.842

3. **Trade-off quan trọng**
   - **Số lượng vs Chất lượng:** Nhiều luật ≠ tốt hơn
   - **Thời gian vs Insight:** Support thấp tốn thời gian nhưng phát hiện mẫu hiếm
   - **Phổ biến vs Niche:** Support cao tập trung mainstream, thấp khám phá niche

4. **Patterns có giá trị**
   - **HERB MARKER series:** Lift 74+ (chỉ ở min_support=0.01)
   - **REGENCY TEACUP series:** Xuất hiện ở mọi ngưỡng - sản phẩm cốt lõi
   - **CHRISTMAS items:** Mối liên hệ mạnh, phù hợp seasonal marketing

5. **Không có giá trị "đúng duy nhất"**
   - Tùy thuộc mục tiêu business:
     - Research & Discovery → min_support thấp (0.01)
     - Production & Deployment → min_support vừa (0.02) ⭐
     - Quick Insights → min_support cao (0.03)

### Đề xuất cho business:

#### Phase 1: Exploration (Khám phá)
```python
MIN_SUPPORT = 0.01  # Phát hiện nhiều patterns, bao gồm niche
```
- Dùng cho: Market research, phân tích sâu
- Output: Báo cáo chi tiết, phát hiện cơ hội mới

#### Phase 2: Development (Phát triển)
```python
MIN_SUPPORT = 0.015  # Cân bằng giữa khám phá và thực tế
```
- Dùng cho: Xây dựng recommendation engine
- Output: Candidate rules cho testing

#### Phase 3: Production (Triển khai) ⭐
```python
MIN_SUPPORT = 0.02  # Tối ưu cho deployment
```
- Dùng cho: Website, mobile app, email campaigns
- Output: 175 luật chất lượng, xử lý nhanh

#### Phase 4: Reporting (Báo cáo)
```python
MIN_SUPPORT = 0.03  # Chỉ top insights
```
- Dùng cho: Dashboard cho management
- Output: Các luật best-seller rõ ràng

### Ứng dụng cụ thể:

1. **Recommendation System:**
   - Dùng min_support = 0.02
   - Hiển thị "Frequently bought together"
   - Update hàng tuần dựa trên sales data mới

2. **Store Layout Optimization:**
   - Phân tích với min_support = 0.015-0.02
   - Đặt sản phẩm có lift cao gần nhau
   - Ví dụ: REGENCY TEACUP series cùng khu vực

3. **Bundle Promotions:**
   - Tạo combo từ luật có confidence > 0.7
   - Ví dụ: "PINK + GREEN REGENCY TEACUP - Save 20%"

4. **Seasonal Campaigns:**
   - Q4: CHRISTMAS SCANDINAVIAN bundles (Lift: 27.2)
   - Chuẩn bị inventory theo patterns

### Next steps - Mở rộng phân tích:

- [ ] **Test thêm tham số:**
  - min_confidence: (0.2, 0.3, 0.4, 0.5)
  - min_lift: (1.0, 1.5, 2.0, 3.0)
  - MAX_LEN: (2 vs 3 vs 4 items)

- [ ] **Phân tích theo segment:**
  - Customers RFM groups
  - Seasonal trends (Q1, Q2, Q3, Q4)
  - Product categories

- [ ] **So sánh algorithms:**
  - Apriori vs FP-Growth (speed comparison)
  - Apriori vs Eclat

- [ ] **A/B Testing:**
  - Deploy recommendations với min_support=0.02
  - Đo lường conversion rate, basket size

### Key Takeaways:

> 💡 **min_support = 0.02 (2%)** là lựa chọn tối ưu cho dataset Online Retail UK, cung cấp 175 luật chất lượng cao trong 1.51 giây, phù hợp cho cả phân tích và triển khai production.

> 📊 Không có tham số "hoàn hảo" - cần điều chỉnh dựa trên mục tiêu cụ thể, thời gian xử lý, và yêu cầu business.

> 🎯 REGENCY TEACUP series và CHRISTMAS SCANDINAVIAN items là các product families mạnh nhất, nên được ưu tiên trong chiến lược marketing.

---

**Người thực hiện:** Nhóm 11 - Data Mining Week 01  
**Thành viên:**
- Nguyễn Hòa Bình - 1671040004
- Đinh Tấn Phát - 1671040022  
- Lưu Thanh Tùng - 1771040029

**Ngày thực hiện:** December 13, 2025  
**Dataset:** Online Retail (UCI) - 485,123 transactions UK
