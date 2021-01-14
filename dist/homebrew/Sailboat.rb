# Created with sailboat, the Python releaser

# v0.12.5

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "🐍 A quick and easy way to distribute your Python projects!"
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
      url "https://files.pythonhosted.org/packages/82/2f/ef7afd98530d07c89deffec833b4b1a91a27a5db6d9f1a216599f5f0316e/setuptools-51.1.2.tar.gz"
      sha256 "4fa149145ba5dcd4aaa89912ec92393a31170eaf17fe0268b1429538bad1f85a"
   end
   resource "pathlib" do
      url "https://files.pythonhosted.org/packages/ac/aa/9b065a76b9af472437a0059f77e8f962fe350438b927cb80184c32f075eb/pathlib-1.0.1.tar.gz"
      sha256 "6940718dfc3eff4258203ad5021090933e5c04707d5ca8cc9e73c94a7894ea9f"
   end


  def install
    virtualenv_install_with_resources
  end
end