# Monster Tulpar T5 V21.5 Linux Guide

This guide is based on a Fedora setup where the machine identifies itself as:

- Vendor: `MONSTER`
- Product: `TULPAR T5 V21.5`
- Kernel family observed: Fedora 42 with the `tuxedo_keyboard` stack loaded

## Recommended stack

Use one owner for each subsystem:

- Power and fans: `TUXEDO Control Center`
- RGB keyboard and RGB bar: `OpenRGB`
- Desktop integration and custom behavior: small local scripts

Avoid letting multiple power managers fight each other.

## TUXEDO Control Center

Observed on this machine:

- `tccd` runs and exposes a D-Bus API on `com.tuxedocomputers.tccd`
- custom and legacy profiles are readable and switchable from D-Bus
- the hardware profile key emits `Super+Alt+F6`

Useful checks:

```bash
systemctl is-active tccd.service
busctl --system introspect com.tuxedocomputers.tccd /com/tuxedocomputers/tccd
```

## TuneD

If `TuneD` is active at the same time as TCC, they can fight over CPU governor and energy preferences.

Recommended state on this machine when using TCC:

```bash
sudo systemctl mask --now tuned.service tuned-ppd.service
```

Verify:

```bash
systemctl is-enabled tuned.service tuned-ppd.service tccd.service
systemctl is-active tuned.service tuned-ppd.service tccd.service
```

Expected:

- `tuned.service`: `masked` and `inactive`
- `tuned-ppd.service`: `masked` and `inactive`
- `tccd.service`: `enabled` and `active`

## Hardware profile key

On this machine, the hardware profile key is visible to Linux and maps to:

- `Super+Alt+F6`

That means you do not need Windows vendor software to detect the key. You can bind it in GNOME and call a script that switches TCC profiles through D-Bus.

This repo includes:

- `monster-cycle-tcc-profile`
- `monster-tcc-profile-manager`

The manager writes its cycle order to:

- `~/.config/monster-tcc/cycle-order.json`

## RGB devices

What Linux exposed in this setup:

- keyboard RGB zones through `rgb:kbd_backlight*`
- OpenRGB `Ionico Keyboard`
- OpenRGB `Ionico Light Bar`

What did not appear to be exposed:

- the separate white profile-indicator LEDs used by the Windows software

So the practical Linux path is:

- use the real hardware profile key for mode switching
- use notifications, keyboard color, or RGB light bar as feedback

## OpenRGB

OpenRGB detects these useful devices here:

- `Ionico Keyboard`
- `Ionico Light Bar`

Check:

```bash
openrgb -l
```

If you dislike the stock OpenRGB UI, a better approach is often:

- keep OpenRGB only as the device backend
- build small purpose-specific frontends for the machine

## Howdy

Howdy is the Windows Hello style face-auth project for Linux.

Official upstream still documents Fedora support through a COPR repo:

```bash
sudo dnf copr enable principis/howdy
sudo dnf --refresh install howdy
```

But for Fedora 42, this is not a clean recommendation right now.

Current caveats observed from upstream issue tracker:

- Fedora 42 packaging has dependency breakage in the stable COPR path
- beta packages also had unresolved dependency reports
- GNOME/GDM tends to behave better than KDE for login integration

Practical recommendation for Fedora 42 on this laptop:

- treat Howdy as experimental
- only enable it after you confirm `sudo howdy test` works reliably
- do not make it your sole auth path
- prefer starting with `sudo` integration before touching login PAM stacks

Suggested cautious workflow:

```bash
sudo howdy test
sudo howdy add
sudo howdy list
```

Only after that should you review PAM integration for:

- `sudo`
- lock screen
- login manager

Security note:

- Howdy is convenience, not stronger security than a password
- keep password auth available

## General Fedora notes for this machine

- GNOME Wayland works fine for the custom profile manager GUI
- TCC plus masked TuneD is a cleaner power-management setup than mixing them
- OpenRGB is useful as a hardware backend even if its UI is not
- keep copies of working profile settings and custom scripts in version control
