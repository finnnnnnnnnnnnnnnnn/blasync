# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Copyright (c) Stef van der Struijk <stefstruijk@protonmail.ch>



import bpy
import sys
import subprocess  # use Python executable (for pip usage)
from pathlib import Path  # Object-oriented filesystem paths since Python 3.4
import importlib
import site
import pprint

#TODO
#Make this good
#Also seperate this into its own thing
#This is all taken from https://github.com/NumesSanguis/Blender-ZMQ-add-on

class Pip:
    @classmethod
    def install(self, name: str, params=''):  # execute() is called when running the operator.
        # enable/import pip
        py_exec = self.ensure_pip(self)

        # update pip to latest version; not necessary anymore (tested 2.93 LTS & 3.3 LTS)
        if bpy.app.version[0] == 2 and bpy.app.version[1] < 91:
            self.update_pip(self, py_exec=py_exec)

        if self.import_module(self, name.replace('-', '_')) is False:
            self.install_package(self, py_exec, name, params)

    def import_module(self, name):
        #https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed
        # pprint.pp(sys.modules)
        if name in sys.modules:
            print(f"{name!r} is already installed and imported")
        elif (spec := importlib.util.find_spec(name)) is not None:
            print(f"{name!r} is already installed")
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
            print(f"{name!r} has been imported")
        else:
            return False

    def ensure_pip(self):
        # TODO check permission rights
        # TODO Windows ask for permission:
        # https://stackoverflow.com/questions/130763/request-uac-elevation-from-within-a-python-script

        # pip in Blender:
        # https://blender.stackexchange.com/questions/139718/install-pip-and-packages-from-within-blender-os-independently/
        # pip 2.81 issues: https://developer.blender.org/T71856

        # no pip enabled by default version < 2.81
        if bpy.app.version[0] == 2 and bpy.app.version[1] < 81:
            # find python binary OS independent (Windows: bin\python.exe; Linux: bin/python3.7m)
            py_path = Path(sys.prefix) / "bin"
            py_exec = str(next(py_path.glob("python*")))  # first file that starts with "python" in "bin" dir

            if subprocess.call([py_exec, "-m", "ensurepip"]) != 0:
                raise Exception("Couldn't activate pip.")

        # from 2.81 pip is enabled by default
        else:
            try:
                # will likely fail the first time, but works after `ensurepip.bootstrap()` has been called once
                import pip
                print("Pip imported")
            # pip not enabled
            except ModuleNotFoundError as e:
                # only first attempt will reach here
                print("Pip import failed with: ", e)
                print("Pip not activated, trying bootstrap()")
                try:
                    import ensurepip
                    ensurepip.bootstrap()
                except:  # catch *all* exceptions
                    e = sys.exc_info()[0]
                    print("Pip not activated, trying bootstrap()")
                    print("bootstrap failed with: ", e)

                print("Pip activated!")
            # 2.81 >= Blender < 2.91
            if bpy.app.version[0] == 2 and bpy.app.version[1] < 91:
                py_exec = bpy.app.binary_path_python
            # (tested on 2.93 LTS & 3.3 LTS) Blender >= 2.91
            else:
                py_exec = sys.executable

        return py_exec

    def update_pip(self, py_exec):
        print("Trying pip upgrade...")

        # pip update
        try:
            output = subprocess.check_output([py_exec, '-m', 'pip', 'install', '--upgrade', 'pip'])
            print(output)
        except subprocess.CalledProcessError as e:
            print("Couldn't update pip. Please restart Blender and try again.")
            raise Exception(f"Couldn't update pip. Please restart Blender and try again. \n {e.output}")
        print("Pip working!")

    def install_package(self, py_exec, name: str, params: str):
        print(f"Trying {name} install...")

        # pyzmq pip install
        try:
            command = [py_exec, '-m', 'pip', 'install', name] + params.split()
            print(f'Installing package {name} with "{" ".join(command)}"')
            output = subprocess.check_output((command))
            print(output)
        except subprocess.CalledProcessError as e:
            print("Couldn't install pyzmq.")
            raise Exception(e.output)

        print(f"{name} installed")