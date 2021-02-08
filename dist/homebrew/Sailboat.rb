# Created with sailboat, the Python releaser

# v0.25.0+7490438.1

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
      url "https://files.pythonhosted.org/packages/12/68/95515eaff788370246dac534830ea9ccb0758e921ac9e9041996026ecaf2/setuptools-53.0.0.tar.gz"
      sha256 "1b18ef17d74ba97ac9c0e4b4265f123f07a8ae85d9cd093949fa056d3eeeead5"
   end
   resource "twine" do
      url "https://files.pythonhosted.org/packages/f9/43/51c3139667e90399a4d7886013631ad020ad102db5c2907cb240ce56f3c1/twine-3.3.0.tar.gz"
      sha256 "fcffa8fc37e8083a5be0728371f299598870ee1eccc94e9a25cef7b1dcfa8297"
   end
   resource "colorama" do
      url "https://files.pythonhosted.org/packages/1f/bb/5d3246097ab77fa083a61bd8d3d527b7ae063c7d8e8671b1cf8c4ec10cbe/colorama-0.4.4.tar.gz"
      sha256 "5941b2b48a20143d2267e95b1c2a7603ce057ee39fd88e7329b0c292aa16869b"
   end
   resource "enlighten" do
      url "https://files.pythonhosted.org/packages/9d/1c/93c71041478b9cadd1aa47b72aed089c16529bad09e8ea6fe86cfd5a8363/enlighten-1.7.2.tar.gz"
      sha256 "48a818c60e6bcec85051b695bac219c8f92a2ae0e53b5a0ad8dc0fcce93dae2f"
   end
   resource "blessed" do
      url "https://files.pythonhosted.org/packages/0e/e6/f02d17a5ac70ca2d5794b105b8d8e9b5513e8b15ca6955440c0dbc90f363/blessed-1.17.12.tar.gz"
      sha256 "580429e7e0c6f6a42ea81b0ae5a4993b6205c6ccbb635d034b4277af8175753e"
   end


  def install
    virtualenv_install_with_resources
  end
end