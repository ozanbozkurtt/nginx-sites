import pandas as pd
import socket

# Excel dosyasını okuyun
file_path = "internal_with_access.xlsx"
sheets = ["Sheet1"]
#, "Stage_Nginx", "Prod_Nginx"]

# Her bir sayfayı okuyup filtreleyin
filtered_data = {}
for sheet in sheets:
    df = pd.read_excel(file_path, sheet_name=sheet)
    filtered_df = df[df["IP Restriction"] == "Any"][["Domain", "Endpoint"]]
    filtered_data[sheet] = filtered_df

# Her bir domain ve endpoint için DNS kontrolü yapın
results = []
for sheet, data in filtered_data.items():
    for index, row in data.iterrows():
        if pd.isna(row["Domain"]) or pd.isna(row["Endpoint"]):
            continue
        domains = row["Domain"].split(',')
        endpoint = row["Endpoint"]
        accessible_domains = []
        for domain in domains:
            domain = domain.strip()
            try:
                socket.gethostbyname(domain)  # Domain'i DNS ile kontrol et
                accessible_domains.append(f"{domain}{endpoint}")
            except socket.gaierror:
                pass
        accessible = bool(accessible_domains)  # Eğer erişilebilir domain varsa True, yoksa False
        results.append(
            {
                "Sheet": sheet,
                "Domain + Endpoint": ", ".join([f"{domain}{endpoint}" for domain in domains]),  # Domain'leri endpoint ile birleştirip stringe çeviririz
                "Accessible Domains": ", ".join(accessible_domains),
                "Accessible": accessible,
            }
        )

# Sonuçları bir DataFrame'e dönüştürün
results_df = pd.DataFrame(results)

# Sonuçları yeni bir Excel dosyasına yazdırın
output_path = "dns_accessibility_results.xlsx"
results_df.to_excel(output_path, index=False)

print(f"Erişim sonuçları '{output_path}' dosyasına yazdırıldı.")
