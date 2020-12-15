# Created with sailboat, the Python releaser

# v0.4.1+e64bcfe.3

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "A quick and easy way to package, freeze, and distribute your Python projects!"
  homepage "https://github.com/cole-wilson/sailboat"
  url "https://files.pythonhosted.org/packages/59/9e/8a968163da9a7ac839e2bb8648907168c76599df4515b38b3bfa304166ef/sailboat-0.3.3.tar.gz" # These lines must be configured during release, not build.
  sha256 "25b8031bdfb01d84f0ecfd6fd9f78dfc138c06fde5475c38747d214e37f2dda3" # ^^^
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