# Created with sailboat, the Python releaser

# v{version}

class {name} < Formula
  include Language::Python::Virtualenv

  desc "{short_description}"
  homepage "{url}"
  url "{{pyhosted}}" # These lines must be configured during release, not build.
  sha256 "{{sha256}}" # ^^^
  license "{license}"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"

{resources2}

  def install
    virtualenv_install_with_resources
  end
end