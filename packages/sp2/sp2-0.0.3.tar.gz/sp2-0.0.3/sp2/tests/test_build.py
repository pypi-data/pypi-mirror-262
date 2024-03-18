import unittest


class TestBuild(unittest.TestCase):
    def test_init_helpers(self):
        """was a build issue where InitHelpers ran on a single instance across all libraries linking _sp2impl"""
        # Take a sample of libraries
        from sp2.lib import _parquetadapterimpl, _sp2baselibimpl, _sp2impl

        self.assertTrue(hasattr(_sp2impl, "PyNode"))
        self.assertFalse(hasattr(_sp2baselibimpl, "PyNode"))
        self.assertFalse(hasattr(_parquetadapterimpl, "PyNode"))

        self.assertFalse(hasattr(_sp2impl, "merge"))
        self.assertTrue(hasattr(_sp2baselibimpl, "merge"))
        self.assertFalse(hasattr(_parquetadapterimpl, "merge"))

        self.assertFalse(hasattr(_sp2impl, "_parquet_input_adapter"))
        self.assertFalse(hasattr(_sp2baselibimpl, "_parquet_input_adapter"))
        self.assertTrue(hasattr(_parquetadapterimpl, "_parquet_input_adapter"))


if __name__ == "__main__":
    unittest.main()
