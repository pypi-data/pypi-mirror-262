from modelbest_sdk.file_format.mbtable_builder import MbTableBuilder


for i in range(10):
    builder = MbTableBuilder(f"test/partition_data/part_{i}.mbt")
    for j in range(100):
        builder.write(f"file_{i}_value_{j}")
    builder.add_metadata("meta_key", "meta_value")
    builder.flush()