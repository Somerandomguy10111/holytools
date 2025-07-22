import os
import sysconfig

from holytools.devtools.envs.repo import RepoTools

# -----------------------------------------------------------------------

class EnvPaths:
    @staticmethod
    def get_env_sypaths(repo_dirpath : str) -> list[str]:
        stdlib_dirpath = EnvPaths.get_stdlib_dirpath()
        dynlib_dirpath = EnvPaths.get_dynlib_dirpath()
        sitepackages_dirpath = EnvPaths.get_sitepackages_dirpath(repo_dirpath=repo_dirpath)
        localinstalls = EnvPaths.get_editable_locations(repo_dirpath=repo_dirpath)

        return [repo_dirpath, stdlib_dirpath, dynlib_dirpath, sitepackages_dirpath] + localinstalls

    @staticmethod
    def get_stdlib_dirpath() -> str:
        return sysconfig.get_paths()['stdlib']

    @staticmethod
    def get_dynlib_dirpath() -> str:
        stdlib_dirpath = EnvPaths.get_stdlib_dirpath()
        return os.path.join(stdlib_dirpath, 'lib-dynload')

    @staticmethod
    def get_sitepackages_dirpath(repo_dirpath : str) -> str:
        venv_dirpath = RepoTools.find_venv(repo_dirpath=repo_dirpath)
        lib_dirpath = os.path.join(venv_dirpath, 'lib')
        pyfolder = os.listdir(lib_dirpath)[0]
        packages_dirpath = os.path.join(lib_dirpath, pyfolder, 'site-packages')

        if not os.path.isdir(packages_dirpath):
            raise ValueError(f'No site-packages found in {lib_dirpath}')

        return packages_dirpath

    @staticmethod
    def get_editable_locations(repo_dirpath: str) -> list[str]:
        sitepackage_dirpath = EnvPaths.get_sitepackages_dirpath(repo_dirpath=repo_dirpath)
        fnames = os.listdir(sitepackage_dirpath)
        fpaths = [os.path.join(sitepackage_dirpath, n) for n in fnames]
        pth_fpaths = [fp for fp in fpaths if fp.endswith('.pth')]

        locations = []
        for fp in pth_fpaths:
            with open(fp, 'r') as f:
                content = f.read()
                content = content.strip()
                if os.path.isdir(content):
                    locations.append(content)

        return locations

