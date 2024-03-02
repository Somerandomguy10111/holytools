# def read(fpath : str,
#          read_type : ReadType = ReadType.STR) -> Optional[Union[str, bytes]]:
#     if not os.path.isfile(fpath):
#         logging(f'No file found at: {fpath}')
#         return None
#
#     mode = 'r' if read_type.STR else 'rb'
#     with open(fpath, mode) as file:
#         return file.read()