# Created with sailboat, the Python releaser

# v0.3.2

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "A quick and easy way to package, freeze, and distribute your Python projects!"
  homepage "https://github.com/cole-wilson/sailboat"
  url "https://files.pythonhosted.org/packages/8d/b1/82c255427538c8d14138b5e30e4bd2846a0658e9299a9f66165800661b7b/sailboat-0.3.2.tar.gz" # These lines must be configured during release, not build.
  sha256 "cf02152aba5267ce3551da55eff9b4110e022c461de2db733926b3bba8e96ad2" # ^^^
  license "MIT"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"

   resource "toml" do
      url "https://files.pythonhosted.org/packages/be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c/toml-0.10.2.tar.gz"
      sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
   end
   resource "requests" do
      url "https://files.pythonhosted.org/packages/9f/14/4a6542a078773957aa83101336375c9597e6fe5889d20abda9c38f9f3ff2/requests-2.25.0.tar.gz"
      sha256 "7f1a0b932f4a60a1a65caa4263921bb7d9ee911957e0ae4a23a6dd08185ad5f8"
   end
   resource "semver" do
      url "https://files.pythonhosted.org/packages/31/a9/b61190916030ee9af83de342e101f192bbb436c59be20a4cb0cdb7256ece/semver-2.13.0.tar.gz"
      sha256 "fa0fe2722ee1c3f57eac478820c3a5ae2f624af8264cbdf9000c980ff7f75e3f"
   end


  def install
    virtualenv_install_with_resources
  end
end