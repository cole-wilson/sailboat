# Created with sailboat, the Python releaser

# v0.1.0

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "A quick and easy way to package, freeze, and distribute your Python projects!"
  homepage "https://github.com/cole-wilson/sailboat"
  url "https://files.pythonhosted.org/packages/54/3b/3bb83cf230b9191f6b4f2f21fa40406ac7dee437d79b0f2277d1a0e46c21/sailboat-0.1.0.tar.gz" # These lines must be configured during release, not build.
  sha256 "ff77ed20d6887fa67d436857cfc04aa7dd3ce0dda3ab392152aa2120601d616f" # ^^^
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


  def install
    virtualenv_install_with_resources
  end
end