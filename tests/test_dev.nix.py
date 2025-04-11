import unittest
import os

class TestDevNix(unittest.TestCase):
    def setUp(self):
        self.dev_nix_path = ".idx/dev.nix"
        self.assertTrue(os.path.exists(self.dev_nix_path), f"File not found: {self.dev_nix_path}")
        with open(self.dev_nix_path, 'r') as f:
            self.dev_nix_content = f.read()

        self.dev_nix_data = {}

        try:
            # Remove comments
            lines = self.dev_nix_content.splitlines()
            filtered_lines = [line for line in lines if not line.strip().startswith('#')]
            self.dev_nix_content = '\n'.join(filtered_lines)

            #remove pkgs,...
            self.dev_nix_content=self.dev_nix_content.replace("{ pkgs, ... }: ", "")

            self.dev_nix_data = eval(self.dev_nix_content.replace('true', 'True').replace('false','False'))

        except Exception as e:
            self.fail(f"Error parsing dev.nix: {e}")

    def test_channel(self):
        self.assertIn('channel', self.dev_nix_data.keys())
        self.assertEqual(self.dev_nix_data['channel'], "stable-24.05")

    def test_packages(self):
        self.assertIn('packages', self.dev_nix_data.keys())
        self.assertListEqual(self.dev_nix_data['packages'], [])

    def test_env(self):
        self.assertIn('env', self.dev_nix_data.keys())
        self.assertDictEqual(self.dev_nix_data['env'], {})

    def test_extensions(self):
      self.assertIn('idx', self.dev_nix_data)
      self.assertIn('extensions', self.dev_nix_data['idx'].keys())
      self.assertListEqual(self.dev_nix_data['idx']['extensions'], [])

    def test_previews(self):
        self.assertIn('idx', self.dev_nix_data.keys())
        self.assertIn('previews', self.dev_nix_data['idx'].keys())
        self.assertTrue(self.dev_nix_data['idx']['previews']['enable'])
        self.assertDictEqual(self.dev_nix_data['idx']['previews']['previews'], {})

    def test_workspace(self):
        self.assertIn('idx', self.dev_nix_data.keys())
        self.assertIn('workspace', self.dev_nix_data['idx'].keys())
        self.assertIn('onCreate', self.dev_nix_data['idx']['workspace'].keys())
        self.assertDictEqual(self.dev_nix_data['idx']['workspace']['onCreate'], {})
        self.assertIn('onStart', self.dev_nix_data['idx']['workspace'].keys())
        self.assertDictEqual(self.dev_nix_data['idx']['workspace']['onStart'], {})

if __name__ == '__main__':
    unittest.main()