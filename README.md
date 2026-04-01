# Monster Linux Toolkit

Utilities and notes for running Fedora Linux on a `Monster Tulpar T5 V21.5` class laptop with TUXEDO components, OpenRGB, and a custom power-profile shortcut workflow.

## What is in this repo

- `scripts/monster-cycle-tcc-profile`
  Cycles TUXEDO Control Center profiles through D-Bus.
- `scripts/monster-tcc-profile-manager`
  GTK/libadwaita GUI for editing the cycle order used by the hardware profile key.
- `scripts/monster_tcc_common.py`
  Shared D-Bus and config logic.
- `desktop/monster-tcc-profile-manager.desktop`
  Desktop launcher.
- `docs/monster-linux-guide.md`
  Machine-specific Linux guide, including TCC, OpenRGB, TuneD, and Howdy notes.
- `install.sh`
  Installs the scripts and desktop file into the current user's local directories.

## Why this exists

This laptop exposes the hardware profile key to Linux as `Super+Alt+F6`, but the vendor software behavior is not reproduced automatically on Fedora. The tools here restore that workflow by:

- binding the hardware key to a TCC profile cycle action
- providing a GUI to reorder or disable profiles in that cycle
- keeping the setup lightweight and user-local

## Requirements

- Fedora Linux with GNOME Wayland
- `tccd` from TUXEDO Control Center running on the system bus
- `busctl`
- Python 3
- GTK 4 and libadwaita Python bindings (`python3-gobject` with GTK4/Adwaita available)

## Install

```bash
git clone https://github.com/beng1z/monster-linux-toolkit.git
cd monster-linux-toolkit
./install.sh
```

After install:

- open `Monster TCC Profile Manager` from the GNOME app grid
- arrange the order you want
- save it
- press the hardware profile key to cycle profiles

## Notes

- The current setup is designed around `TUXEDO Control Center` for power/fan profiles and `OpenRGB` for lighting.
- `TuneD` should stay masked on this machine if you want TCC to own power-profile behavior.
- The separate white profile-indicator LEDs do not currently appear to be exposed through Linux `sysfs`, `tccd`, or OpenRGB on this hardware. The RGB keyboard and RGB front light bar are visible; the white indicator LEDs are not.

## Sources

- Howdy official repository: https://github.com/boltgolt/howdy
- Fedora 42 Howdy packaging issue: https://github.com/boltgolt/howdy/issues/1018
- Howdy KDE/SDDM behavior discussion: https://github.com/boltgolt/howdy/issues/843
- TUXEDO keyboard power-mode LED discussion: https://github.com/tuxedocomputers/tuxedo-keyboard/issues/86
