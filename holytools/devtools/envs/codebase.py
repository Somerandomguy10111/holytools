import os

# ----------------------------------------------

class RepoAnalysis:
    @staticmethod
    def get_sourcefpaths(repo_dirpath: str) -> list[str]:
        fpaths = []
        for parent_dirpath, folders, files in os.walk(repo_dirpath):
            ignored_dirpaths = RepoAnalysis.ignored_dirpaths()
            if any([x in parent_dirpath for x in ignored_dirpaths]):
                continue

            py_filenames = [fn for fn in files if fn.endswith('.py')]
            for fname in py_filenames:
                fp = os.path.join(parent_dirpath, fname)
                fpaths.append(fp)

        return fpaths

    @staticmethod
    def find_venv(repo_dirpath : str) -> str:
        child_names = os.listdir(repo_dirpath)
        child_paths = [os.path.join(repo_dirpath, n) for n in child_names]
        dirpaths = [x for x in child_paths if os.path.isdir(x)]

        for d in dirpaths:
            python_fpath = os.path.join(d, 'bin', 'python')
            is_venv = os.path.isfile(python_fpath)
            if is_venv:
                return d

        raise FileNotFoundError(f'No virtual environment found in {repo_dirpath}. ')

    @staticmethod
    def ignored_dirpaths() -> list[str]:
        return ['build', '.venv']