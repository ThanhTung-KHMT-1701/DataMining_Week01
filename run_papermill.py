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
        PLOT_REVENUE=True,         # Bật để hiển thị biểu đồ
        PLOT_TIME_PATTERNS=True,
        PLOT_PRODUCTS=True,
        PLOT_CUSTOMERS=True,
        PLOT_RFM=True,
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

        # === Tham số Apriori ===
        # MIN_SUPPORT: Tỷ lệ tối thiểu giao dịch chứa itemset
        # - Cao (0.02): Chỉ tìm mẫu phổ biến, ít luật, nhanh
        # - Thấp (0.005): Nhiều mẫu, nhiều luật, chậm hơn
        MIN_SUPPORT=0.01,
        MAX_LEN=3,

        # Generate rules
        METRIC="lift",
        MIN_THRESHOLD=1.0,

        # === Lọc luật (Q2: Thay đổi các tham số này) ===
        # FILTER_MIN_SUPPORT: Support tối thiểu của luật (0.01 = 1%)
        FILTER_MIN_SUPPORT=0.01,
        
        # FILTER_MIN_CONF: Confidence tối thiểu (xác suất B khi có A)
        # - Cao (0.5): Luật tin cậy, phù hợp recommendation
        # - Thấp (0.2): Nhiều luật, có thể kém tin cậy
        FILTER_MIN_CONF=0.3,
        
        # FILTER_MIN_LIFT: Lift tối thiểu (mức độ liên kết)
        # - Lift > 1: A và B có liên quan dương
        # - Cao (2.0): Mối liên hệ mạnh, ít luật
        # - Thấp (1.0): Nhiều luật, bao gồm cả luật yếu
        FILTER_MIN_LIFT=1.2,
        
        FILTER_MAX_ANTECEDENTS=2,
        FILTER_MAX_CONSEQUENTS=1,

        # Số luật để vẽ
        TOP_N_RULES=20,

        # Bật tất cả plot để hiển thị biểu đồ
        PLOT_TOP_LIFT=True,
        PLOT_TOP_CONF=True,
        PLOT_SCATTER=True,
        PLOT_NETWORK=True,
        PLOT_PLOTLY_NETWORK=True,
        PLOT_PLOTLY_SCATTER=True,  
    ),
    kernel_name="python3",
)


print("Đã chạy xong pipeline")
