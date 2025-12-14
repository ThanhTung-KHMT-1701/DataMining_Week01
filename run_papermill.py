import papermill as pm
import os

os.makedirs("notebooks/runs", exist_ok=True)

# run_preprocessing_and_eda.py
pm.execute_notebook(
    "notebooks/preprocessing_and_eda.ipynb",
    "notebooks/runs/preprocessing_and_eda_run.ipynb",
    parameters=dict(
        DATA_PATH="data/raw/online_retail.csv",
        COUNTRY="United Kingdom",
        OUTPUT_DIR="data/processed",
        PLOT_REVENUE=True,         # Hiển thị biểu đồ doanh thu
        PLOT_TIME_PATTERNS=True,   # Hiển thị xu hướng theo thời gian
        PLOT_PRODUCTS=True,        # Hiển thị phân tích sản phẩm
        PLOT_CUSTOMERS=True,       # Hiển thị phân tích khách hàng
        PLOT_RFM=True,            # Hiển thị phân tích RFM
    ),
    kernel_name="python3",
)

# run_basket_preparation.py

pm.execute_notebook(
    "notebooks/basket_preparation.ipynb",
    "notebooks/runs/basket_preparation_run.ipynb",
    parameters=dict(
        CLEANED_DATA_PATH="data/processed/cleaned_uk_data.csv",
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",
        INVOICE_COL="InvoiceNo",
        ITEM_COL="Description",
        QUANTITY_COL="Quantity",
        THRESHOLD=1,
    ),
    kernel_name="python3",
)

# Chạy Notebook Apriori Modelling
pm.execute_notebook(
    "notebooks/apriori_modelling.ipynb",
    "notebooks/runs/apriori_modelling_run.ipynb",
    parameters=dict(
        BASKET_BOOL_PATH="data/processed/basket_bool.parquet",
        RULES_OUTPUT_PATH="data/processed/rules_apriori_filtered.csv",

        # Tham số Apriori
        MIN_SUPPORT=0.01,
        MAX_LEN=3,

        # Generate rules
        METRIC="lift",
        MIN_THRESHOLD=1.0,

        # Lọc luật
        FILTER_MIN_SUPPORT=0.01,
        FILTER_MIN_CONF=0.3,
        FILTER_MIN_LIFT=1.2,
        FILTER_MAX_ANTECEDENTS=2,
        FILTER_MAX_CONSEQUENTS=1,

        # Số luật để vẽ
        TOP_N_RULES=20,

        # Bật tất cả biểu đồ để xem kết quả phân tích
        PLOT_TOP_LIFT=True,        # Top luật theo Lift
        PLOT_TOP_CONF=True,        # Top luật theo Confidence
        PLOT_SCATTER=True,         # Scatter plot Support-Confidence
        PLOT_NETWORK=True,         # Biểu đồ mạng luật kết hợp
        PLOT_PLOTLY_SCATTER=True,  # Scatter plot tương tác (Plotly)
    ),
    kernel_name="python3",
)

# Chạy Notebook Thử Nghiệm Chủ Đề 07 - Phân tích luật niche
pm.execute_notebook(
    "notebooks/ThuNghiem_ChuDe07.ipynb",
    "notebooks/runs/ThuNghiem_ChuDe07_run.ipynb",
    parameters=dict(
        RULES_PATH="data/processed/rules_apriori_filtered.csv",
        OUTPUT_DIR="data/processed",

        # Ngưỡng phân tích luật niche
        LOW_SUPPORT_THRESHOLD=0.02,  # Support dưới 2% = niche
        HIGH_LIFT_THRESHOLD=10.0,    # Lift trên 10 = liên kết mạnh
        TOP_N_RULES=20,              # Số luật top để phân tích chi tiết

        # Bật các biểu đồ phân tích
        PLOT_SUPPORT_LIFT_SCATTER=True,  # Scatter plot Support vs Lift
        PLOT_TOP_NICHE_RULES=True,       # Top luật niche
        PLOT_SEGMENT_ANALYSIS=True,      # Phân tích theo phân khúc
    ),
    kernel_name="python3",
)


print("Đã chạy xong pipeline")
