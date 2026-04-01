# Monster Tulpar T5 V21.5 Linux Rehberi

Bu rehber doğrudan şu makine üzerinden hazırlanmıştır:

- Üretici: `MONSTER`
- Model: `TULPAR T5 V21.5`
- Dağıtım: Fedora

Bu yüzden genel Linux tavsiyesinden çok, bu modelde gerçekten karşıma çıkan pratik durumlara odaklanır.

## Önerdiğim genel kurgu

Her işi tek bir araç yapsın:

- Güç ve fan: `TUXEDO Control Center`
- RGB klavye ve RGB bar: `OpenRGB`
- Özel davranışlar ve entegrasyon: küçük yerel scriptler

Aynı anda iki farklı güç yöneticisinin sistemi çekiştirmesine izin verme.

## TUXEDO Control Center

Bu makinede gözlediğim durum:

- `tccd` çalışıyor
- sistem D-Bus üzerinde `com.tuxedocomputers.tccd` arayüzünü açıyor
- profiller okunabiliyor ve değiştirilebiliyor
- fiziksel profil tuşu Linux'ta görülüyor

Kontrol etmek için:

```bash
systemctl is-active tccd.service
busctl --system introspect com.tuxedocomputers.tccd /com/tuxedocomputers/tccd
```

## TuneD

Bu makinede `TuneD` ile `TUXEDO Control Center` aynı anda çalışınca CPU governor ve enerji tercihleri tarafında çakışma oluşuyor.

Bu yüzden TCC kullanıyorsan önerilen durum:

```bash
sudo systemctl mask --now tuned.service tuned-ppd.service
```

Doğrulama:

```bash
systemctl is-enabled tuned.service tuned-ppd.service tccd.service
systemctl is-active tuned.service tuned-ppd.service tccd.service
```

Beklenen çıktı mantığı:

- `tuned.service`: `masked` ve `inactive`
- `tuned-ppd.service`: `masked` ve `inactive`
- `tccd.service`: `enabled` ve `active`

## Fiziksel profil tuşu

Bu makinede fiziksel profil tuşu Linux'ta doğrudan görülebiliyor.

Gözlenen eşleme:

- `Super+Alt+F6`

Yani Windows yazılımı olmadan da bu tuşu Linux tarafında kullanabiliyorsun. Yapılan çözüm şuydu:

- tuşu GNOME tarafında yakalamak
- TCC profilini D-Bus üzerinden değiştiren script çağırmak

Bu repodaki ilgili dosyalar:

- `monster-cycle-tcc-profile`
- `monster-tcc-profile-manager`

Profil sırası burada tutulur:

- `~/.config/monster-tcc/cycle-order.json`

## RGB cihazlar

Bu kurulumda Linux tarafında görülenler:

- `rgb:kbd_backlight*` üzerinden klavye RGB bölgeleri
- OpenRGB içinde `Ionico Keyboard`
- OpenRGB içinde `Ionico Light Bar`

Görünmeyen şey:

- Windows tarafında güç modu göstergesi gibi çalışan ayrı beyaz LED'ler

Yani pratikte Linux tarafında yapılabilen geri bildirim yöntemleri:

- fiziksel profil tuşu ile gerçek profil değişimi
- masaüstü bildirimi
- klavye rengi
- RGB lightbar rengi

Ama bağımsız beyaz gösterge LED'leri için şu an açık bir Linux arayüzü görünmüyor.

## OpenRGB

Bu makinede işe yarayan cihazlar:

- `Ionico Keyboard`
- `Ionico Light Bar`

Kontrol:

```bash
openrgb -l
```

OpenRGB arayüzünü sevmiyorsan en mantıklı yaklaşım şudur:

- OpenRGB'yi sadece donanım arka ucu olarak kullan
- gündelik kullanım için küçük özel arayüzler yaz

Bu repodaki GTK arayüzü de tam bu mantıkla hazırlanmıştır.

## Howdy

Howdy, Linux için Windows Hello benzeri yüz tanıma projesidir.

Resmi proje:

- https://github.com/boltgolt/howdy

Kağıt üstünde Fedora desteği COPR üzerinden anlatılıyor:

```bash
sudo dnf copr enable principis/howdy
sudo dnf --refresh install howdy
```

Ama Fedora 42 tarafında bunu şu an temiz ve sorunsuz bir çözüm diye önermiyorum.

Bunun nedeni:

- upstream issue'larda Fedora 42 için bağımlılık kırıkları görülüyor
- beta paket hattında da sorun raporları var
- giriş yöneticisi entegrasyonu her masaüstünde aynı kaliteyle çalışmıyor

Pratik önerim:

- Howdy'yi deneysel kabul et
- önce sadece test et
- doğrudan giriş ekranına bağlamadan önce `sudo` ile güvenilir çalıştığını doğrula
- parolayı asla tamamen devre dışı bırakma

Temkinli test akışı:

```bash
sudo howdy test
sudo howdy add
sudo howdy list
```

Bunlar stabil değilse PAM tarafına hiç dokunma.

## Bu model için genel Linux notları

- GNOME Wayland bu araçlar için sorunsuz çalışıyor
- `TCC + masked TuneD` kombinasyonu, karışık güç yöneticilerinden daha temiz
- `OpenRGB` arayüz olarak zayıf olsa da donanım arka ucu olarak iş görüyor
- çalışan ayarları ve scriptleri git ile saklamak çok faydalı

## Bu repodaki araçların amacı

Bu depo tam olarak şunları çözmek için oluşturuldu:

- `Monster Tulpar T5 V21.5` üzerinde Fedora kullanımını rahatlatmak
- TCC güç profillerini fiziksel tuşla tekrar kullanılır hale getirmek
- profil sırasını görsel arayüzden düzenlemek
- bu modelde hangi parçanın Linux'ta gerçekten çalıştığını belgelemek
