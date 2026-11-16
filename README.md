# Deliverables-Milestone-1-Mid-Project-Pertemuan-7-Sebelum-UTS-

Link file impyb google drive Project Milestone 1
https://drive.google.com/drive/folders/1FQlHueqtcx2zFjMO-5ndDhe-r3Au3WUW?usp=drive_link

Link Video  Milestone 1
https://drive.google.com/drive/folders/1mZ0yy_Q1NJNL15Ho7Ti4FQrGWNBBZ8uu?usp=drive_link

 +---------------------------------------------------------------------------------------------------------+
    |                                    BIG DATA PLANNING CANVAS                                             |
    |                                Proyek: E-Commerce & Retail Analytics                                    |
    +------------------------------------+-----------------------------------+--------------------------------+
    | 1. BUSINESS PROBLEM & OBJECTIVES   | 3. DATA ARCHITECTURE & SCHEMAS    | 5. STORAGE BENCHMARK STRATEGY  |
    | - Masalah: Data transaksi e-commerce| - Main Fact Table (Structured):   | - Format CSV:                  |
    |   mengalami degradasi kualitas        `transactions.csv` (1.000.000 baris)|   Format tabel umum (besar &   |
    |   (5-10% data kotor/anomali).        - Dimension Table 1 (Master Data):  |   lambat dibaca).              |
    | - Dampak: Keputusan bisnis keliru.   `customers.csv` (50.000 baris)     | - Format JSONL:                |
    | - Tujuan: Pipeline cleansing data  | - Dimension Table 2 (Semi-struct):|   Format fleksibel untuk log   |
    |   skala besar & uji efisiensi        `clickstream.json` (200.000 events)|   event (ukuran paling boros). |
    |   format penyimpanan (Storage).     |                                   | - Format Apache Parquet:       |
    +------------------------------------+-----------------------------------+   Pemenang kompresi kolumnar   |
    | 2. BIG DATA CHARACTERISTICS (5V)   | 4. PROCESSING & PIPELINE          |   (ukuran hemat & query cepat).|
    | - Volume: Total ~1,25 Juta baris   | - Processing Engine:              +--------------------------------+
    | - Variety: Tabular (CSV) & JSON    |   Apache Spark (PySpark)          | 6. VALUE & STAKEHOLDERS        |
    | - Velocity: Log transaksi & klik   | - Veracity Actions:               | - Stakeholder: Tim Analyst,    |
    | - Veracity: Anomali 5% diuji       |   1. Deduplikasi transaction_id   |   Marketing, & Manajemen Toko. |
    | - Value: Keputusan presisi & hemat |   2. Drop Null kolom vital        | - Dampak: Biaya storage hemat, |
    |   biaya infrastruktur storage      |   3. Standarisasi nama kota       |   laporan penjualan akurat.    |
    |                                    |   4. Filter harga minus & thn 2099|                                |
    +------------------------------------+-----------------------------------+--------------------------------+
Blok 1: Business Problem & Objectives (Latar Belakang & Masalah Bisnis)

• Masalah Bisnis: Pertumbuhan transaksi e-commerce menghasilkan volume data yang masif, namun rentan tercemar data
  kotor (duplikasi, nilai kosong, tanggal masa depan, harga minus, dan penulisan kota yang tidak seragam).
• Tujuan Proyek:
    1. Membangun pipeline pembersihan data otomatis berbasis PySpark untuk memulihkan akurasi data transaksi
      (Veracity).
    2. Melakukan Storage Benchmark untuk menentukan format penyimpanan data terbaik (antara CSV, JSONL, dan Parquet)
      dalam hal efisiensi kapasitas disk dan kecepatan query.


Blok 2: Big Data Characteristics (Karakteristik 5V)

• Volume (Jumlah): Skala data mencapai skala jutaan baris (1.000.000 transaksi + 50.000 data pelanggan + 200.000 log
  clickstream).
• Variety (Keberagaman): Terdiri dari data terstruktur (Structured: tabel relasional CSV) dan data semi-terstruktur
  (Semi-Structured: payload JSON clickstream).
• Velocity (Kecepatan): Menggambarkan data log aktivitas klik dan transaksi yang masuk secara berkelanjutan dari
  web/aplikasi retail.
• Veracity (Kebersihan/Integritas): Terdapat injeksi anomali 5% kotor yang disengaja untuk menguji keandalan
  algoritma pembersihan data.
• Value (Nilai Manfaat): Menyediakan basis data bersih (Curated Data) yang siap digunakan untuk keputusan bisnis
  (analisis omzet, segmentasi pelanggan, evaluasi konversi).

Blok 3: Data Architecture & Schemas (Arsitektur 3 Dataset)

Menggunakan model dimensional (Star Schema) retail analytics:
1. Main Fact Table (transactions.csv - 1.000.000 baris): Berisi catatan kuantitatif penjualan (metrik: quantity,
  price, discount) serta foreign key pelanggan dan produk.
2. Dimension Table 1 (customers.csv - 50.000 baris): Master data pelanggan (profil demografis: age_group, gender,
  membership_tier, city).
3. Dimension Table 2 / Log Telemetri (clickstream.json - 200.000 events): Log aktivitas klik pengguna (halaman: home,
  product, cart, checkout).

Blok 4: Data Cleansing & Processing Pipeline (Teknologi Pemrosesan)
  Menggunakan Apache Spark (PySpark) untuk pemrosesan paralel terdistribusi:

• Duplicate Records: Menghapus duplikat ID transaksi (dropDuplicates(subset=['transaction_id'])).
• Missing Values: Mengeliminasi baris kosong pada data krusial (dropna(subset=['customer_id', 'timestamp',
    'category'])).
• Inconsistent Formatting: Menyeragamkan variasi penulisan kota (misal: "JKT", "jakarta", "DKI Jakarta" menjadi
  "Jakarta").
• Outliers & Invalid Values: Menghapus anomali harga negatif (misal: -250.000) dan tanggal masa depan yang mustahil
  (misal: 2099-12-31).

Blok 5: Storage & Benchmark Strategy (Evaluasi Penyimpanan)

Data bersih disimpan ke dalam 3 format berbeda untuk diuji:

• CSV: Format umum berbentuk tabel, namun ukuran file besar dan lambat saat dibaca kembali.
• JSONL: Format berbasis teks per baris yang fleksibel, namun memakan kapasitas penyimpanan paling besar.
• Parquet: Format kolumnar modern dengan kompresi bawaan (Snappy), memberikan ukuran file paling ringkas dan
  kecepatan baca query tercepat (column pruning).

Blok 6: Business Value & Stakeholders (Dampak & Pengguna)

• Target Pengguna: Tim Business Intelligence, Data Analyst, dan Divisi Marketing.
• Hasil Nyata:
      • Menghemat kapasitas server dan biaya penyimpanan cloud berkat penggunaan Parquet.
      • Memastikan laporan metrik penjualan bebas dari anomali data kotor.



    
