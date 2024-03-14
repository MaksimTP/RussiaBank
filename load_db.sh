clickhouse-client --query "CREATE TABLE test_table (id UInt32, document_name String, document_url String, create_date String, modification_date String, chunk_number UInt32, chunk_embeding Array(Float32), chunk_text String) ENGINE Memory"
clickhouse-client -q "INSERT INTO test_table FORMAT CSV" < data.csv
