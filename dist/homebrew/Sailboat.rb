# Created with sailboat, the Python releaser

# v0.26.1

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
      url "https://files.pythonhosted.org/packages/f6/e9/19af16328705915233299f6f1f02db95899fb00c75ac9da4757aa1e5d1de/setuptools-56.0.0.tar.gz"
      sha256 "08a1c0f99455307c48690f00d5c2ac2c1ccfab04df00454fef854ec145b81302"
   end
   resource "twine" do
      url "https://files.pythonhosted.org/packages/ac/5c/e12811190a3560c85dfb4caea752635abea59c53390592493549d88f086a/twine-3.4.1.tar.gz"
      sha256 "a56c985264b991dc8a8f4234eb80c5af87fa8080d0c224ad8f2cd05a2c22e83b"
   end
   resource "colorama" do
      url "https://files.pythonhosted.org/packages/1f/bb/5d3246097ab77fa083a61bd8d3d527b7ae063c7d8e8671b1cf8c4ec10cbe/colorama-0.4.4.tar.gz"
      sha256 "5941b2b48a20143d2267e95b1c2a7603ce057ee39fd88e7329b0c292aa16869b"
   end
   resource "enlighten" do
      url "https://files.pythonhosted.org/packages/cf/3f/f0e005fea4a5216423369250167263a7e2fba5b0c72d7e97ec9e54d80ac1/enlighten-1.9.0.tar.gz"
      sha256 "539cc308ccc0c3bfb50feb1b2da94c1a1ac21e80fe95e984221de8966d48f428"
   end
   resource "blessed" do
      url "https://files.pythonhosted.org/packages/68/c7/5f21c1b0e7f343bad166c3139e594639cd54e9b97db7760dff035b35065e/blessed-1.18.0.tar.gz"
      sha256 "1312879f971330a1b7f2c6341f2ae7e2cbac244bfc9d0ecfbbecd4b0293bc755"
   end


  def install
    virtualenv_install_with_resources
  end
end