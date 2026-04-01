# Monster Tulpar T5 V21.5 Fedora 42 Kurulum Rehberi

Bu rehber, doğrudan şu makineye göre yazılmıştır:

- Üretici: `MONSTER`
- Model: `TULPAR T5 V21.5`
- GPU: `Intel UHD Graphics + NVIDIA GeForce RTX 3070 Mobile / Max-Q`
- Wi-Fi: `Intel CNVi`
- Ethernet: `Realtek RTL8125 2.5GbE`

Hedef:

- sıfırdan Fedora kurulduktan sonra sistemi günlük kullanıma hazır hale getirmek
- güç profilleri, fan kontrolü, ekran kartı sürücüleri ve yüz tanıma tarafını toparlamak

## 1. Fedora kurulumundan hemen sonra

Önce sistemi tamamen güncelle:

```bash
sudo dnf upgrade --refresh -y
sudo reboot
```

Ben bu rehberi `Fedora 42 Workstation` üzerinde hazırladım. GNOME Wayland ile sorunsuz çalışıyor.

## 2. Donanımı doğrula

İlk olarak sistemin doğru donanımı gördüğünü kontrol et:

```bash
cat /sys/devices/virtual/dmi/id/sys_vendor
cat /sys/devices/virtual/dmi/id/product_name
lspci -nn | grep -Ei 'vga|3d|display|network|ethernet|wireless'
```

Bu makinede beklenen temel tablo:

- `MONSTER`
- `TULPAR T5 V21.5`
- Intel iGPU
- NVIDIA RTX 3070 Mobile
- Intel Wi-Fi
- Realtek RTL8125 Ethernet

## 3. RPM Fusion depolarını ekle

NVIDIA ve bazı ek paketler için önce RPM Fusion gerekir.

Fedora dökümantasyonundaki standart yöntem:

```bash
sudo dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

İstersen ardından tekrar yenile:

```bash
sudo dnf upgrade --refresh -y
```

## 4. NVIDIA sürücüsünü kur

Bu modelde en kritik sürücü adımı NVIDIA tarafıdır.

Bu makinede çalışan kurgu:

```bash
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia xorg-x11-drv-nvidia-cuda
```

İsteğe bağlı ama faydalı ek paketler:

```bash
sudo dnf install nvidia-settings xorg-x11-drv-nvidia-power
```

Kurulumdan sonra yeniden başlat:

```bash
sudo reboot
```

Doğrulama:

```bash
lsmod | grep nvidia
nvidia-smi
```

Not:

- Secure Boot açıksa NVIDIA modülü yüklenmeyebilir.
- Böyle bir durumda ya Secure Boot'u kapatman ya da modül imzalama yoluna gitmen gerekir.

## 5. TUXEDO deposunu ekle

TUXEDO, Fedora için kendi RPM deposunu sağlıyor.

Kolay yol:

```bash
cd ~/Downloads
sudo dnf install ./tuxedo-repository*.noarch.rpm
sudo dnf update
```

Alternatif terminal yöntemi:

```bash
sudo dnf config-manager addrepo --from-repofile="https://rpm.tuxedocomputers.com/fedora/tuxedo.repo"
sudo rpm --import https://rpm.tuxedocomputers.com/fedora/42/0x54840598.pub.asc
sudo dnf makecache
```

Kontrol:

```bash
cat /etc/yum.repos.d/tuxedo.repo
```

Bu makinede çalışan repo satırı şu mantıktadır:

- `baseurl=https://rpm.tuxedocomputers.com/fedora/42/x86_64/base`

## 6. TUXEDO Control Center ve sürücüleri kur

Kurulum:

```bash
sudo dnf install tuxedo-control-center
```

Bu paketle birlikte gerekli bağımlılıklar da gelir. Bu sistemde `tuxedo-drivers` otomatik geldi.

Kontrol:

```bash
rpm -qa | grep -E 'tuxedo-control-center|tuxedo-drivers'
systemctl status tccd.service
lsmod | grep -E 'tuxedo|uniwill|clevo'
```

Bu makinede beklenen modüller:

- `tuxedo_keyboard`
- `tuxedo_io`
- `uniwill_wmi`
- bazı durumlarda `clevo_wmi`

## 7. TuneD çakışmasını kalıcı kapat

Fedora tarafında `TuneD` ve `tuned-ppd`, TCC ile çakışabiliyor.

Bu modelde tavsiyem:

```bash
sudo systemctl mask --now tuned.service tuned-ppd.service
```

Kontrol:

```bash
systemctl is-enabled tuned.service tuned-ppd.service tccd.service
systemctl is-active tuned.service tuned-ppd.service tccd.service
```

Beklenen durum:

- `tuned.service`: `masked` / `inactive`
- `tuned-ppd.service`: `masked` / `inactive`
- `tccd.service`: `enabled` / `active`

Bu adım çok önemli. Bunu yapmazsan TCC ile TuneD aynı anda güç profili uygulamaya çalışır.

## 8. OpenRGB kur

Klavye RGB ve RGB lightbar için OpenRGB pratik çözüm.

Kurulum:

```bash
sudo dnf install openrgb openrgb-udev-rules
```

Kontrol:

```bash
openrgb -l
```

Bu makinede Linux tarafında görülen cihazlar:

- `Ionico Keyboard`
- `Ionico Light Bar`

Not:

- Windows'taki ayrı beyaz profil gösterge LED'leri Linux'ta görünmüyor.
- OpenRGB ile görünen cihazlar RGB klavye ve RGB bar ile sınırlı.

## 9. Fiziksel profil tuşu

Bu laptopta profil tuşu Linux'a gerçekten geliyor.

Bizim yakaladığımız eşleme:

- `Super+Alt+F6`

Yani Windows yazılımı olmadan da bu tuşu kullanabiliyorsun.

Bu repo içindeki araçlar tam olarak bunun için var:

- `scripts/monster-cycle-tcc-profile`
- `scripts/monster-tcc-profile-manager`

Kurulum:

```bash
cd ~/monster-linux-toolkit
./install.sh
```

Sonra uygulama menüsünden `Monster TCC Profile Manager` açıp profil sırasını ayarlayabilirsin.

## 10. Howdy kur

`Howdy`, Linux için Windows Hello benzeri yüz tanıma projesidir.

Resmi Fedora yolu upstream README içinde COPR üzerinden anlatılıyor:

```bash
sudo dnf copr enable principis/howdy
sudo dnf --refresh install howdy
```

Ama Fedora 42 tarafında bu yol uzun süre problemli oldu. Bu makinede çalışan kurulum yolu `howdy-beta` deposu oldu.

Bu sistemde kullanılan repo:

```bash
sudo dnf copr remove principis/howdy
sudo dnf copr enable principis/howdy-beta
sudo dnf --refresh install howdy
```

Bu makinede kurulu paket örneği:

- `howdy-3.0.0-7.20250714gitd3ab993.fc42.x86_64`

Kurulumdan sonra önce test et:

```bash
sudo howdy version
sudo howdy add
sudo howdy list
sudo howdy test
```

Önemli not:

- önce sadece `sudo` tarafında test et
- doğrudan giriş ekranına bağlama
- parola girişini yedek olarak mutlaka açık bırak

## 11. Howdy yapılandırırken dikkat

Eğer kamera algılanmıyorsa:

```bash
sudo howdy config
```

Bakılacak ana ayarlar:

- doğru kamera aygıtı
- karanlık ortam performansı
- yüz model sayısı

Eğer `sudo howdy test` stabil değilse PAM giriş yapılarını elleme.

## 12. Wi-Fi ve Ethernet

Bu modelde ek bir özel Wi-Fi kurulumu gerekmedi.

Görülen donanım:

- Intel Wi-Fi
- Realtek RTL8125 Ethernet

Fedora çekirdeği bu ikisini temel kullanım için gördü.

Kontrol:

```bash
nmcli device status
ip -br link
```

Eğer LAN tarafında sorun yaşarsan önce şuna bak:

```bash
lspci -nn | grep Ethernet
```

Ama bu sistemde ekstra bir üçüncü parti Ethernet sürücüsü kurmak gerekmedi.

## 13. Son kontrol listesi

Kurulum sonunda şunları tek tek doğrula:

```bash
systemctl is-active tccd.service
systemctl is-active tuned.service tuned-ppd.service
lsmod | grep nvidia
lsmod | grep tuxedo
openrgb -l
```

Beklenen durum:

- `tccd` aktif
- `tuned` ve `tuned-ppd` inaktif
- `nvidia` modülleri yüklü
- `tuxedo_keyboard` modülü yüklü
- OpenRGB cihaz listesi geliyor

## 14. Bu repodaki araçların amacı

Bu repo rehber + yardımcı araç deposudur.

Araçlar:

- fiziksel profil tuşuna TCC profil döngüsü bağlar
- profil sırasını GTK arayüzünden düzenletir

Ama asıl amaç:

- `Monster Tulpar T5 V21.5` için düzgün, sıfırdan kurulum rehberi sunmak

## Kaynaklar

- Fedora Docs, RPM Fusion repository setup:
  https://docs.fedoraproject.org/quick-docs/rpmfusion-setup/
- TUXEDO repository and Fedora installation page:
  https://www.tuxedocomputers.com/en/Add-TUXEDO-software-package-sources.tuxedo
- Howdy official repository:
  https://github.com/boltgolt/howdy
- Howdy Fedora instructions in upstream README:
  https://github.com/boltgolt/howdy
- Fedora 42 Howdy packaging issue:
  https://github.com/boltgolt/howdy/issues/1018
