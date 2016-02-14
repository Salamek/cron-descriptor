# Maintainer: Adam Schubert <adam.schubert@sg1-game.net>

pkgname=python-cron-descriptor
pkgver=1.2.4
pkgrel=1
pkgdesc="A Python library that converts cron expressions into human readable strings."
arch=('any')
license=('MIT')
url='https://github.com/Salamek/cron-descriptor'
depends=('python')
makedepends=()
source=("https://github.com/Salamek/cron-descriptor/archive/$pkgver.tar.gz")
noextract=()
md5sums=('')

package() {
  cd "$srcdir/$pkgname-$pkgver"
  ./setup.py install --root=$pkgdir/ --optimize=1
}
