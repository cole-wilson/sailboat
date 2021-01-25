# Created with sailboat, the Python releaser

# v0.23.0

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "A quick and easy way to distribute your Python projects!"
  homepage "https://github.com/cole-wilson/sailboat"
  url "{pyhosted}" # These lines must be configured during release, not build.
  sha256 "{sha256}" # ^^^
  license "MIT"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"

   resource "toml" do
      url "https://files.pythonhosted.org/packages/be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c/toml-0.10.2.tar.gz"
      sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
   end
   resource "semver" do
      url "https://files.pythonhosted.org/packages/31/a9/b61190916030ee9af83de342e101f192bbb436c59be20a4cb0cdb7256ece/semver-2.13.0.tar.gz"
      sha256 "fa0fe2722ee1c3f57eac478820c3a5ae2f624af8264cbdf9000c980ff7f75e3f"
   end
   resource "requests" do
      url "https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz"
      sha256 "27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804"
   end
   resource "setuptools" do
      url "https://files.pythonhosted.org/packages/84/48/5c99d8770fd0a9eb0f82654c3294aad6d0ba9f8600638c2e2ad74f2c5d52/setuptools-52.0.0.tar.gz"
      sha256 "fb3a1ee622509550dbf1d419f241296169d7f09cb1eb5b1736f2f10965932b96"
   end
   resource "twine" do
      url "https://files.pythonhosted.org/packages/f9/43/51c3139667e90399a4d7886013631ad020ad102db5c2907cb240ce56f3c1/twine-3.3.0.tar.gz"
      sha256 "fcffa8fc37e8083a5be0728371f299598870ee1eccc94e9a25cef7b1dcfa8297"
   end


  def install
    virtualenv_install_with_resources
  end
end