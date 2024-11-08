import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


def load_data(file_names: list[str]) -> list[pd.DataFrame]:
    data_frames = []
    for fn in file_names:
        with open(fn, "r", encoding="utf-8") as f:
            df = pd.read_csv(f)
            data_frames.append(df)
    return data_frames


def get_nan_count(df: pd.DataFrame) -> dict[str, int]:
    nans = dict()
    for attr in df.columns:
        nans[attr] = len(df[attr]) - df[attr].count()
        if nans[attr] / len(df[attr]) > 0:
            print(f"NaN Values {attr}: {nans[attr]} / {len(df[attr])}")
    return nans


if __name__ == "__main__":
    data_folder = "./data"
    data_files = [
        f"{data_folder}/Organizations.csv",
        # f"{data_folder}/ProductCategories.csv",
        f"{data_folder}/ProductItems.csv",
        f"{data_folder}/Products.csv",
        f"{data_folder}/Receipts.csv"
    ]
    data_frames = load_data(data_files)

    # Organizations processing / analysis
    print("Organizations:")
    org_df = data_frames[0]
    org_df.drop(["color", "image", "image_content_type"], axis=1, inplace=True)
    org_df["created_date"] = pd.to_datetime(org_df["created_date"], errors='coerce')
    org_df["last_modified_date"] = pd.to_datetime(org_df["last_modified_date"], errors='coerce')
    # get_nan_count(org_df)
    print(org_df.head())

    # Product items processing / analysis
    print("Product items:")
    prod_it_df = data_frames[1]
    prod_it_df.drop([
        "created_date", 
        "last_modified_date", 
        "created_by",
        "last_modified_by"
    ], axis=1, inplace=True)
    prod_it_df["product_id"] = prod_it_df["product_id"].astype(int)
    prod_it_df["fs_receipt_id"] = prod_it_df["fs_receipt_id"].astype(int)
    # get_nan_count(prod_it_df)
    print(prod_it_df.head())

    # Products processing / analysis
    print("Products:")
    prods_df = data_frames[2]
    prods_df["price"] = pd.to_numeric(prods_df["price"], errors='coerce')
    prods_df["vat_rate"] = pd.to_numeric(prods_df["vat_rate"], errors='coerce')
    prods_df["organization_id"] = prods_df["organization_id"].astype(int)
    prods_df["created_date"] = pd.to_datetime(prods_df["created_date"], errors='coerce')
    prods_df["last_modified_date"] = pd.to_datetime(prods_df["last_modified_date"], errors='coerce')
    prods_df["is_overridden"] = prods_df["is_overridden"].replace("b'\\x00'", 0)
    prods_df["is_overridden"] = prods_df["is_overridden"].replace("b'\\x01'", 1)
    print(prods_df.head())
    # get_nan_count(prods_df)

    # Receipts processing / analysis
    print("Receipts:")
    receipts_df = data_frames[3]
    receipts_df.drop([
        "customer_id", 
        "invoice_number", 
        "paragon_number",
        "org_postal_code",
        "unit_name"
    ], axis=1, inplace=True)
    receipts_df["issue_date"] = pd.to_datetime(receipts_df["issue_date"], errors='coerce', format="%d.%m.%Y %H:%M:%S")
    receipts_df["create_date"] = pd.to_datetime(receipts_df["create_date"], errors='coerce', format="%d.%m.%Y %H:%M:%S")
    receipts_df["created_date"] = pd.to_datetime(receipts_df["created_date"], errors='coerce')
    receipts_df["last_modified_date"] = pd.to_datetime(receipts_df["last_modified_date"], errors='coerce')
    receipts_df["organization_id"] = receipts_df["organization_id"].astype(int)
    # get_nan_count(receipts_df)
    print(receipts_df.head())
