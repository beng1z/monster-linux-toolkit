# Monster Tulpar T5 V21.5 Linux Toolkit

Bu depo, özellikle `MONSTER / TULPAR T5 V21.5` laptopta Fedora Linux kullanırken işime yarayan araçları ve notları içerir.

Odak noktası:

- `TUXEDO Control Center` ile güç/fan profilleri
- `OpenRGB` ile RGB cihazlar
- fiziksel profil tuşunu Linux'ta tekrar kullanılır hale getirmek
- bu model için pratik Linux rehberi

## Bu repoda ne var

- `scripts/monster-cycle-tcc-profile`
  TUXEDO Control Center profillerini D-Bus üzerinden sırayla değiştirir.
- `scripts/monster-tcc-profile-manager`
  Fiziksel profil tuşunun dolaştığı profil sırasını düzenlemek için GTK/libadwaita arayüzü.
- `scripts/monster_tcc_common.py`
  Ortak D-Bus ve yapılandırma mantığı.
- `desktop/monster-tcc-profile-manager.desktop`
  Uygulama menüsü kısayolu.
- `docs/monster-linux-guide.md`
  `Monster Tulpar T5 V21.5` için Linux kullanım rehberi.
- `install.sh`
  Scriptleri ve masaüstü dosyasını kullanıcı dizinine kurar.

## Bu neden gerekli

Bu laptopta fiziksel profil tuşu Linux tarafından görülebiliyor, ama Windows'taki üretici yazılımı davranışı Fedora üzerinde kendiliğinden gelmiyor.

Bu depodaki araçlar şu işi çözüyor:

- fiziksel profil tuşunu tekrar işe yarar hale getirmek
- TCC profil sırasını kullanıcı dostu bir arayüzden ayarlamak
- kurulumu kullanıcı dizininde, hafif ve sade tutmak

## Gereksinimler

- Fedora Linux
- GNOME Wayland
- çalışan `tccd` servisi
- `busctl`
- Python 3
- GTK 4 / libadwaita Python bağları

## Kurulum

```bash
git clone https://github.com/beng1z/monster-linux-toolkit.git
cd monster-linux-toolkit
./install.sh
```

Kurulumdan sonra:

- GNOME uygulama menüsünden `Monster TCC Profile Manager` aç
- profil sırasını istediğin gibi düzenle
- kaydet
- fiziksel profil tuşuna basarak profiller arasında geç

## Notlar

- Bu kurgu güç/fan tarafında `TUXEDO Control Center`, ışık tarafında `OpenRGB` mantığıyla hazırlanmıştır.
- Bu makinede `TuneD`, TCC ile çakıştığı için maskelenmiş olmalıdır.
- Windows'taki ayrı beyaz profil gösterge LED'leri bu donanımda Linux tarafında `sysfs`, `tccd` veya `OpenRGB` üzerinden görünmüyor.
- Linux'ta görünen RGB cihazlar klavye ve RGB lightbar ile sınırlı.

## Kaynaklar

- Howdy resmi repo: https://github.com/boltgolt/howdy
- Fedora 42 Howdy paketleme sorunu: https://github.com/boltgolt/howdy/issues/1018
- Howdy KDE/SDDM davranışı: https://github.com/boltgolt/howdy/issues/843
- TUXEDO klavye güç modu LED tartışması: https://github.com/tuxedocomputers/tuxedo-keyboard/issues/86
