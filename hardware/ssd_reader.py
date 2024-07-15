from hardware.ssd_reader_interface import ISSDReader


class SSDReader(ISSDReader):
    def read(
            self,
            read_file_name,
            logical_bytes_address: int
    ) -> str:
        return ''
