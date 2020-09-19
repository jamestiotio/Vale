import unittest
import subprocess
import os.path
import os
import sys
import shutil
import glob

from typing import Dict, Any, List, Callable


def procrun(args: List[str], **kwargs) -> subprocess.CompletedProcess:
    # print("Running: " + " ".join(args))
    return subprocess.run(args, capture_output=True, text=True, **kwargs)


PATH_TO_SAMPLES = "../Valestrom/Samples/test/main/resources/"

class ValeTest(unittest.TestCase):
    GENPATH: str = os.environ.get('GENPATH', ".")

    def valec(self,
              in_filepaths: List[str],
              o_files_dir: str,
              exe_name: str,
              region_override: str) -> subprocess.CompletedProcess:
        assert self.GENPATH
        return procrun(
            ["python3.8", f"{self.GENPATH}/valec.py", "--verify", "--llvmir", "--census", "--flares", "--region-override", region_override, "--output-dir",
             o_files_dir, "-o", exe_name] + in_filepaths)

    def exec(self, exe_file: str) -> subprocess.CompletedProcess:
        return procrun([f"./{exe_file}"])

    @classmethod
    def setUpClass(cls) -> None:
        print(
            f"Using valec from {cls.GENPATH}. " +
            "Set GENPATH env var if this is incorrect",
            file=sys.stderr
        )

    def setUp(self) -> None:
        self.GENPATH: str = type(self).GENPATH

    def compile_and_execute(
            self, in_filepaths: List[str], region_override: str) -> subprocess.CompletedProcess:
        first_vale_filepath = in_filepaths[0]
        file_name_without_extension = os.path.splitext(os.path.basename(first_vale_filepath))[0]
        build_dir = f"test/test_build/{file_name_without_extension}_build"

        proc = self.valec(in_filepaths, build_dir, file_name_without_extension, region_override)
        self.assertEqual(proc.returncode, 0,
                         f"valec couldn't compile {in_filepaths}:\n" +
                         proc.stdout + "\n" + proc.stderr)

        exe_file = f"{build_dir}/{file_name_without_extension}"

        proc = self.exec(exe_file)
        return proc

    def compile_and_execute_and_expect_return_code(
        self, vale_files: List[str], region_override: str, expected_return_code) -> None:
        proc = self.compile_and_execute(vale_files, region_override)
        # print(proc.stdout)
        # print(proc.stderr)
        self.assertEqual(proc.returncode, expected_return_code,
                         f"Unexpected result: {proc.returncode}\n" + proc.stdout + proc.stderr)

    def test_assist_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "assist", 7)
    def test_unsafefast_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "unsafe-fast", 7)
    def test_resilientv0_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "resilient-v0", 7)
    def test_resilientv1_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "resilient-v1", 7)
    def test_resilientv2_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "resilient-v2", 7)
    def test_naiverc_addret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/addret.vale"], "naive-rc", 7)

    def test_assist_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "assist", 5)
    def test_unsafefast_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "unsafe-fast", 5)
    def test_resilientv0_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "resilient-v0", 5)
    def test_resilientv1_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "resilient-v1", 5)
    def test_resilientv2_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "resilient-v2", 5)
    def test_naiverc_immstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/immstruct.vale"], "naive-rc", 5)

    def test_assist_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "assist", 5)
    def test_unsafefast_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "unsafe-fast", 5)
    def test_resilientv0_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "resilient-v0", 5)
    def test_resilientv1_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "resilient-v1", 5)
    def test_resilientv2_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "resilient-v2", 5)
    def test_naiverc_memberrefcount(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/memberrefcount.vale"], "naive-rc", 5)

    def test_assist_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "assist", 42)
    def test_unsafefast_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "unsafe-fast", 42)
    def test_resilientv0_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "resilient-v0", 42)
    def test_resilientv1_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "resilient-v1", 42)
    def test_resilientv2_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "resilient-v2", 42)
    def test_naiverc_bigimmstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/bigimmstruct.vale"], "naive-rc", 42)

    def test_assist_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "assist", 8)
    def test_unsafefast_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "unsafe-fast", 8)
    def test_resilientv0_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "resilient-v0", 8)
    def test_resilientv1_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "resilient-v1", 8)
    def test_resilientv2_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "resilient-v2", 8)
    def test_naiverc_mutstruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstruct.vale"], "naive-rc", 8)

    def test_assist_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "assist", 42)
    def test_unsafefast_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "unsafe-fast", 42)
    def test_resilientv0_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "resilient-v0", 42)
    def test_resilientv1_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "resilient-v1", 42)
    def test_resilientv2_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "resilient-v2", 42)
    def test_naiverc_lambda(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambda.vale"], "naive-rc", 42)

    def test_assist_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "assist", 42)
    def test_unsafefast_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "unsafe-fast", 42)
    def test_resilientv0_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "resilient-v0", 42)
    def test_resilientv1_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "resilient-v1", 42)
    def test_resilientv2_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "resilient-v2", 42)
    def test_naiverc_if(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/if.vale"], "naive-rc", 42)

    def test_assist_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "assist", 42)
    def test_unsafefast_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "unsafe-fast", 42)
    def test_resilientv0_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "resilient-v0", 42)
    def test_resilientv1_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "resilient-v1", 42)
    def test_resilientv2_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "resilient-v2", 42)
    def test_naiverc_mutlocal(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/mutlocal.vale"], "naive-rc", 42)

    def test_assist_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "assist", 42)
    def test_unsafefast_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "unsafe-fast", 42)
    def test_resilientv0_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "resilient-v0", 42)
    def test_resilientv1_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "resilient-v1", 42)
    def test_resilientv2_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "resilient-v2", 42)
    def test_naiverc_while(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/while/while.vale"], "naive-rc", 42)

    def test_assist_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "assist", 8)
    def test_unsafefast_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "unsafe-fast", 8)
    def test_resilientv0_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "resilient-v0", 8)
    def test_resilientv1_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "resilient-v1", 8)
    def test_resilientv2_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "resilient-v2", 8)
    def test_naiverc_constraintRef(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/constraintRef.vale"], "naive-rc", 8)

    def test_assist_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "assist", 42)
    def test_unsafefast_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "unsafe-fast", 42)
    def test_resilientv0_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "resilient-v0", 42)
    def test_resilientv1_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "resilient-v1", 42)
    def test_resilientv2_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "resilient-v2", 42)
    def test_naiverc_knownsizeimmarray(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/knownsizeimmarray.vale"], "naive-rc", 42)

    def test_assist_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "assist", 42)
    def test_unsafefast_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "unsafe-fast", 42)
    def test_resilientv0_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "resilient-v0", 42)
    def test_resilientv1_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "resilient-v1", 42)
    def test_resilientv2_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "resilient-v2", 42)
    def test_naiverc_imminterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/imminterface.vale"], "naive-rc", 42)

    def test_assist_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "assist", 42)
    def test_unsafefast_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "unsafe-fast", 42)
    def test_resilientv0_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "resilient-v0", 42)
    def test_resilientv1_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "resilient-v1", 42)
    def test_resilientv2_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "resilient-v2", 42)
    def test_naiverc_mutinterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/virtuals/mutinterface.vale"], "naive-rc", 42)

    def test_assist_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "assist", 42)
    def test_unsafefast_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "unsafe-fast", 42)
    def test_resilientv0_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "resilient-v0", 42)
    def test_resilientv1_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "resilient-v1", 42)
    def test_resilientv2_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "resilient-v2", 42)
    def test_naiverc_mutstructstore(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/structs/mutstructstore.vale"], "naive-rc", 42)

    def test_assist_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "assist", 3)
    def test_unsafefast_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "unsafe-fast", 3)
    def test_resilientv0_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "resilient-v0", 3)
    def test_resilientv1_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "resilient-v1", 3)
    def test_resilientv2_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "resilient-v2", 3)
    def test_naiverc_immusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusa.vale"], "naive-rc", 3)

    def test_assist_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "assist", 5)
    def test_unsafefast_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "unsafe-fast", 5)
    def test_resilientv0_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "resilient-v0", 5)
    def test_resilientv1_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "resilient-v1", 5)
    def test_resilientv2_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "resilient-v2", 5)
    def test_naiverc_immusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/immusalen.vale"], "naive-rc", 5)

    def test_assist_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "assist", 3)
    def test_unsafefast_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "unsafe-fast", 3)
    def test_resilientv0_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "resilient-v0", 3)
    def test_resilientv1_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "resilient-v1", 3)
    def test_resilientv2_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "resilient-v2", 3)
    def test_naiverc_mutusa(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusa.vale"], "naive-rc", 3)

    def test_assist_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "assist", 5)
    def test_unsafefast_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "unsafe-fast", 5)
    def test_resilientv0_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "resilient-v0", 5)
    def test_resilientv1_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "resilient-v1", 5)
    def test_resilientv2_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "resilient-v2", 5)
    def test_naiverc_mutusalen(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/mutusalen.vale"], "naive-rc", 5)

    def test_assist_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "assist", 42)
    def test_unsafefast_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "unsafe-fast", 42)
    def test_resilientv0_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "resilient-v0", 42)
    def test_resilientv1_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "resilient-v1", 42)
    def test_resilientv2_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "resilient-v2", 42)
    def test_naiverc_stradd(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/stradd.vale"], "naive-rc", 42)

    def test_assist_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "assist", 42)
    def test_unsafefast_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "unsafe-fast", 42)
    def test_resilientv0_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "resilient-v0", 42)
    def test_resilientv1_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "resilient-v1", 42)
    def test_resilientv2_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "resilient-v2", 42)
    def test_naiverc_strneq(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strneq.vale"], "naive-rc", 42)

    def test_assist_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "assist", 42)
    def test_unsafefast_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "unsafe-fast", 42)
    def test_resilientv0_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "resilient-v0", 42)
    def test_resilientv1_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "resilient-v1", 42)
    def test_resilientv2_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "resilient-v2", 42)
    def test_naiverc_lambdamut(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/lambdas/lambdamut.vale"], "naive-rc", 42)

    def test_assist_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "assist", 42)
    def test_unsafefast_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "unsafe-fast", 42)
    def test_resilientv0_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "resilient-v0", 42)
    def test_resilientv1_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "resilient-v1", 42)
    def test_resilientv2_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "resilient-v2", 42)
    def test_naiverc_strprint(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/strprint.vale"], "naive-rc", 42)

    def test_assist_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "assist", 42)
    def test_unsafefast_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "unsafe-fast", 42)
    def test_resilientv0_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "resilient-v0", 42)
    def test_resilientv1_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "resilient-v1", 42)
    def test_resilientv2_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "resilient-v2", 42)
    def test_naiverc_inttostr(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/strings/inttostr.vale"], "naive-rc", 42)

    def test_assist_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "assist", 42)
    def test_unsafefast_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "unsafe-fast", 42)
    def test_resilientv0_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "resilient-v0", 42)
    def test_resilientv1_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "resilient-v1", 42)
    def test_resilientv2_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "resilient-v2", 42)
    def test_naiverc_nestedif(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/if/nestedif.vale"], "naive-rc", 42)

    def test_assist_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "assist", 42)
    def test_unsafefast_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "unsafe-fast", 42)
    def test_resilientv0_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "resilient-v0", 42)
    def test_resilientv1_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "resilient-v1", 42)
    def test_resilientv2_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "resilient-v2", 42)
    def test_naiverc_unstackifyret(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unstackifyret.vale"], "naive-rc", 42)

    def test_assist_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "assist", 42)
    def test_unsafefast_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "unsafe-fast", 42)
    def test_resilientv0_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "resilient-v0", 42)
    def test_resilientv1_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "resilient-v1", 42)
    def test_resilientv2_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "resilient-v2", 42)
    def test_naiverc_swapmutusadestroy(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/arrays/swapmutusadestroy.vale"], "naive-rc", 42)

    def test_assist_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "assist", 42)
    def test_unsafefast_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "unsafe-fast", 42)
    def test_resilientv0_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "resilient-v0", 42)
    def test_resilientv1_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "resilient-v1", 42)
    def test_resilientv2_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "resilient-v2", 42)
    def test_naiverc_unreachablemoot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/unreachablemoot.vale"], "naive-rc", 42)

    def test_assist_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "assist", 255)
    def test_unsafefast_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "unsafe-fast", 255)
    def test_resilientv0_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "resilient-v0", 255)
    def test_resilientv1_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "resilient-v1", 255)
    def test_resilientv2_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "resilient-v2", 255)
    def test_naiverc_panic(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panic.vale"], "naive-rc", 255)

    def test_assist_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "assist", 42)
    def test_unsafefast_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "unsafe-fast", 42)
    def test_resilientv0_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "resilient-v0", 42)
    def test_resilientv1_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "resilient-v1", 42)
    def test_resilientv2_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "resilient-v2", 42)
    def test_naiverc_panicnot(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/panicnot.vale"], "naive-rc", 42)

    def test_assist_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "assist", 42)
    def test_unsafefast_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "unsafe-fast", 42)
    def test_resilientv0_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "resilient-v0", 42)
    def test_resilientv1_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "resilient-v1", 42)
    def test_resilientv2_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "resilient-v2", 42)
    def test_naiverc_nestedblocks(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/nestedblocks.vale"], "naive-rc", 42)

    def test_assist_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 42)
    def test_unsafefast_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 42)
    def test_resilientv0_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 42)
    def test_resilientv1_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 42)
    def test_resilientv2_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 42)
    def test_naiverc_weakDropThenLockStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 42)

    def test_assist_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakLockWhileLiveStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakFromLocalCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakFromCRefStruct(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefStruct.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_loadFromWeakable(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/loadFromWeakable.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 42)
    def test_unsafefast_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 42)
    def test_resilientv0_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 42)
    def test_resilientv1_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 42)
    def test_resilientv2_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 42)
    def test_naiverc_weakDropThenLockInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/dropThenLockInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 42)

    def test_assist_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakLockWhileLiveInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/lockWhileLiveInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakFromLocalCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromLocalCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 7)
    def test_unsafefast_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 7)
    def test_resilientv0_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 7)
    def test_resilientv1_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 7)
    def test_resilientv2_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 7)
    def test_naiverc_weakFromCRefInterface(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/weakFromCRefInterface.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 7)

    def test_assist_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 42)
    def test_unsafefast_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 42)
    def test_resilientv0_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 42)
    def test_resilientv1_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 42)
    def test_resilientv2_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 42)
    def test_naiverc_weakSelfMethodCallWhileLive(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodWhileLive.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 42)

    def test_assist_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "assist", 0)
    def test_unsafefast_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "unsafe-fast", 0)
    def test_resilientv0_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v0", 0)
    def test_resilientv1_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v1", 0)
    def test_resilientv2_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "resilient-v2", 0)
    def test_naiverc_weakSelfMethodCallAfterDrop(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/weaks/callWeakSelfMethodAfterDrop.vale", PATH_TO_SAMPLES + "libraries/opt.vale"], "naive-rc", 0)

    def test_assist_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "assist", 4)
    def test_unsafefast_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "unsafe-fast", 4)
    def test_resilientv0_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "resilient-v0", 4)
    def test_resilientv1_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "resilient-v1", 4)
    def test_resilientv2_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "resilient-v2", 4)
    def test_naiverc_extern(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/extern.vale"], "naive-rc", 4)

    def test_assist_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "assist", 42)
    def test_unsafefast_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "unsafe-fast", 42)
    def test_resilientv0_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "resilient-v0", 42)
    def test_resilientv1_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "resilient-v1", 42)
    def test_resilientv2_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "resilient-v2", 42)
    def test_naiverc_externtuple(self) -> None:
        self.compile_and_execute_and_expect_return_code([PATH_TO_SAMPLES + "programs/externs/externtuple.vale", PATH_TO_SAMPLES + "programs/externs/externtuple.c"], "naive-rc", 42)


if __name__ == '__main__':
    unittest.main()
